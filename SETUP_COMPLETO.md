# 🚀 Setup Completo - Sistema de Reativação WhatsApp

## 📋 Estado Atual do Projeto

### ✅ O que já está configurado:

1. **Supabase (Banco de Dados)**
   - URL: `https://oprrsfeljeyuebqarhjn.supabase.co`
   - Schema completo criado (tabelas, views, functions, triggers)
   - 346 leads importados da planilha `ModeloVencidas.xlsx`

2. **WAHA (WhatsApp API)**
   - Deploy no Render.com
   - URL: `https://waha-latest-yaa7.onrender.com`
   - API Key configurada: `eCf1Zo2N2Gdj54WzXajbmeOdBT1y7CT0iRIWCn8nLqQ`

3. **Scripts Python**
   - `processar_vencidos.py` - Processa planilha Excel e gera SQL
   - `enviar_diario.py` - Envia mensagens WhatsApp (até 30/dia)
   - Todas as dependências instaladas

---

## 🔧 Para usar em outro computador:

### 1️⃣ Clonar o repositório

```bash
git clone <URL_DO_SEU_REPO>
cd waha-n8n-stack
```

### 2️⃣ Instalar Python e dependências

```bash
# Verificar Python instalado
python --version  # ou py --version no Windows

# Instalar dependências
cd scripts
pip install -r requirements.txt
```

### 3️⃣ Criar arquivo .env

Copie `scripts/.env.sample` para `scripts/.env` e configure:

```bash
# Supabase Configuration
SUPABASE_URL=https://oprrsfeljeyuebqarhjn.supabase.co
SUPABASE_SERVICE_ROLE=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wcnJzZmVsamV5dWVicWFyaGpuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1OTUyNzc2OCwiZXhwIjoyMDc1MTAzNzY4fQ.VY8b_r7tPumQvRtEBeh1POSFuPdwY9fBnf_9vm2U2Ec

# WAHA Configuration
WAHA_BASE_URL=https://waha-latest-yaa7.onrender.com
WAHA_SEND_TEXT_PATH=/api/sendText
WAHA_SESSION=default
WAHA_API_KEY=eCf1Zo2N2Gdj54WzXajbmeOdBT1y7CT0iRIWCn8nLqQ

# Limites
LIMITE_DIARIO=30
```

### 4️⃣ Conectar WhatsApp (se ainda não conectou)

1. Acesse: https://waha-latest-yaa7.onrender.com/api/default/auth/qr
2. Escaneie o QR Code com WhatsApp
3. Verifique conexão: https://waha-latest-yaa7.onrender.com/api/sessions

### 5️⃣ Testar envio

```bash
cd scripts
python enviar_diario.py
```

---

## 📊 Estrutura do Projeto

```
waha-n8n-stack/
├── scripts/
│   ├── processar_vencidos.py    # Processa Excel → SQL
│   ├── enviar_diario.py          # Envia WhatsApp
│   ├── requirements.txt          # Dependências Python
│   └── .env                      # Credenciais (NÃO commitar!)
│
├── supabase/
│   └── schema.sql                # Schema do banco de dados
│
├── ModeloVencidas.xlsx           # Planilha de leads
│
└── documentação/
    ├── COMECE_AQUI.md
    ├── GUIA_MVP_5MIN.md
    ├── QUICKSTART.md
    └── SECURITY_LGPD.md
```

---

## 🔑 Credenciais Importantes (guardar com segurança!)

### Supabase
- **URL**: https://oprrsfeljeyuebqarhjn.supabase.co
- **Anon Key**: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wcnJzZmVsamV5dWVicWFyaGpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk1Mjc3NjgsImV4cCI6MjA3NTEwMzc2OH0.6hQngVyKniCVXHs4C9586yWavPToYZ0XZNuFzfBUFFg
- **Service Role**: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wcnJzZmVsamV5dWVicWFyaGpuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1OTUyNzc2OCwiZXhwIjoyMDc1MTAzNzY4fQ.VY8b_r7tPumQvRtEBeh1POSFuPdwY9fBnf_9vm2U2Ec

### WAHA (Render.com)
- **URL**: https://waha-latest-yaa7.onrender.com
- **API Key**: eCf1Zo2N2Gdj54WzXajbmeOdBT1y7CT0iRIWCn8nLqQ

### Render.com
- Acesse: https://dashboard.render.com
- Serviço: `waha-latest-yaa7`

---

## 📝 Queries Úteis (Supabase SQL Editor)

```sql
-- Ver total de leads
SELECT COUNT(*) FROM leads;

-- Ver leads prontos para envio
SELECT * FROM leads_para_ativar LIMIT 10;

-- Ver histórico de envios
SELECT * FROM whatsapp_envios ORDER BY enviado_em DESC LIMIT 20;

-- Resetar lead para teste
UPDATE leads SET whatsapp_ativado = false WHERE telefone = '+5566999999999';

-- Marcar lead como opt-out
SELECT opt_out_lead('+5566999999999');
```

---

## 🚨 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'supabase'"
```bash
pip install -r scripts/requirements.txt
```

### Erro: "WAHA connection refused"
- Verifique se WAHA está rodando: https://waha-latest-yaa7.onrender.com/api/sessions
- Verifique se WhatsApp está conectado (QR Code escaneado)

### Erro: "Supabase unauthorized"
- Confirme que está usando `SUPABASE_SERVICE_ROLE` (não `anon`)
- Verifique se não há espaços extras na chave

### Nenhum lead encontrado
```sql
-- Verificar leads disponíveis
SELECT COUNT(*) FROM leads WHERE consentido = true AND whatsapp_ativado = false;
```

---

## 📞 Próximos Passos

1. ✅ Conectar WhatsApp (se ainda não conectou)
2. ✅ Testar envio com 1 lead
3. ✅ Ajustar mensagem em `scripts/enviar_diario.py`
4. ✅ Configurar automação (Windows Task Scheduler ou cron)

---

**Última atualização**: 2025-10-03
**Status**: ✅ Pronto para uso
