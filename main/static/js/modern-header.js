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
                // Скрыть все категории
                categories.forEach(category => category.classList.remove('active'));
            }, 300);
        });
        
        // Функция для умного позиционирования панели услуг
        function adjustServicesPanelPosition(category) {
            const servicesPanel = category.querySelector('.brutal-mega-menu-services');
            if (!servicesPanel) return;
            
            // Сброс позиционирования
            servicesPanel.style.left = '0';
            servicesPanel.style.right = 'auto';
            servicesPanel.style.transform = 'none';
            
            // Получаем позицию категории и панели
            const categoryRect = category.getBoundingClientRect();
            const panelRect = servicesPanel.getBoundingClientRect();
            const viewportWidth = window.innerWidth;
            
            // Если панель выходит за правый край экрана
            if (panelRect.right > viewportWidth - 20) {
                // Смещаем влево
                const offset = panelRect.right - viewportWidth + 20;
                servicesPanel.style.left = `-${offset}px`;
            }
            
            // Если панель выходит за левый край экрана
            if (panelRect.left < 20) {
                servicesPanel.style.left = '20px';
            }
        }
        
        // Обработка наведения на категорию
        categories.forEach(category => {
            category.addEventListener('mouseenter', function() {
                // Убрать активность с других категорий
                categories.forEach(cat => cat.classList.remove('active'));
                
                // Активировать текущую категорию
                this.classList.add('active');
                
                // Умное позиционирование панели услуг
                setTimeout(() => {
                    adjustServicesPanelPosition(this);
                }, 10);
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
                    
                    // Активировать текущую категорию
                    category.classList.add('active');
                    console.log('Категория активирована:', categorySlug); // Отладка
                    
                    // Умное позиционирование панели услуг
                    setTimeout(() => {
                        adjustServicesPanelPosition(category);
                    }, 10);
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
                // Скрыть все категории
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
            // Скрыть все категории
            categories.forEach(category => category.classList.remove('active'));
        }
    });
    
    // Пересчитывать позиции при изменении размера окна
    window.addEventListener('resize', function() {
        const activeCategory = document.querySelector('.brutal-mega-menu-category.active');
        if (activeCategory) {
            adjustServicesPanelPosition(activeCategory);
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
