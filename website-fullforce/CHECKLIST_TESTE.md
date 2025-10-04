# ✅ CHECKLIST DE TESTE - FULL FORCE ACADEMIA

**Arquivo**: `index-optimized.html`
**Data**: 2025-10-03
**Versão**: 2.0

---

## 🎯 INSTRUÇÕES DE USO

1. Marque ✅ cada item após testar
2. Anote problemas encontrados na seção "Notas"
3. Prioridade: 🔴 Crítico | 🟡 Importante | 🟢 Desejável
4. Testar em ordem (essencial → desejável)

---

## 📱 1. TESTES MOBILE (PRIORITY 1)

### 1.1 Dispositivos Físicos - Android

**Dispositivo**: ___________ (ex: Samsung Galaxy S21)
**Navegador**: Chrome Android

- [ ] 🔴 Página carrega em < 3 segundos
- [ ] 🔴 Header fixo visível ao scrollar
- [ ] 🔴 Logo + nome visíveis
- [ ] 🔴 Localização "Matupá-MT" legível
- [ ] 🔴 Botão WhatsApp header clicável (área > 44x44px)
- [ ] 🔴 Hero title legível sem zoom (min 32px)
- [ ] 🔴 Badges visíveis e alinhados (horário, equipamentos, etc)
- [ ] 🔴 CTA principal "AGENDAR AULA EXPERIMENTAL" grande e verde
- [ ] 🔴 CTA clicável e abre WhatsApp com mensagem pré-preenchida
- [ ] 🔴 Telefone clicável (abre discador)
- [ ] 🔴 Galeria de equipamentos (4 fotos) visível
- [ ] 🔴 Planos: 4 cards empilhados verticalmente
- [ ] 🔴 Preços legíveis (R$ 119, R$ 109, R$ 119, R$ 99)
- [ ] 🔴 Clube+ Full destacado (badge amarelo + background diferenciado)
- [ ] 🔴 Botão "Contratar" em cada plano abre WhatsApp
- [ ] 🔴 Depoimentos legíveis
- [ ] 🔴 Mapa Google visível e interativo
- [ ] 🔴 Contato: 3 cards (Telefone, Horário, Endereço)
- [ ] 🔴 WhatsApp fixo (canto inferior direito) visível e pulsante
- [ ] 🔴 WhatsApp fixo não sobrepõe conteúdo importante
- [ ] 🔴 Footer completo visível
- [ ] 🟡 Sem scroll horizontal (overflow-x)
- [ ] 🟡 Fontes legíveis (min 16px no body)
- [ ] 🟡 Imagens carregam progressivamente (lazy loading)
- [ ] 🟢 Animações suaves (sem lag)

**Notas Mobile Android**:
```
_________________________________________________
_________________________________________________
_________________________________________________
```

---

### 1.2 Dispositivos Físicos - iOS

**Dispositivo**: ___________ (ex: iPhone 13)
**Navegador**: Safari iOS

- [ ] 🔴 Página carrega em < 3 segundos
- [ ] 🔴 Header fixo não "pula" ao scrollar
- [ ] 🔴 Botão WhatsApp abre app WhatsApp (não browser)
- [ ] 🔴 Telefone abre FaceTime/Discador
- [ ] 🔴 Touch targets suficientemente grandes (44x44px mínimo)
- [ ] 🔴 Zoom controlado (não permite zoom excessivo)
- [ ] 🔴 Fontes do sistema renderizam corretamente (San Francisco)
- [ ] 🔴 Cores consistentes com Android
- [ ] 🟡 Smooth scroll funciona
- [ ] 🟡 Status bar não sobrepõe header
- [ ] 🟡 Viewport height correta (sem barra de URL cortando)

**Notas Mobile iOS**:
```
_________________________________________________
_________________________________________________
_________________________________________________
```

---

### 1.3 Testes de Resolução (Chrome DevTools)

**Resoluções a testar**:

#### 📱 320x568 (iPhone SE)
- [ ] 🔴 Todo conteúdo visível
- [ ] 🔴 Sem quebras de layout
- [ ] 🔴 CTAs acessíveis
- [ ] 🟡 Fontes legíveis

#### 📱 375x667 (iPhone 6/7/8)
- [ ] 🔴 Layout perfeito
- [ ] 🔴 Espaçamentos adequados

#### 📱 414x896 (iPhone 11 Pro Max)
- [ ] 🔴 Hero não fica com muito espaço vazio
- [ ] 🔴 Badges alinhados

#### 📱 360x640 (Android médio)
- [ ] 🔴 Layout Android consistente

**Notas Resoluções**:
```
_________________________________________________
_________________________________________________
```

---

## 💻 2. TESTES DESKTOP

### 2.1 Navegadores - Windows

#### Chrome (Windows)
- [ ] 🔴 Página carrega em < 2 segundos
- [ ] 🔴 Hero background visível (placeholder SVG)
- [ ] 🔴 Header sticky funciona
- [ ] 🔴 Hover em botões (efeito scale)
- [ ] 🔴 WhatsApp fixo animação pulse
- [ ] 🔴 Galeria equipamentos: 4 colunas
- [ ] 🔴 Planos: 4 colunas ou 2x2 (dependendo largura)
- [ ] 🔴 Mapa 400px altura
- [ ] 🟡 Fontes sistema (Segoe UI) renderizam bem
- [ ] 🟡 Console 100% limpo (F12 → Console)

**Notas Chrome Windows**:
```
_________________________________________________
```

#### Edge (Windows)
- [ ] 🔴 Renderização igual ao Chrome
- [ ] 🟡 Sem warnings de compatibilidade

**Notas Edge**:
```
_________________________________________________
```

#### Firefox (Windows)
- [ ] 🔴 Layout consistente
- [ ] 🔴 Fontes sistema corretas
- [ ] 🟡 Smooth scroll funciona
- [ ] 🟡 Focus outline visível (laranja)

**Notas Firefox**:
```
_________________________________________________
```

---

### 2.2 Navegadores - Mac

#### Safari (macOS)
- [ ] 🔴 Layout perfeito
- [ ] 🔴 Fontes sistema (SF Pro) bonitas
- [ ] 🔴 WhatsApp abre desktop app se instalado
- [ ] 🟡 Sem gaps no layout
- [ ] 🟡 Cores consistentes

**Notas Safari macOS**:
```
_________________________________________________
```

---

### 2.3 Resoluções Desktop

#### 🖥️ 1920x1080 (Full HD)
- [ ] 🔴 Container max-width 1200px centralizado
- [ ] 🔴 Hero ocupa ~70vh
- [ ] 🔴 Espaçamentos balanceados
- [ ] 🟡 Background hero cobre tela inteira

#### 🖥️ 1366x768 (Laptop comum)
- [ ] 🔴 Todo conteúdo above the fold visível
- [ ] 🔴 Sem scroll horizontal

#### 🖥️ 2560x1440 (2K)
- [ ] 🟡 Layout não fica "perdido" (container 1200px OK)
- [ ] 🟡 Fontes escaláveis (clamp funciona)

#### 🖥️ 3840x2160 (4K)
- [ ] 🟢 Fontes legíveis
- [ ] 🟢 Layout não desproporcional

**Notas Resoluções Desktop**:
```
_________________________________________________
```

---

## ⚡ 3. PERFORMANCE

### 3.1 Lighthouse (Chrome DevTools)

**Como executar**:
1. Abrir DevTools (F12)
2. Aba "Lighthouse"
3. Modo: Desktop + Mobile
4. Categorias: Performance, SEO, Accessibility, Best Practices
5. Executar 3x e tirar média

#### 📊 Resultados Desktop

| Métrica | Score | Status | Meta |
|---------|-------|--------|------|
| **Performance** | ____ / 100 | [ ] >90 | 95+ |
| **SEO** | ____ / 100 | [ ] >95 | 98+ |
| **Accessibility** | ____ / 100 | [ ] >95 | 95+ |
| **Best Practices** | ____ / 100 | [ ] >95 | 100 |

**Core Web Vitals**:
- [ ] 🔴 FCP (First Contentful Paint) < 1s (____ s)
- [ ] 🔴 LCP (Largest Contentful Paint) < 2.5s (____ s)
- [ ] 🔴 TBT (Total Blocking Time) < 200ms (____ ms)
- [ ] 🔴 CLS (Cumulative Layout Shift) < 0.1 (____ )
- [ ] 🔴 Speed Index < 2s (____ s)

#### 📊 Resultados Mobile

| Métrica | Score | Status | Meta |
|---------|-------|--------|------|
| **Performance** | ____ / 100 | [ ] >85 | 90+ |
| **SEO** | ____ / 100 | [ ] >95 | 98+ |
| **Accessibility** | ____ / 100 | [ ] >95 | 95+ |
| **Best Practices** | ____ / 100 | [ ] >95 | 100 |

**Core Web Vitals Mobile**:
- [ ] 🔴 FCP < 1.8s (____ s)
- [ ] 🔴 LCP < 4s (____ s)
- [ ] 🔴 TBT < 300ms (____ ms)
- [ ] 🔴 CLS < 0.1 (____ )

**Oportunidades de Melhoria** (se score < 90):
```
_________________________________________________
_________________________________________________
```

---

### 3.2 PageSpeed Insights (Google)

**URL**: https://pagespeed.web.dev/

- [ ] 🔴 Performance Mobile > 85
- [ ] 🔴 Performance Desktop > 95
- [ ] 🔴 Core Web Vitals: "Pass"
- [ ] 🟡 Field data (se disponível): "Good"

**Screenshot do resultado**:
```
(Anexar screenshot ou anotar scores)
Desktop: ____
Mobile: ____
```

---

### 3.3 WebPageTest

**URL**: https://www.webpagetest.org/

**Configuração**:
- Location: South America (São Paulo ou Rio)
- Browser: Chrome
- Connection: 4G

- [ ] 🔴 Load Time < 3s
- [ ] 🔴 First Byte < 500ms
- [ ] 🔴 Start Render < 1s
- [ ] 🟡 Speed Index < 2s
- [ ] 🟡 Fully Loaded < 4s

**Filmstrip**: Todo conteúdo visível em < 2s?
- [ ] 🔴 Sim
- [ ] ❌ Não (especificar problema): _______________

---

## 🔍 4. SEO

### 4.1 Validação de Tags

#### Meta Tags Essenciais
- [ ] 🔴 `<title>` presente e < 60 caracteres
- [ ] 🔴 `<meta name="description">` presente e < 160 caracteres
- [ ] 🔴 `<meta name="viewport">` correta
- [ ] 🔴 `<link rel="canonical">` presente
- [ ] 🟡 `<meta name="keywords">` presente (opcional mas desejável)
- [ ] 🟡 `<meta name="robots">` com "index, follow"

#### Open Graph (Facebook/WhatsApp)
- [ ] 🔴 `og:title` presente
- [ ] 🔴 `og:description` presente
- [ ] 🔴 `og:image` presente (URL absoluta)
- [ ] 🔴 `og:url` presente
- [ ] 🔴 `og:type` = "website"
- [ ] 🟡 `og:locale` = "pt_BR"

**Teste compartilhamento**:
- [ ] 🔴 Compartilhar no WhatsApp → card visual aparece
- [ ] 🟡 Compartilhar no Facebook → preview correto

#### Twitter Card
- [ ] 🟡 `twitter:card` = "summary_large_image"
- [ ] 🟡 `twitter:title` presente
- [ ] 🟡 `twitter:description` presente
- [ ] 🟡 `twitter:image` presente

#### Geo Tags (SEO Local)
- [ ] 🟡 `geo.region` = "BR-MT"
- [ ] 🟡 `geo.placename` = "Matupá"
- [ ] 🟡 `geo.position` com coordenadas corretas

---

### 4.2 Schema Markup (JSON-LD)

**Validação**: https://validator.schema.org/

- [ ] 🔴 JSON-LD presente no `<head>`
- [ ] 🔴 `@type`: "HealthClub" e "LocalBusiness"
- [ ] 🔴 `name`: "Full Force Academia"
- [ ] 🔴 `telephone`: formato E.164 (+55-66-99999-9999)
- [ ] 🔴 `address`: completo (rua, cidade, estado, CEP, país)
- [ ] 🔴 `geo`: latitude e longitude corretas
- [ ] 🔴 `openingHoursSpecification`: 04:30-21:00, todos os dias
- [ ] 🔴 `priceRange`: "R$ 99 - R$ 129"
- [ ] 🟡 `aggregateRating`: ratingValue 5, reviewCount > 0
- [ ] 🟡 `sameAs`: link Instagram
- [ ] 🟡 `image`: logo URL absoluta

**Resultado do validador**:
- [ ] 🔴 Zero erros
- [ ] 🟡 Zero warnings (se possível)

**Notas Schema**:
```
_________________________________________________
```

---

### 4.3 Ferramentas SEO

#### Google Search Console (após indexação)
- [ ] 🟡 Página indexada
- [ ] 🟡 Sem erros de cobertura
- [ ] 🟡 Core Web Vitals: "Good"
- [ ] 🟡 Mobile usability: "No issues"

#### Rich Results Test (Google)
**URL**: https://search.google.com/test/rich-results

- [ ] 🔴 LocalBusiness detectado
- [ ] 🔴 Horários visíveis no preview
- [ ] 🔴 Telefone visível
- [ ] 🟡 Avaliações visíveis (estrelas)

**Screenshot**:
```
(Anexar ou descrever o que aparece no preview do Google)
_________________________________________________
```

---

## ♿ 5. ACESSIBILIDADE (WCAG 2.1 AA)

### 5.1 Validação Automática

#### WAVE (WebAIM)
**URL**: https://wave.webaim.org/

- [ ] 🔴 Zero erros
- [ ] 🟡 < 3 alertas
- [ ] 🟡 Contraste: todos elementos passam

**Erros encontrados**:
```
_________________________________________________
```

#### axe DevTools (extensão Chrome)
**URL**: https://www.deque.com/axe/devtools/

- [ ] 🔴 Zero erros críticos
- [ ] 🟡 Zero erros sérios
- [ ] 🟡 < 5 avisos moderados

**Erros encontrados**:
```
_________________________________________________
```

---

### 5.2 Testes Manuais de Acessibilidade

#### Navegação por Teclado
- [ ] 🔴 Tab: foco visível em todos elementos interativos
- [ ] 🔴 Ordem de foco lógica (top → bottom, left → right)
- [ ] 🔴 Enter/Space: ativa botões e links
- [ ] 🔴 Escape: fecha modais (se houver)
- [ ] 🔴 Skip to content: Tab inicial foca link "Pular para conteúdo"
- [ ] 🟡 Shift+Tab: navegação reversa funciona

**Ordem de foco esperada**:
1. Skip to content
2. Logo (se link)
3. Header WhatsApp
4. Hero CTA primário
5. Hero CTA secundário
6. Telefone
7. ... (demais elementos na ordem visual)

#### Screen Reader (Windows: NVDA | Mac: VoiceOver)

**NVDA (Windows)**:
- [ ] 🔴 Landmarks anunciados (banner, main, navigation, contentinfo)
- [ ] 🔴 Headings: hierarquia correta (H1 → H2 → H3)
- [ ] 🔴 Links: texto descritivo ("Agendar aula grátis", não "Clique aqui")
- [ ] 🔴 Imagens: alt text presente e descritivo
- [ ] 🔴 Botões: ARIA labels quando necessário
- [ ] 🟡 Tabela de preços: headers corretos (se tiver)
- [ ] 🟡 Iframe mapa: título descritivo

**VoiceOver (Mac)**:
- [ ] 🔴 Navegação fluida
- [ ] 🔴 Todos elementos interativos acessíveis
- [ ] 🔴 Rotor: headings listados corretamente

**Notas Screen Reader**:
```
_________________________________________________
_________________________________________________
```

#### Contraste de Cores

**Ferramenta**: Colour Contrast Analyser ou DevTools

- [ ] 🔴 Texto principal (#333) em fundo branco: > 4.5:1
- [ ] 🔴 Texto links (#ff6b00) em fundo branco: > 4.5:1
- [ ] 🔴 Texto botões brancos em fundo verde (#25D366): > 4.5:1
- [ ] 🔴 Texto badges em fundo laranja: > 4.5:1
- [ ] 🟡 Todos elementos UI: > 3:1

**Resultados**:
```
Texto principal: ____:1
Links: ____:1
Botões: ____:1
```

#### Touch Targets (Mobile)

- [ ] 🔴 Todos botões/links: min 44x44px
- [ ] 🔴 Espaçamento entre elementos tocáveis: min 8px
- [ ] 🔴 WhatsApp fixo: 60x60px
- [ ] 🔴 Header CTA: > 44px altura

**Medições** (DevTools → Measure):
```
Header CTA: ____ x ____ px
Hero CTA: ____ x ____ px
WhatsApp fixo: ____ x ____ px
```

---

### 5.3 HTML Semântico

**Validação**: https://validator.w3.org/

- [ ] 🔴 HTML válido (zero erros)
- [ ] 🟡 Warnings aceitáveis (< 5)
- [ ] 🔴 Headings em ordem (H1 → H2 → H3, sem pulos)
- [ ] 🔴 Landmarks corretos (`<header>`, `<main>`, `<footer>`, `<nav>`)
- [ ] 🔴 ARIA labels em elementos ambíguos
- [ ] 🟡 Idioma declarado (`lang="pt-BR"`)

**Erros W3C**:
```
_________________________________________________
```

---

## 📲 6. FUNCIONALIDADE

### 6.1 Links e CTAs

#### WhatsApp Links
- [ ] 🔴 Header WhatsApp: abre com mensagem "Quero agendar minha aula GRÁTIS"
- [ ] 🔴 Hero CTA: abre com mensagem "Quero agendar minha aula EXPERIMENTAL"
- [ ] 🔴 Plano Trimestral: mensagem "Quero o plano TRIMESTRAL (R$119/mês)"
- [ ] 🔴 Plano Semestral: mensagem "Quero o plano SEMESTRAL (R$109/mês)"
- [ ] 🔴 Clube+ Full: mensagem "Quero o CLUBE+ FULL (11x R$129)"
- [ ] 🔴 Plano Anual: mensagem "Quero o plano ANUAL (R$99/mês)"
- [ ] 🔴 WhatsApp fixo: mensagem "Tenho interesse na Full Force Academia"
- [ ] 🔴 Contato WhatsApp: link funciona

**Teste**: Clicar em CADA link WhatsApp e verificar:
- [ ] 🔴 Abre WhatsApp (app mobile ou web.whatsapp.com desktop)
- [ ] 🔴 Número correto: +55 66 99999-9999
- [ ] 🔴 Mensagem pré-preenchida correta para cada CTA

#### Telefone Links
- [ ] 🔴 Hero telefone: `tel:+5566999999999` abre discador (mobile)
- [ ] 🔴 Contato telefone: link funciona

#### Links Externos
- [ ] 🔴 Instagram: abre em nova aba (`target="_blank"`)
- [ ] 🔴 Instagram: tem `rel="noopener"` (segurança)
- [ ] 🟡 Links externos têm ícone/indicador visual

#### Navegação Interna
- [ ] 🔴 Hero "Ver Planos": scroll suave até #planos
- [ ] 🔴 Scroll suave funciona (CSS `scroll-behavior: smooth`)

---

### 6.2 Google Maps

- [ ] 🔴 Iframe carrega corretamente
- [ ] 🔴 Mapa interativo (zoom, arrastar funcionam)
- [ ] 🔴 Coordenadas corretas: Matupá-MT
- [ ] 🔴 Lazy loading funciona (`loading="lazy"`)
- [ ] 🟡 Marcador no local correto (se visível)
- [ ] 🟡 Título do iframe descritivo (acessibilidade)

**Endereço no mapa**:
```
Verificar se o pin está no local correto:
Lat: -10.25
Lng: -54.9333
_________________________________________________
```

---

### 6.3 Imagens

#### Placeholders (antes de substituir)
- [ ] 🔴 Hero background: SVG placeholder visível
- [ ] 🔴 Equipamentos: 4 divs com classe `img-loading`
- [ ] 🔴 Animação skeleton funciona (gradiente)

#### Após substituir com WebP
- [ ] 🔴 Hero background: carrega rápido (< 1s)
- [ ] 🔴 Equipamentos: lazy loading funciona
- [ ] 🔴 Equipamentos: aparecem progressivamente ao scrollar
- [ ] 🔴 Alt text descritivo em todas imagens
- [ ] 🟡 Imagens responsivas (diferentes tamanhos para mobile/desktop)

**Tamanhos de arquivo** (meta: <100KB hero, <30KB cada equipamento):
```
hero-bg.webp: ____ KB
equipamento-1.webp: ____ KB
equipamento-2.webp: ____ KB
equipamento-3.webp: ____ KB
equipamento-4.webp: ____ KB
```

---

### 6.4 Elementos Visuais

#### Header Sticky
- [ ] 🔴 Scroll down: header permanece fixo no topo
- [ ] 🔴 Scroll up: header não "pula"
- [ ] 🔴 Z-index correto (não esconde WhatsApp fixo)

#### WhatsApp Fixo
- [ ] 🔴 Visível em todas resoluções
- [ ] 🔴 Animação pulse contínua
- [ ] 🔴 Hover: aumenta tamanho (scale 1.1)
- [ ] 🔴 Não sobrepõe conteúdo importante
- [ ] 🔴 Posição fixa mesmo ao scrollar

#### Hover Effects (Desktop)
- [ ] 🟡 Botões: scale + sombra ao hover
- [ ] 🟡 Cards de planos: translateY(-8px) ao hover
- [ ] 🟡 Links: mudança de cor
- [ ] 🟡 Equipamentos: imagem zoom (scale 1.05)

#### Responsive Grid
- [ ] 🔴 Mobile: 1 coluna
- [ ] 🔴 Tablet (768px+): 2-4 colunas (dependendo seção)
- [ ] 🔴 Desktop: 4 colunas (equipamentos, planos)

---

## 🔒 7. SEGURANÇA E PRIVACIDADE

### 7.1 HTTPS
- [ ] 🔴 Site servido via HTTPS (cadeado verde)
- [ ] 🔴 Mixed content: zero avisos (todas resources HTTPS)
- [ ] 🔴 Certificado válido (Let's Encrypt ou similar)

### 7.2 Headers de Segurança

**Ferramenta**: https://securityheaders.com/

- [ ] 🟡 `X-Frame-Options`: DENY ou SAMEORIGIN
- [ ] 🟡 `X-Content-Type-Options`: nosniff
- [ ] 🟡 `Referrer-Policy`: no-referrer-when-downgrade
- [ ] 🟢 `Content-Security-Policy`: (opcional mas desejável)

### 7.3 Links Externos

- [ ] 🔴 Todos links externos: `rel="noopener"`
- [ ] 🟡 Links externos: `rel="noreferrer"` (privacidade)
- [ ] 🔴 Instagram: `target="_blank"` funciona

---

## 🌐 8. COMPATIBILIDADE DE NAVEGADOR

### 8.1 Desktop

| Navegador | Versão | Layout | Funcionalidade | Performance | Status |
|-----------|--------|--------|----------------|-------------|--------|
| Chrome | 120+ | [ ] OK | [ ] OK | [ ] OK | [ ] ✅ |
| Edge | 120+ | [ ] OK | [ ] OK | [ ] OK | [ ] ✅ |
| Firefox | 115+ | [ ] OK | [ ] OK | [ ] OK | [ ] ✅ |
| Safari | 17+ | [ ] OK | [ ] OK | [ ] OK | [ ] ✅ |
| Opera | 100+ | [ ] OK | [ ] OK | [ ] OK | [ ] 🟡 |

### 8.2 Mobile

| Navegador | Sistema | Layout | Funcionalidade | Performance | Status |
|-----------|---------|--------|----------------|-------------|--------|
| Chrome | Android | [ ] OK | [ ] OK | [ ] OK | [ ] ✅ |
| Samsung Internet | Android | [ ] OK | [ ] OK | [ ] OK | [ ] ✅ |
| Safari | iOS | [ ] OK | [ ] OK | [ ] OK | [ ] ✅ |
| Firefox | Android | [ ] OK | [ ] OK | [ ] OK | [ ] 🟡 |

**Problemas encontrados**:
```
_________________________________________________
_________________________________________________
```

---

## 📊 9. ANALYTICS E RASTREAMENTO

### 9.1 Google Analytics 4 (após configurar)

- [ ] 🟡 Tag instalada corretamente
- [ ] 🟡 Pageview registrado
- [ ] 🟡 Eventos customizados:
  - [ ] Clique WhatsApp header
  - [ ] Clique WhatsApp hero
  - [ ] Clique WhatsApp fixo
  - [ ] Clique plano (cada um)
  - [ ] Clique telefone
  - [ ] Scroll 25%, 50%, 75%, 100%

### 9.2 Meta Pixel (Facebook Ads - opcional)

- [ ] 🟢 Pixel instalado
- [ ] 🟢 PageView evento disparado
- [ ] 🟢 Lead evento em cliques WhatsApp

---

## 🚀 10. CRITÉRIOS DE ACEITAÇÃO FINAL

### 10.1 Performance ✅

- [ ] 🔴 Lighthouse Desktop Performance > 90
- [ ] 🔴 Lighthouse Mobile Performance > 85
- [ ] 🔴 PageSpeed Insights: Core Web Vitals "Pass"
- [ ] 🔴 Tempo de carregamento mobile 4G < 3s

### 10.2 SEO ✅

- [ ] 🔴 Lighthouse SEO > 95
- [ ] 🔴 Schema markup válido (zero erros)
- [ ] 🔴 Meta tags completas (title, description, OG, Twitter)
- [ ] 🔴 Rich Results Test: LocalBusiness detectado

### 10.3 Acessibilidade ✅

- [ ] 🔴 Lighthouse Accessibility > 95
- [ ] 🔴 WAVE: zero erros
- [ ] 🔴 Navegação teclado 100% funcional
- [ ] 🔴 Screen reader: todos elementos anunciados corretamente

### 10.4 Funcionalidade ✅

- [ ] 🔴 Todos links WhatsApp funcionam (7 CTAs diferentes)
- [ ] 🔴 Telefones clicáveis (2 lugares)
- [ ] 🔴 Google Maps interativo
- [ ] 🔴 Instagram abre em nova aba
- [ ] 🔴 Scroll suave funciona

### 10.5 Mobile ✅

- [ ] 🔴 Design 100% responsivo (320px → 2560px)
- [ ] 🔴 Touch targets > 44x44px
- [ ] 🔴 Fontes legíveis (min 16px)
- [ ] 🔴 Sem scroll horizontal
- [ ] 🔴 Layout mobile-first perfeito

### 10.6 Conversão ✅

- [ ] 🔴 WhatsApp visível em 4+ lugares
- [ ] 🔴 CTAs claros e grandes
- [ ] 🔴 Mensagens pré-preenchidas por contexto
- [ ] 🔴 Clube+ Full destacado (badge + cor)
- [ ] 🔴 Planos escaneáveis (preços grandes)

---

## ✅ APROVAÇÃO FINAL

### Checklist de Entrega

- [ ] 🔴 TODOS testes críticos (🔴) passaram
- [ ] 🟡 > 80% testes importantes (🟡) passaram
- [ ] 🟢 > 50% testes desejáveis (🟢) passaram
- [ ] 🔴 Lighthouse Performance > 90 (desktop) e > 85 (mobile)
- [ ] 🔴 Lighthouse SEO > 95
- [ ] 🔴 Lighthouse Accessibility > 95
- [ ] 🔴 Zero erros de console
- [ ] 🔴 Zero erros W3C HTML Validator
- [ ] 🔴 Zero erros Schema Validator
- [ ] 🔴 Funciona sem JavaScript
- [ ] 🔴 Todos links WhatsApp testados e funcionando

### Pendências (se houver)

```
1. _________________________________________________
2. _________________________________________________
3. _________________________________________________
```

### Responsável pelo Teste

**Nome**: _________________________________
**Data**: _________________________________
**Assinatura**: ✅ Aprovado | ⚠️ Aprovado com ressalvas | ❌ Reprovado

**Observações finais**:
```
_________________________________________________
_________________________________________________
_________________________________________________
_________________________________________________
```

---

## 📝 NOTAS COMPLEMENTARES

### Ferramentas Utilizadas

- [ ] Chrome DevTools (Performance, Lighthouse, Accessibility)
- [ ] PageSpeed Insights (Google)
- [ ] Schema Markup Validator (Google)
- [ ] W3C HTML Validator
- [ ] WAVE (WebAIM)
- [ ] axe DevTools
- [ ] Colour Contrast Analyser
- [ ] BrowserStack ou similar (teste multi-device)
- [ ] NVDA (screen reader Windows)
- [ ] VoiceOver (screen reader macOS)

### Próximos Passos Após Aprovação

1. **Deploy em produção**
2. **Configurar Google Search Console**
3. **Submit sitemap**
4. **Configurar Google Analytics 4**
5. **Monitorar Core Web Vitals (28 dias)**
6. **Coletar feedback de usuários reais**
7. **A/B testing de CTAs (futuro)**

---

**Versão do Checklist**: 1.0
**Última atualização**: 2025-10-03
