const Store = {
    getTheme() { return localStorage.getItem('theme') || 'dark'; },
    setTheme(v) { localStorage.setItem('theme', v); },
    isSidebarCollapsed() { return localStorage.getItem('sidebarCollapsed') === '1'; },
    setSidebarCollapsed(v) { localStorage.setItem('sidebarCollapsed', v ? '1' : '0'); },
    setRepeatParams(p) {
        if (p.query) localStorage.setItem('repeat_query', p.query);
        if (p.profile) localStorage.setItem('repeat_profile', p.profile);
        if (p.model) localStorage.setItem('repeat_model', p.model);
    },
    takeRepeatParams() {
        const out = {
            query: localStorage.getItem('repeat_query'),
            profile: localStorage.getItem('repeat_profile'),
            model: localStorage.getItem('repeat_model'),
        };
        localStorage.removeItem('repeat_query');
        localStorage.removeItem('repeat_profile');
        localStorage.removeItem('repeat_model');
        return out;
    },
};