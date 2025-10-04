# Deploy Guide - WAHA + n8n + Supabase

## RUNBOOK 5 MIN

### 1. Criar projeto Supabase
- Acesse https://supabase.com
- Crie novo projeto
- Copie: `Project URL` e `service_role key` (Settings → API)

### 2. Executar schema SQL
```bash
# No Supabase SQL Editor, cole e execute:
cat ../supabase/schema.sql
```

### 3. Configurar variáveis locais
```bash
cd ops
cp .env.sample .env
# Edite .env com suas credenciais:
# - SUPABASE_URL
# - SUPABASE_SERVICE_ROLE
# - N8N_BASIC_AUTH_PASSWORD (mude!)
```

### 4. Subir stack local
```bash
cd ../infra
docker compose --env-file ../ops/.env up -d
```

### 5. Acessar WAHA e conectar WhatsApp
- URL: http://localhost:3000
- Conectar sessão "default"
- Escanear QR Code com WhatsApp

### 6. Acessar n8n
- URL: http://localhost:5678
- Login: admin / (senha do .env)

### 7. Importar workflow
- n8n → Import from File
- Selecione: `n8n/workflow.ativacao.json`
- Ative o workflow

### 8. Inserir lead de teste
```sql
INSERT INTO public.leads (nome, telefone, email, consentido, data_consentimento, origem_consentimento)
VALUES ('Seu Nome', '65999999999', 'teste@email.com', true, NOW(), 'teste_manual');
```

### 9. Testar envio manual
- n8n → Workflow "Ativação WhatsApp Diária"
- Botão "Execute Workflow"
- Verificar mensagem no WhatsApp

### 10. Verificar logs
```sql
SELECT * FROM public.whatsapp_envios ORDER BY enviado_em DESC LIMIT 10;
```

---

## Deploy Railway (WAHA em produção)

### Opção A: WAHA no Railway
```bash
cd infra
railway login
railway init
railway up --dockerfile railway.waha.Dockerfile

# Configurar variáveis no Railway Dashboard:
# - WAHA_PRINT_QR=true
# - WAHA_LOG_LEVEL=info
```

### Opção B: n8n Cloud
- Use https://n8n.cloud (grátis 5k execuções)
- Configure variáveis de ambiente:
  - SUPABASE_URL
  - SUPABASE_SERVICE_ROLE
  - WAHA_BASE_URL (URL do Railway)
  - WAHA_SEND_TEXT_PATH=/api/sendText

---

## Normalização de Telefone

O schema aplica automaticamente:
- Remove caracteres especiais: `(65) 99999-9999` → `65999999999`
- Adiciona DDI Brasil: `65999999999` → `+5565999999999`

**Formato aceito pelo WAHA:**
```json
{
  "chatId": "5565999999999@c.us",
  "text": "Mensagem"
}
```

---

## Opt-Out (LGPD)

### Registrar opt-out manual
```sql
SELECT opt_out_lead('+5565999999999');
```

### Detectar "PARAR" automaticamente (adicionar ao workflow)
1. Criar webhook no n8n para receber mensagens WAHA
2. Filtrar texto = "PARAR"
3. Executar função `opt_out_lead(telefone)`

---

## Payload de Envio (WAHA API)

### Request
```json
POST http://localhost:3000/api/sendText
Content-Type: application/json

{
  "chatId": "5565999999999@c.us",
  "text": "Olá! Mensagem de teste.",
  "session": "default"
}
```

### Response (Sucesso)
```json
{
  "id": "true_5565999999999@c.us_3EB0XXXXXXXXXXXX",
  "timestamp": 1234567890,
  "status": "SENT"
}
```

### Response (Erro)
```json
{
  "error": {
    "message": "Session 'default' not found",
    "code": "SESSION_NOT_FOUND"
  }
}
```

---

## Troubleshooting

### Porta 3000 ocupada
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9
```

### WAHA não conecta
- Verifique QR Code: http://localhost:3000
- Reinicie container: `docker restart waha`
- Limpe cache: `docker volume rm infra_waha_data`

### n8n não encontra Supabase
- Teste URL manualmente:
```bash
curl -H "apikey: YOUR_KEY" https://your-project.supabase.co/rest/v1/leads?limit=1
```
- Verifique firewall/CORS

### Workflow não executa
- Verifique timezone: `CRON_TZ=America/Cuiaba`
- Teste execução manual primeiro
- Logs: `docker logs n8n -f`

---

## Estrutura de Dados

### Tabela: leads
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | UUID | Identificador único |
| nome | TEXT | Nome do lead |
| telefone | TEXT | +5565999999999 (normalizado) |
| consentido | BOOLEAN | Consentimento LGPD |
| whatsapp_ativado | BOOLEAN | Já recebeu mensagem |
| opt_out | BOOLEAN | Solicitou cancelamento |

### Tabela: whatsapp_envios
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | SERIAL | ID do log |
| lead_id | UUID | Referência ao lead |
| mensagem | TEXT | Conteúdo enviado |
| status_envio | TEXT | sucesso/falha/pendente |
| resposta | TEXT | JSON do retorno WAHA |
| enviado_em | TIMESTAMPTZ | Data/hora do envio |

---

## Configuração Avançada

### Alterar limite diário (padrão: 20)
```sql
-- Edite a view:
CREATE OR REPLACE VIEW public.leads_para_ativar AS
SELECT ...
LIMIT 50; -- altere aqui
```

### Alterar horário do cron
```json
// n8n/workflow.ativacao.json
{
  "cronExpression": "0 14 * * *" // 14:00
}
```

### Adicionar campos customizados
```sql
ALTER TABLE public.leads ADD COLUMN empresa TEXT;
ALTER TABLE public.leads ADD COLUMN segmento TEXT;
```

---

## Segurança

1. **Nunca commite `.env`** com credenciais reais
2. **Use RLS no Supabase** (comentado no schema.sql)
3. **Mude senha padrão do n8n**
4. **Habilite HTTPS em produção**

---

## Próximos Passos

- [ ] Configurar webhook para receber respostas do WhatsApp
- [ ] Implementar detecção automática de "PARAR"
- [ ] Criar dashboard de métricas (Metabase/Grafana)
- [ ] Adicionar rate limiting (proteção anti-spam)
- [ ] Configurar backup automático do Supabase
