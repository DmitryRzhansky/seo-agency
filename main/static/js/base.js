// Анимации появления при прокрутке и вспомогательные эффекты
document.addEventListener('DOMContentLoaded', function() {
    // Ленивая загрузка изображений
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        if (!img.hasAttribute('loading')) {
            img.setAttribute('loading', 'lazy');
        }
    });
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Добавляем анимации к элементам
    const animatedElements = document.querySelectorAll('.card, .section-title, .btn, .badge');
    animatedElements.forEach((el, index) => {
        el.classList.add('fade-in');
        el.style.animationDelay = `${index * 0.1}s`;
        observer.observe(el);
    });

    // Специальные анимации для разных секций
    const heroElements = document.querySelectorAll('.hero-section h1, .hero-section p, .hero-section .btn, .hero-section .director-card');
    heroElements.forEach((el, index) => {
        el.classList.add('slide-in-left');
        el.style.animationDelay = `${index * 0.2}s`;
        observer.observe(el);
    });

    const teamCards = document.querySelectorAll('.team-member, .review-author');
    teamCards.forEach((el, index) => {
        el.classList.add('scale-in');
        el.style.animationDelay = `${index * 0.15}s`;
        observer.observe(el);
    });

    // Плавная прокрутка для якорных ссылок
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Добавляем пульсирующую анимацию к кнопке CTA
    const ctaButtons = document.querySelectorAll('.btn-primary');
    ctaButtons.forEach(btn => {
        if (btn.textContent.includes('Получить') || btn.textContent.includes('Выбрать')) {
            btn.classList.add('pulse-animation');
        }
    });

    // Прокрутка контента блога колесиком мыши
    const blogScrollable = document.querySelector('.brutal-post-scrollable');
    if (blogScrollable) {
        blogScrollable.addEventListener('wheel', function(e) {
            e.preventDefault();
            this.scrollTop += e.deltaY;
        });
        
        // Делаем контейнер фокусируемым для клавиатуры
        blogScrollable.setAttribute('tabindex', '0');
        
        // Прокрутка клавишами
        blogScrollable.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowUp') {
                e.preventDefault();
                this.scrollTop -= 50;
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                this.scrollTop += 50;
            } else if (e.key === 'PageUp') {
                e.preventDefault();
                this.scrollTop -= 200;
            } else if (e.key === 'PageDown') {
                e.preventDefault();
                this.scrollTop += 200;
            }
        });
    }
    
    // Прокрутка контента услуг колесиком мыши
    const serviceScrollableElements = document.querySelectorAll('.brutal-service-scrollable, .brutal-content-text, .brutal-content-preview, .brutal-content-full');
    serviceScrollableElements.forEach(function(element) {
        element.addEventListener('wheel', function(e) {
            e.preventDefault();
            this.scrollTop += e.deltaY;
        });
        
        // Делаем контейнер фокусируемым для клавиатуры
        element.setAttribute('tabindex', '0');
        
        // Прокрутка клавишами
        element.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowUp') {
                e.preventDefault();
                this.scrollTop -= 50;
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                this.scrollTop += 50;
            } else if (e.key === 'PageUp') {
                e.preventDefault();
                this.scrollTop -= 200;
            } else if (e.key === 'PageDown') {
                e.preventDefault();
                this.scrollTop += 200;
            }
        });
    });
    
    // Прокрутка контента портфолио колесиком мыши
    const portfolioScrollableElements = document.querySelectorAll('.brutal-portfolio-scrollable');
    portfolioScrollableElements.forEach(function(element) {
        element.addEventListener('wheel', function(e) {
            e.preventDefault();
            this.scrollTop += e.deltaY;
        });
        
        // Делаем контейнер фокусируемым для клавиатуры
        element.setAttribute('tabindex', '0');
        
        // Прокрутка клавишами
        element.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowUp') {
                e.preventDefault();
                this.scrollTop -= 50;
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                this.scrollTop += 50;
            } else if (e.key === 'PageUp') {
                e.preventDefault();
                this.scrollTop -= 200;
            } else if (e.key === 'PageDown') {
                e.preventDefault();
                this.scrollTop += 200;
            }
        });
    });
});


// Cookie consent logic
(function() {
    const STORAGE_KEY = 'isakov_cookie_consent_accepted_v1';
    function showConsent() {
        const banner = document.getElementById('cookie-consent');
        if (!banner) return;
        banner.classList.remove('cookie-hidden');
        requestAnimationFrame(() => banner.classList.add('cookie-visible'));
        const accept = function() {
                try { localStorage.setItem(STORAGE_KEY, '1'); } catch (e) {}
                banner.classList.remove('cookie-visible');
                setTimeout(() => banner.classList.add('cookie-hidden'), 250);
        };
        const btn = document.getElementById('cookie-accept-btn');
        if (btn) {
            btn.addEventListener('click', accept);
        }
        // мобильная ссылка удалена — оставляем только кнопку
    }

    try {
        const accepted = localStorage.getItem(STORAGE_KEY) === '1';
        if (!accepted) {
            if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', showConsent);
            else showConsent();
        }
    } catch (e) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', showConsent);
        else showConsent();
    }
})();

// Back-to-top button logic
(function() {
    const btn = document.getElementById('back-to-top');
    if (!btn) return;
    const threshold = 400; // px
    function onScroll() {
        if (window.scrollY > threshold) btn.classList.add('show');
        else btn.classList.remove('show');
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    btn.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
})();

// AJAX-подгрузка списков для блога, услуг и портфолио (без перезагрузки страницы)
(function() {
    function fetchAndSwap(url, sectionSelector) {
        return fetch(url, { headers: { 'X-Requested-With': 'fetch' } })
            .then(r => r.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newSection = doc.querySelector(sectionSelector);
                const currentSection = document.querySelector(sectionSelector);
                if (newSection && currentSection) {
                    currentSection.innerHTML = newSection.innerHTML;
                    history.pushState({}, '', url);
                    currentSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            })
            .catch(() => {});
    }

    // Блог: форма поиска и фильтры категорий
    (function initBlogAjax() {
        const sectionSelector = '#blog-list';
        const section = document.querySelector(sectionSelector);
        if (!section) return;

        // Перехватываем submit формы поиска
        section.addEventListener('submit', function(e) {
            const form = e.target.closest('form');
            if (!form) return;
            e.preventDefault();
            const url = form.getAttribute('action') || window.location.href;
            const params = new URLSearchParams(new FormData(form));
            const finalUrl = url.split('#')[0] + '?' + params.toString() + '#blog-list';
            fetchAndSwap(finalUrl, sectionSelector);
        });

        // Перехватываем клики по кнопкам категорий/пагинации
        section.addEventListener('click', function(e) {
            const a = e.target.closest('a');
            if (!a) return;
            const href = a.getAttribute('href') || '';
            if (href.includes('#blog-list')) {
                e.preventDefault();
                fetchAndSwap(href, sectionSelector);
            }
        });
    })();

    // Услуги: форма поиска и категории
    (function initServicesAjax() {
        const sectionSelector = '#services-list';
        const section = document.querySelector(sectionSelector);
        if (!section) return;

        section.addEventListener('submit', function(e) {
            const form = e.target.closest('form');
            if (!form) return;
            e.preventDefault();
            const url = form.getAttribute('action') || window.location.href;
            const params = new URLSearchParams(new FormData(form));
            const finalUrl = url.split('#')[0] + '?' + params.toString() + '#services-list';
            fetchAndSwap(finalUrl, sectionSelector);
        });

        section.addEventListener('click', function(e) {
            const a = e.target.closest('a');
            if (!a) return;
            const href = a.getAttribute('href') || '';
            if (href.includes('#services-list')) {
                e.preventDefault();
                fetchAndSwap(href, sectionSelector);
            }
        });
    })();

    // Портфолио: форма поиска
    (function initPortfolioAjax() {
        const sectionSelector = '#portfolio';
        const section = document.querySelector(sectionSelector);
        if (!section) return;
        const searchForm = document.getElementById('search-form');
        if (searchForm) {
            searchForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const url = window.location.pathname;
                const params = new URLSearchParams(new FormData(searchForm));
                const finalUrl = url + '?' + params.toString() + '#portfolio';
                fetchAndSwap(finalUrl, sectionSelector);
            });
        }
    })();
    
// Анимация полос загрузки в кейсах (оригинальная логика)
function initProgressBars() {
    const observerOptions = {
        threshold: 0.15,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Анимация для результатов кейсов
                if (entry.target.querySelector('.bar-fill')) {
                    entry.target.querySelectorAll('.bar-fill').forEach(bar => {
                        const width = bar.style.width;
                        bar.style.width = '0';
                        setTimeout(() => {
                            bar.style.width = width;
                        }, 100);
                    });
                }
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Наблюдаем за кейсами
    document.querySelectorAll('.case-item').forEach(el => {
        observer.observe(el);
    });
}

// Вызываем функцию инициализации полос загрузки
initProgressBars();

// Инициализация селектора городов
(function initCitySelector() {
    const citySelect = document.getElementById('citySelect');
    if (!citySelect) return;

    citySelect.addEventListener('change', function() {
        const selectedCitySlug = this.value;
        if (selectedCitySlug && selectedCitySlug !== '') {
            // Переходим на страницу города
            window.location.href = `/cities/${selectedCitySlug}/`;
        }
    });
})();
});
