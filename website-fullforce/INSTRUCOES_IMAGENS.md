# 📸 INSTRUÇÕES PARA OTIMIZAÇÃO DE IMAGENS

**Full Force Academia - Website Otimizado**

---

## 🎯 OBJETIVO

Substituir placeholders SVG/animados por imagens reais otimizadas em **WebP**, garantindo:
- ✅ Carregamento rápido (< 1s por imagem)
- ✅ Qualidade visual profissional
- ✅ Lighthouse Performance > 90
- ✅ Tamanho total de imagens < 500KB

---

## 📋 IMAGENS NECESSÁRIAS

### 1. Hero Background
- **Arquivo**: `images/hero-bg.webp`
- **Dimensões**: 1920 x 600 px
- **Peso máximo**: 100 KB
- **Qualidade**: 75-80
- **Conteúdo**: Foto da academia (área de musculação ou fachada)
- **Filtro**: Escurecer 30-40% (hero tem overlay escuro)

### 2. Equipamentos (4 fotos)

#### Equipamento 1: Esteiras
- **Arquivo**: `images/equipamento-esteiras.webp`
- **Dimensões**: 400 x 300 px (aspect ratio 4:3)
- **Peso máximo**: 30 KB
- **Qualidade**: 80
- **Conteúdo**: Esteiras profissionais, vista frontal

#### Equipamento 2: Musculação
- **Arquivo**: `images/equipamento-musculacao.webp`
- **Dimensões**: 400 x 300 px
- **Peso máximo**: 30 KB
- **Qualidade**: 80
- **Conteúdo**: Área de pesos livres ou máquinas

#### Equipamento 3: Funcional
- **Arquivo**: `images/equipamento-funcional.webp`
- **Dimensões**: 400 x 300 px
- **Peso máximo**: 30 KB
- **Qualidade**: 80
- **Conteúdo**: Área de treino funcional (TRX, kettlebells, etc)

#### Equipamento 4: CrossFit/HIIT
- **Arquivo**: `images/equipamento-crossfit.webp`
- **Dimensões**: 400 x 300 px
- **Peso máximo**: 30 KB
- **Qualidade**: 80
- **Conteúdo**: Área de CrossFit ou HIIT (box jump, cordas, etc)

### 3. Logo (opcional - pode usar CSS)
- **Arquivo**: `images/logo.png` ou `logo.svg`
- **Dimensões**: 100 x 100 px (se PNG)
- **Peso máximo**: 10 KB
- **Formato**: SVG preferível, ou PNG com fundo transparente

---

## 🛠️ FERRAMENTAS DE CONVERSÃO

### Opção 1: Online (Mais Fácil)

**Squoosh (Google)**
- URL: https://squoosh.app/
- Passos:
  1. Arrastar imagem JPG/PNG
  2. Escolher formato: **WebP**
  3. Ajustar qualidade: **75-80**
  4. Redimensionar: largura **1920** (hero) ou **400** (equipamentos)
  5. Baixar

**CloudConvert**
- URL: https://cloudconvert.com/jpg-to-webp
- Upload múltiplo: converter várias imagens de uma vez

### Opção 2: Linha de Comando (Mais Profissional)

**Instalar cwebp (Windows/Mac/Linux)**

Windows (via Chocolatey):
```bash
choco install webp
```

Mac (via Homebrew):
```bash
brew install webp
```

Linux (Ubuntu/Debian):
```bash
sudo apt install webp
```

**Converter imagens**:

```bash
# Hero background (qualidade 75, resize automático)
cwebp -q 75 -resize 1920 0 hero-original.jpg -o hero-bg.webp

# Equipamentos (qualidade 80, resize para 400px largura)
cwebp -q 80 -resize 400 0 esteiras.jpg -o equipamento-esteiras.webp
cwebp -q 80 -resize 400 0 musculacao.jpg -o equipamento-musculacao.webp
cwebp -q 80 -resize 400 0 funcional.jpg -o equipamento-funcional.webp
cwebp -q 80 -resize 400 0 crossfit.jpg -o equipamento-crossfit.webp
```

**Script batch para converter tudo de uma vez** (Windows):
```batch
@echo off
echo Convertendo imagens para WebP...

cwebp -q 75 -resize 1920 0 hero-original.jpg -o hero-bg.webp
cwebp -q 80 -resize 400 0 esteiras.jpg -o equipamento-esteiras.webp
cwebp -q 80 -resize 400 0 musculacao.jpg -o equipamento-musculacao.webp
cwebp -q 80 -resize 400 0 funcional.jpg -o equipamento-funcional.webp
cwebp -q 80 -resize 400 0 crossfit.jpg -o equipamento-crossfit.webp

echo Conversao concluida!
pause
```

Salvar como `converter-imagens.bat` e executar.

### Opção 3: Photoshop / GIMP

**Photoshop (2023+)**:
1. File → Export → Save for Web (Legacy)
2. Formato: WebP
3. Qualidade: 75-80
4. Image Size: 1920x600 ou 400x300
5. Save

**GIMP (gratuito)**:
1. Instalar plugin WebP: https://github.com/webmproject/WebP
2. File → Export As
3. Escolher `.webp`
4. Quality: 75-80
5. Export

---

## 📁 ESTRUTURA DE PASTAS

```
website-fullforce/
├── index-optimized.html
├── images/
│   ├── hero-bg.webp (1920x600, ~100KB)
│   ├── equipamento-esteiras.webp (400x300, ~30KB)
│   ├── equipamento-musculacao.webp (400x300, ~30KB)
│   ├── equipamento-funcional.webp (400x300, ~30KB)
│   ├── equipamento-crossfit.webp (400x300, ~30KB)
│   └── logo.png ou logo.svg (~10KB)
└── ...
```

---

## 🔄 SUBSTITUIR NO HTML

### 1. Hero Background

**Encontrar** (linha ~106):
```html
<section class="hero" aria-labelledby="hero-title">
```

**Alterar CSS inline** (no `<style>` do `<head>`):
```css
.hero{
    background:linear-gradient(rgba(26,26,26,0.7),rgba(26,26,26,0.7)),
               url('images/hero-bg.webp') center/cover no-repeat;
    /* Resto do CSS... */
}
```

**OU criar versão responsiva** (mobile = imagem menor):
```css
.hero{
    background:linear-gradient(rgba(26,26,26,0.7),rgba(26,26,26,0.7)),
               url('images/hero-bg-mobile.webp') center/cover no-repeat;
}

@media(min-width:768px){
    .hero{
        background-image:linear-gradient(rgba(26,26,26,0.7),rgba(26,26,26,0.7)),
                         url('images/hero-bg.webp');
    }
}
```

### 2. Galeria de Equipamentos

**Encontrar** (linhas ~263-285):
```html
<div class="equipment-item img-loading">
    <div class="equipment-label">Esteiras Profissionais</div>
</div>
```

**Substituir por**:
```html
<div class="equipment-item">
    <img src="images/equipamento-esteiras.webp"
         alt="Esteiras profissionais 2024 - Full Force Academia"
         loading="eager"
         width="400"
         height="300">
    <div class="equipment-label">Esteiras Profissionais</div>
</div>

<div class="equipment-item">
    <img src="images/equipamento-musculacao.webp"
         alt="Área de musculação completa com equipamentos novos 2024"
         loading="eager"
         width="400"
         height="300">
    <div class="equipment-label">Musculação Completa</div>
</div>

<div class="equipment-item">
    <img src="images/equipamento-funcional.webp"
         alt="Área de treino funcional com TRX e kettlebells"
         loading="eager"
         width="400"
         height="300">
    <div class="equipment-label">Área Funcional</div>
</div>

<div class="equipment-item">
    <img src="images/equipamento-crossfit.webp"
         alt="Espaço CrossFit e HIIT com equipamentos profissionais"
         loading="eager"
         width="400"
         height="300">
    <div class="equipment-label">CrossFit / HIIT</div>
</div>
```

**Importante**:
- `loading="eager"` → carrega imediatamente (está above the fold)
- `width` e `height` → previne layout shift (CLS)
- `alt` → SEO e acessibilidade (descrição detalhada)

### 3. Logo (opcional)

**Encontrar** (linha ~213):
```html
<div class="logo-img" style="background:var(--primary);...">FF</div>
```

**Substituir por**:
```html
<img src="images/logo.png"
     alt="Logo Full Force Academia"
     class="logo-img"
     width="50"
     height="50">
```

**OU usar SVG inline** (melhor performance):
```html
<svg class="logo-img" width="50" height="50" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="48" fill="#ff6b00"/>
    <text x="50%" y="50%" text-anchor="middle" dy=".35em"
          font-size="36" font-weight="900" fill="white">FF</text>
</svg>
```

---

## ✅ CHECKLIST DE VERIFICAÇÃO

Após substituir imagens:

### Qualidade Visual
- [ ] Hero background: nítida, sem artefatos
- [ ] Equipamentos: fotos profissionais (boa iluminação)
- [ ] Cores vibrantes (não desbotadas pela compressão)
- [ ] Textos/labels legíveis sobre as imagens

### Performance
- [ ] Hero carrega em < 1s (3G)
- [ ] Equipamentos carregam progressivamente
- [ ] Tamanho total de imagens < 500 KB
- [ ] Lighthouse Performance > 90

### SEO & Acessibilidade
- [ ] Todas imagens têm `alt` descritivo
- [ ] `width` e `height` declarados (previne CLS)
- [ ] `loading="eager"` para above-fold, `loading="lazy"` para below-fold

### Compatibilidade
- [ ] WebP funciona em Chrome, Edge, Firefox, Safari 14+
- [ ] Fallback para navegadores antigos (opcional):

```html
<picture>
    <source srcset="equipamento-esteiras.webp" type="image/webp">
    <source srcset="equipamento-esteiras.jpg" type="image/jpeg">
    <img src="equipamento-esteiras.jpg" alt="...">
</picture>
```

---

## 🎨 DICAS DE FOTOGRAFIA

### Para o Hero Background
- **Horário**: Manhã (luz natural) ou fim de tarde
- **Ângulo**: Panorâmica da academia (piso até teto)
- **Foco**: Equipamentos em primeiro plano
- **Pessoas**: Opcional (adiciona dinamismo, mas exige autorização LGPD)
- **Pós-produção**: Aumentar contraste, saturação +10-20%

### Para Equipamentos
- **Iluminação**: Uniforme (evitar sombras duras)
- **Ângulo**: Frontal ou 3/4 (mostre profundidade)
- **Composição**: Equipamento centralizado, fundo limpo
- **Detalhes**: Mostre marca/modelo (ex: "Technogym 2024")
- **Limpeza**: Equipamentos limpos e organizados

### Equipamentos Mínimos
- Smartphone moderno (iPhone 12+, Galaxy S21+)
- OU câmera DSLR/mirrorless
- Tripeé (opcional, mas ajuda)
- Iluminação extra se academia for escura

---

## 🚀 OTIMIZAÇÕES AVANÇADAS (OPCIONAL)

### 1. Imagens Responsivas (srcset)

```html
<img src="images/equipamento-esteiras-400.webp"
     srcset="images/equipamento-esteiras-400.webp 400w,
             images/equipamento-esteiras-800.webp 800w"
     sizes="(max-width: 768px) 100vw, 400px"
     alt="Esteiras profissionais"
     loading="eager"
     width="400"
     height="300">
```

**Criar versões**:
```bash
cwebp -q 80 -resize 400 0 esteiras.jpg -o equipamento-esteiras-400.webp
cwebp -q 80 -resize 800 0 esteiras.jpg -o equipamento-esteiras-800.webp
```

### 2. Lazy Loading com Blur-up (LQIP)

**Criar placeholder baixa qualidade** (< 1KB):
```bash
cwebp -q 20 -resize 20 0 esteiras.jpg -o equipamento-esteiras-placeholder.webp
```

**HTML**:
```html
<img src="equipamento-esteiras-placeholder.webp"
     data-src="equipamento-esteiras.webp"
     class="lazy-blur"
     alt="...">

<script>
// Código para trocar src quando imagem entra no viewport
</script>
```

### 3. CDN para Imagens (Produção)

**Cloudflare Images**:
- Otimização automática
- Redimensionamento on-the-fly
- Cache global
- Custo: ~$5/mês para 100k imagens

**Cloudinary (gratuito até 25GB)**:
```html
<img src="https://res.cloudinary.com/fullforce/image/upload/w_400,q_auto,f_auto/equipamento-esteiras.jpg">
```

Otimização automática (WebP, AVIF, tamanho) baseado no browser.

---

## 📞 SUPORTE

### Problemas Comuns

**Imagem muito grande (> 100KB)**:
- Reduzir qualidade: `-q 70` ou `-q 65`
- Reduzir dimensões: `-resize 1600 0` (hero)
- Recortar áreas desnecessárias (GIMP/Photoshop)

**Imagem pixelada/borrada**:
- Aumentar qualidade: `-q 85` ou `-q 90`
- Usar imagem original de maior resolução
- Evitar upscale (sempre fazer downscale)

**WebP não funciona em navegador antigo**:
- Safari < 14 (iOS < 14): usar fallback JPG
- Implementar `<picture>` com múltiplos formatos

**Conversão falha**:
- Verificar se `cwebp` está instalado: `cwebp -version`
- Verificar permissões de arquivo
- Tentar ferramenta online (Squoosh)

---

## ✅ VALIDAÇÃO FINAL

**Após substituir TODAS as imagens**:

1. **Testar carregamento**:
   - Abrir DevTools → Network → Disable cache
   - Recarregar página
   - Verificar tamanho de cada imagem
   - Tempo de carregamento total < 3s (3G)

2. **Lighthouse**:
   - Executar Lighthouse (Performance)
   - Meta: > 90 desktop, > 85 mobile
   - Verificar sugestões de otimização

3. **Visual**:
   - Comparar com mockup/site original
   - Cores vivas, contraste adequado
   - Sem blur ou pixelização

4. **Acessibilidade**:
   - Todas imagens têm `alt`
   - Alt text descritivo (não "imagem1.jpg")
   - Screen reader anuncia corretamente

---

**Última atualização**: 2025-10-03
**Versão**: 1.0
