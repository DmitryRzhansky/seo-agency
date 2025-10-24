// Современный хедер с мега-меню
document.addEventListener('DOMContentLoaded', function() {
    const servicesMenu = document.getElementById('servicesMenu');
    const servicesDropdown = document.getElementById('servicesDropdown');
    const servicesMegaMenu = document.querySelector('.services-mega-menu');
    
    // Показать/скрыть мега-меню при наведении
    if (servicesMenu && servicesMegaMenu) {
        let hoverTimeout;
        
        servicesMenu.addEventListener('mouseenter', function() {
            clearTimeout(hoverTimeout);
            servicesMegaMenu.classList.add('show');
            servicesDropdown.setAttribute('aria-expanded', 'true');
        });
        
        servicesMenu.addEventListener('mouseleave', function() {
            hoverTimeout = setTimeout(function() {
                servicesMegaMenu.classList.remove('show');
                servicesDropdown.setAttribute('aria-expanded', 'false');
            }, 300);
        });
        
        // Клик для мобильных устройств
        servicesDropdown.addEventListener('click', function(e) {
            if (window.innerWidth < 992) {
                e.preventDefault();
                servicesMegaMenu.classList.toggle('show');
                servicesDropdown.setAttribute('aria-expanded', 
                    servicesMegaMenu.classList.contains('show') ? 'true' : 'false'
                );
            }
        });
    }
    
    // Закрыть мега-меню при клике вне его
    document.addEventListener('click', function(e) {
        if (servicesMegaMenu && !servicesMenu.contains(e.target)) {
            servicesMegaMenu.classList.remove('show');
            servicesDropdown.setAttribute('aria-expanded', 'false');
        }
    });
    
    // Эффект скролла для хедера
    const navbar = document.querySelector('.navbar-modern');
    if (navbar) {
        let lastScrollTop = 0;
        
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
            
            lastScrollTop = scrollTop;
        });
    }
    
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
});
