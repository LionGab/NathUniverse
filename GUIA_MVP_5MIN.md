# GUIA MVP 5 MINUTOS - Sistema de Reativacao de Alunos via WhatsApp

**Tempo estimado:** 5-10 minutos
**Objetivo:** Sistema funcional enviando mensagens WhatsApp para alunos inativos

---

## PRE-REQUISITOS

- [ ] Python 3.8+ instalado
- [ ] Conta Supabase (gratuita)
- [ ] Conta Railway (gratuita - $5 de credito inicial)
- [ ] Planilha `AlunosInativos.xlsx` em `C:\Users\User\Downloads\`
- [ ] WhatsApp Business ou pessoal para conectar

---

## PASSO 1: INSTALAR PYTHON E DEPENDENCIAS (2 min)

### 1.1 Verificar Python

```bash
python --version
# Deve retornar Python 3.8 ou superior
```

**Se nao tiver Python instalado:**
- Windows: https://www.python.org/downloads/
- Durante instalacao: MARQUE "Add Python to PATH"

### 1.2 Instalar Dependencias

```bash
cd C:\Users\User\waha-n8n-stack\scripts
pip install -r requirements.txt
```

**Pacotes que serao instalados:**
- `supabase` - Cliente Supabase
- `requests` - HTTP requests
- `python-dotenv` - Variaveis de ambiente
- `openpyxl` - Leitura Excel
- `pandas` - Manipulacao de dados

---

## PASSO 2: CONFIGURAR SUPABASE (2 min)

### 2.1 Acessar Supabase

1. Acesse: https://supabase.com/dashboard/project/eiqzckhcmmfyddruaxdj
2. Login com sua conta

### 2.2 Executar Schema SQL

1. No menu lateral: **SQL Editor**
2. Click em **New Query**
3. Cole o conteudo do arquivo: `C:\Users\User\waha-n8n-stack\supabase\schema.sql`
4. Click em **RUN** (ou F5)

**Resultado esperado:**
```
Success. No rows returned
```

### 2.3 Obter Credenciais

1. No menu lateral: **Settings** > **API**
2. Copie:
   - **Project URL**: `https://eiqzckhcmmfyddruaxdj.supabase.co`
   - **service_role key** (secret): Clique em "Reveal" e copie

**IMPORTANTE:** Guarde essas credenciais! Vamos usar no Passo 5.

---

## PASSO 3: PROCESSAR PLANILHA DE INATIVOS (1 min)

### 3.1 Verificar Planilha

Confirme que o arquivo existe:
```bash
dir C:\Users\User\Downloads\AlunosInativos.xlsx
```

### 3.2 Executar Processador

```bash
cd C:\Users\User\waha-n8n-stack\scripts
python processar_inativos.py
```

**O script vai:**
1. Ler o Excel
2. Normalizar telefones (+5565XXXXXXXXX)
3. Priorizar os 30 alunos mais importantes
4. Gerar arquivo `inserir_inativos.sql`

### 3.3 Importar para Supabase

1. Abra o arquivo gerado: `inserir_inativos.sql`
2. Volte ao **SQL Editor** do Supabase
3. Cole o conteudo do arquivo
4. Click em **RUN**

**Verificar:**
```sql
SELECT COUNT(*) FROM leads WHERE origem_consentimento = 'planilha_inativos';
-- Deve retornar 30 (ou o numero de alunos processados)
```

---

## PASSO 4: DEPLOY WAHA NO RAILWAY (3 min)

### 4.1 Criar Conta Railway

1. Acesse: https://railway.app/
2. Login com GitHub

### 4.2 Criar Projeto

1. Click em **New Project**
2. Selecione **Deploy from GitHub repo**
3. Conecte seu repositorio `waha-n8n-stack` (ou use template)

### 4.3 Configurar WAHA

**Opcao A: Deploy via Dockerfile**

1. No Railway, click em **New Service**
2. Selecione **Dockerfile**
3. Aponte para: `infra/railway.waha.Dockerfile`
4. Click em **Deploy**

**Opcao B: Deploy via Imagem Docker**

1. No Railway, click em **New Service**
2. Selecione **Docker Image**
3. Imagem: `devlikeapro/waha:latest`
4. Click em **Deploy**

### 4.4 Expor URL Publica

1. Na aba **Settings** do servico WAHA
2. Secao **Networking**
3. Click em **Generate Domain**
4. Copie a URL gerada (ex: `waha-production-abc123.up.railway.app`)

### 4.5 Escanear QR Code

1. Aguarde deploy finalizar (1-2 min)
2. Acesse os **Logs** do servico
3. Procure por QR Code ASCII art
4. Escaneie com WhatsApp (Configuracoes > Aparelhos conectados)

**Aguarde mensagem:** `WhatsApp session started`

---

## PASSO 5: CONFIGURAR VARIAVEIS DE AMBIENTE (1 min)

### 5.1 Criar arquivo .env

```bash
cd C:\Users\User\waha-n8n-stack\ops
copy .env.sample .env
```

### 5.2 Editar .env

Abra `ops\.env` e preencha:

```env
# Supabase (do Passo 2.3)
SUPABASE_URL=https://eiqzckhcmmfyddruaxdj.supabase.co
SUPABASE_SERVICE_ROLE=eyJhbGc...seu-service-role-key-aqui

# WAHA (URL do Railway - Passo 4.4)
WAHA_BASE_URL=https://waha-production-abc123.up.railway.app
WAHA_SEND_TEXT_PATH=/api/sendText
WAHA_SESSION=default

# Limites
LIMITE_DIARIO=30
```

**Salve o arquivo!**

---

## PASSO 6: TESTAR ENVIO MANUAL (1 min)

### 6.1 Carregar Variaveis de Ambiente

```bash
cd C:\Users\User\waha-n8n-stack\scripts

# Windows CMD
set SUPABASE_URL=https://eiqzckhcmmfyddruaxdj.supabase.co
set SUPABASE_SERVICE_ROLE=sua-key-aqui
set WAHA_BASE_URL=https://sua-url-railway.up.railway.app
set LIMITE_DIARIO=1

# Windows PowerShell
$env:SUPABASE_URL="https://eiqzckhcmmfyddruaxdj.supabase.co"
$env:SUPABASE_SERVICE_ROLE="sua-key-aqui"
$env:WAHA_BASE_URL="https://sua-url-railway.up.railway.app"
$env:LIMITE_DIARIO="1"
```

### 6.2 Executar Teste

```bash
python enviar_diario.py
```

**Resultado esperado:**
```
Iniciando envio diario de WhatsApp
Timestamp: 2025-10-03T...
Limite: 1 mensagens

Variaveis de ambiente validadas
Conectado ao Supabase
1 leads encontrados para envio

[1/1] Processando [Nome do Aluno]...
Enviado para [Nome] (+5565XXXXXXXXX)
Log registrado para [Nome]
Lead [id] marcado como ativado

==================================================
Concluido!
Sucessos: 1
Erros: 0
Total processado: 1
==================================================
```

### 6.3 Verificar no WhatsApp

- Abra o WhatsApp conectado
- Deve aparecer a mensagem enviada

**IMPORTANTE:** Se der erro, verifique:
1. WAHA esta rodando? (Logs no Railway)
2. WhatsApp esta conectado? (QR Code escaneado?)
3. Credenciais Supabase corretas?

---

## PASSO 7: AUTOMATIZAR ENVIOS DIARIOS (OPCIONAL)

### Opcao A: Agendador Windows (Task Scheduler)

1. Abra **Task Scheduler** (Agendador de Tarefas)
2. **Create Basic Task** (Criar Tarefa Basica)
3. Nome: `Enviar WhatsApp Inativos`
4. Trigger: **Daily** - 09:00 AM
5. Action: **Start a program**
   - Program: `python`
   - Arguments: `C:\Users\User\waha-n8n-stack\scripts\enviar_diario.py`
   - Start in: `C:\Users\User\waha-n8n-stack\scripts`

### Opcao B: Usar N8N (Workflow Visual)

1. Suba o N8N local:
```bash
cd C:\Users\User\waha-n8n-stack\infra
docker-compose up -d
```

2. Acesse: http://localhost:5678
3. Login: `admin` / `change_this_password_123`
4. Importe workflow do repositorio (se disponivel)

### Opcao C: Railway Cron Job (Recomendado para Producao)

1. No Railway, adicione **Cron Job Service**
2. Schedule: `0 9 * * *` (todo dia 9h)
3. Command:
```bash
cd /app/scripts && python enviar_diario.py
```

---

## VERIFICACOES FINAIS

### Checklist de Funcionamento

- [ ] Python instalado e dependencias OK
- [ ] Schema SQL executado no Supabase
- [ ] 30 leads importados (verificar: `SELECT COUNT(*) FROM leads;`)
- [ ] WAHA deployado no Railway
- [ ] QR Code escaneado e WhatsApp conectado
- [ ] Arquivo `.env` configurado
- [ ] Teste manual enviou 1 mensagem com sucesso
- [ ] Automacao configurada (opcional)

### Monitoramento

**Ver leads pendentes:**
```sql
SELECT * FROM leads_para_ativar LIMIT 10;
```

**Ver historico de envios:**
```sql
SELECT
  l.nome,
  l.telefone,
  e.status_envio,
  e.enviado_em
FROM whatsapp_envios e
JOIN leads l ON e.lead_id = l.id
ORDER BY e.enviado_em DESC
LIMIT 20;
```

**Ver estatisticas:**
```sql
SELECT
  status_envio,
  COUNT(*) as total
FROM whatsapp_envios
GROUP BY status_envio;
```

---

## TROUBLESHOOTING

### Erro: "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### Erro: "WAHA connection refused"
- Verifique se WAHA esta rodando (Railway Logs)
- Teste URL: `https://sua-url.railway.app/health`

### Erro: "Supabase unauthorized"
- Confirme que esta usando `service_role` (nao `anon` key)
- Verifique se a key nao tem espacos extras

### Erro: "No leads found"
- Execute novamente: `python processar_inativos.py`
- Verifique: `SELECT * FROM leads WHERE consentido = true;`

### WhatsApp desconecta
- Reescaneie QR Code nos logs do Railway
- WAHA salva sessao, mas pode expirar

---

## PROXIMOS PASSOS

1. **Monitorar primeiros 7 dias**
   - Acompanhe taxa de resposta
   - Ajuste mensagem se necessario

2. **Implementar opt-out**
   - Usuarios podem responder "PARAR"
   - Adicionar webhook para processar respostas

3. **Escalar para N8N**
   - Workflows visuais
   - Respostas automaticas
   - Funis de reativacao

4. **Analytics**
   - Dashboard de metricas
   - Taxa de conversao
   - ROI do sistema

---

## SUPORTE

- **Documentacao Supabase:** https://supabase.com/docs
- **Documentacao WAHA:** https://waha.devlike.pro/
- **Railway Docs:** https://docs.railway.app/

## CONFORMIDADE LGPD

Este sistema foi projetado em conformidade com a LGPD:
- Consentimento explicito rastreado (`consentido` = true)
- Opt-out disponivel (funcao `opt_out_lead`)
- Auditoria completa (tabela `whatsapp_envios`)
- Retencao controlada (`data_exclusao_programada`)

**Consulte:** `SECURITY_LGPD.md` para detalhes completos.

---

**MVP PRONTO! Voce agora tem um sistema funcional de reativacao via WhatsApp.**
