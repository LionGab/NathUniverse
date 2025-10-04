# Script Python - Alternativa ao n8n

## Vantagens
- ✅ Mais simples que n8n
- ✅ Fácil de debugar
- ✅ Pode rodar localmente ou no GitHub Actions (grátis)
- ✅ Menos dependências

## Setup Local

### 1. Instalar dependências
```bash
cd scripts
pip install -r requirements.txt
```

### 2. Configurar .env
```bash
cp ../ops/.env.sample .env
# Edite .env com suas credenciais
```

### 3. Executar manualmente
```bash
python enviar_diario.py
```

## Setup GitHub Actions (Automação Grátis)

### 1. Criar workflow
```bash
mkdir -p ../.github/workflows
```

### 2. Criar arquivo `.github/workflows/whatsapp_diario.yml`:
```yaml
name: Envio WhatsApp Diário

on:
  schedule:
    - cron: '0 12 * * *' # 09:00 BRT (UTC-3)
  workflow_dispatch: # Permite execução manual

jobs:
  enviar:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Instalar dependências
        run: |
          cd scripts
          pip install -r requirements.txt

      - name: Executar envio
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_SERVICE_ROLE: ${{ secrets.SUPABASE_SERVICE_ROLE }}
          WAHA_BASE_URL: ${{ secrets.WAHA_BASE_URL }}
          WAHA_SEND_TEXT_PATH: /api/sendText
          WAHA_SESSION: default
          LIMITE_DIARIO: 30
        run: |
          cd scripts
          python enviar_diario.py
```

### 3. Adicionar secrets no GitHub
Settings → Secrets and variables → Actions → New repository secret:

- `SUPABASE_URL`: https://eiqzckhcmmfyddruaxdj.supabase.co
- `SUPABASE_SERVICE_ROLE`: (service_role key)
- `WAHA_BASE_URL`: https://waha-production-XXXX.up.railway.app

### 4. Testar
- Actions → Envio WhatsApp Diário → Run workflow

## Custo
**R$ 0/mês** (GitHub Actions: 2000 min/mês grátis)

## Personalizar Mensagem

Edite `enviar_diario.py` linha 18:
```python
MENSAGEM_TEMPLATE = """Sua mensagem aqui com {nome} dinâmico"""
```

## Troubleshooting

### Erro: "No module named 'supabase'"
```bash
pip install -r requirements.txt
```

### Erro: "SUPABASE_URL not set"
Configure `.env` ou variáveis de ambiente

### Testar conexão Supabase
```python
python -c "from supabase import create_client; print('OK')"
```
