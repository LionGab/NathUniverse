# Full Force Academia - Site Responsivo com Automação WhatsApp

## 🎯 Objetivo
Site moderno, mobile-first e com conversão otimizada para a Full Force Academia, integrado com sistema de captura de leads automático via WhatsApp.

## 📋 Melhorias Implementadas

### ✅ Design & Performance
- **Responsivo mobile-first** - Funciona perfeitamente em todos dispositivos
- **Loading otimizado** - Lazy loading de imagens
- **Design moderno** - Gradientes, animações e UI profissional
- **SEO otimizado** - Meta tags e estrutura semântica

### ✅ Conversão & Vendas
- **CTAs destacados** - "Agendar Aula Grátis" em múltiplos pontos
- **Formulário de captura** - Coleta nome, telefone, email e objetivo
- **Planos visíveis** - Preços claros (Mensal R$149, Trimestral R$119, Anual R$99)
- **Botão WhatsApp flutuante** - Acesso direto em toda navegação

### ✅ Automação WhatsApp
- **Captura automática de leads** - Formulário → Supabase → WhatsApp
- **Notificação instantânea** - Academia recebe alerta via WAHA quando há novo lead
- **Mensagens personalizadas** - Nome e objetivo do lead incluídos
- **Integração com CRM** - Todos leads salvos no Supabase para follow-up

## 🚀 Como Usar

### 1. Configurar Credenciais
Edite `js/main.js` e atualize:

```javascript
const CONFIG = {
    supabaseUrl: 'https://oprrsfeljeyuebqarhjn.supabase.co',
    supabaseKey: 'sua_anon_key_aqui',
    whatsappNumber: '5566999999999', // Número da academia
    wahaUrl: 'https://sua-waha-url.up.railway.app'
};
```

### 2. Deploy do Site

**Opção A: GitHub Pages (Grátis)**
```bash
# Criar repositório no GitHub
git init
git add .
git commit -m "Site Full Force Academia"
git remote add origin https://github.com/seu-usuario/fullforce-site.git
git push -u origin main

# Ativar GitHub Pages em Settings → Pages → Source: main branch
# URL ficará: https://seu-usuario.github.io/fullforce-site
```

**Opção B: Netlify (Grátis)**
```bash
# Instalar Netlify CLI
npm install -g netlify-cli

# Deploy
cd website-fullforce
netlify deploy --prod
```

**Opção C: Vercel (Grátis)**
```bash
# Instalar Vercel CLI
npm install -g vercel

# Deploy
cd website-fullforce
vercel --prod
```

### 3. Configurar Supabase

Executar SQL para criar campo `objetivo` na tabela `leads`:

```sql
ALTER TABLE leads ADD COLUMN IF NOT EXISTS objetivo TEXT;
```

### 4. Testar Integração

1. Abrir site: `index.html` no navegador
2. Preencher formulário com dados de teste
3. Verificar se lead foi salvo no Supabase:
   ```sql
   SELECT * FROM leads ORDER BY created_at DESC LIMIT 5;
   ```
4. Confirmar que WhatsApp abriu com mensagem personalizada
5. Verificar notificação WAHA no número da academia

## 📊 Fluxo de Conversão

```
Usuário visita site
    ↓
Preenche formulário "Ganhe 1 Semana Grátis"
    ↓
Lead salvo no Supabase (com consentimento LGPD)
    ↓
WhatsApp abre automaticamente com mensagem personalizada
    ↓
Academia recebe notificação via WAHA
    ↓
Equipe entra em contato para agendar
```

## 🎨 Personalização

### Alterar Cores
Em `css/styles.css`:
```css
:root {
    --primary-color: #ff6b00;  /* Laranja Full Force */
    --secondary-color: #1a1a1a; /* Preto */
}
```

### Alterar Mensagens WhatsApp
Em `js/main.js`:
```javascript
function openWhatsApp() {
    const message = 'Sua mensagem personalizada aqui';
    // ...
}
```

### Alterar Planos e Preços
Em `index.html`, seção `<section class="planos">`:
- Editar valores em `<span class="valor">`
- Alterar benefícios em `<ul>`

### Adicionar Google Analytics
Em `index.html`, antes de `</head>`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Adicionar Meta Pixel (Facebook Ads)
Em `index.html`, antes de `</head>`:
```html
<!-- Meta Pixel -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', 'SEU_PIXEL_ID');
fbq('track', 'PageView');
</script>
```

## 📱 Recursos Mobile

- Menu hamburger automático em telas < 768px
- Botões otimizados para toque (min 44x44px)
- Imagens responsivas com srcset
- Formulário adaptável para teclado mobile
- Máscara automática para telefone: (66) 99999-9999

## 🔒 LGPD Compliance

✅ Formulário já configurado com:
- `consentido: true` - Usuário concorda ao preencher
- `origem_consentimento: 'formulario_site'` - Rastreabilidade
- `data_consentimento` - Timestamp automático

**Importante:** Adicionar link para Política de Privacidade no footer.

## 🚀 Próximas Melhorias

### Fase 2 (Semana 2)
- [ ] Integrar agendamento online (Calendly/Google Calendar)
- [ ] Adicionar galeria de fotos da academia
- [ ] Implementar chat online (Tawk.to ou similar)
- [ ] Criar blog com dicas de treino/nutrição

### Fase 3 (Semana 3)
- [ ] Painel administrativo para gerenciar leads
- [ ] Dashboard de métricas (conversão, origem de leads)
- [ ] Email marketing automático (Mailchimp/SendGrid)
- [ ] Sistema de cupons de desconto

### Fase 4 (Semana 4)
- [ ] App mobile (PWA)
- [ ] Sistema de check-in QR Code
- [ ] Integração com wearables (Apple Watch, Fitbit)
- [ ] Gamificação (ranking de alunos, desafios)

## 📈 Métricas para Acompanhar

**Google Analytics:**
- Taxa de conversão (formulário preenchido / visitantes)
- Origem de tráfego (orgânico, social, direto)
- Taxa de rejeição
- Tempo médio no site

**Supabase:**
```sql
-- Leads por dia
SELECT DATE(created_at) as data, COUNT(*) as total
FROM leads
WHERE origem_consentimento = 'formulario_site'
GROUP BY DATE(created_at)
ORDER BY data DESC;

-- Objetivos mais comuns
SELECT objetivo, COUNT(*) as total
FROM leads
GROUP BY objetivo
ORDER BY total DESC;

-- Taxa de conversão WhatsApp
SELECT
  COUNT(*) FILTER (WHERE whatsapp_ativado = true) as contatados,
  COUNT(*) as total,
  ROUND(COUNT(*) FILTER (WHERE whatsapp_ativado = true) * 100.0 / COUNT(*), 2) as taxa_conversao
FROM leads
WHERE origem_consentimento = 'formulario_site';
```

## 🐛 Troubleshooting

**Formulário não envia:**
- Verificar console do navegador (F12)
- Confirmar `supabaseKey` está correta
- Checar se tabela `leads` existe no Supabase
- Verificar CORS configurado no Supabase

**WhatsApp não abre:**
- Verificar formato do número: `5566999999999` (sem +, sem espaços)
- Confirmar número está ativo no WhatsApp
- Testar link manual: `https://wa.me/5566999999999`

**WAHA não notifica:**
- Verificar `wahaUrl` está correto
- Confirmar sessão 'default' está conectada
- Checar logs do Railway: `railway logs`
- Testar endpoint: `curl https://sua-waha-url.up.railway.app/health`

## 📞 Suporte

Para dúvidas ou melhorias:
1. Abrir issue no GitHub
2. WhatsApp: (66) 99999-9999
3. Email: contato@fullforceacademia.com.br

---

**Desenvolvido com ❤️ para Full Force Academia - Matupá/MT**
