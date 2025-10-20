// Анимации появления при прокрутке и вспомогательные эффекты
document.addEventListener('DOMContentLoaded', function() {
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

    // Навигация: пункт "Услуги" должен открывать dropdown на мобилке и вести на страницу на десктопе
    const servicesLink = document.getElementById('servicesDropdown');
    function updateServicesToggle() {
        if (!servicesLink) return;
        if (window.innerWidth >= 992) {
            // На десктопе убираем dropdown-поведение, оставляем переход по ссылке
            servicesLink.removeAttribute('data-bs-toggle');
        } else {
            // На мобилке оставляем открытие dropdown по клику
            servicesLink.setAttribute('data-bs-toggle', 'dropdown');
        }
    }
    updateServicesToggle();
    window.addEventListener('resize', updateServicesToggle);
});


