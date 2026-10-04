#!/bin/bash

cd "$(dirname "$0")"

echo "========================================"
echo "  ИТ/ИБ Дайджест - запуск"
echo "========================================"
echo ""

# --- Проверка venv ---
if [ ! -f ".venv/bin/python" ]; then
    echo "[ОШИБКА] Виртуальное окружение .venv не найдено."
    echo "Создайте его командой:"
    echo "    python3 -m venv .venv"
    echo "    source .venv/bin/activate"
    echo "    pip install -r requirements.txt"
    echo ""
    read -p "Нажмите Enter для выхода..."
    exit 1
fi

# --- Запуск бэкенда в новом окне Terminal ---
echo "[1/3] Запускаю бэкенд на http://localhost:8000 ..."
osascript <<EOF
tell application "Terminal"
    activate
    do script "cd '$(pwd)' && .venv/bin/python -m uvicorn backend.main:app --reload --port 8000"
end tell
EOF

# --- Пауза ---
sleep 3

# --- Запуск фронтенда в новом окне Terminal ---
echo "[2/3] Запускаю фронтенд на http://localhost:5500 ..."
osascript <<EOF
tell application "Terminal"
    activate
    do script "cd '$(pwd)' && .venv/bin/python -m http.server 5500 --directory frontend"
end tell
EOF

# --- Пауза и открытие браузера ---
sleep 2
echo "[3/3] Открываю браузер..."
open http://localhost:5500

echo ""
echo "========================================"
echo "  Готово."
echo "  Фронт:   http://localhost:5500"
echo "  API:     http://localhost:8000"
echo "  Swagger: http://localhost:8000/docs"
echo "========================================"
echo ""
echo "Закрыть серверы: закройте открывшиеся окна Terminal."
read -p "Нажмите Enter для выхода..."