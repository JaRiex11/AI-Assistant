@echo off
chcp 65001 >nul
setlocal

cd /d "%~dp0"

echo ========================================
echo   ИТ/ИБ Дайджест - запуск
echo ========================================
echo.

REM --- Проверка venv ---
if not exist ".venv\Scripts\python.exe" (
    echo [ОШИБКА] Виртуальное окружение .venv не найдено.
    echo Создайте его командой:
    echo     python -m venv .venv
    echo     .venv\Scripts\Activate.ps1
    echo     pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM --- Запуск бэкенда в отдельном окне ---
echo [1/3] Запускаю бэкенд на http://localhost:8000 ...
start "Digest Backend" cmd /k ".venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000"

REM --- Небольшая пауза, чтобы бэкенд успел стартовать ---
timeout /t 3 /nobreak >nul

REM --- Запуск фронтенда в отдельном окне ---
echo [2/3] Запускаю фронтенд на http://localhost:5500 ...
start "Digest Frontend" cmd /k ".venv\Scripts\python.exe -m http.server 5500 --directory frontend"

REM --- Пауза и открытие браузера ---
timeout /t 2 /nobreak >nul
echo [3/3] Открываю браузер...
start "" http://localhost:5500

echo.
echo ========================================
echo   Готово.
echo   Фронт:   http://localhost:5500
echo   API:     http://localhost:8000
echo   Swagger: http://localhost:8000/docs
echo ========================================
echo.
echo Закрыть серверы: закройте окна "Digest Backend" и "Digest Frontend".
echo.
pause
endlocal