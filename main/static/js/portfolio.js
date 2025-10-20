document.addEventListener('DOMContentLoaded', function() {
    // Плавная прокрутка к секции портфолио
    const portfolioLink = document.querySelector('a[href="#portfolio"]');
    if (portfolioLink) {
        portfolioLink.addEventListener('click', function(e) {
            e.preventDefault();
            const portfolioSection = document.getElementById('portfolio');
            if (portfolioSection) {
                portfolioSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    }

    // Анимация появления карточек при прокрутке
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Наблюдаем за карточками портфолио
    const portfolioCards = document.querySelectorAll('.portfolio-card');
    portfolioCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // Добавляем индикатор загрузки для изображений
    const portfolioImages = document.querySelectorAll('.portfolio-image img');
    portfolioImages.forEach(img => {
        img.addEventListener('load', function() {
            this.style.opacity = '1';
        });

        img.addEventListener('error', function() {
            const placeholder = this.parentElement.querySelector('.no-image-placeholder');
            if (placeholder) {
                placeholder.style.display = 'flex';
            }
            this.style.display = 'none';
        });
    });

    // Обработка формы поиска
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');

    if (searchForm && searchInput) {
        // Сохраняем текущие параметры фильтрации
        const urlParams = new URLSearchParams(window.location.search);
        const currentType = urlParams.get('type');

        // Добавляем скрытое поле для типа, если он есть
        if (currentType) {
            const hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = 'type';
            hiddenInput.value = currentType;
            searchForm.appendChild(hiddenInput);
        }

        // Если есть поисковый запрос, прокручиваем к результатам
        const searchQuery = urlParams.get('q');
        if (searchQuery) {
            // Ждем загрузки всех элементов
            setTimeout(() => {
                const portfolioSection = document.getElementById('portfolio');
                if (portfolioSection) {
                    portfolioSection.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }, 100);
        }

        // Обработка отправки формы поиска
        searchForm.addEventListener('submit', function(e) {
            const searchValue = searchInput.value.trim();
            if (searchValue) {
                // Прокручиваем к результатам поиска после отправки
                setTimeout(() => {
                    const portfolioSection = document.getElementById('portfolio');
                    if (portfolioSection) {
                        portfolioSection.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                }, 200);
            }
        });

        // Обработка очистки поиска
        const clearSearchBtn = document.querySelector('a[href*="portfolio_list"]');
        if (clearSearchBtn) {
            clearSearchBtn.addEventListener('click', function(e) {
                // Прокручиваем к началу портфолио после очистки
                setTimeout(() => {
                    const portfolioSection = document.getElementById('portfolio');
                    if (portfolioSection) {
                        portfolioSection.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                }, 200);
            });
        }
    }

    // Фильтрация портфолио без перезагрузки страницы
    const filterButtons = document.querySelectorAll('.filter-btn');
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    const portfolioGrid = document.getElementById('portfolio-grid');

    if (filterButtons.length > 0 && portfolioItems.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                const selectedType = this.getAttribute('data-type');

                // Обновляем активную кнопку
                filterButtons.forEach(btn => {
                    btn.classList.remove('btn-primary');
                    btn.classList.add('btn-outline-primary');
                });
                this.classList.remove('btn-outline-primary');
                this.classList.add('btn-primary');

                // Фильтруем элементы
                let visibleCount = 0;
                portfolioItems.forEach(item => {
                    const itemType = item.getAttribute('data-type');

                    if (selectedType === '' || itemType === selectedType) {
                        item.style.display = 'block';
                        item.style.opacity = '0';
                        item.style.transform = 'translateY(30px)';

                        // Анимация появления
                        setTimeout(() => {
                            item.style.opacity = '1';
                            item.style.transform = 'translateY(0)';
                        }, visibleCount * 100);

                        visibleCount++;
                    } else {
                        item.style.display = 'none';
                    }
                });

                // Показываем сообщение, если нет результатов
                let noResultsMessage = document.getElementById('no-results-message');
                if (visibleCount === 0) {
                    if (!noResultsMessage) {
                        noResultsMessage = document.createElement('div');
                        noResultsMessage.id = 'no-results-message';
                        noResultsMessage.className = 'col-12 text-center py-5';
                        noResultsMessage.innerHTML = '<p class="lead text-muted">В выбранной категории пока нет проектов.</p>';
                        portfolioGrid.appendChild(noResultsMessage);
                    }
                    noResultsMessage.style.display = 'block';
                } else {
                    if (noResultsMessage) {
                        noResultsMessage.style.display = 'none';
                    }
                }

                // Обновляем URL без перезагрузки страницы
                const url = new URL(window.location);
                if (selectedType) {
                    url.searchParams.set('type', selectedType);
                } else {
                    url.searchParams.delete('type');
                }
                window.history.pushState({}, '', url);
            });
        });
    }
});


