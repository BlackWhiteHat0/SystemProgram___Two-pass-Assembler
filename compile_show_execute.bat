@echo off
if "%~1"=="" (
    echo Usage: compile_show_execute.bat ^<filename.s^>
    exit /b 1
)

:: 處理檔案路徑，如果直接給檔名，嘗試加上 Demo\
set INPUT_FILE=%~1
if not exist "%INPUT_FILE%" (
    if exist "Demo\%INPUT_FILE%" (
        set INPUT_FILE=Demo\%INPUT_FILE%
    ) else (
        echo Error: File "%INPUT_FILE%" not found.
        exit /b 1
    )
)

echo ===== 1. Compiling =====
python compiler.py "%INPUT_FILE%"
if %ERRORLEVEL% NEQ 0 (
    echo Compilation failed.
    exit /b %ERRORLEVEL%
)

:: 將檔名的 .s 替換為 .obj0
set OBJ_FILE=%INPUT_FILE:.s=.obj0%

echo.
echo ===== 2. Hex Dump (%OBJ_FILE%) =====
xxd "%OBJ_FILE%"

echo.
echo ===== 3. Executing with vm0 =====
:: 如果 vm0 是當前目錄的執行檔，加上 .\vm0
.\vm0 "%OBJ_FILE%"
