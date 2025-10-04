@echo off
REM Script para criar tarefa agendada no Windows Task Scheduler
REM Executa envio diario as 09:00

echo ========================================
echo  Criar Tarefa Agendada Windows
echo  Envio Diario WhatsApp - 09:00
echo ========================================
echo.

REM Verificar privilegios de administrador
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Este script precisa ser executado como Administrador
    echo Clique com botao direito e selecione "Executar como administrador"
    pause
    exit /b 1
)

cd /d "%~dp0"

echo Criando tarefa agendada...
echo.

REM Criar tarefa usando schtasks
schtasks /create /tn "WhatsApp_Envio_Diario_Inativos" /xml agendar_tarefa_windows.xml /f

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  Tarefa criada com sucesso!
    echo ========================================
    echo.
    echo Nome: WhatsApp_Envio_Diario_Inativos
    echo Horario: Diariamente as 09:00
    echo Script: executar_envio.bat
    echo.
    echo Para gerenciar a tarefa:
    echo - Abra: Agendador de Tarefas (taskschd.msc)
    echo - Procure: WhatsApp_Envio_Diario_Inativos
    echo.
    echo Para testar agora:
    echo - Execute: schtasks /run /tn "WhatsApp_Envio_Diario_Inativos"
    echo.
) else (
    echo.
    echo ========================================
    echo  ERRO ao criar tarefa
    echo  Codigo: %ERRORLEVEL%
    echo ========================================
    echo.
    echo Tente criar manualmente:
    echo 1. Abra: taskschd.msc
    echo 2. Acao: Criar Tarefa Basica
    echo 3. Trigger: Diario - 09:00
    echo 4. Acao: Iniciar programa
    echo 5. Programa: %~dp0executar_envio.bat
    echo.
)

pause
