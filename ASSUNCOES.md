# Assunções do Projeto

## Endpoints da API WAHA

### ⚠️ ASSUMIDO (verificar documentação oficial)
```
POST /api/sendText
```

**Payload assumido:**
```json
{
  "chatId": "5565999999999@c.us",
  "text": "Mensagem",
  "session": "default"
}
```

### Como verificar o endpoint correto:
1. Acesse a documentação WAHA: https://waha.devlike.pro/docs
2. Ou teste localmente:
```bash
curl http://localhost:3000/api/docs
```

### Se o endpoint for diferente:
Edite `ops/.env`:
```bash
WAHA_SEND_TEXT_PATH=/api/messages/text
# ou
WAHA_SEND_TEXT_PATH=/api/v1/sendText
```

---

## Limites e Volume

### Limite diário: **20 leads**
- Definido em: `supabase/schema.sql` (view `leads_para_ativar`)
- Para alterar:
```sql
CREATE OR REPLACE VIEW public.leads_para_ativar AS
SELECT ... LIMIT 50; -- altere aqui
```

### Justificativa:
- WhatsApp Business limita envios em massa
- Prevenção de bloqueio/ban
- Volume baixo conforme solicitado ("poucas pessoas")

---

## Timezone

### Assumido: `America/Cuiaba` (MT, Brasil)
- Horário do cron: **09:00 MT**
- Configurado em:
  - `ops/.env`: `CRON_TZ=America/Cuiaba`
  - `n8n/workflow.ativacao.json`: `timezone: "America/Cuiaba"`

### Para alterar:
```bash
# Lista de timezones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
CRON_TZ=America/Sao_Paulo
```

---

## Formato de Telefone

### Assumido: **Brasil (+55)**
- Normalização automática adiciona `+55`
- Formato final: `+5565999999999`
- WAHA espera: `5565999999999@c.us`

### Para outros países:
Edite função `normalize_telefone()` em `supabase/schema.sql`:
```sql
-- Exemplo: Portugal (+351)
IF length(NEW.telefone) = 9 THEN
    NEW.telefone := '+351' || NEW.telefone;
END IF;
```

---

## Sessão do WAHA

### Assumido: `"session": "default"`
- Nome fixo no workflow
- Conecte WhatsApp com ID "default"

### Para múltiplas sessões:
1. Crie sessão no WAHA: `POST /api/sessions/start {"name": "producao"}`
2. Altere workflow: `"session": "producao"`

---

## Infraestrutura

### Assumido: Docker local + serviços gerenciados
- **WAHA**: Local (Docker) ou Railway
- **n8n**: Local (Docker) ou n8n Cloud
- **Supabase**: Sempre cloud (free tier)
- **PostgreSQL local**: Desativado (comentado no docker-compose)

### Custos estimados (free tier):
- Supabase: Grátis até 500MB
- Railway: Grátis até 500h/mês
- n8n Cloud: Grátis até 5.000 execuções
- **Total: R$ 0/mês** para baixo volume

---

## Deploy em Nuvem (Resposta à dúvida)

### Opção 1: WAHA no Railway (RECOMENDADO)
```bash
cd infra
railway login
railway init
railway up --dockerfile railway.waha.Dockerfile
# Copiar URL gerada: https://waha-production-XXXX.up.railway.app
```

**Configure no n8n Cloud:**
```
WAHA_BASE_URL=https://waha-production-XXXX.up.railway.app
```

### Opção 2: Tudo no Render.com
```yaml
# render.yaml
services:
  - type: web
    name: waha
    env: docker
    dockerfilePath: ./infra/railway.waha.Dockerfile
    plan: free

  - type: web
    name: n8n
    env: docker
    dockerCommand: n8n start
    plan: free
```

### Opção 3: Sem n8n (MAIS SIMPLES)
**Use script Python + GitHub Actions** (automação grátis):
```yaml
# .github/workflows/enviar_whatsapp.yml
on:
  schedule:
    - cron: '0 12 * * *' # 09:00 BRT (UTC-3)

jobs:
  enviar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: python scripts/enviar_diario.py
```

Script: `scripts/enviar_diario.py`
```python
import os
import requests
from supabase import create_client

supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
waha_url = os.getenv('WAHA_URL')

# Buscar leads
leads = supabase.table('leads_para_ativar').select('*').execute()

for lead in leads.data:
    # Enviar WhatsApp
    requests.post(f'{waha_url}/api/sendText', json={
        'chatId': f"{lead['telefone'].replace('+', '')}@c.us",
        'text': f"Olá {lead['nome']}! Mensagem...",
        'session': 'default'
    })

    # Marcar como enviado
    supabase.table('leads').update({'whatsapp_ativado': True}).eq('id', lead['id']).execute()
```

**Custo: R$ 0** (GitHub Actions = grátis até 2000 min/mês)

---

## SMTP (Notificações de Erro)

### Assumido: **Opcional/Desabilitado**
- Variáveis `SMTP_*` vazias por padrão
- Workflow verifica `SMTP_HOST` antes de enviar email

### Para habilitar:
```bash
# Gmail gratuito
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu@gmail.com
SMTP_PASS=senha_app_gmail
SMTP_FROM=seu@gmail.com
```

---

## Segurança

### Assumido: Ambiente de desenvolvimento
- `N8N_BASIC_AUTH_PASSWORD=change_this_password_123` → **MUDAR!**
- RLS no Supabase **comentado** (desabilitado)
- HTTPS não obrigatório localmente

### Para produção:
1. **Mude senha n8n** antes de subir
2. **Habilite RLS** no Supabase
3. **Force HTTPS** (Railway/Render fazem automaticamente)

---

## Substituir Assunções

### 1. Descobrir endpoint real do WAHA
```bash
docker exec -it waha cat /app/docs/api.json
# ou
curl http://localhost:3000/api/docs.json | jq '.paths'
```

### 2. Testar envio manual
```bash
curl -X POST http://localhost:3000/api/sendText \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "5565999999999@c.us",
    "text": "Teste",
    "session": "default"
  }'
```

Se retornar erro 404, tente:
- `/api/messages/text`
- `/api/v1/sendText`
- `/sendText`

### 3. Atualizar `.env`
```bash
WAHA_SEND_TEXT_PATH=/api/rota_correta
```

---

## Decisões Arquiteturais

### Por que Supabase?
- PostgreSQL gerenciado
- API REST automática
- Free tier generoso
- Funções SQL (triggers, views)

### Por que WAHA em vez de Baileys direto?
- API HTTP simples (não precisa Node.js)
- Multi-sessão nativo
- Gestão de QR Code

### Por que n8n?
- Visual workflow (não-devs conseguem editar)
- Cron embutido
- **ALTERNATIVA**: Script Python é mais simples para baixo volume

---

## Próximas Decisões Necessárias

1. **Endpoint WAHA correto** → validar na doc oficial
2. **Deploy**: local, Railway, Render ou GitHub Actions?
3. **Usar n8n ou script Python?** (Python é mais simples)
4. **Habilitar RLS** no Supabase?
5. **Implementar webhook** para receber respostas?

---

**Última atualização**: 2025-01-03
