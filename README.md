# Sistema de Reativacao de Alunos via WhatsApp

**MVP Completo** - Sistema automatizado para reativar alunos inativos usando WhatsApp Business API (WAHA) + Supabase

---

## Visao Geral

Sistema que processa lista de alunos inativos e envia mensagens personalizadas via WhatsApp de forma automatizada, com total conformidade LGPD.

**Funcionalidades:**
- Processamento automatico de planilhas Excel
- Envio programado de mensagens WhatsApp
- Rastreamento de consentimento LGPD
- Auditoria completa de envios
- Opt-out automatico
- Priorizacao inteligente de leads

---

## Inicio Rapido (5 minutos)

### Opcao 1: Guia Visual Passo-a-Passo
**Recomendado para iniciantes**

Siga o guia completo: **[GUIA_MVP_5MIN.md](GUIA_MVP_5MIN.md)**

### Opcao 2: Checklist Executavel
**Para usuarios experientes**

Execute conforme: **[QUICKSTART.md](QUICKSTART.md)**

### Opcao 3: Setup Automatizado
**Automatiza instalacao e configuracao**

```bash
cd C:\Users\User\waha-n8n-stack\scripts
setup_completo.bat
```

---

## Arquitetura do Sistema

```
┌─────────────────┐
│  Excel          │
│  (Inativos)     │
└────────┬────────┘
         │
         │ processar_inativos.py
         ▼
┌─────────────────┐
│  Supabase       │
│  (PostgreSQL)   │◄────┐
└────────┬────────┘     │
         │              │
         │ enviar_      │ logs
         │ diario.py    │
         ▼              │
┌─────────────────┐     │
│  WAHA API       │─────┘
│  (Railway)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  WhatsApp       │
│  Business       │
└─────────────────┘
```

### Componentes

1. **Supabase (Banco de Dados)**
   - Tabela `leads`: Dados dos alunos
   - Tabela `whatsapp_envios`: Auditoria de mensagens
   - View `leads_para_ativar`: Lista priorizada
   - Funcoes LGPD: Opt-out, retencao

2. **WAHA (WhatsApp API)**
   - Deploy no Railway (gratis)
   - Conecta WhatsApp via QR Code
   - API REST para envio de mensagens

3. **Scripts Python**
   - `processar_inativos.py`: Processa Excel
   - `enviar_diario.py`: Envia mensagens
   - Automacao via Task Scheduler ou Cron

---

## Estrutura do Projeto

```
waha-n8n-stack/
├── README.md                    # Este arquivo
├── GUIA_MVP_5MIN.md            # Guia passo-a-passo completo
├── QUICKSTART.md               # Checklist executavel
├── SECURITY_LGPD.md            # Conformidade LGPD
├── ASSUNCOES.md                # Premissas do projeto
│
├── supabase/
│   └── schema.sql              # Schema do banco (LGPD compliant)
│
├── scripts/
│   ├── requirements.txt        # Dependencias Python
│   ├── processar_inativos.py   # Processa planilha Excel
│   ├── enviar_diario.py        # Envia mensagens WhatsApp
│   │
│   ├── executar_envio.bat      # Script Windows para envio
│   ├── executar_envio.ps1      # Script PowerShell para envio
│   ├── processar_e_importar.bat # Processa e gera SQL
│   ├── setup_completo.bat      # Setup automatizado
│   │
│   ├── criar_tarefa_agendada.bat        # Cria agendamento Windows
│   └── agendar_tarefa_windows.xml       # Config Task Scheduler
│
├── ops/
│   ├── .env.sample             # Template de configuracao
│   └── README_deploy.md        # Guia de deploy
│
├── infra/
│   ├── docker-compose.yml      # WAHA + N8N local
│   └── railway.waha.Dockerfile # Deploy WAHA no Railway
│
└── n8n/
    └── workflows/              # Workflows N8N (opcional)
```

---

## Pre-Requisitos

- **Python 3.8+** (instalar de: https://www.python.org/downloads/)
- **Conta Supabase** (gratis: https://supabase.com)
- **Conta Railway** (gratis - $5 credito: https://railway.app)
- **WhatsApp** (pessoal ou Business)
- **Planilha Excel** com dados dos alunos inativos

---

## Instalacao

### 1. Clonar/Baixar Projeto

```bash
# Se for Git
git clone https://github.com/seu-usuario/waha-n8n-stack.git
cd waha-n8n-stack

# Ou baixar ZIP e extrair
```

### 2. Instalar Dependencias Python

```bash
cd scripts
pip install -r requirements.txt
```

**Pacotes instalados:**
- `supabase==2.3.4` - Cliente Supabase
- `requests==2.31.0` - HTTP requests
- `python-dotenv==1.0.0` - Variaveis de ambiente
- `openpyxl==3.1.2` - Leitura de Excel
- `pandas==2.1.4` - Manipulacao de dados

### 3. Configurar Supabase

1. Acesse: https://supabase.com/dashboard/project/eiqzckhcmmfyddruaxdj
2. SQL Editor > New Query
3. Cole e execute: `supabase/schema.sql`

### 4. Deploy WAHA no Railway

1. Acesse: https://railway.app/new
2. New Service > Docker Image
3. Image: `devlikeapro/waha:latest`
4. Generate Domain (copie a URL)
5. Escaneie QR Code nos logs

### 5. Configurar Variaveis

```bash
cd ops
copy .env.sample .env
notepad .env
```

Preencha:
```env
SUPABASE_URL=https://eiqzckhcmmfyddruaxdj.supabase.co
SUPABASE_SERVICE_ROLE=sua-key-aqui
WAHA_BASE_URL=https://sua-url-railway.up.railway.app
```

---

## Uso

### Processar Planilha de Inativos

```bash
cd scripts
python processar_inativos.py
```

**Ou use o script automatizado:**
```bash
processar_e_importar.bat
```

**Resultado:**
- Gera `inserir_inativos.sql`
- Importe no Supabase SQL Editor

### Enviar Mensagens Manualmente

```bash
cd scripts
python enviar_diario.py
```

**Ou use os scripts:**

Windows CMD:
```bash
executar_envio.bat
```

PowerShell:
```powershell
.\executar_envio.ps1
```

### Automatizar Envios Diarios

**Windows Task Scheduler:**
```bash
# Execute como Administrador
cd scripts
criar_tarefa_agendada.bat
```

**Railway Cron Job (Recomendado):**
1. New Service > Cron Job
2. Schedule: `0 9 * * *`
3. Command: `cd /app/scripts && python enviar_diario.py`

---

## Monitoramento

### Ver Status no Supabase

```sql
-- Leads totais
SELECT COUNT(*) FROM leads;

-- Leads pendentes (prontos para enviar)
SELECT COUNT(*) FROM leads_para_ativar;

-- Leads ja ativados
SELECT COUNT(*) FROM leads WHERE whatsapp_ativado = true;

-- Historico de envios hoje
SELECT * FROM whatsapp_envios
WHERE DATE(enviado_em) = CURRENT_DATE
ORDER BY enviado_em DESC;

-- Taxa de sucesso
SELECT
  status_envio,
  COUNT(*) as total,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentual
FROM whatsapp_envios
GROUP BY status_envio;
```

### Verificar WAHA

```bash
# Health check
curl https://sua-url-railway.up.railway.app/health

# Status da sessao
curl https://sua-url-railway.up.railway.app/api/sessions
```

---

## Conformidade LGPD

O sistema esta 100% conforme com a LGPD (Lei Geral de Protecao de Dados):

- **Consentimento Explicito**: Campo `consentido` rastreado
- **Finalidade Especifica**: Origem do consentimento registrada
- **Direito ao Opt-Out**: Funcao `opt_out_lead()` disponivel
- **Auditoria Completa**: Todas as operacoes em `whatsapp_envios`
- **Retencao Controlada**: `data_exclusao_programada` automatica
- **Minimizacao de Dados**: Apenas dados essenciais coletados

**Detalhes completos:** [SECURITY_LGPD.md](SECURITY_LGPD.md)

---

## Troubleshooting

### Python nao encontrado
```bash
# Windows: Baixar de python.org
# Marcar "Add Python to PATH" na instalacao
```

### Erro ao instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

### WAHA desconectou
- Reescaneie QR Code nos logs do Railway
- Verifique se o plano Railway nao expirou

### Supabase unauthorized
- Confirme que esta usando `service_role` key (nao `anon`)
- Verifique se a key esta sem espacos extras

### Nenhum lead encontrado
```sql
-- Verificar se leads foram importados
SELECT * FROM leads WHERE consentido = true LIMIT 10;

-- Verificar se ja foram ativados
SELECT * FROM leads WHERE whatsapp_ativado = false LIMIT 10;
```

---

## Proximos Passos

### Curto Prazo (7 dias)
- [ ] Monitorar primeiros envios
- [ ] Ajustar mensagem conforme feedback
- [ ] Medir taxa de resposta

### Medio Prazo (30 dias)
- [ ] Implementar resposta automatica a opt-out
- [ ] Adicionar webhook para processar respostas
- [ ] Criar funil de reativacao (3 mensagens)

### Longo Prazo
- [ ] Migrar para N8N workflows visuais
- [ ] Dashboard de metricas e KPIs
- [ ] Integracao com CRM
- [ ] Segmentacao avancada de leads

---

## Scripts Disponiveis

| Script | Descricao | Uso |
|--------|-----------|-----|
| `setup_completo.bat` | Setup automatizado completo | `setup_completo.bat` |
| `processar_inativos.py` | Processa Excel e gera SQL | `python processar_inativos.py` |
| `processar_e_importar.bat` | Wrapper para processar | `processar_e_importar.bat` |
| `enviar_diario.py` | Envia mensagens WhatsApp | `python enviar_diario.py` |
| `executar_envio.bat` | Wrapper Windows para envio | `executar_envio.bat` |
| `executar_envio.ps1` | Wrapper PowerShell para envio | `.\executar_envio.ps1` |
| `criar_tarefa_agendada.bat` | Cria agendamento Windows | `criar_tarefa_agendada.bat` (Admin) |

---

## Recursos

### Documentacao
- **[GUIA_MVP_5MIN.md](GUIA_MVP_5MIN.md)** - Guia completo passo-a-passo
- **[QUICKSTART.md](QUICKSTART.md)** - Checklist executavel rapido
- **[SECURITY_LGPD.md](SECURITY_LGPD.md)** - Conformidade LGPD
- **[ASSUNCOES.md](ASSUNCOES.md)** - Premissas do projeto

### Links Externos
- **Supabase Docs**: https://supabase.com/docs
- **WAHA Docs**: https://waha.devlike.pro/
- **Railway Docs**: https://docs.railway.app/
- **N8N Docs**: https://docs.n8n.io/

### Suporte
- Issues: [GitHub Issues](https://github.com/seu-usuario/waha-n8n-stack/issues)
- Discussions: [GitHub Discussions](https://github.com/seu-usuario/waha-n8n-stack/discussions)

---

## Contribuir

Contribuicoes sao bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudancas (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## Licenca

Este projeto esta sob a licenca MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## Creditos

Desenvolvido com:
- **Supabase** - Banco de dados PostgreSQL serverless
- **WAHA** - WhatsApp HTTP API (devlikeapro)
- **Railway** - Plataforma de deploy
- **Python** - Scripts de automacao
- **N8N** - Workflow automation (opcional)

---

**MVP Pronto! Comece reativando seus alunos hoje mesmo!**

Para suporte e duvidas, consulte a documentacao ou abra uma issue no GitHub.
