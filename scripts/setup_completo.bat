@echo off
REM Setup completo do sistema - Instala tudo e configura
REM Uso: setup_completo.bat

echo ========================================
echo  SETUP COMPLETO - Sistema WhatsApp
echo  Instalacao e Configuracao
echo ========================================
echo.

cd /d "%~dp0"

REM 1. Verificar Python
echo [1/5] Verificando Python...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.8+ de: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo OK!
echo.

REM 2. Instalar dependencias
echo [2/5] Instalando dependencias Python...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Falha ao instalar dependencias
    pause
    exit /b 1
)
echo OK!
echo.

REM 3. Criar .env se nao existir
echo [3/5] Configurando arquivo .env...
cd ..
if not exist "ops\.env" (
    copy ops\.env.sample ops\.env
    echo Arquivo .env criado! IMPORTANTE: Edite ops\.env e preencha:
    echo - SUPABASE_URL
    echo - SUPABASE_SERVICE_ROLE
    echo - WAHA_BASE_URL
    echo.
    notepad ops\.env
) else (
    echo Arquivo .env ja existe
)
echo OK!
echo.

REM 4. Verificar planilha
echo [4/5] Verificando planilha de inativos...
set PLANILHA=C:\Users\User\Downloads\AlunosInativos.xlsx
if exist "%PLANILHA%" (
    echo Planilha encontrada: %PLANILHA%
    echo OK!
) else (
    echo AVISO: Planilha nao encontrada em: %PLANILHA%
    echo Certifique-se de ter o arquivo AlunosInativos.xlsx em Downloads
)
echo.

REM 5. Instrucoes finais
echo [5/5] Setup basico concluido!
echo.
echo ========================================
echo  PROXIMOS PASSOS MANUAIS:
echo ========================================
echo.
echo 1. SUPABASE:
echo    - Acesse: https://supabase.com/dashboard/project/eiqzckhcmmfyddruaxdj/sql
echo    - Execute o schema: supabase\schema.sql
echo.
echo 2. RAILWAY (WAHA):
echo    - Acesse: https://railway.app/
echo    - Deploy da imagem: devlikeapro/waha:latest
echo    - Escaneie QR Code para conectar WhatsApp
echo.
echo 3. CONFIGURAR .env:
echo    - Edite: ops\.env
echo    - Preencha SUPABASE_URL, SUPABASE_SERVICE_ROLE, WAHA_BASE_URL
echo.
echo 4. PROCESSAR PLANILHA:
echo    - Execute: scripts\processar_e_importar.bat
echo.
echo 5. TESTAR ENVIO:
echo    - Execute: scripts\executar_envio.bat
echo.
echo ========================================
echo  Consulte QUICKSTART.md para detalhes
echo ========================================
echo.

pause
