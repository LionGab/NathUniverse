@echo off
REM Script para processar planilha e gerar SQL de importacao
REM Uso: processar_e_importar.bat [caminho_planilha]

echo ========================================
echo  Processador de Alunos Inativos
echo  Gera SQL para importar no Supabase
echo ========================================
echo.

cd /d "%~dp0"

REM Definir caminho padrao da planilha
set PLANILHA=C:\Users\User\Downloads\AlunosInativos.xlsx

REM Se passou argumento, usar ele
if not "%~1"=="" set PLANILHA=%~1

REM Verificar se planilha existe
if not exist "%PLANILHA%" (
    echo ERRO: Planilha nao encontrada: %PLANILHA%
    echo.
    echo Uso: processar_e_importar.bat [caminho_da_planilha]
    echo.
    pause
    exit /b 1
)

echo Planilha: %PLANILHA%
echo.

REM Executar processador
echo Processando planilha...
python processar_inativos.py "%PLANILHA%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  Processamento concluido!
    echo ========================================
    echo.
    echo Arquivo gerado: inserir_inativos.sql
    echo.
    echo PROXIMOS PASSOS:
    echo 1. Revise o arquivo: inserir_inativos.sql
    echo 2. Acesse Supabase SQL Editor
    echo 3. Cole e execute o SQL
    echo 4. Verifique: SELECT * FROM leads;
    echo.
) else (
    echo.
    echo ========================================
    echo  ERRO ao processar planilha
    echo  Codigo de erro: %ERRORLEVEL%
    echo ========================================
)

echo.
pause
