# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sistema de reativação de alunos inativos via WhatsApp automatizado, usando WAHA (WhatsApp HTTP API), Supabase (PostgreSQL), e Python scripts. O sistema é LGPD-compliant e permite envio programado de mensagens personalizadas.

**Tech Stack:**
- **Backend**: Supabase (PostgreSQL serverless)
- **WhatsApp API**: WAHA (devlikeapro/waha) deployed on Railway
- **Automation**: Python scripts + optional n8n workflows
- **Infrastructure**: Docker Compose (local) + Railway (production)

## Common Commands

### Development Setup

```bash
# Install Python dependencies
cd C:\Users\User\waha-n8n-stack\scripts
pip install -r requirements.txt

# Start local WAHA + n8n stack
cd C:\Users\User\waha-n8n-stack\infra
docker-compose up -d

# Stop services
docker-compose down
```

### Database Operations

```bash
# Execute Supabase schema (via Supabase Dashboard SQL Editor)
# URL: https://supabase.com/dashboard/project/eiqzckhcmmfyddruaxdj/sql/new
# Paste content from: supabase/schema.sql

# Verify tables created
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

# Check leads status
SELECT COUNT(*) FROM leads_para_ativar;
SELECT * FROM whatsapp_envios ORDER BY enviado_em DESC LIMIT 10;
```

### WhatsApp Operations

```bash
# Process Excel and generate SQL
cd scripts
python processar_inativos.py

# Send WhatsApp messages (manual test)
python enviar_diario.py

# Windows automation wrappers
executar_envio.bat
executar_envio.ps1

# Setup Windows Task Scheduler (requires Admin)
criar_tarefa_agendada.bat
```

### Testing

```bash
# Test WAHA health
curl https://your-railway-url.up.railway.app/health

# Test single WhatsApp message
curl -X POST https://your-railway-url.up.railway.app/api/sendText \
  -H "Content-Type: application/json" \
  -d '{"chatId": "5565999999999@c.us", "text": "Teste", "session": "default"}'

# Reset lead for retesting (dev only)
UPDATE leads SET whatsapp_ativado = false WHERE telefone = '+5565999999999';
```

## Architecture

### System Flow

```
Excel (AlunosInativos.xlsx)
    ↓ processar_inativos.py
Supabase (PostgreSQL) ← Insert via SQL
    ↓ leads_para_ativar (view)
enviar_diario.py → WAHA API (Railway) → WhatsApp Business
    ↓ logs
whatsapp_envios (audit table)
```

### Key Components

**1. Database (Supabase)**
- `leads` table: Student data with LGPD consent tracking
- `whatsapp_envios` table: Message audit log
- `leads_para_ativar` view: Filtered leads ready for activation (max 20/day)
- Triggers: `normalize_telefone_trigger`, `update_leads_updated_at`
- Functions: `opt_out_lead(telefone)` for LGPD compliance

**2. Python Scripts**
- `processar_inativos.py`: Processes Excel file, normalizes phone numbers, generates SQL
- `enviar_diario.py`: Main automation script - queries leads, sends WhatsApp, logs results
- Dependencies: supabase, requests, python-dotenv, openpyxl, pandas

**3. WAHA (WhatsApp API)**
- Deployed on Railway using `infra/railway.waha.Dockerfile`
- Connects via QR code scan
- API endpoint: `POST /api/sendText` with `{chatId, text, session}`
- Phone format: `5565999999999@c.us` (without +, with @c.us suffix)

**4. Infrastructure**
- Local: `infra/docker-compose.yml` runs WAHA + n8n
- Production: Railway deployment for WAHA
- Configuration: `ops/.env.sample` template

### LGPD Compliance Architecture

Sistema implementa LGPD (Lei Geral de Proteção de Dados) compliance:
- **Consent tracking**: `consentido`, `data_consentimento`, `origem_consentimento` fields
- **Opt-out mechanism**: `opt_out` flag + `opt_out_lead()` function
- **Audit trail**: All messages logged in `whatsapp_envios` with timestamps
- **Data retention**: `data_exclusao_programada` for automatic deletion
- **Data minimization**: Only essential fields collected

## Environment Variables

Required in `ops/.env`:

```bash
# Supabase (use service_role key, not anon key)
SUPABASE_URL=https://eiqzckhcmmfyddruaxdj.supabase.co
SUPABASE_SERVICE_ROLE=eyJhbGc...

# WAHA (Railway public URL)
WAHA_BASE_URL=https://your-app.up.railway.app
WAHA_SEND_TEXT_PATH=/api/sendText
WAHA_SESSION=default

# Limits
LIMITE_DIARIO=30
```

## Important Implementation Details

### Phone Number Normalization

- Input formats accepted: Various (Excel formatting, with/without spaces)
- Stored format: `+5565999999999` (E.164 format)
- WAHA format: `5565999999999@c.us` (WhatsApp chat ID)
- Normalization happens via `normalize_telefone()` database trigger and Python functions

### Message Flow

1. `enviar_diario.py` queries `leads_para_ativar` view (filters: `consentido=true`, `whatsapp_ativado=false`, `opt_out=false`)
2. Limit enforced: `LIMITE_DIARIO` (default 30)
3. For each lead:
   - Format personalized message with `{nome}` and `{data_consentimento}`
   - Convert phone to WAHA format (`normalizar_chat_id()`)
   - POST to WAHA `/api/sendText`
   - Log result to `whatsapp_envios` (always, success or failure)
   - Mark `whatsapp_ativado=true` only on success

### Error Handling

- Network errors: Logged with status='falha', lead remains `whatsapp_ativado=false`
- Supabase errors: Script exits with error message
- WAHA disconnection: Check Railway logs for QR code to reconnect
- Missing environment variables: Script validates and exits early

## Development Workflow

### Adding New Leads

1. Update Excel file: `C:\Users\User\Downloads\AlunosInativos.xlsx`
2. Run: `python processar_inativos.py`
3. Review generated: `scripts/inserir_inativos.sql`
4. Execute SQL in Supabase SQL Editor
5. Verify: `SELECT * FROM leads WHERE origem_consentimento = 'planilha_inativos';`

### Customizing Messages

Edit `MENSAGEM_TEMPLATE` in `scripts/enviar_diario.py`:
```python
MENSAGEM_TEMPLATE = """Olá {nome}! 👋
[Your custom message]
Para cancelar, responda PARAR.
Autorizado em {data_consentimento}."""
```

### Deployment

**Railway (WAHA only):**
1. New Project > Docker Image: `devlikeapro/waha:latest`
2. Generate Domain (copy URL to `WAHA_BASE_URL`)
3. View logs, scan QR code with WhatsApp
4. Verify: `curl https://your-url.up.railway.app/health`

**Automation (Daily execution):**
- Option A: Windows Task Scheduler via `criar_tarefa_agendada.bat`
- Option B: Railway Cron Job (run `enviar_diario.py` with env vars)
- Option C: n8n workflow (Schedule trigger → Execute Command)

## Project Structure Notes

- `/scripts`: Executable Python scripts (main automation logic)
- `/supabase`: Database schema only (no migrations, execute manually)
- `/infra`: Docker setup for local dev + Railway deployment file
- `/ops`: Configuration templates and deployment guides
- `/n8n`: Optional workflow automation (not required for MVP)
- Documentation: `COMECE_AQUI.md` (start here), `GUIA_MVP_5MIN.md` (detailed guide), `QUICKSTART.md` (checklist), `SECURITY_LGPD.md` (compliance details)

## Useful SQL Queries

```sql
-- System status overview
SELECT COUNT(*) as total_leads FROM leads;
SELECT COUNT(*) as pending FROM leads_para_ativar;
SELECT COUNT(*) as activated FROM leads WHERE whatsapp_ativado = true;

-- Today's sending activity
SELECT COUNT(*) FROM whatsapp_envios WHERE DATE(enviado_em) = CURRENT_DATE;

-- Success rate analysis
SELECT status_envio, COUNT(*) as total,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentual
FROM whatsapp_envios GROUP BY status_envio;

-- Recent errors
SELECT * FROM whatsapp_envios
WHERE status_envio = 'falha'
ORDER BY enviado_em DESC LIMIT 10;
```

## Troubleshooting

- **ModuleNotFoundError**: Run `pip install -r scripts/requirements.txt`
- **Supabase Unauthorized**: Verify using `service_role` key (not `anon`), check for trailing spaces
- **WAHA Connection Refused**: Check Railway container is running, rescan QR if session expired
- **No leads found**: Verify `SELECT * FROM leads WHERE consentido = true AND whatsapp_ativado = false;`
- **Phone format issues**: Database trigger auto-normalizes, verify output: `SELECT telefone FROM leads LIMIT 5;`

## Security & Compliance

- **Never commit** `.env` files (use `.env.sample` as template)
- **Use service_role key** only server-side, never expose in frontend/logs
- **LGPD compliance**: Always verify `consentido=true` before sending messages
- **Opt-out support**: Implement webhook to process "PARAR" responses and call `opt_out_lead(telefone)`
- **Rate limiting**: Respect `LIMITE_DIARIO=30` to avoid WhatsApp blocking
