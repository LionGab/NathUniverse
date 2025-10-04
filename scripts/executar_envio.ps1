# Script PowerShell para executar envio diario de WhatsApp
# Uso: .\executar_envio.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Sistema de Reativacao via WhatsApp" -ForegroundColor Cyan
Write-Host " Envio Diario de Mensagens" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Definir diretorio base
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$baseDir = Split-Path -Parent $scriptDir
$envFile = Join-Path $baseDir "ops\.env"

# Verificar se .env existe
if (-not (Test-Path $envFile)) {
    Write-Host "ERRO: Arquivo ops\.env nao encontrado!" -ForegroundColor Red
    Write-Host "Execute: copy ops\.env.sample ops\.env" -ForegroundColor Yellow
    Write-Host "E preencha as variaveis de ambiente." -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host "Carregando variaveis de ambiente..." -ForegroundColor Green

# Carregar variaveis do .env
Get-Content $envFile | ForEach-Object {
    if ($_ -match '^([^#][^=]+)=(.*)$') {
        $name = $matches[1].Trim()
        $value = $matches[2].Trim()
        Set-Item -Path "env:$name" -Value $value
    }
}

# Verificar variaveis obrigatorias
if (-not $env:SUPABASE_URL) {
    Write-Host "ERRO: SUPABASE_URL nao configurada no .env" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

if (-not $env:SUPABASE_SERVICE_ROLE) {
    Write-Host "ERRO: SUPABASE_SERVICE_ROLE nao configurada no .env" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

if (-not $env:WAHA_BASE_URL) {
    Write-Host "ERRO: WAHA_BASE_URL nao configurada no .env" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host "Variaveis carregadas com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "SUPABASE_URL: $env:SUPABASE_URL" -ForegroundColor Gray
Write-Host "WAHA_BASE_URL: $env:WAHA_BASE_URL" -ForegroundColor Gray
Write-Host "LIMITE_DIARIO: $env:LIMITE_DIARIO" -ForegroundColor Gray
Write-Host ""

# Executar script Python
Write-Host "Executando envio..." -ForegroundColor Cyan
Write-Host ""

Set-Location (Join-Path $baseDir "scripts")
python enviar_diario.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host " Envio concluido com sucesso!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host " ERRO ao executar envio" -ForegroundColor Red
    Write-Host " Codigo de erro: $LASTEXITCODE" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
}

Write-Host ""
Read-Host "Pressione Enter para sair"
