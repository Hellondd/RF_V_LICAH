document.addEventListener('DOMContentLoaded', () => {
    
    // Фильтрация регионов
    const regionSearch = document.getElementById('regionSearch');
    const districtFilter = document.getElementById('districtFilter');
    const regionsGrid = document.getElementById('regionsGrid');

    if (regionSearch && districtFilter && regionsGrid) {
        const cards = regionsGrid.getElementsByClassName('card');

        function filterRegions() {
            const searchValue = regionSearch.value.toLowerCase();
            const filterValue = districtFilter.value;

            for (let card of cards) {
                const title = card.querySelector('h3').innerText.toLowerCase();
                const text = card.innerText.toLowerCase();
                const district = card.getAttribute('data-district');

                const matchesSearch = title.includes(searchValue) || text.includes(searchValue);
                const matchesFilter = filterValue === "" || district === filterValue;

                if (matchesSearch && matchesFilter) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            }
        }

        regionSearch.addEventListener('input', filterRegions);
        districtFilter.addEventListener('change', filterRegions);
    }

    // Фильтрация персоналий
    const filterButtons = document.querySelectorAll('.filter-btn');
    const personsGrid = document.getElementById('personsGrid');

    if (filterButtons.length > 0 && personsGrid) {
        const cards = personsGrid.getElementsByClassName('card');

        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                filterButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');

                const category = button.getAttribute('data-category');

                for (let card of cards) {
                    const cardCat = card.getAttribute('data-cat');
                    if (category === 'all' || cardCat === category) {
                        card.style.display = "block";
                    } else {
                        card.style.display = "none";
                    }
                }
            });
        });
    }
});