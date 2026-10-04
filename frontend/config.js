/**
 * Единый конфиг приложения.
 * Меняйте здесь — и весь интерфейс адаптируется под вашу отрасль.
 */
const CONFIG = {
    /* ---------- Брендинг и тема ---------- */
    brand: {
        name: 'ИИ-ассистент',           // Название приложения
        logo: '✨',                      // Эмодзи-логотип
        accent: '#ffd700',               // Основной акцентный цвет
        accentHover: '#ffed4a',          // Акцент при наведении
        accentText: '#0f0f0f',           // Текст на акцентном фоне
    },

    /* ---------- Отраслевые тексты ---------- */
    domain: {
        title: 'ИИ-ассистент',
        subtitle: 'Отберу релевантные публикации из ваших источников ' +
                  'и сформирую тематический дайджест',
        inputPlaceholder: 'Опишите интересы или тему дайджеста',
        digestAction: 'Сгенерировать дайджест',
        profileNamePlaceholder: 'Например: Для отдела ИБ',
    },

    /* ---------- Навигация (одинаковая на всех страницах) ---------- */
    navigation: [
        { id: 'digest',    label: 'Дайджест',   href: 'index.html',     icon: 'sparkles' },
        { id: 'sources',   label: 'Источники',  href: 'sources.html',   icon: 'book' },
        { id: 'interests', label: 'Интересы',   href: 'interests.html', icon: 'target', soon: true },
        { id: 'history',   label: 'История',    href: 'history.html',   icon: 'clock' },
        { id: 'settings',  label: 'Настройки',  href: 'settings.html',  icon: 'settings' },
    ],

    /* ---------- Доступные модели ---------- */
    models: [
        { value: 'gpt-oss:120b',     label: 'gpt-oss:120b'},
        { value: 'alice-ai-art',     label: 'Alice AI ART',     disabled: true },
        { value: 'qwen3.6:35b-a3b',  label: 'Qwen3.6 35B-A3B',  disabled: true },
    ],

    /* Облачный режим — по умолчанию включён */
    cloud: {
        enabled: true,
    },

    /* ---------- Профили интересов по умолчанию ---------- */
    defaultProfiles: [
        {
            id: 1,
            icon: '👤',
            name: 'Моя подборка',
            topics: [
                { id: 't1', name: 'ИБ в энергетике', weight: 'high',
                  keywords: ['инцидент', 'утечка', 'АСУ ТП', 'SCADA'] },
                { id: 't2', name: 'Атаки на энергосистемы', weight: 'high',
                  keywords: ['APT', 'малварь', 'кибератака'] },
                { id: 't3', name: 'Импортозамещение ПО', weight: 'medium',
                  keywords: ['российское ПО', 'реестр', 'замена'] },
            ],
            stopwords: ['маркетинг', 'реклама', 'акция'],
            threshold: 65,
            period: 7,
        },
        {
            id: 2,
            icon: '🛡️',
            name: 'Для отдела ИБ',
            topics: [
                { id: 't4', name: 'Уязвимости', weight: 'high',
                  keywords: ['CVE', '0-day', 'патч'] },
                { id: 't5', name: 'SOC и мониторинг', weight: 'medium',
                  keywords: ['SIEM', 'SOC', 'детект'] },
            ],
            stopwords: [],
            threshold: 75,
            period: 1,
        },
        {
            id: 3,
            icon: '📊',
            name: 'Для руководства',
            topics: [
                { id: 't6', name: 'Регулирование', weight: 'high',
                  keywords: ['ФСТЭК', 'приказ', 'ГОСТ'] },
                { id: 't7', name: 'Стратегия и инвестиции', weight: 'medium',
                  keywords: ['инвестиции', 'проект', 'развитие'] },
            ],
            stopwords: ['технический', 'код'],
            threshold: 50,
            period: 30,
        },
    ],

    /* ---------- Периоды выборки ---------- */
    periods: [
        { value: 1,  label: 'За сутки' },
        { value: 7,  label: 'За неделю' },
        { value: 30, label: 'За месяц' },
        { value: 90, label: 'За 3 месяца' },
    ],

    /* ---------- Тексты интерфейса ---------- */
    ui: {
        interestsTitle: 'Интересы пользователя',
        interestsSubtitle: 'Настройте темы, ключевые слова и приоритеты. ' +
                           'Изменения напрямую влияют на состав генерируемого дайджеста.',
        profilesLabel: 'Профили интересов',
        topicsLabel: 'Темы',
        topicsHint: '— отметьте важность и добавьте ключевые слова',
        stopwordsLabel: 'Стоп-слова',
        stopwordsHint: '— публикации с этими словами не попадут в дайджест',
        thresholdLabel: 'Строгость отбора',
        thresholdHint: '— минимальная релевантность публикации',
        periodLabel: 'Период выборки по умолчанию',
        saveBtn: 'Сохранить профиль',
        addTopicBtn: 'Добавить тему',
        addProfileBtn: 'Новый профиль',
        resetBtn: 'Сбросить',
        unsavedIndicator: 'Есть несохранённые изменения',
        weights: { high: 'Важно', medium: 'Средне', low: 'Низко' },
    },
     
    /* ---------- Настройки ---------- */
    settings: {
        title: 'Настройки',
        subtitle: 'Параметры генерации дайджеста, подключения к моделям и формат вывода.',

        sections: {
            output:  'Формат вывода',
            model:   'Модель по умолчанию',
            api:     'Подключение к моделям (API)',
            advanced: 'Дополнительно',
        },

        outputFormats: [
            {
                value: 'md',
                label: 'Markdown (.md)',
                hint: 'Удобно для вставки в wiki или Git',
                enabled: true,
            },
            {
                value: 'docx',
                label: 'Word (.docx)',
                hint: 'Требуется бэкенд (в разработке)',
                enabled: false,
            },
            {
                value: 'both',
                label: 'Оба формата',
                hint: 'Требуется бэкенд (в разработке)',
                enabled: false,
            },
        ],

        languages: [
            { value: 'ru', label: 'Русский' },
            { value: 'en', label: 'English' },
            { value: 'auto', label: 'Авто (по источнику)' },
        ],

        digestOptions: {
            maxArticles:  { min: 5,  max: 100, default: 25, label: 'Максимум публикаций в дайджесте' },
            groupByTopic: { default: true,  label: 'Группировать по темам' },
            addSources:   { default: true,  label: 'Сохранять ссылки на источники' },
            addSummary:   { default: true,  label: 'Краткое резюме для каждой публикации' },
            dedup:        { default: true,  label: 'Удалять дубликаты' },
        },

        apiProviders: [
            { value: 'gpt-oss-120b',    label: 'gpt-oss-120b',    keyHint: 'sk-...' },
            { value: 'alice-ai-art',    label: 'Alice AI ART',    keyHint: 'alice-...' },
            { value: 'qwen3.6-35b-a3b', label: 'Qwen3.6 35B-A3B', keyHint: 'qwen-...' },
            { value: 'yandexgpt',       label: 'YandexGPT',       keyHint: 'AQVN...' },
        ],
    },

        /* ---------- Источники ---------- */
    sources: {
        title: 'Источники публикаций',
        subtitle: 'RSS-ленты, Telegram-каналы и сайты, из которых ассистент собирает публикации для дайджеста.',

        groups: [
            { id: 'news',      label: 'Новости отрасли',    icon: '📰' },
            { id: 'telegram',  label: 'Telegram-каналы',    icon: '💬' },
            { id: 'research',  label: 'Исследования и CVE', icon: '🔬' },
            { id: 'official',  label: 'Официальные органы', icon: '🏛️' },
        ],

        types: [
            { value: 'rss',      label: 'RSS',      icon: '📡' },
            { value: 'telegram', label: 'Telegram', icon: '💬' },
            { value: 'website',  label: 'Сайт',     icon: '🌐' },
        ],

        /** Предзаполненные источники (демо) */
        defaultSources: [
            {
                id: 's1', group: 'news', type: 'rss',
                name: 'SecurityLab.ru',
                url: 'https://www.securitylab.ru/rss/all.xml',
                active: true,
                articlesPerDay: 24,
                lastFetch: '5 мин назад',
                status: 'ok',
            },
            {
                id: 's2', group: 'news', type: 'rss',
                name: 'Anti-Malware.ru',
                url: 'https://www.anti-malware.ru/rss.xml',
                active: true,
                articlesPerDay: 12,
                lastFetch: '12 мин назад',
                status: 'ok',
            },
            {
                id: 's3', group: 'telegram', type: 'telegram',
                name: '@secrussia',
                url: 'https://t.me/s/secrussia',
                active: true,
                articlesPerDay: 38,
                lastFetch: '2 мин назад',
                status: 'ok',
            },
            {
                id: 's4', group: 'telegram', type: 'telegram',
                name: '@energysec',
                url: 'https://t.me/s/energysec',
                active: true,
                articlesPerDay: 15,
                lastFetch: '4 мин назад',
                status: 'ok',
            },
            {
                id: 's5', group: 'research', type: 'rss',
                name: 'NVD CVE Feed',
                url: 'https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss-analyzed.xml',
                active: true,
                articlesPerDay: 87,
                lastFetch: '1 мин назад',
                status: 'ok',
            },
            {
                id: 's6', group: 'official', type: 'website',
                name: 'ФСТЭК России — новости',
                url: 'https://fstec.ru/component/option,com_newsfeeds/',
                active: false,
                articlesPerDay: 2,
                lastFetch: '3 дня назад',
                status: 'stale',
            },
            {
                id: 's7', group: 'news', type: 'rss',
                name: 'EnergyLand.info',
                url: 'https://www.energyland.info/rss',
                active: true,
                articlesPerDay: 9,
                lastFetch: '18 мин назад',
                status: 'ok',
            },
            {
                id: 's8', group: 'research', type: 'rss',
                name: 'Kaspersky Securelist',
                url: 'https://securelist.com/feed/',
                active: true,
                articlesPerDay: 3,
                lastFetch: '2 ч назад',
                status: 'error',
                errorMessage: 'HTTP 403',
            },
        ],

        /** Тексты для статусов */
        statusLabels: {
            ok:    { label: 'Активен',         cls: 'ok' },
            stale: { label: 'Давно не было',   cls: 'stale' },
            error: { label: 'Ошибка загрузки', cls: 'error' },
        },

        ui: {
            addSourceBtn: 'Добавить источник',
            addGroupBtn:  'Новая группа',
            refreshAll:   'Обновить все',
            importOpml:   'Импорт OPML',
            exportOpml:   'Экспорт OPML',
            searchPlaceholder: 'Поиск по названию или адресу...',
            emptyState:   'Источников пока нет. Добавьте первый.',
            saveBtn:      'Сохранить',
            resetBtn:     'Сбросить',
            deleteConfirm: 'Удалить источник?',
        },
    },

        /* ---------- История дайджестов ---------- */
    history: {
        title: 'История дайджестов',
        subtitle: 'Ранее сгенерированные подборки. Можно просмотреть, скачать заново или удалить.',

        /** Статусы */
        statusLabels: {
            done:    { label: 'Готов',      cls: 'ok' },
            partial: { label: 'Частично',   cls: 'stale' },
            failed:  { label: 'Ошибка',     cls: 'error' },
        },

        /** Демо-записи */
        defaultEntries: [
            {
                id: 'd1',
                createdAt: '2026-10-03T09:15:00',
                profileName: 'Для отдела ИБ',
                profileIcon: '🛡️',
                query: 'кибератаки на АСУ ТП в энергетике',
                model: 'gpt-oss-120b',
                format: 'md',
                topicsCount: 3,
                articlesCount: 24,
                sourcesCount: 6,
                status: 'done',
                durationSec: 42,
                preview: `# Дайджест: кибератаки на АСУ ТП в энергетике\n\n## Уязвимости\n- CVE-2026-12345 в SCADA-системе...\n- Новый эксплойт для Siemens SIMATIC...\n\n## Атаки\n- APT-группа атаковала энергокомпанию...\n- Фишинговая кампания против операторов...`,
                sources: [
                    { name: 'SecurityLab.ru',     url: 'https://www.securitylab.ru/news/123456.php' },
                    { name: 'Anti-Malware.ru',    url: 'https://www.anti-malware.ru/news/123' },
                    { name: 'NVD CVE Feed',       url: 'https://nvd.nist.gov/vuln/detail/CVE-2026-12345' },
                ],
            },
            {
                id: 'd2',
                createdAt: '2026-10-02T18:40:00',
                profileName: 'Моя подборка',
                profileIcon: '👤',
                query: 'импортозамещение ПО в энергетике',
                model: 'alice-ai-art',
                format: 'docx',
                topicsCount: 2,
                articlesCount: 17,
                sourcesCount: 5,
                status: 'done',
                durationSec: 28,
                preview: `# Дайджест: импортозамещение ПО\n\n## Регулирование\n- Новые требования Минцифры...\n\n## Реестр российского ПО\n- Добавлены 12 новых продуктов...`,
                sources: [
                    { name: 'EnergyLand.info', url: 'https://www.energyland.info/news/1' },
                ],
            },
            {
                id: 'd3',
                createdAt: '2026-10-02T11:20:00',
                profileName: 'Для руководства',
                profileIcon: '📊',
                query: 'стратегия и инвестиции в энергетике',
                model: 'qwen3.6-35b-a3b',
                format: 'md',
                topicsCount: 3,
                articlesCount: 31,
                sourcesCount: 7,
                status: 'partial',
                durationSec: 55,
                preview: `# Дайджест: стратегия и инвестиции\n\n## Проекты\n- Запуск новой генерации в Сибири...\n\n## Инвестиции\n- Крупный игрок объявил о вложениях в ВИЭ...`,
                sources: [],
            },
            {
                id: 'd4',
                createdAt: '2026-10-01T16:05:00',
                profileName: 'Для отдела ИБ',
                profileIcon: '🛡️',
                query: 'новые CVE за неделю',
                model: 'gpt-oss-120b',
                format: 'md',
                topicsCount: 1,
                articlesCount: 89,
                sourcesCount: 3,
                status: 'done',
                durationSec: 38,
                preview: `# Дайджест: новые CVE\n\n## Критические уязвимости\n- CVE-2026-10001 (CVSS 9.8)...\n- CVE-2026-10002 (CVSS 9.1)...`,
                sources: [
                    { name: 'NVD CVE Feed', url: 'https://nvd.nist.gov/' },
                ],
            },
            {
                id: 'd5',
                createdAt: '2026-09-30T10:00:00',
                profileName: 'Моя подборка',
                profileIcon: '👤',
                query: 'SOC и мониторинг событий',
                model: 'gpt-oss-120b',
                format: 'both',
                topicsCount: 2,
                articlesCount: 12,
                sourcesCount: 4,
                status: 'failed',
                durationSec: 8,
                errorMessage: 'Модель недоступна (HTTP 503)',
                preview: '',
                sources: [],
            },
        ],

        /** Периоды для фильтра */
        filterPeriods: [
            { value: 'all', label: 'Все время' },
            { value: '1',   label: 'Сегодня' },
            { value: '7',   label: 'За неделю' },
            { value: '30',  label: 'За месяц' },
        ],

        ui: {
            searchPlaceholder: 'Поиск по теме или профилю...',
            emptyState: 'Здесь появятся сгенерированные дайджесты',
            emptyHint: 'Сгенерируйте первый дайджест на главной странице',
            openBtn: 'Открыть',
            downloadBtn: 'Скачать',
            repeatBtn: 'Повторить',
            deleteConfirm: 'Удалить эту запись из истории?',
            clearAllBtn: 'Очистить историю',
            clearAllConfirm: 'Удалить всю историю дайджестов? Это действие нельзя отменить.',
        },
    },
};

    

/**
 * Применяет цвета из CONFIG к CSS-переменным.
 * Вызывается на каждой странице при загрузке.
 */
function applyTheme() {
    /**
 * Осветляет HEX-цвет на заданную долю.
 * @param {string} hex   — цвет в формате #rrggbb
 * @param {number} amount — 0..1, насколько осветлить
 */
function lighten(hex, amount) {
    const num = parseInt(hex.replace('#', ''), 16);
    let r = (num >> 16) + Math.round(255 * amount);
    let g = ((num >> 8) & 0x00FF) + Math.round(255 * amount);
    let b = (num & 0x0000FF) + Math.round(255 * amount);
    r = Math.min(255, r);
    g = Math.min(255, g);
    b = Math.min(255, b);
    return '#' + ((r << 16) | (g << 8) | b).toString(16).padStart(6, '0');
}

/**
 * Проверяет, светлый ли цвет (по воспринимаемой яркости).
 * Нужно, чтобы выбирать контрастный цвет текста на акцентном фоне.
 */
function isLightColor(hex) {
    const num = parseInt(hex.replace('#', ''), 16);
    const r = (num >> 16) & 255;
    const g = (num >> 8) & 255;
    const b = num & 255;
    const brightness = (r * 299 + g * 587 + b * 114) / 1000;
    return brightness > 150;
}
    const root = document.documentElement;
    const accent = localStorage.getItem('accent') || CONFIG.brand.accent;
    root.style.setProperty('--accent', accent);
    root.style.setProperty('--accent-hover', lighten(accent, 0.15));
    root.style.setProperty('--accent-text', isLightColor(accent) ? '#0f0f0f' : '#ffffff');
    applyColorScheme();
}

/**
 * Управляет светлой/тёмной темой.
 * @param {'dark'|'light'|'auto'} [scheme] — если не передано, берёт из localStorage
 */
function applyColorScheme(scheme) {
    if (scheme === undefined) {
        scheme = localStorage.getItem('theme') || 'dark';
    }
    localStorage.setItem('theme', scheme);

    let effective = scheme;
    if (scheme === 'auto') {
        effective = window.matchMedia('(prefers-color-scheme: light)').matches
            ? 'light' : 'dark';
    }
    document.documentElement.setAttribute('data-theme', effective);
}

// Реакция на смену системной темы, если выбрано "auto"
window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', () => {
    if (localStorage.getItem('theme') === 'auto') applyColorScheme('auto');
});

/**
 * SVG-иконки для навигации и кнопок.
 * Достаются по имени: getIcon('sparkles')
 */
const ICONS = {
    sparkles: `<svg viewBox="0 0 24 24"><path d="M12 2l1.5 4.5L18 8l-4.5 1.5L12 14l-1.5-4.5L6 8l4.5-1.5z"/><path d="M18 15l1 2.5 2.5 1-2.5 1-1 2.5-1-2.5-2.5-1 2.5-1z"/></svg>`,
    book:     `<svg viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>`,
    target:   `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>`,
    clock:    `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
    settings: `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>`,
    menu:     `<svg viewBox="0 0 24 24" stroke-linecap="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>`,
    plus:     `<svg viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>`,
    trash:    `<svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6M14 11v6"/></svg>`,
    save:     `<svg viewBox="0 0 24 24"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>`,
    check:    `<svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>`,
    calendar: `<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>`,
    drag:     `<svg viewBox="0 0 24 24"><circle cx="9" cy="6" r="1.5" fill="currentColor"/><circle cx="15" cy="6" r="1.5" fill="currentColor"/><circle cx="9" cy="12" r="1.5" fill="currentColor"/><circle cx="15" cy="12" r="1.5" fill="currentColor"/><circle cx="9" cy="18" r="1.5" fill="currentColor"/><circle cx="15" cy="18" r="1.5" fill="currentColor"/></svg>`,
    key:      `<svg viewBox="0 0 24 24"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>`,
    download: `<svg viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>`,
    upload:   `<svg viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>`,
    palette:  `<svg viewBox="0 0 24 24"><circle cx="13.5" cy="6.5" r=".5"/><circle cx="17.5" cy="10.5" r=".5"/><circle cx="8.5" cy="7.5" r=".5"/><circle cx="6.5" cy="12.5" r=".5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg>`,
    globe:    `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>`,
    layers:   `<svg viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>`,
    rss:      `<svg viewBox="0 0 24 24"><path d="M4 11a9 9 0 0 1 9 9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1.5" fill="currentColor"/></svg>`,
    telegram: `<svg viewBox="0 0 24 24"><path d="M21.5 3.5L2.5 11l5 2 1.5 6 3-4 5 4 4.5-15.5z"/><path d="M9.5 13l8-6-5 9"/></svg>`,
    website:  `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>`,
    refresh:  `<svg viewBox="0 0 24 24"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>`,
    search:   `<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>`,
    edit:     `<svg viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>`,
    history:  `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
    file:     `<svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>`,
    repeat:   `<svg viewBox="0 0 24 24"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>`,
    eye:      `<svg viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>`,
    external: `<svg viewBox="0 0 24 24"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>`,
};

function getIcon(name) { return ICONS[name] || ''; }

/**
 * Рендерит левую навигацию на любой странице.
 * @param {string} activeId — id активного пункта (из CONFIG.navigation)
 */
function renderSidebar(activeId) {
    const sidebar = document.getElementById('sidebar');
    if (!sidebar) return;

    const navHtml = CONFIG.navigation.map(item => `
        <a href="${item.href}" class="nav-item ${item.id === activeId ? 'active' : ''}">
            ${getIcon(item.icon)}
            <span>${item.label}</span>
            ${item.soon ? '<span class="nav-badge-soon">скоро</span>' : ''}
        </a>
    `).join('');

    sidebar.innerHTML = `
        <div class="menu-toggle" id="toggle-btn" title="Свернуть меню">
            ${getIcon('menu')}
        </div>
        ${navHtml}
    `;
    if (Store.isSidebarCollapsed()) {
        sidebar.classList.add('collapsed');
    }
document.getElementById('toggle-btn').addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    Store.setSidebarCollapsed(sidebar.classList.contains('collapsed'));
});
}