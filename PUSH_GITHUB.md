# 🚀 Push para GitHub - Dois Repositórios

## 📋 Remotes Configurados

O projeto está configurado para fazer push em **2 repositórios**:

1. **PrimeLionTech** (origin):
   - URL: git@github.com:PrimeLionTech/FullForceGym.git
   - Remote: `origin`

2. **LionGab** (backup):
   - URL: https://github.com/LionGab/FullForceGym.git
   - Remote: `liongab`

---

## ✅ Para fazer push nos dois repositórios:

### Opção 1: Push individual

```bash
cd C:\Users\User\waha-n8n-stack

# Push para PrimeLionTech
git push -u origin main

# Push para LionGab
git push -u liongab main
```

### Opção 2: Push em ambos de uma vez

```bash
cd C:\Users\User\waha-n8n-stack

# Adicionar push URL adicional ao origin
git remote set-url --add --push origin https://github.com/LionGab/FullForceGym.git

# Agora um único push vai para os dois
git push origin main
```

---

## 🔑 Autenticação

### Para PrimeLionTech (SSH):
- Requer SSH key configurada
- Se não tiver: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### Para LionGab (HTTPS):
- **Username**: LionGab
- **Password**: Use Personal Access Token
  - Criar em: https://github.com/settings/tokens
  - Permissões: `repo` (full control)

---

## 🆘 Se der erro de autenticação:

### Converter origin para HTTPS:
```bash
cd C:\Users\User\waha-n8n-stack
git remote set-url origin https://github.com/PrimeLionTech/FullForceGym.git
git push -u origin main
```

---

## ✅ Verificar remotes configurados:

```bash
git remote -v
```

**Deve mostrar:**
```
liongab   https://github.com/LionGab/FullForceGym.git (fetch)
liongab   https://github.com/LionGab/FullForceGym.git (push)
origin    git@github.com:PrimeLionTech/FullForceGym.git (fetch)
origin    git@github.com:PrimeLionTech/FullForceGym.git (push)
```

---

## 📊 Status Atual:

- ✅ Git local: 4 commits prontos
- ✅ Remote origin: PrimeLionTech configurado
- ✅ Remote liongab: LionGab configurado
- ⏳ Push pendente (problema de rede local)

**Assim que tiver conexão, execute:**
```bash
git push -u origin main
git push -u liongab main
```

---

**Última atualização**: 2025-10-03 22:55
