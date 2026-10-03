/* ============================================================
   Общие утилиты интерфейса
   ============================================================ */

function escapeHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;')
        .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function formatDate(iso) {
    const d = new Date(iso);
    const now = new Date();
    const diffMs = now - d;
    const diffMin = Math.floor(diffMs / 60000);
    const diffH   = Math.floor(diffMs / 3600000);
    const diffD   = Math.floor(diffMs / 86400000);

    if (diffMin < 1) return 'только что';
    if (diffMin < 60) return `${diffMin} мин назад`;
    if (diffH < 24)   return `${diffH} ч назад`;
    if (diffD < 7)    return `${diffD} дн назад`;
    return d.toLocaleDateString('ru-RU',
        { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
}

/* --- Toast --- */
let __toastTimer;
function showToast(text, isError = false) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    const txt = document.getElementById('toastText');
    const ico = document.getElementById('toastIcon');
    if (txt) txt.textContent = text;
    if (ico && typeof getIcon === 'function') ico.innerHTML = getIcon('check');
    toast.style.borderLeftColor = isError ? 'var(--danger)' : 'var(--accent)';
    toast.classList.add('show');
    clearTimeout(__toastTimer);
    __toastTimer = setTimeout(() => toast.classList.remove('show'), 3000);
}

/* --- Dirty-состояние с автосохранением черновика --- */
const Dirty = {
    _key: null,
    _state: false,

    init(key) {
        this._key = key;
        this._state = false;
    },

    set(value) {
        this._state = value;
        const ind = document.getElementById('unsavedIndicator');
        if (ind) ind.classList.toggle('show', value);
    },

    get() { return this._state; },
};

window.addEventListener('beforeunload', (e) => {
    if (Dirty.get()) {
        e.preventDefault();
        e.returnValue = '';
    }
});