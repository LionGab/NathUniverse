# QUICKSTART - Sistema de Reativacao via WhatsApp

**Checklist executavel para colocar o MVP no ar rapidamente**

---

## PARTE 1: PREPARACAO (5 min)

### 1.1 Python e Dependencias

```bash
# Verificar Python
python --version

# Instalar dependencias
cd C:\Users\User\waha-n8n-stack\scripts
pip install -r requirements.txt
```

**Checklist:**
- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas sem erros
- [ ] Modulos: supabase, requests, dotenv, openpyxl, pandas OK

---

### 1.2 Supabase - Criar Banco

1. **Acessar SQL Editor:**
   - URL: https://supabase.com/dashboard/project/eiqzckhcmmfyddruaxdj/sql/new

2. **Executar Schema:**
   ```sql
   -- Cole o conteudo de: C:\Users\User\waha-n8n-stack\supabase\schema.sql
   -- Click RUN ou F5
   ```

3. **Verificar Tabelas:**
   ```sql
   SELECT table_name FROM information_schema.tables
   WHERE table_schema = 'public';
   ```

**Checklist:**
- [ ] Tabela `leads` criada
- [ ] Tabela `whatsapp_envios` criada
- [ ] View `leads_para_ativar` criada
- [ ] Triggers e funcoes criadas

---

### 1.3 Obter Credenciais Supabase

1. **Ir para Settings > API**
2. **Copiar:**
   - Project URL: `https://eiqzckhcmmfyddruaxdj.supabase.co`
   - service_role key: (click "Reveal" e copie)

**Checklist:**
- [ ] Project URL copiada
- [ ] service_role key copiada (comeca com eyJhbGc...)

---

## PARTE 2: IMPORTAR ALUNOS (3 min)

### 2.1 Processar Planilha

```bash
cd C:\Users\User\waha-n8n-stack\scripts
python processar_inativos.py
```

**Output esperado:**
```
Processando: C:\Users\User\Downloads\AlunosInativos.xlsx
30 linhas carregadas
Top 30 inativos priorizados
SQL gerado: inserir_inativos.sql
```

**Checklist:**
- [ ] Arquivo `inserir_inativos.sql` gerado
- [ ] Preview dos 10 primeiros apareceu
- [ ] Sem erros de processamento

---

### 2.2 Importar para Supabase

1. **Abrir arquivo gerado:**
   - `C:\Users\User\waha-n8n-stack\scripts\inserir_inativos.sql`

2. **Copiar conteudo**

3. **No Supabase SQL Editor:**
   - Cole o SQL
   - Click **RUN**

4. **Verificar:**
   ```sql
   SELECT COUNT(*) FROM leads;
   SELECT * FROM leads LIMIT 5;
   ```

**Checklist:**
- [ ] SQL executado sem erros
- [ ] Leads importados (COUNT >= 30)
- [ ] Telefones no formato +5565XXXXXXXXX

---

## PARTE 3: DEPLOY WAHA (5 min)

### 3.1 Criar Projeto Railway

1. **Acessar:** https://railway.app/new
2. **Login com GitHub**
3. **New Project** > **Empty Project**

**Checklist:**
- [ ] Conta Railway criada
- [ ] Projeto criado

---

### 3.2 Deploy WAHA

**Opcao A - Via Docker Image (Mais Rapido):**

1. **New Service** > **Docker Image**
2. **Image:** `devlikeapro/waha:latest`
3. **Deploy**

**Opcao B - Via Dockerfile:**

1. **Conectar GitHub:** Link repo `waha-n8n-stack`
2. **New Service** > **GitHub Repo**
3. **Dockerfile Path:** `infra/railway.waha.Dockerfile`
4. **Deploy**

**Checklist:**
- [ ] Deploy iniciado
- [ ] Build concluido (1-2 min)
- [ ] Container "Running"

---

### 3.3 Gerar URL Publica

1. **Click no servico WAHA**
2. **Settings** > **Networking**
3. **Generate Domain**
4. **Copiar URL** (ex: `waha-production-abc.up.railway.app`)

**Checklist:**
- [ ] Domain gerado
- [ ] URL copiada
- [ ] Acessivel via browser (testa: `/health`)

---

### 3.4 Conectar WhatsApp

1. **Abrir Logs** do servico WAHA
2. **Procurar QR Code ASCII**
3. **Escanear com WhatsApp:**
   - WhatsApp > Configuracoes > Aparelhos conectados > Conectar aparelho

4. **Aguardar:** `✓ WhatsApp session started`

**Checklist:**
- [ ] QR Code apareceu nos logs
- [ ] Escaneado com sucesso
- [ ] Mensagem "session started" apareceu
- [ ] WhatsApp mostra "Dispositivo conectado"

---

## PARTE 4: CONFIGURAR VARIAVEIS (2 min)

### 4.1 Criar .env

```bash
cd C:\Users\User\waha-n8n-stack\ops
copy .env.sample .env
notepad .env
```

### 4.2 Preencher Valores

```env
SUPABASE_URL=https://eiqzckhcmmfyddruaxdj.supabase.co
SUPABASE_SERVICE_ROLE=eyJhbGc....(sua key do Passo 1.3)

WAHA_BASE_URL=https://waha-production-abc.up.railway.app
WAHA_SEND_TEXT_PATH=/api/sendText
WAHA_SESSION=default

LIMITE_DIARIO=30
```

**Checklist:**
- [ ] Arquivo `.env` criado
- [ ] SUPABASE_URL preenchida
- [ ] SUPABASE_SERVICE_ROLE preenchida
- [ ] WAHA_BASE_URL preenchida (URL do Railway)
- [ ] Arquivo salvo

---

## PARTE 5: TESTE DE ENVIO (2 min)

### 5.1 Carregar Variaveis

**Windows CMD:**
```cmd
cd C:\Users\User\waha-n8n-stack\scripts
set SUPABASE_URL=https://eiqzckhcmmfyddruaxdj.supabase.co
set SUPABASE_SERVICE_ROLE=sua-key-aqui
set WAHA_BASE_URL=https://sua-url-railway.up.railway.app
set LIMITE_DIARIO=1
```

**Windows PowerShell:**
```powershell
cd C:\Users\User\waha-n8n-stack\scripts
$env:SUPABASE_URL="https://eiqzckhcmmfyddruaxdj.supabase.co"
$env:SUPABASE_SERVICE_ROLE="sua-key-aqui"
$env:WAHA_BASE_URL="https://sua-url-railway.up.railway.app"
$env:LIMITE_DIARIO="1"
```

---

### 5.2 Executar Teste

```bash
python enviar_diario.py
```

**Output esperado:**
```
Iniciando envio diario de WhatsApp
Variaveis de ambiente validadas
Conectado ao Supabase
1 leads encontrados para envio

[1/1] Processando [Nome]...
Enviado para [Nome] (+5565...)
Log registrado
Lead marcado como ativado

Concluido!
Sucessos: 1
Erros: 0
```

**Checklist:**
- [ ] Script executou sem erros
- [ ] 1 mensagem enviada
- [ ] Apareceu no WhatsApp conectado
- [ ] Lead marcado como `whatsapp_ativado=true` no Supabase

---

### 5.3 Verificar no Supabase

```sql
-- Ver leads ativados
SELECT * FROM leads WHERE whatsapp_ativado = true;

-- Ver historico de envios
SELECT * FROM whatsapp_envios ORDER BY enviado_em DESC LIMIT 5;

-- Leads restantes para enviar
SELECT * FROM leads_para_ativar LIMIT 10;
```

**Checklist:**
- [ ] 1 lead com `whatsapp_ativado = true`
- [ ] 1 registro em `whatsapp_envios`
- [ ] Status = 'sucesso'

---

## PARTE 6: AUTOMATIZAR (OPCIONAL - 3 min)

### Opcao A: Task Scheduler Windows

1. **Abrir:** `taskschd.msc`
2. **Create Basic Task**
   - Nome: `WhatsApp Inativos Diario`
   - Trigger: Daily - 09:00 AM
   - Action: Start a program
   - Program: `C:\Python311\python.exe` (ajuste path)
   - Arguments: `C:\Users\User\waha-n8n-stack\scripts\enviar_diario.py`
   - Start in: `C:\Users\User\waha-n8n-stack\scripts`
3. **Edit Trigger:** Repeat every 1 day
4. **Finish**

**Checklist:**
- [ ] Tarefa criada
- [ ] Trigger configurado (diario)
- [ ] Path do Python correto
- [ ] Testado manualmente (Run)

---

### Opcao B: Railway Cron (Recomendado)

1. **No Railway:** New > Cron Job
2. **Schedule:** `0 9 * * *` (todo dia 9h)
3. **Command:**
   ```bash
   cd /app/scripts && python enviar_diario.py
   ```
4. **Environment Variables:**
   - Adicione as mesmas variaveis do .env

**Checklist:**
- [ ] Cron Job criado
- [ ] Schedule configurado
- [ ] Variaveis de ambiente adicionadas
- [ ] Primeiro run testado

---

### Opcao C: N8N Workflow

1. **Subir N8N:**
   ```bash
   cd C:\Users\User\waha-n8n-stack\infra
   docker-compose up -d n8n
   ```

2. **Acessar:** http://localhost:5678
3. **Login:** admin / change_this_password_123
4. **Criar Workflow:**
   - Trigger: Schedule (Cron: `0 9 * * *`)
   - Action: Execute Command
   - Command: `python /path/to/enviar_diario.py`

**Checklist:**
- [ ] N8N rodando
- [ ] Workflow criado
- [ ] Trigger agendado
- [ ] Ativo

---

## VERIFICACAO FINAL

### Sistema Completo Checklist

**Infraestrutura:**
- [ ] Python + dependencias instaladas
- [ ] Supabase com schema completo
- [ ] WAHA deployado no Railway
- [ ] WhatsApp conectado
- [ ] .env configurado

**Dados:**
- [ ] 30 leads importados
- [ ] Telefones normalizados (+55...)
- [ ] Consentimento = true

**Funcional:**
- [ ] Teste manual funcionou
- [ ] Mensagem recebida no WhatsApp
- [ ] Log registrado no Supabase
- [ ] Lead marcado como ativado

**Automacao (Opcional):**
- [ ] Agendador configurado
- [ ] Execucao diaria garantida

---

## COMANDOS RAPIDOS

### Ver Status do Sistema

```sql
-- Leads totais
SELECT COUNT(*) FROM leads;

-- Leads pendentes
SELECT COUNT(*) FROM leads_para_ativar;

-- Leads ativados
SELECT COUNT(*) FROM leads WHERE whatsapp_ativado = true;

-- Historico hoje
SELECT COUNT(*) FROM whatsapp_envios
WHERE DATE(enviado_em) = CURRENT_DATE;

-- Taxa de sucesso
SELECT
  status_envio,
  COUNT(*) as total,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentual
FROM whatsapp_envios
GROUP BY status_envio;
```

### Testar WAHA Manualmente

```bash
# Health check
curl https://sua-url.railway.app/health

# Enviar mensagem de teste
curl -X POST https://sua-url.railway.app/api/sendText \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "5565999999999@c.us",
    "text": "Teste manual",
    "session": "default"
  }'
```

### Resetar Lead para Reenvio (DEV only)

```sql
UPDATE leads
SET whatsapp_ativado = false
WHERE telefone = '+5565999999999';
```

---

## TROUBLESHOOTING RAPIDO

| Erro | Causa | Solucao |
|------|-------|---------|
| `ModuleNotFoundError` | Dependencias nao instaladas | `pip install -r requirements.txt` |
| `Connection refused (WAHA)` | WAHA offline | Verificar Railway logs |
| `Unauthorized (Supabase)` | Key incorreta | Usar `service_role` key |
| `No leads found` | Importacao falhou | Reexecutar `processar_inativos.py` |
| `WhatsApp desconectado` | Sessao expirou | Reescanear QR Code |
| `Timeout` | WAHA sobrecarregado | Adicionar delay entre envios |

---

## PROXIMOS PASSOS

**Curto Prazo (proximos 7 dias):**
1. Monitorar envios diarios
2. Ajustar mensagem conforme feedback
3. Analisar taxa de resposta

**Medio Prazo (proximas 4 semanas):**
1. Implementar opt-out automatico
2. Adicionar respostas automaticas
3. Criar funil de reativacao

**Longo Prazo:**
1. Dashboard de metricas
2. Integracao com CRM
3. Segmentacao avancada

---

## RECURSOS

- **Documentacao completa:** `GUIA_MVP_5MIN.md`
- **Seguranca LGPD:** `SECURITY_LGPD.md`
- **Deploy avancado:** `ops/README_deploy.md`

---

**SISTEMA PRONTO PARA PRODUCAO!**

Se todos os itens da verificacao final estao marcados, seu MVP esta funcionando e pronto para reativar alunos.
