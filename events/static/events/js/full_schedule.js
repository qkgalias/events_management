(function () {
    const searchInput = document.getElementById('search-input');
    if (!searchInput) {
        return;
    }

    searchInput.addEventListener('input', () => {
        sessionStorage.setItem('searchActive', 'true');
    });

    const restoreFocus = () => {
        const isSearchActive = sessionStorage.getItem('searchActive') === 'true';
        const forceFocus = localStorage.getItem('forceFocus') === 'true';

        if (isSearchActive || forceFocus) {
            searchInput.focus();
            const value = searchInput.value || '';
            searchInput.setSelectionRange(value.length, value.length);
            sessionStorage.removeItem('searchActive');
            localStorage.removeItem('forceFocus');
        }
    };

    document.addEventListener('DOMContentLoaded', restoreFocus);
    window.addEventListener('pageshow', restoreFocus);
})();
