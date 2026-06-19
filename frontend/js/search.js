document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('globalSearch');
    const results = document.getElementById('searchResults');
    if (!input || !results) return;

    let debounceTimer;

    input.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        const q = input.value.trim();
        if (q.length < 2) {
            results.classList.remove('active');
            results.innerHTML = '';
            return;
        }

        debounceTimer = setTimeout(async () => {
            try {
                const { data } = await api.get('/search/', { params: { q } });
                renderResults(data, results);
            } catch {
                results.innerHTML = '<div style="padding:12px;color:#999">Ошибка поиска</div>';
                results.classList.add('active');
            }
        }, 300);
    });

    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-box')) {
            results.classList.remove('active');
        }
    });
});

function renderResults(data, container) {
    const items = [...data.regions, ...data.persons];
    if (items.length === 0) {
        container.innerHTML = '<div style="padding:12px;color:#999">Ничего не найдено</div>';
    } else {
        container.innerHTML = items.map((item) => {
            const href = item.type === 'region'
                ? `region.html?id=${item.id}`
                : `person.html?id=${item.id}`;
            return `<a href="${href}"><strong>${item.title}</strong><br><small>${item.description?.slice(0, 60)}...</small></a>`;
        }).join('');
    }
    container.classList.add('active');
}
