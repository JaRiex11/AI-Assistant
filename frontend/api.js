/* ============================================================
   API-слой приложения.

   Единая точка выхода на бэкенд. Все страницы работают только
   через объект API. Пока USE_MOCK = true, данные берутся из
   mock-заглушек (для демо). Когда бэкенд готов — переключить
   USE_MOCK на false, и всё заработает через fetch.

   Контракт (что должен реализовать бэкенд) — см. JSDoc над
   каждой функцией. Формат ошибок: { error: "текст" },
   HTTP-статусы 4xx/5xx.
   ============================================================ */

/* ---------- Настройки окружения ---------- */

/** Базовый URL бэкенда. Для локальной разработки — пустой. */
const API_BASE = '';   // например: 'http://localhost:8000'

/** true — данные из мока; false — реальные запросы к бэкенду. */
const USE_MOCK = true;

/** Таймаут запроса в миллисекундах. */
const REQUEST_TIMEOUT_MS = 15000;


/* ============================================================
   API
   ============================================================ */

const API = {

    /* ==========================================================
       ДАЙДЖЕСТ
       ========================================================== */

    /**
     * Сгенерировать дайджест.
     *
     * POST /api/generate
     * Body:  { query, model, period, profileId, sourceIds }
     * Response: Digest
     *
     * @param {Object}   params
     * @param {string}   params.query      — текстовый запрос пользователя
     * @param {string}   params.model      — id модели, например 'gpt-oss-120b'
     * @param {number}   params.period     — период в днях (1, 7, 30, 90)
     * @param {string?}  params.profileId  — id профиля интересов (опционально)
     * @param {string[]} params.sourceIds  — id выбранных источников
     * @returns {Promise<Digest>}
     */
    async generateDigest({ query, model, period, profileId = null, sourceIds = [] }) {
        if (USE_MOCK) {
            await sleep(1500);
            return {
                id: 'd' + Date.now(),
                status: 'done',
                query, model, period, profileId, sourceIds,
                createdAt: new Date().toISOString(),
                preview: `# Дайджест: ${query}\n\n(здесь будет результат генерации)`,
                sources: [],
                articlesCount: 0,
                durationSec: 0,
            };
        }
        return request('POST', '/api/generate',
            { query, model, period, profileId, sourceIds });
    },

    /**
     * Получить один дайджест по id (для просмотра из истории).
     *
     * GET /api/digests/:id
     * Response: Digest
     *
     * @param {string} id
     * @returns {Promise<Digest>}
     */
    async getDigest(id) {
        if (USE_MOCK) {
            await sleep(200);
            const found = CONFIG.history.defaultEntries.find(e => e.id === id);
            return found ? JSON.parse(JSON.stringify(found)) : null;
        }
        return request('GET', `/api/digests/${id}`);
    },

    /**
     * Скачать дайджест в указанном формате.
     *
     * GET /api/digests/:id/download?format=md|docx
     * Response: binary (Content-Type: application/octet-stream)
     *
     * @param {string} id
     * @param {'md'|'docx'} format
     * @returns {Promise<{ blob: Blob, filename: string }>}
     */
    async downloadDigest(id, format = 'md') {
        if (format === 'docx') {
        throw new Error('Экспорт в DOCX пока не поддерживается');
        }
        if (USE_MOCK) {
            const entry = CONFIG.history.defaultEntries.find(e => e.id === id);
            const content = (entry?.preview || '') + '\n';
            return {
                blob: new Blob([content], { type: 'text/markdown' }),
                filename: `digest-${id}.md`,
            };
        }
        const res = await fetch(
            `${API_BASE}/api/digests/${id}/download?format=${format}`
        );
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const blob = await res.blob();
        const cd = res.headers.get('Content-Disposition') || '';
        const match = cd.match(/filename="?([^"]+)"?/);
        return { blob, filename: match ? match[1] : `digest-${id}` };
    },


    /* ==========================================================
       ИСТОЧНИКИ
       ========================================================== */

    /**
     * Получить список источников.
     *
     * GET /api/sources
     * Response: Source[]
     *
     * Source:
     *   { id, group, type, name, url, active,
     *     articlesPerDay, lastFetch, status, errorMessage? }
     *
     * @returns {Promise<Source[]>}
     */
    async getSources() {
        if (USE_MOCK) {
            await sleep(200);
            return JSON.parse(JSON.stringify(CONFIG.sources.defaultSources));
        }
        return request('GET', '/api/sources');
    },

    /**
     * Создать источник.
     *
     * POST /api/sources
     * Body: { group, type, name, url }
     * Response: Source
     *
     * @param {Object} source
     * @returns {Promise<Source>}
     */
    async createSource(source) {
        if (USE_MOCK) {
            await sleep(300);
            return {
                id: 's' + Date.now(),
                active: true,
                articlesPerDay: 0,
                lastFetch: 'ещё не загружался',
                status: 'ok',
                ...source,
            };
        }
        return request('POST', '/api/sources', source);
    },

    /**
     * Обновить источник (частичное обновление).
     *
     * PUT /api/sources/:id
     * Body: { name?, url?, group?, type?, active? }
     * Response: Source
     *
     * @param {string} id
     * @param {Object} patch
     * @returns {Promise<Source>}
     */
    async updateSource(id, patch) {
        if (USE_MOCK) {
            await sleep(300);
            return { id, ...patch };
        }
        return request('PUT', `/api/sources/${id}`, patch);
    },

    /**
     * Удалить источник.
     *
     * DELETE /api/sources/:id
     * Response: { ok: true }
     *
     * @param {string} id
     * @returns {Promise<{ok: true}>}
     */
    async deleteSource(id) {
        if (USE_MOCK) { await sleep(150); return { ok: true }; }
        return request('DELETE', `/api/sources/${id}`);
    },

    /**
     * Обновить один источник (перечитать RSS / Telegram).
     *
     * POST /api/sources/:id/refresh
     * Response: { status, articlesPerDay, lastFetch }
     *
     * @param {string} id
     * @returns {Promise<{status: string, articlesPerDay: number, lastFetch: string}>}
     */
    async refreshSource(id) {
        if (USE_MOCK) {
            await sleep(900);
            return {
                status: 'ok',
                articlesPerDay: Math.floor(Math.random() * 30) + 5,
                lastFetch: 'только что',
            };
        }
        return request('POST', `/api/sources/${id}/refresh`);
    },

    /**
     * Обновить все активные источники.
     *
     * POST /api/sources/refresh-all
     * Response: { ok: true, updated: number }
     *
     * @returns {Promise<{ok: true, updated: number}>}
     */
    async refreshAllSources() {
        if (USE_MOCK) { await sleep(1200); return { ok: true, updated: 0 }; }
        return request('POST', '/api/sources/refresh-all');
    },

    /**
     * Импортировать источники из OPML-файла.
     *
     * POST /api/sources/import-opml
     * Body: multipart/form-data, поле "file"
     * Response: { added: number, skipped: number, sources: Source[] }
     *
     * @param {File} file
     * @returns {Promise<{added: number, skipped: number, sources: Source[]}>}
     */
    async importOpml(file) {
        if (USE_MOCK) {
            await sleep(500);
            return { added: 0, skipped: 0, sources: [] };
        }
        const form = new FormData();
        form.append('file', file);
        const res = await fetch(`${API_BASE}/api/sources/import-opml`, {
            method: 'POST',
            body: form,
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
    },

    /**
     * Экспортировать источники в OPML.
     *
     * GET /api/sources/export-opml
     * Response: text/xml
     *
     * @returns {Promise<{blob: Blob, filename: string}>}
     */
    async exportOpml() {
        if (USE_MOCK) {
            const opml = `<?xml version="1.0" encoding="UTF-8"?>\n<opml version="2.0"><body/></opml>`;
            return {
                blob: new Blob([opml], { type: 'text/xml' }),
                filename: 'sources.opml',
            };
        }
        const res = await fetch(`${API_BASE}/api/sources/export-opml`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const blob = await res.blob();
        return { blob, filename: 'sources.opml' };
    },


    /* ==========================================================
       ПРОФИЛИ ИНТЕРЕСОВ
       ========================================================== */

    /**
     * Получить все профили интересов.
     *
     * GET /api/profiles
     * Response: Profile[]
     *
     * Profile:
     *   { id, icon, name, topics[], stopwords[], threshold, period }
     *
     * Topic:
     *   { id, name, weight: 'high'|'medium'|'low', keywords[] }
     *
     * @returns {Promise<Profile[]>}
     */
    async getProfiles() {
        if (USE_MOCK) {
            await sleep(200);
            return JSON.parse(JSON.stringify(CONFIG.defaultProfiles));
        }
        return request('GET', '/api/profiles');
    },

    /**
     * Создать профиль.
     *
     * POST /api/profiles
     * Body: Profile (без id)
     * Response: Profile (с id)
     *
     * @param {Object} profile
     * @returns {Promise<Profile>}
     */
    async createProfile(profile) {
        if (USE_MOCK) {
            await sleep(300);
            return { id: Date.now(), ...profile };
        }
        return request('POST', '/api/profiles', profile);
    },

    /**
     * Обновить профиль (полная замена).
     *
     * PUT /api/profiles/:id
     * Body: Profile
     * Response: Profile
     *
     * @param {string|number} id
     * @param {Object} profile
     * @returns {Promise<Profile>}
     */
    async updateProfile(id, profile) {
        if (USE_MOCK) { await sleep(300); return { id, ...profile }; }
        return request('PUT', `/api/profiles/${id}`, profile);
    },

    /**
     * Удалить профиль.
     *
     * DELETE /api/profiles/:id
     * Response: { ok: true }
     *
     * @param {string|number} id
     * @returns {Promise<{ok: true}>}
     */
    async deleteProfile(id) {
        if (USE_MOCK) { await sleep(200); return { ok: true }; }
        return request('DELETE', `/api/profiles/${id}`);
    },


    /* ==========================================================
       ИСТОРИЯ ДАЙДЖЕСТОВ
       ========================================================== */

    /**
     * Получить историю дайджестов.
     *
     * GET /api/history?period=7&search=CVE
     * Response: DigestEntry[]
     *
     * DigestEntry — то же, что Digest, плюс поля
     *   profileName, profileIcon, status, errorMessage?.
     *
     * @param {Object} [filter]
     * @param {number} [filter.period]  — период в днях
     * @param {string} [filter.search]  — поиск по теме/профилю
     * @returns {Promise<DigestEntry[]>}
     */
    async getHistory(filter = {}) {
        if (USE_MOCK) {
            await sleep(200);
            return JSON.parse(JSON.stringify(CONFIG.history.defaultEntries));
        }
        const qs = new URLSearchParams();
        if (filter.period) qs.set('period', filter.period);
        if (filter.search) qs.set('search', filter.search);
        const query = qs.toString();
        return request('GET', `/api/history${query ? '?' + query : ''}`);
    },

    /**
     * Удалить одну запись истории.
     *
     * DELETE /api/history/:id
     * Response: { ok: true }
     *
     * @param {string} id
     * @returns {Promise<{ok: true}>}
     */
    async deleteHistoryEntry(id) {
        if (USE_MOCK) { await sleep(150); return { ok: true }; }
        return request('DELETE', `/api/history/${id}`);
    },

    /**
     * Очистить всю историю.
     *
     * DELETE /api/history
     * Response: { ok: true }
     *
     * @returns {Promise<{ok: true}>}
     */
    async clearHistory() {
        if (USE_MOCK) { await sleep(200); return { ok: true }; }
        return request('DELETE', '/api/history');
    },

    /**
     * Повторить генерацию — создать новый дайджест на основе
     * сохранённых параметров старого.
     *
     * POST /api/history/:id/repeat
     * Response: Digest
     *
     * @param {string} id — id записи из истории
     * @returns {Promise<Digest>}
     */
    async repeatDigest(id) {
        if (USE_MOCK) {
            await sleep(1500);
            const entry = CONFIG.history.defaultEntries.find(e => e.id === id);
            if (!entry) throw new Error('Запись не найдена');
            return {
                id: 'd' + Date.now(),
                status: 'done',
                query: entry.query,
                model: entry.model,
                period: 7,
                preview: entry.preview,
                sources: entry.sources || [],
            };
        }
        return request('POST', `/api/history/${id}/repeat`);
    },


    /* ==========================================================
       НАСТРОЙКИ
       ========================================================== */

    /**
     * Получить сохранённые настройки пользователя.
     *
     * GET /api/settings
     * Response: Settings | null
     *
     * Settings:
     *   { outputFormat, defaultModel, language, maxArticles,
     *     groupByTopic, addSources, addSummary, dedup }
     *
     * @returns {Promise<Settings|null>}
     */
    async getSettings() {
        if (USE_MOCK) { await sleep(150); return null; }
        return request('GET', '/api/settings');
    },

    /**
     * Сохранить настройки.
     *
     * PUT /api/settings
     * Body: Settings
     * Response: Settings
     *
     * @param {Object} settings
     * @returns {Promise<Settings>}
     */
    async updateSettings(settings) {
        if (USE_MOCK) { await sleep(300); return settings; }
        return request('PUT', '/api/settings', settings);
    },


    /* ==========================================================
       API-КЛЮЧИ
       ========================================================== */

    /**
     * Проверить API-ключ провайдера модели.
     *
     * POST /api/keys/check
     * Body: { provider, key }
     * Response: { ok: boolean, message?: string }
     *
     * @param {string} provider — 'gpt-oss-120b' | 'alice-ai-art' | ...
     * @param {string} key
     * @returns {Promise<{ok: boolean, message?: string}>}
     */
    async checkApiKey(provider, key) {
        if (USE_MOCK) {
            await sleep(600);
            return { ok: key.length > 8 };
        }
        return request('POST', '/api/keys/check', { provider, key });
    },


    /* ==========================================================
       МЕТА
       ========================================================== */

    /**
     * Проверка доступности бэкенда.
     *
     * GET /api/health
     * Response: { ok: true, version: string }
     *
     * @returns {Promise<{ok: true, version: string}>}
     */
    async healthCheck() {
        if (USE_MOCK) { await sleep(100); return { ok: true, version: 'mock' }; }
        return request('GET', '/api/health');
    },
};


/* ============================================================
   Служебные функции
   ============================================================ */

/** Пауза (для мок-режима). */
function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}

/**
 * Универсальный запрос с таймаутом и разбором ошибок.
 *
 * @param {string} method — 'GET' | 'POST' | 'PUT' | 'DELETE'
 * @param {string} url    — относительный путь (без API_BASE)
 * @param {Object} [body] — тело запроса (для POST/PUT)
 * @returns {Promise<any>}
 * @throws {Error} с человекочитаемым сообщением
 */
async function request(method, url, body) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

    try {
        const res = await fetch(API_BASE + url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: body ? JSON.stringify(body) : undefined,
            signal: controller.signal,
        });

        if (!res.ok) {
            let msg = `HTTP ${res.status}`;
            try {
                const data = await res.json();
                msg = data.error || data.message || msg;
            } catch (e) { /* тело не JSON — оставляем статус */ }
            throw new Error(msg);
        }

        // Некоторые эндпоинты могут не вернуть тело (204 No Content)
        if (res.status === 204) return null;
        return res.json();

    } catch (err) {
        if (err.name === 'AbortError') {
            throw new Error('Превышено время ожидания запроса');
        }
        throw err;
    } finally {
        clearTimeout(timer);
    }
}

/**
 * Единый обработчик ошибок API — показывает toast.
 * Использовать в catch-блоках на страницах.
 *
 * @param {Error} err
 * @param {string} [userMessage] — текст для пользователя
 */
function handleApiError(err, userMessage) {
    console.error('[API]', err);
    if (typeof showToast === 'function') {
        showToast(userMessage || 'Ошибка: ' + (err.message || 'неизвестная'), true);
    }
}