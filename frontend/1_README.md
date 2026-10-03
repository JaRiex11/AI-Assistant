# ИИ-ассистент для энергетики — фронтенд

Прототип для хакатона. Формирует тематические дайджесты публикаций
из выбранных пользователем источников.

## Технологии
- Чистый HTML + CSS + Vanilla JS (без сборки, без npm)
- Все данные — mock в `api.js` (`USE_MOCK = true`)
- Состояние UI (тема, sidebar, черновик) — в `localStorage`

## Запуск
```bash
# Вариант 1: Python
python -m http.server 8000

# Вариант 2: VS Code Live Server
# Правой кнопкой на index.html → Open with Live Server