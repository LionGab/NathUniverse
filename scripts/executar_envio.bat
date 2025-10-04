@echo off
REM Script para executar envio diario de WhatsApp
REM Uso: executar_envio.bat

echo ========================================
echo  Sistema de Reativacao via WhatsApp
echo  Envio Diario de Mensagens
echo ========================================
echo.

REM Carregar variaveis do .env
cd /d "%~dp0"
cd ..

if not exist "ops\.env" (
    echo ERRO: Arquivo ops\.env nao encontrado!
    echo Execute: copy ops\.env.sample ops\.env
    echo E preencha as variaveis de ambiente.
    pause
    exit /b 1
)

echo Carregando variaveis de ambiente...
for /f "usebackq tokens=1,* delims==" %%a in ("ops\.env") do (
    set "line=%%a"
    setlocal enabledelayedexpansion
    if not "!line:~0,1!"=="#" (
        endlocal
        set "%%a=%%b"
    ) else (
        endlocal
    )
)

REM Verificar variaveis obrigatorias
if "%SUPABASE_URL%"=="" (
    echo ERRO: SUPABASE_URL nao configurada no .env
    pause
    exit /b 1
)

if "%SUPABASE_SERVICE_ROLE%"=="" (
    echo ERRO: SUPABASE_SERVICE_ROLE nao configurada no .env
    pause
    exit /b 1
)

if "%WAHA_BASE_URL%"=="" (
    echo ERRO: WAHA_BASE_URL nao configurada no .env
    pause
    exit /b 1
)

echo Variaveis carregadas com sucesso!
echo.
echo SUPABASE_URL: %SUPABASE_URL%
echo WAHA_BASE_URL: %WAHA_BASE_URL%
echo LIMITE_DIARIO: %LIMITE_DIARIO%
echo.

REM Executar script Python
echo Executando envio...
echo.

cd scripts
python enviar_diario.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  Envio concluido com sucesso!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo  ERRO ao executar envio
    echo  Codigo de erro: %ERRORLEVEL%
    echo ========================================
)

echo.
pause
