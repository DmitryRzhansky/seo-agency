// ============================================
// BRUTALIST SEO STUDIO - PREMIUM JAVASCRIPT
// v4.0 LEBEDEV EDITION
// ============================================

'use strict';

// ============================================
// ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
// ============================================
let customCursor, cursorFollower;
let mouseX = 0, mouseY = 0;
let followerX = 0, followerY = 0;

// ============================================
// ПРЕЛОАДЕР
// ============================================
let preloaderProgress = 0;

function initPreloader() {
    const preloader = document.getElementById('preloader');
    const percentText = document.getElementById('percentText');
    const barProgress = document.querySelector('.bar-progress');
    
    if (!preloader) return;

    // Анимация прогресса
    const progressInterval = setInterval(() => {
        if (preloaderProgress < 100) {
            preloaderProgress += Math.random() * 15;
            if (preloaderProgress > 100) preloaderProgress = 100;
            
            percentText.textContent = Math.floor(preloaderProgress) + '%';
            barProgress.style.width = preloaderProgress + '%';
        } else {
            clearInterval(progressInterval);
            setTimeout(() => {
                preloader.classList.add('hidden');
                setTimeout(() => {
                    preloader.style.display = 'none';
                }, 500);
            }, 300);
        }
    }, 100);
}

// Запускаем прелоадер немедленно
initPreloader();

// ============================================
// ИНИЦИАЛИЗАЦИЯ ПРИ ЗАГРУЗКЕ
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    // initCustomCursor(); // Отключен - тормозит
    initScrollProgress();
    initMobileMenu();
    initSmoothScroll();
    initScrollAnimations();
    initNumberCounters();
    initFormHandling();
    // initTopBarButtons(); // Удалено - обработчики перенесены в base.html
    initScrollToTop();
    initCookieNotice();
    initDiscountButton();
    initFAQ();
    // initGlitchEffect(); // Отключен - выглядит как баг
    initParallax();
    initTiltEffect();
    // initCursorInteractions(); // Отключен - не нужен без кастомного курсора
    
    console.log('%c ЗА ДЕНЬГИ В ТОП | BRUTALISM LOADED ', 'background: #000; color: #3cc33c; font-size: 20px; padding: 10px;');
});

// ============================================
// КАСТОМНЫЙ КУРСОР
// ============================================
function initCustomCursor() {
    if (window.innerWidth <= 768) return;

    customCursor = document.querySelector('.custom-cursor');
    cursorFollower = document.querySelector('.cursor-follower');

    if (!customCursor || !cursorFollower) return;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;

        customCursor.style.transform = `translate(${mouseX - 10}px, ${mouseY - 10}px)`;
    });

    // Плавное следование для follower
    const animateFollower = () => {
        followerX += (mouseX - followerX) * 0.1;
        followerY += (mouseY - followerY) * 0.1;

        cursorFollower.style.transform = `translate(${followerX - 20}px, ${followerY - 20}px)`;
        requestAnimationFrame(animateFollower);
    };
    animateFollower();

    // Эффекты при наведении на интерактивные элементы
    document.querySelectorAll('a, button, input, textarea, .service-card, .case-item').forEach(el => {
        el.addEventListener('mouseenter', () => {
            customCursor.style.transform += ' scale(2)';
            cursorFollower.style.transform += ' scale(1.5)';
        });

        el.addEventListener('mouseleave', () => {
            customCursor.style.transform = customCursor.style.transform.replace(' scale(2)', '');
            cursorFollower.style.transform = cursorFollower.style.transform.replace(' scale(1.5)', '');
        });
    });

    // Клик эффект
    document.addEventListener('mousedown', () => {
        customCursor.style.transform += ' scale(0.8)';
    });

    document.addEventListener('mouseup', () => {
        customCursor.style.transform = customCursor.style.transform.replace(' scale(0.8)', '');
    });
}

// ============================================
// ПРОГРЕСС СКРОЛЛА
// ============================================
function initScrollProgress() {
    const progressBar = document.querySelector('.scroll-progress');
    if (!progressBar) return;

    window.addEventListener('scroll', () => {
        const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (window.scrollY / windowHeight) * 100;
        progressBar.style.width = scrolled + '%';
    });
}

// ============================================
// МОБИЛЬНОЕ МЕНЮ
// ============================================
function initMobileMenu() {
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.querySelector('.nav-menu');

    if (!menuToggle || !navMenu) return;

    menuToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        document.body.classList.toggle('menu-open');
        menuToggle.textContent = navMenu.classList.contains('active') ? '✕' : '☰';
    });

    // Закрытие меню при клике на ссылку
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            document.body.classList.remove('menu-open');
            menuToggle.textContent = '☰';
        });
    });

    // Закрытие меню при клике вне его
    document.addEventListener('click', (e) => {
        if (!navMenu.contains(e.target) && !menuToggle.contains(e.target)) {
            navMenu.classList.remove('active');
            document.body.classList.remove('menu-open');
            menuToggle.textContent = '☰';
        }
    });
    
    // Закрытие меню при изменении размера окна
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768 && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            document.body.classList.remove('menu-open');
            menuToggle.textContent = '☰';
        }
    });
}

// ============================================
// ПЛАВНАЯ ПРОКРУТКА
// ============================================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                const offsetTop = target.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ============================================
// АНИМАЦИИ ПРИ СКРОЛЛЕ (INTERSECTION OBSERVER)
// ============================================
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.15,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                
                // Специальная анимация для карточек
                if (entry.target.classList.contains('service-card') || 
                    entry.target.classList.contains('case-item')) {
                    entry.target.style.transform = 'translateY(0) translateX(0)';
                }

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

    // Наблюдаем за различными элементами
    const elementsToAnimate = [
        '.service-card',
        '.case-item',
        '.feature-item',
        '.metric-item',
        '.contact-form-wrapper',
        '.contact-info-wrapper'
    ];

    elementsToAnimate.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(40px)';
            el.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            observer.observe(el);
        });
    });
}

// ============================================
// СЧЕТЧИКИ ЦИФР
// ============================================
function initNumberCounters() {
    const counters = document.querySelectorAll('[data-target]');
    
    const animateCounter = (counter) => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;

        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };

        updateCounter();
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

// ============================================
// КНОПКИ ВЕРХНЕЙ ПАНЕЛИ
// ============================================
// Функция удалена - обработчики перенесены в base.html для модального окна

// ============================================
// КАЛЬКУЛЯТОР
// ============================================
const btnCalc = document.querySelector('.btn-calc');
if (btnCalc) {
    btnCalc.addEventListener('click', () => {
        const selects = document.querySelectorAll('.calc-select');
        const values = Array.from(selects).map(s => s.value);
        
        // Простой расчет (можно усложнить)
        let basePrice = 45000;
        
        // Корректировка по количеству запросов
        if (values[1] === '50-100') basePrice = 55000;
        if (values[1] === '100-200') basePrice = 70000;
        if (values[1] === '200+') basePrice = 90000;
        
        // Обновляем цену
        const resultPrice = document.querySelector('.result-price');
        if (resultPrice) {
            resultPrice.textContent = `от ${basePrice.toLocaleString('ru-RU')} ₽`;
        }
        
        showNotification('РАСЧЕТ ГОТОВ', `Примерная стоимость: от ${basePrice.toLocaleString('ru-RU')} ₽/месяц`, 'success');
    });
}

const btnOrder = document.querySelector('.btn-order');
if (btnOrder) {
    btnOrder.addEventListener('click', () => {
        showNotification('ЗАКАЗАТЬ КОНСУЛЬТАЦИЮ', 'Мы свяжемся с вами для обсуждения деталей', 'success');
    });
}

// ============================================
// ОБРАБОТКА ФОРМЫ
// ============================================
function initFormHandling() {
    // Hero форма
    const heroForm = document.getElementById('heroForm');
    if (heroForm) {
        heroForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(heroForm);
            const data = Object.fromEntries(formData);
            
            try {
                const response = await fetch(heroForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': data.csrfmiddlewaretoken
                    }
                });
                
                if (response.ok) {
                    showNotification('ЗАЯВКА ОТПРАВЛЕНА!', 'Мы свяжемся с вами в течение 15 минут.', 'success');
                    heroForm.reset();
                    console.log('Hero form data:', data);
                } else {
                    showNotification('ОШИБКА!', 'Произошла ошибка при отправке заявки.', 'error');
                }
            } catch (error) {
                console.error('Error submitting hero form:', error);
                showNotification('ОШИБКА!', 'Произошла ошибка при отправке заявки.', 'error');
            }
        });
    }

    // Контактная форма
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(contactForm);
            const data = Object.fromEntries(formData);
            
            try {
                const response = await fetch(contactForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': data.csrfmiddlewaretoken
                    }
                });
                
                if (response.ok) {
                    showNotification('ЗАЯВКА ОТПРАВЛЕНА!', 'Мы свяжемся с вами в ближайшее время.', 'success');
                    contactForm.reset();
                    console.log('Contact form data:', data);
                } else {
                    showNotification('ОШИБКА!', 'Произошла ошибка при отправке заявки.', 'error');
                }
            } catch (error) {
                console.error('Error submitting contact form:', error);
                showNotification('ОШИБКА!', 'Произошла ошибка при отправке заявки.', 'error');
            }
        });
    }

    // Валидация полей в реальном времени
    const allInputs = document.querySelectorAll('input, textarea');
    allInputs.forEach(input => {
        input.addEventListener('blur', () => {
            if (input.validity.valid) {
                input.style.borderColor = '#000';
            } else {
                input.style.borderColor = '#3cc33c';
            }
        });
    });
}

// ============================================
// УВЕДОМЛЕНИЯ
// ============================================
function showNotification(title, message, type = 'success') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0.8);
        background-color: ${type === 'success' ? '#000' : '#FF0000'};
        color: white;
        padding: 50px 70px;
        border: 3px solid black;
        font-size: 18px;
        font-weight: 900;
        letter-spacing: 2px;
        z-index: 10002;
        box-shadow: 15px 15px 0 rgba(0, 0, 0, 0.3);
        max-width: 90%;
        text-align: center;
        opacity: 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    `;
    
    notification.innerHTML = `
        <div style="font-size: 24px; margin-bottom: 15px;">${title}</div>
        <div style="font-size: 16px; font-weight: 500; opacity: 0.9;">${message}</div>
    `;

    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.8);
        z-index: 10001;
        opacity: 0;
        transition: opacity 0.3s;
        backdrop-filter: blur(5px);
    `;

    document.body.appendChild(overlay);
    document.body.appendChild(notification);

    // Анимация появления
    requestAnimationFrame(() => {
        overlay.style.opacity = '1';
        notification.style.opacity = '1';
        notification.style.transform = 'translate(-50%, -50%) scale(1)';
    });

    // Автоматическое закрытие
    setTimeout(() => {
        closeNotification();
    }, 3000);

    // Закрытие по клику
    overlay.addEventListener('click', closeNotification);

    function closeNotification() {
        notification.style.opacity = '0';
        notification.style.transform = 'translate(-50%, -50%) scale(0.8)';
        overlay.style.opacity = '0';

        setTimeout(() => {
            if (document.body.contains(notification)) document.body.removeChild(notification);
            if (document.body.contains(overlay)) document.body.removeChild(overlay);
        }, 300);
    }
}

// ============================================
// ГЛИТЧ ЭФФЕКТ ДЛЯ ЗАГОЛОВКОВ
// ============================================
function initGlitchEffect() {
    const titles = document.querySelectorAll('.hero-title, .section-title h2');
    
    titles.forEach(title => {
        title.addEventListener('mouseenter', () => {
            applyGlitch(title);
        });
    });
}

function applyGlitch(element) {
    const originalText = element.textContent;
    const glitchChars = '!@#$%^&*()_+-=[]{}|;:,.<>?/~`';
    let iterations = 0;
    const maxIterations = 10;

    const interval = setInterval(() => {
        element.textContent = originalText
            .split('')
            .map((char, index) => {
                if (char === ' ') return char;
                if (Math.random() > 0.7) {
                    return glitchChars[Math.floor(Math.random() * glitchChars.length)];
                }
                return char;
            })
            .join('');

        iterations++;
        if (iterations >= maxIterations) {
            clearInterval(interval);
            element.textContent = originalText;
        }
    }, 50);
}

// ============================================
// ПАРАЛЛАКС ЭФФЕКТ
// ============================================
function initParallax() {
    let ticking = false;

    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const scrolled = window.pageYOffset;

                // Параллакс для фоновых фигур
                document.querySelectorAll('.shape').forEach((shape, index) => {
                    const speed = (index + 1) * 0.02;
                    shape.style.transform = `translateY(${scrolled * speed}px) rotate(${scrolled * 0.02}deg)`;
                });

                // Параллакс для визуальных элементов hero
                document.querySelectorAll('.visual-box').forEach((box, index) => {
                    const speed = (index + 1) * 0.03;
                    const baseTransform = box.style.transform || '';
                    if (scrolled < window.innerHeight) {
                        box.style.transform = `translateY(${scrolled * speed}px)`;
                    }
                });

                ticking = false;
            });
            ticking = true;
        }
    });
}

// ============================================
// TILT ЭФФЕКТ (3D)
// ============================================
function initTiltEffect() {
    const tiltElements = document.querySelectorAll('[data-tilt]');

    tiltElements.forEach(element => {
        element.addEventListener('mousemove', handleTilt);
        element.addEventListener('mouseleave', resetTilt);
    });

    function handleTilt(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;

        this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.05)`;
    }

    function resetTilt() {
        this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
    }
}

// ============================================
// ИНТЕРАКТИВНОСТЬ КУРСОРА
// ============================================
function initCursorInteractions() {
    // Кнопки
    document.querySelectorAll('button, .cta-button').forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            if (customCursor) {
                customCursor.style.width = '40px';
                customCursor.style.height = '40px';
                customCursor.style.background = '#FF0000';
            }
        });

        btn.addEventListener('mouseleave', () => {
            if (customCursor) {
                customCursor.style.width = '20px';
                customCursor.style.height = '20px';
                customCursor.style.background = '#FF0000';
            }
        });
    });

    // Ссылки
    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('mouseenter', () => {
            if (customCursor) {
                customCursor.style.borderRadius = '50%';
            }
        });

        link.addEventListener('mouseleave', () => {
            if (customCursor) {
                customCursor.style.borderRadius = '0';
            }
        });
    });
}

// ============================================
// АНИМАЦИЯ КАРТОЧЕК УСЛУГ
// ============================================
document.querySelectorAll('.service-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.zIndex = '10';
        
        // Анимация иконки
        const icon = this.querySelector('.service-icon');
        if (icon) {
            icon.style.transform = 'scale(1.1) rotate(5deg)';
        }
    });

    card.addEventListener('mouseleave', function() {
        this.style.zIndex = '1';
        
        // Возврат иконки
        const icon = this.querySelector('.service-icon');
        if (icon) {
            icon.style.transform = 'scale(1) rotate(0deg)';
        }
    });
    
    // Добавляем transition для иконки
    const icon = card.querySelector('.service-icon');
    if (icon) {
        icon.style.transition = 'transform 0.3s ease';
    }
});

// ============================================
// АНИМАЦИЯ КЕЙСОВ
// ============================================
document.querySelectorAll('.case-item').forEach(caseItem => {
    caseItem.addEventListener('mouseenter', function() {
        const resultValues = this.querySelectorAll('.result-value');
        resultValues.forEach(value => {
            // Эффект "подпрыгивания" цифр
            value.style.transform = 'scale(1.1)';
            setTimeout(() => {
                value.style.transform = 'scale(1)';
            }, 200);
        });
        
        // Перезапуск анимации прогресс-баров
        const bars = this.querySelectorAll('.bar-fill');
        bars.forEach(bar => {
            const width = bar.style.width;
            bar.style.transition = 'none';
            bar.style.width = '0';
            setTimeout(() => {
                bar.style.transition = 'width 1s cubic-bezier(0.4, 0, 0.2, 1)';
                bar.style.width = width;
            }, 50);
        });
    });
    
    // Добавляем transition для плавности
    const resultValues = caseItem.querySelectorAll('.result-value');
    resultValues.forEach(value => {
        value.style.transition = 'transform 0.2s ease';
    });
});

// ============================================
// ДИНАМИЧЕСКАЯ СМЕНА ТЕКСТА В HERO
// ============================================
function initDynamicText() {
    const words = ['ПРОДВИЖЕНИЕ', 'АНАЛИТИКА', 'РЕЗУЛЬТАТЫ', 'ТРАФИК'];
    let currentIndex = 0;
    const heroTitle = document.querySelector('.hero-title .word:first-child');

    if (!heroTitle) return;

    setInterval(() => {
        currentIndex = (currentIndex + 1) % words.length;
        heroTitle.style.opacity = '0';
        
        setTimeout(() => {
            heroTitle.textContent = words[currentIndex];
            heroTitle.style.opacity = '1';
        }, 300);
    }, 3000);
}

// Раскомментируйте для активации динамического текста
// initDynamicText();

// ============================================
// СТАТИСТИКА ВЗАИМОДЕЙСТВИЙ
// ============================================
let interactions = {
    clicks: 0,
    scrolls: 0,
    hovers: 0
};

document.addEventListener('click', () => {
    interactions.clicks++;
});

window.addEventListener('scroll', () => {
    interactions.scrolls++;
});

document.querySelectorAll('a, button, .service-card, .case-item').forEach(el => {
    el.addEventListener('mouseenter', () => {
        interactions.hovers++;
    });
});

// Логирование статистики (для аналитики)
window.addEventListener('beforeunload', () => {
    console.log('User Interactions:', interactions);
});

// ============================================
// EASTER EGG
// ============================================
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.key);
    konamiCode = konamiCode.slice(-10);

    if (konamiCode.join('') === konamiSequence.join('')) {
        activateEasterEgg();
    }
});

function activateEasterEgg() {
    document.body.style.animation = 'rainbow 2s infinite';
    showNotification('🎉 KONAMI CODE!', 'Вы нашли секретный код брутализма!', 'success');

    // Добавляем анимацию радуги
    const style = document.createElement('style');
    style.textContent = `
        @keyframes rainbow {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(360deg); }
        }
    `;
    document.head.appendChild(style);

    setTimeout(() => {
        document.body.style.animation = '';
    }, 5000);
}

// ============================================
// ПРОИЗВОДИТЕЛЬНОСТЬ
// ============================================
// Throttle функция для оптимизации
function throttle(func, delay) {
    let lastCall = 0;
    return function(...args) {
        const now = new Date().getTime();
        if (now - lastCall < delay) return;
        lastCall = now;
        return func(...args);
    };
}

// Debounce функция
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Оптимизация скролл событий
window.addEventListener('scroll', throttle(() => {
    // Ваш код для скролла
}, 100));

// ============================================
// КНОПКА НАВЕРХ
// ============================================
function initScrollToTop() {
    const scrollBtn = document.getElementById('scrollToTop');
    if (!scrollBtn) return;

    // Показываем кнопку при скролле
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollBtn.classList.add('visible');
        } else {
            scrollBtn.classList.remove('visible');
        }
    });

    // Клик по кнопке
    scrollBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// ============================================
// COOKIE УВЕДОМЛЕНИЕ
// ============================================
function initCookieNotice() {
    const cookieNotice = document.getElementById('cookieNotice');
    const acceptBtn = document.getElementById('acceptCookie');
    
    if (!cookieNotice || !acceptBtn) return;

    // Проверяем localStorage
    const cookieAccepted = localStorage.getItem('cookieAccepted');
    
    if (!cookieAccepted) {
        // Показываем уведомление через 1 секунду
        setTimeout(() => {
            cookieNotice.classList.add('active');
        }, 1000);
    }

    // Обработка принятия
    acceptBtn.addEventListener('click', () => {
        localStorage.setItem('cookieAccepted', 'true');
        cookieNotice.classList.remove('active');
        
        setTimeout(() => {
            cookieNotice.style.display = 'none';
        }, 400);
    });
}

// ============================================
// ПЛАВАЮЩАЯ КНОПКА СКИДКИ
// ============================================
function initDiscountButton() {
    const discountBtn = document.getElementById('discountBtn');
    if (!discountBtn) return;

    // Показываем кнопку сразу после загрузки
    setTimeout(() => {
        discountBtn.classList.add('visible');
    }, 2000);

    // Клик по кнопке
    discountBtn.addEventListener('click', () => {
        showNotification('СКИДКА 50%', 'Оставьте заявку прямо сейчас и получите скидку 50% на первый месяц продвижения!', 'success');
    });
}

// ============================================
// FAQ АККОРДЕОН
// ============================================
function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', () => {
            // Закрываем все остальные
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                }
            });
            
            // Переключаем текущий
            item.classList.toggle('active');
        });
    });
}

// ============================================
// MOUSE PARALLAX ДЛЯ HERO
// ============================================
function initMouseParallax() {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    
    const shapes = hero.querySelectorAll('.shape');
    
    hero.addEventListener('mousemove', (e) => {
        const { clientX, clientY } = e;
        const { width, height } = hero.getBoundingClientRect();
        
        const xPos = (clientX / width - 0.5) * 2;
        const yPos = (clientY / height - 0.5) * 2;
        
        shapes.forEach((shape, index) => {
            const speed = (index + 1) * 10;
            const x = xPos * speed;
            const y = yPos * speed;
            shape.style.transform = `translate(${x}px, ${y}px) rotate(${x}deg)`;
        });
    });
}

// Запускаем только на десктопе
if (window.innerWidth > 768) {
    initMouseParallax();
}

// ============================================
// ДОБАВЛЕНИЕ ЭФФЕКТА RIPPLE ПРИ КЛИКЕ
// ============================================
function addRippleEffect() {
    const buttons = document.querySelectorAll('button, .cta-button, .service-btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple-effect');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

addRippleEffect();

// Добавляем стили для ripple
const style = document.createElement('style');
style.textContent = `
    .ripple-effect {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ============================================
// ВЫВОД ВЕРСИИ
// ============================================
console.log(`
    ╔═══════════════════════════════════════╗
    ║     ЗА ДЕНЬГИ В ТОП - v4.0           ║
    ║   🎨 LEBEDEV EDITION 🎨               ║
    ║   Designed with perfection            ║
    ╚═══════════════════════════════════════╝
`);

// ============================================
// ПЛАВАЮЩИЙ БАННЕР С АКЦИЕЙ
// ============================================
function initFloatingPromo() {
    const promo = document.getElementById('floatingPromo');
    const closeBtn = document.getElementById('promoClose');
    const ctaBtn = document.getElementById('promoCTA');
    const timerValue = document.getElementById('timerValue');
    
    if (!promo) return;
    
    // Проверяем, был ли баннер закрыт ранее
    const promoClosed = localStorage.getItem('promoClosed');
    if (promoClosed) {
        promo.style.display = 'none';
        return;
    }
    
    // Показываем баннер при скролле вниз на 500px
    let promoShown = false;
    
    function checkScroll() {
        if (promoShown) return;
        
        const scrolled = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrolled > 500) { // Появляется после скролла на 500px
            promo.style.display = 'block';
            promoShown = true;
            // Убираем listener после показа
            window.removeEventListener('scroll', checkScroll);
        }
    }
    
    window.addEventListener('scroll', checkScroll);
    
    // Закрытие баннера
    closeBtn.addEventListener('click', () => {
        promo.classList.add('hidden');
        localStorage.setItem('promoClosed', 'true');
        setTimeout(() => {
            promo.style.display = 'none';
        }, 400);
    });
    
    // CTA кнопка
    ctaBtn.addEventListener('click', () => {
        // Скроллим к форме
        const form = document.querySelector('.hero-form');
        if (form) {
            form.scrollIntoView({ behavior: 'smooth', block: 'center' });
            // Фокусируемся на первом поле
            setTimeout(() => {
                const firstInput = form.querySelector('input');
                if (firstInput) firstInput.focus();
            }, 500);
        }
        // Закрываем баннер
        promo.classList.add('hidden');
        setTimeout(() => {
            promo.style.display = 'none';
        }, 400);
    });
    
    // Таймер обратного отсчета
    let hours = 2;
    let minutes = 45;
    let seconds = 30;
    
    function updateTimer() {
        seconds--;
        
        if (seconds < 0) {
            seconds = 59;
            minutes--;
        }
        
        if (minutes < 0) {
            minutes = 59;
            hours--;
        }
        
        if (hours < 0) {
            hours = 0;
            minutes = 0;
            seconds = 0;
        }
        
        const h = String(hours).padStart(2, '0');
        const m = String(minutes).padStart(2, '0');
        const s = String(seconds).padStart(2, '0');
        
        timerValue.textContent = `${h}:${m}:${s}`;
        
        if (hours === 0 && minutes === 0 && seconds === 0) {
            clearInterval(timerInterval);
            timerValue.textContent = '00:00:00';
        }
    }
    
    const timerInterval = setInterval(updateTimer, 1000);
}

// Инициализация плавающего баннера
initFloatingPromo();

// ============================================
// СКОРОСТЬ РЕНДЕРИНГА
// ============================================
function displayRenderSpeed() {
    const renderSpeedEl = document.getElementById('renderSpeed');
    if (!renderSpeedEl) return;
    
    // Используем Performance API
    window.addEventListener('load', () => {
        setTimeout(() => {
            if (window.performance && window.performance.timing) {
                const perfData = window.performance.timing;
                const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
                const domReadyTime = perfData.domContentLoadedEventEnd - perfData.navigationStart;
                
                // Форматируем время
                const loadSeconds = (pageLoadTime / 1000).toFixed(2);
                const domSeconds = (domReadyTime / 1000).toFixed(2);
                
                // Выводим информацию
                renderSpeedEl.innerHTML = `
                    Рендеринг: <strong>${domSeconds}s</strong> 
                    | Загрузка: <strong>${loadSeconds}s</strong>
                `;
            } else {
                renderSpeedEl.textContent = 'Рендеринг: < 1s ⚡';
            }
        }, 100);
    });
}

// Запускаем вычисление скорости
displayRenderSpeed();

// ============================================
// ЭКСПОРТ ДЛЯ МОДУЛЬНОЙ СИСТЕМЫ (опционально)
// ============================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initCustomCursor,
        showNotification,
        applyGlitch
    };
}
