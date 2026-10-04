## Установка

### 1. Клонировать проект

```bash
git clone <url-репозитория>
cd assistent-dlya-sozdaniya-it-ib-daydzhestov
```

### 2. Создать виртуальное окружение

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Установить и запустить Ollama

Скачайте и установите Ollama с [ollama.com](https://ollama.com).
Запустите сервер локально:

```bash
ollama serve
```

Скачайте модель для эмбеддингов:

```bash
ollama pull bge-m3
```

### 5. Настроить API-ключ Ollama Cloud

Создайте файл `.env` в корне проекта:

```
OLLAMA_API_KEY=ваш_ключ_из_ollama.com
```

Либо задайте переменную окружения вручную.

**Windows (PowerShell):**
```powershell
$env:OLLAMA_API_KEY="ваш_ключ"
```

**macOS / Linux:**
```bash
export OLLAMA_API_KEY="ваш_ключ"
```

## Требования к окружению

- **Python 3.11 или новее**
- **Ollama** — установленная и запущенная ([ollama.com](https://ollama.com))
- **API-ключ Ollama Cloud** ([ollama.com/settings](https://ollama.com/settings))
- **Скачанная локальная модель** `bge-m3` для эмбеддингов

## Запуск

### Быстрый старт

**Windows:** двойной клик по `start.bat`.

**macOS:** первый раз — сделать исполняемым и запустить:
```bash
chmod +x start.command
./start.command
```
Затем можно запускать двойным кликом из Finder.

Оба скрипта:
1. Запускают бэкенд на `http://localhost:8000`.
2. Запускают фронтенд на `http://localhost:5500`.
3. Открывают браузер с фронтом.

### Ручной запуск

Нужно два терминала.

**Терминал 1 — бэкенд:**
```bash
# Windows
.venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000

# macOS / Linux
.venv/bin/python -m uvicorn backend.main:app --reload --port 8000
```

**Терминал 2 — фронтенд:**
```bash
# Windows
.venv\Scripts\python.exe -m http.server 5500 --directory frontend

# macOS / Linux
.venv/bin/python -m http.server 5500 --directory frontend
```

Открыть в браузере: **http://localhost:5500**

### Доступные адреса

| Адрес | Что там |
|---|---|
| http://localhost:5500 | Веб-интерфейс |
| http://localhost:8000/docs | Swagger — интерактивная документация API |
| http://localhost:8000/api/health | Проверка живости бэкенда |

### Запуск из командной строки (без фронта)

```bash
python main.py                  # дневной дайджест (аудитория из profile.yaml)
python main.py --audience tech  # явно для ИБ-специалистов
python main.py --audience exec  # явно для руководства
python main.py --monthly        # месячная выжимка
python main.py --monthly --days 60
```


# ИИ-ассистент для создания ИТ/ИБ дайджестов

Прототип ИИ-помощника, который собирает публикации из RSS-источников,
отбирает релевантные, классифицирует через LLM и формирует тематический
дайджест. Решение для хакатона.

## Что умеет

- Собирает публикации из RSS-источников (ИТ/ИБ-тематика).
- Удаляет дубли (fuzzy + эмбеддинги).
- Фильтрует нерелевантное через эмбеддинги и адаптивный порог.
- Классифицирует публикации через LLM (тип, приоритет, теги, impact).
- Группирует по типу и формирует Markdown-дайджест.
- Два типа дайджестов:
  - **Ежедневный** — для ИБ-специалистов (атаки, уязвимости, инциденты).
  - **Месячная выжимка** — для руководства (тренды, потери, регуляторика).
- Веб-интерфейс с историей дайджестов, управлением источниками,
  профилями интересов и настройками.
- Скачивание готового дайджеста в `.md`.

## Стек

- **Python 3.11+**
- **FastAPI** + **Uvicorn** — REST API
- **Ollama** — облачная модель `gpt-oss:120b-cloud` (классификация) и
  локальная `bge-m3` (эмбеддинги)
- **Jinja2** — шаблоны промптов
- **Pydantic** — схемы данных
- **feedparser** + **httpx** — сбор RSS
- **numpy** — косинусная близость
- **rapidfuzz** — fuzzy-дедупликация
- **PyYAML** — конфиги
- **Vanilla JS** — фронтенд без сборки

## Структура проекта

```
.
├── backend/              # REST API (FastAPI)
│   ├── main.py           # точка входа
│   ├── routes/           # эндпоинты по группам
│   ├── storage.py        # чтение YAML + память
│   ├── jobs.py           # статусы задач
│   └── runner.py         # вызов пайплайна
│
├── src/                  # ИИ-агент (пайплайн)
│   ├── models/           # pydantic-схемы
│   ├── pipeline/         # слои обработки
│   ├── providers/        # абстракция LLM
│   └── utils/            # логгер, промпты, эмбеддер
│
├── frontend/             # HTML + CSS + Vanilla JS
│   ├── index.html        # главная: генерация дайджеста
│   ├── sources.html      # управление источниками
│   ├── interests.html    # профили интересов
│   ├── history.html      # история дайджестов
│   ├── settings.html     # настройки
│   ├── api.js            # клиент HTTP
│   ├── config.js         # конфиг интерфейса
│   ├── ui.js             # утилиты UI
│   ├── storage.js        # localStorage
│   └── styles.css
│
├── config/               # YAML-конфиги
│   ├── sources.yaml      # активные RSS-источники
│   ├── profile.yaml      # профили security / management
│   ├── models.yaml       # настройки моделей
│   ├── tags.yaml         # список тегов
│   ├── source_categories.yaml
│   └── few_shots_*.yaml  # few-shot примеры
│
├── prompts/              # Jinja2-шаблоны промптов
├── scripts/              # тестовые скрипты
├── data/                 # логи, настройки (не в git)
├── output/               # сгенерированные дайджесты
│
├── main.py               # CLI-точка входа
├── requirements.txt
├── start.bat             # запуск на Windows
├── start.command         # запуск на macOS
└── README.md
```

## Конфигурация

### Источники

`config/sources.yaml` — список RSS-источников. Управляется через
интерфейс на странице «Источники». Каждый источник имеет поля:
- `id`, `name`, `url`, `type` (`rss` / `telegram` / `website`)
- `category` (`tech` / `exec`)
- `active` — включён ли в сбор

### Профили интересов

`config/profile.yaml` — два профиля:
- `security` → аудитория `tech`
- `management` → аудитория `exec`

Поле `active` указывает, какой используется по умолчанию.
В UI профили выбираются автоматически по типу дайджеста
(Ежедневный → security, Месячный → management).

### Модели

`config/models.yaml` — настройки моделей. Переключение между локальной
и облачной моделью — через тумблер ☁️ в интерфейсе.

## API (краткая справка)

| Метод | URL | Назначение |
|---|---|---|
| `GET` | `/api/health` | Проверка живости |
| `POST` | `/api/generate` | Запустить генерацию дайджеста |
| `GET` | `/api/tasks/{id}` | Статус задачи + текущий этап |
| `GET` | `/api/tasks/{id}/result` | Готовый дайджест |
| `GET` | `/api/tasks/{id}/download` | Скачать `.md` |
| `GET` | `/api/sources` | Список источников |
| `POST/PUT/DELETE` | `/api/sources[/{id}]` | Управление источниками |
| `GET` | `/api/profiles` | Профили интересов |
| `GET` | `/api/history` | История дайджестов |
| `DELETE` | `/api/history[/{id}]` | Удаление из истории |
| `GET/PUT` | `/api/settings` | Настройки |

Полная документация — в Swagger: http://localhost:8000/docs

## Логи и трассировка

Все решения пайплайна пишутся в `data/pipeline.jsonl` в формате JSONL
(один JSON на строку). Можно смотреть глазами:

```bash
tail -f data/pipeline.jsonl
```

**Windows PowerShell:**
```powershell
Get-Content data\pipeline.jsonl -Wait -Tail 5
```

## Ограничения прототипа

- Нет авторизации и разграничения доступа.
- Хранилище истории — в памяти + sidecar JSON-файлы в `output/`.
  Перезапуск не теряет дайджесты, но общая БД отсутствует.
- Экспорт в DOCX не реализован (только Markdown).
- Динамический поиск новых источников через LLM — заготовка
  (промпты есть, интеграция — в разработке).
- Часть публичных RSS-источников отдаёт 403/404 — их можно
  отключить через UI.
- Классификация идёт по одной публикации последовательно —
  узкое место по времени (1–3 минуты на полный цикл).
- Нет стриминга прогресса внутри этапа классификации.

## Возможные проблемы

| Проблема | Решение |
|---|---|
| `OLLAMA_API_KEY` не найден | Создайте `.env` в корне или задайте переменную окружения |
| `model 'gpt-oss:120b-cloud' not found` | Проверьте ключ: `curl -H "Authorization: Bearer $OLLAMA_API_KEY" https://ollama.com/api/tags` |
| `Connection refused` к Ollama | Запустите `ollama serve` в отдельном терминале |
| `bge-m3` не скачана | `ollama pull bge-m3` |
| Порт занят | Поменяйте `--port 8001` для бэкенда или `5501` для фронта |
| Кириллица в консоли Windows | `chcp 65001` или запуск через Windows Terminal |
| CORS-ошибка в браузере | Убедитесь, что `uvicorn` запущен на порту 8000 |
| Кнопка генерации не работает | Откройте DevTools → Console, пришлите ошибку |

## Лицензия

Учебный проект для хакатона. Свободное использование.