// Многоуровневое мега-меню
document.addEventListener('DOMContentLoaded', function() {
    const servicesMenu = document.getElementById('servicesMenu');
    const servicesDropdown = document.getElementById('servicesDropdown');
    const servicesMegaMenu = document.getElementById('servicesMegaMenu');
    const categories = document.querySelectorAll('.brutal-mega-menu-category');
    const servicesPanels = document.querySelectorAll('.brutal-mega-menu-services-panel');
    
    if (servicesMenu && servicesMegaMenu) {
        let hoverTimeout;
        
        // Показать мега-меню при наведении
        servicesMenu.addEventListener('mouseenter', function() {
            clearTimeout(hoverTimeout);
            servicesMegaMenu.classList.add('show');
            servicesDropdown.querySelector('i').style.transform = 'rotate(180deg)';
        });
        
        // Скрыть мега-меню при уходе мыши
        servicesMenu.addEventListener('mouseleave', function() {
            hoverTimeout = setTimeout(function() {
                servicesMegaMenu.classList.remove('show');
                servicesDropdown.querySelector('i').style.transform = 'rotate(0deg)';
                // Скрыть контейнер услуг и все панели
                const servicesContainer = document.querySelector('.brutal-mega-menu-services');
                if (servicesContainer) {
                    servicesContainer.classList.remove('show');
                }
                servicesPanels.forEach(panel => panel.classList.remove('show'));
                categories.forEach(category => category.classList.remove('active'));
            }, 300);
        });
        
        // Обработка наведения на категорию
        categories.forEach(category => {
            category.addEventListener('mouseenter', function() {
                const categorySlug = this.dataset.category;
                
                // Убрать активность с других категорий
                categories.forEach(cat => cat.classList.remove('active'));
                servicesPanels.forEach(panel => panel.classList.remove('show'));
                
                // Активировать текущую категорию
                this.classList.add('active');
                
                // Показать контейнер услуг
                const servicesContainer = document.querySelector('.brutal-mega-menu-services');
                if (servicesContainer) {
                    servicesContainer.classList.add('show');
                    
                    // Показать панель услуг
                    const servicesPanel = servicesContainer.querySelector(`[data-panel="${categorySlug}"]`);
                    if (servicesPanel) {
                        servicesPanel.classList.add('show');
                    }
                }
            });
        });
        
        // Обработка клика на категорию - раскрывает услуги
        categories.forEach(category => {
            const title = category.querySelector('.brutal-mega-menu-category-title');
            if (title) {
                title.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    const categorySlug = category.dataset.category;
                    console.log('Клик на категорию:', categorySlug); // Отладка
                    
                    // Убрать активность с других категорий
                    categories.forEach(cat => cat.classList.remove('active'));
                    servicesPanels.forEach(panel => panel.classList.remove('show'));
                    
                    // Активировать текущую категорию
                    category.classList.add('active');
                    
                    // Показать контейнер услуг
                    const servicesContainer = document.querySelector('.brutal-mega-menu-services');
                    if (servicesContainer) {
                        servicesContainer.classList.add('show');
                        
                        // Показать панель услуг
                        const servicesPanel = servicesContainer.querySelector(`[data-panel="${categorySlug}"]`);
                        console.log('Найдена панель услуг:', servicesPanel); // Отладка
                        if (servicesPanel) {
                            servicesPanel.classList.add('show');
                            console.log('Панель услуг показана'); // Отладка
                        }
                    }
                });
            }
        });
        
        // Предотвратить закрытие при наведении на само меню
        servicesMegaMenu.addEventListener('mouseenter', function() {
            clearTimeout(hoverTimeout);
        });
        
        servicesMegaMenu.addEventListener('mouseleave', function() {
            hoverTimeout = setTimeout(function() {
                servicesMegaMenu.classList.remove('show');
                servicesDropdown.querySelector('i').style.transform = 'rotate(0deg)';
                // Скрыть контейнер услуг и все панели
                const servicesContainer = document.querySelector('.brutal-mega-menu-services');
                if (servicesContainer) {
                    servicesContainer.classList.remove('show');
                }
                servicesPanels.forEach(panel => panel.classList.remove('show'));
                categories.forEach(category => category.classList.remove('active'));
            }, 300);
        });
        
        // Клик для мобильных устройств
        servicesDropdown.addEventListener('click', function(e) {
            if (window.innerWidth < 992) {
                e.preventDefault();
                const isOpen = servicesMegaMenu.classList.contains('show');
                servicesMegaMenu.classList.toggle('show');
                servicesDropdown.querySelector('i').style.transform = isOpen ? 'rotate(0deg)' : 'rotate(180deg)';
            }
        });
    }
    
    // Закрыть мега-меню при клике вне его
    document.addEventListener('click', function(e) {
        if (servicesMegaMenu && !servicesMenu.contains(e.target)) {
            servicesMegaMenu.classList.remove('show');
            if (servicesDropdown.querySelector('i')) {
                servicesDropdown.querySelector('i').style.transform = 'rotate(0deg)';
            }
            // Скрыть контейнер услуг и все панели
            const servicesContainer = document.querySelector('.brutal-mega-menu-services');
            if (servicesContainer) {
                servicesContainer.classList.remove('show');
            }
            servicesPanels.forEach(panel => panel.classList.remove('show'));
            categories.forEach(category => category.classList.remove('active'));
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
    
    // Поддержка прокрутки для мега-меню
    const servicesGrid = document.querySelector('.services-grid');
    if (servicesGrid) {
        let isScrolling = false;
        
        // Сенсорная прокрутка
        servicesGrid.addEventListener('touchstart', function() {
            isScrolling = true;
        });
        
        servicesGrid.addEventListener('touchend', function() {
            isScrolling = false;
        });
        
        // Предотвращаем закрытие меню при прокрутке
        servicesGrid.addEventListener('touchmove', function(e) {
            if (isScrolling) {
                e.stopPropagation();
            }
        });
        
        // Прокрутка колесиком мыши
        servicesGrid.addEventListener('wheel', function(e) {
            e.preventDefault();
            servicesGrid.scrollLeft += e.deltaY;
        });
        
        // Прокрутка клавишами
        servicesGrid.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowLeft') {
                e.preventDefault();
                servicesGrid.scrollLeft -= 300;
            } else if (e.key === 'ArrowRight') {
                e.preventDefault();
                servicesGrid.scrollLeft += 300;
            }
        });
        
        // Делаем контейнер фокусируемым для клавиатуры
        servicesGrid.setAttribute('tabindex', '0');
        
        // Обновляем индикаторы прокрутки
        function updateScrollIndicators() {
            const megaMenu = document.querySelector('.services-mega-menu');
            const scrollLeft = servicesGrid.scrollLeft;
            const maxScroll = servicesGrid.scrollWidth - servicesGrid.clientWidth;
            
            megaMenu.classList.remove('scroll-left', 'scroll-right');
            
            if (scrollLeft > 10) {
                megaMenu.classList.add('scroll-left');
            }
            if (scrollLeft < maxScroll - 10) {
                megaMenu.classList.add('scroll-right');
            }
        }
        
        // Обновляем индикаторы при прокрутке
        servicesGrid.addEventListener('scroll', updateScrollIndicators);
        
        // Инициализируем индикаторы
        setTimeout(updateScrollIndicators, 100);
    }
    
    // Кнопка "наверх"
    const backToTopBtn = document.getElementById('back-to-top');
    if (backToTopBtn) {
        // Показать/скрыть кнопку при скролле
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        });
        
        // Плавная прокрутка вверх при клике
        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});
