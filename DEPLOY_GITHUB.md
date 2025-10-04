# 🚀 Deploy para GitHub - Instruções

## ✅ Tudo já está pronto!

O commit já foi criado com todos os arquivos. Agora só falta fazer push para o GitHub.

## 📋 Passo a passo:

### 1️⃣ Criar repositório no GitHub

1. Acesse: https://github.com/new
2. Preencha:
   - **Repository name**: `waha-whatsapp-reativacao`
   - **Description**: Sistema de reativação de alunos via WhatsApp automatizado
   - **Visibility**: ✅ Private (recomendado - contém credenciais no histórico)
   - **NÃO marque**: "Add a README file"
   - **NÃO marque**: "Add .gitignore"
3. Clique em **"Create repository"**

### 2️⃣ Copiar URL do repositório

Após criar, você verá uma página com comandos. Copie a URL que aparece (algo como):
```
https://github.com/SEU-USUARIO/waha-whatsapp-reativacao.git
```

### 3️⃣ Fazer push do código

Abra o terminal e execute:

```bash
cd C:\Users\User\waha-n8n-stack

# Adicionar o remote do GitHub
git remote add origin https://github.com/SEU-USUARIO/waha-whatsapp-reativacao.git

# Fazer push
git push -u origin master
```

Se pedir autenticação:
- Username: seu username do GitHub
- Password: use um **Personal Access Token** (não a senha)
  - Crie em: https://github.com/settings/tokens
  - Permissões: `repo` (full control)

---

## 🔄 Para usar em outro computador:

```bash
# Clonar o repositório
git clone https://github.com/SEU-USUARIO/waha-whatsapp-reativacao.git
cd waha-whatsapp-reativacao

# Instalar dependências
cd scripts
pip install -r requirements.txt

# Configurar .env
cp .env.sample .env
# Editar .env com suas credenciais

# Testar
python enviar_diario.py
```

---

## ⚠️ IMPORTANTE - Segurança

O arquivo `.env` está no `.gitignore` e **NÃO será commitado**.

Mas se você já commitou credenciais antes, recomendo:

1. **Rotacionar as credenciais**:
   - Gerar nova `WAHA_API_KEY` no Render
   - Criar novo `service_role` no Supabase (opcional)

2. **Limpar histórico** (se necessário):
```bash
# CUIDADO: Isso reescreve o histórico!
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch scripts/.env" \
  --prune-empty --tag-name-filter cat -- --all
```

---

## 📦 Arquivos incluídos no repositório:

✅ Scripts Python (processar_vencidos.py, enviar_diario.py)
✅ Schema Supabase (supabase/schema.sql)
✅ Documentação completa (SETUP_COMPLETO.md, README.md, etc)
✅ Configurações de exemplo (.env.sample)
✅ Planilha ModeloVencidas.xlsx
✅ Workflows de automação

❌ Arquivo .env (ignorado - você precisa criar manualmente)

---

## 🎯 Commit criado:

```
feat: Sistema completo de reativação WhatsApp

- Supabase: Schema completo com LGPD compliance
- WAHA: Deploy no Render.com configurado
- Scripts Python: processar_vencidos.py e enviar_diario.py
- 346 leads importados da planilha ModeloVencidas.xlsx
- Documentação completa de setup e uso
- Automação de envios diários (até 30 leads/dia)

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

**Status**: ✅ Pronto para push!
