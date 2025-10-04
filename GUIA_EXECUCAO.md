# 🚀 GUIA DE EXECUÇÃO - Passo a Passo

## ✅ PASSO 1: Instalar Python (5 minutos)

### Opção A: Microsoft Store (MAIS FÁCIL)
1. Aperte `Win + S`
2. Digite "Microsoft Store"
3. Pesquise "Python 3.11"
4. Clique em "Obter" / "Instalar"
5. Aguarde instalação

### Opção B: Download direto
1. Acesse: https://www.python.org/downloads/
2. Baixe "Python 3.11.x" (Windows installer)
3. Execute o instalador
4. ⚠️ **IMPORTANTE**: Marque "Add Python to PATH"
5. Clique "Install Now"

### Verificar instalação
Abra um NOVO terminal (Git Bash ou CMD) e digite:
```bash
python --version
# Deve mostrar: Python 3.11.x
```

---

## ✅ PASSO 2: Configurar Supabase (2 minutos)

### 2.1 Acessar Supabase
1. Abra: https://supabase.com/dashboard/project/eiqzckhcmmfyddruaxdj/sql/new
2. Faça login (você já tem o projeto)

### 2.2 Executar Schema SQL
1. Abra o arquivo: `C:\Users\User\waha-n8n-stack\supabase\schema.sql`
2. Copie TODO o conteúdo (Ctrl+A, Ctrl+C)
3. Cole no Supabase SQL Editor
4. Clique "Run" (▶️)
5. Aguarde confirmação: "Success. No rows returned"

### 2.3 Pegar credenciais
1. Vá em: Settings → API
2. Copie:
   - **Project URL**: `https://eiqzckhcmmfyddruaxdj.supabase.co`
   - **service_role key** (secreta, começa com `eyJ...`)

---

## ✅ PASSO 3: Configurar Variáveis (.env)

### 3.1 Criar arquivo .env
```bash
cd C:\Users\User\waha-n8n-stack\ops
copy .env.sample .env
```

### 3.2 Editar .env
Abra `C:\Users\User\waha-n8n-stack\ops\.env` no Bloco de Notas e preencha:

```env
SUPABASE_URL=https://eiqzckhcmmfyddruaxdj.supabase.co
SUPABASE_SERVICE_ROLE=eyJ... (cole aqui a chave do passo 2.3)
WAHA_BASE_URL=http://localhost:3000
WAHA_SEND_TEXT_PATH=/api/sendText
LIMITE_DIARIO=30
```

Salve e feche.

---

## ✅ PASSO 4: Processar AlunosInativos.xlsx

### 4.1 Instalar dependências Python
```bash
cd C:\Users\User\waha-n8n-stack\scripts
pip install openpyxl pandas
```

### 4.2 Executar processador
```bash
python processar_inativos.py C:\Users\User\Downloads\AlunosInativos.xlsx
```

**Resultado esperado:**
- ✅ Mostra preview dos 10 primeiros alunos
- ✅ Gera arquivo: `inserir_inativos.sql`

---

## ✅ PASSO 5: Inserir Leads no Supabase

### 5.1 Abrir SQL gerado
Abra: `C:\Users\User\waha-n8n-stack\scripts\inserir_inativos.sql`

### 5.2 Executar no Supabase
1. Volte ao Supabase SQL Editor
2. Cole o conteúdo de `inserir_inativos.sql`
3. Clique "Run" (▶️)
4. Aguarde: "Success"

### 5.3 Verificar inserção
Execute no Supabase:
```sql
SELECT * FROM leads WHERE origem_consentimento = 'planilha_inativos' LIMIT 10;
```

Deve mostrar os alunos importados.

---

## ✅ PASSO 6: Deploy WAHA (WhatsApp)

### Opção A: Railway (Nuvem - RECOMENDADO)

#### 6.1 Instalar Railway CLI
```bash
# Windows (Git Bash)
npm install -g @railway/cli
# OU baixe: https://railway.app/cli
```

#### 6.2 Login
```bash
railway login
```

#### 6.3 Deploy WAHA
```bash
cd C:\Users\User\waha-n8n-stack\infra
railway init
railway up --dockerfile railway.waha.Dockerfile
```

Copie a URL gerada (ex: `https://waha-production-xxxx.up.railway.app`)

#### 6.4 Conectar WhatsApp
1. Acesse a URL do Railway
2. Vá em "Sessions" → "Start new session"
3. Nome: `default`
4. Escanear QR Code com WhatsApp

### Opção B: Local (Docker)

#### 6.1 Instalar Docker Desktop
1. Baixe: https://www.docker.com/products/docker-desktop/
2. Instale e reinicie o PC
3. Abra Docker Desktop

#### 6.2 Subir WAHA localmente
```bash
cd C:\Users\User\waha-n8n-stack\infra
docker compose --env-file ../ops/.env up -d waha
```

#### 6.3 Conectar WhatsApp
1. Acesse: http://localhost:3000
2. Siga passo 6.4 acima

---

## ✅ PASSO 7: Testar Envio

### 7.1 Atualizar WAHA_BASE_URL

Se usou Railway, edite `ops/.env`:
```env
WAHA_BASE_URL=https://waha-production-xxxx.up.railway.app
```

### 7.2 Instalar dependências do script
```bash
cd C:\Users\User\waha-n8n-stack\scripts
pip install -r requirements.txt
```

### 7.3 Executar script de envio
```bash
python enviar_diario.py
```

**Resultado esperado:**
```
🚀 Iniciando envio diário de WhatsApp
✅ Conectado ao Supabase
📋 30 leads encontrados para envio
✅ Enviado para João Silva (+5565999999999)
...
✅ Concluído!
📊 Sucessos: 30
```

---

## ✅ PASSO 8: Verificar Logs

No Supabase SQL Editor:
```sql
SELECT
    l.nome,
    l.telefone,
    e.status_envio,
    e.enviado_em
FROM whatsapp_envios e
JOIN leads l ON e.lead_id = l.id
ORDER BY e.enviado_em DESC
LIMIT 30;
```

---

## ✅ PASSO 9: Automatizar (Opcional)

### Opção A: Windows Task Scheduler
1. Abra "Agendador de Tarefas"
2. Criar Tarefa Básica
3. Nome: "Envio WhatsApp Diário"
4. Gatilho: Diariamente às 09:00
5. Ação: Iniciar programa
   - Programa: `python`
   - Argumentos: `C:\Users\User\waha-n8n-stack\scripts\enviar_diario.py`
6. Salvar

### Opção B: GitHub Actions (Grátis, nuvem)
Veja: `scripts/README.md` seção "Setup GitHub Actions"

---

## 🆘 TROUBLESHOOTING

### Python não encontrado
```bash
# Feche e reabra o terminal após instalar Python
# Ou adicione manualmente ao PATH:
# Win + R → sysdm.cpl → Avançado → Variáveis de Ambiente
# Adicione: C:\Users\User\AppData\Local\Programs\Python\Python311
```

### Erro "ModuleNotFoundError: No module named 'supabase'"
```bash
cd C:\Users\User\waha-n8n-stack\scripts
pip install -r requirements.txt
```

### WAHA não conecta WhatsApp
- Verifique se WhatsApp Web está funcionando no navegador
- Use número que nunca foi banido
- Tente recriar a sessão

### Erro "SUPABASE_URL not set"
- Verifique se o arquivo `.env` está na pasta `ops/`
- Certifique-se de salvar o arquivo após editar

### Leads não aparecem
```sql
-- Verificar se schema foi criado:
SELECT * FROM leads LIMIT 1;

-- Se der erro "relation does not exist":
-- Execute novamente o schema.sql (Passo 2.2)
```

---

## 📞 PRÓXIMOS PASSOS

1. ✅ Processar planilha → Gerar SQL → Inserir no Supabase
2. ✅ Deploy WAHA → Conectar WhatsApp
3. ✅ Testar envio manual (`python enviar_diario.py`)
4. ✅ Automatizar (Task Scheduler ou GitHub Actions)
5. ✅ Monitorar logs no Supabase

---

## 📊 CUSTOS

- **Supabase**: R$ 0 (free tier 500MB)
- **Railway**: R$ 0 (free tier 500h/mês)
- **GitHub Actions**: R$ 0 (free tier 2000min/mês)
- **TOTAL**: R$ 0/mês para até 900 mensagens/mês

---

## ⚠️ IMPORTANTE LGPD

Antes de enviar em massa, confirme que os alunos **consentiram** em receber mensagens.

Veja: `SECURITY_LGPD.md` para detalhes completos.
