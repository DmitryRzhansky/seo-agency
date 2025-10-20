// Космические абстрактные фигуры для заднего фона
document.addEventListener('DOMContentLoaded', function() {
    // Создаем контейнер для космических фигур
    const spaceContainer = document.createElement('div');
    spaceContainer.id = 'space-animation-container';
    spaceContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        width: 100vw;
        height: 100vh;
        min-width: 100vw;
        min-height: 100vh;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
        margin: 0;
        padding: 0;
    `;
    
    // Добавляем контейнер в body
    document.body.appendChild(spaceContainer);
    
    // Убеждаемся, что контейнер занимает всю область экрана
    function updateContainerSize() {
        spaceContainer.style.width = window.innerWidth + 'px';
        spaceContainer.style.height = window.innerHeight + 'px';
        spaceContainer.style.minHeight = window.innerHeight + 'px';
    }
    
    // Обновляем размер при загрузке
    updateContainerSize();
    
    // Массив для хранения фигур
    const spaceObjects = [];
    
    // Класс для космических объектов
    class SpaceObject {
        constructor() {
            this.element = document.createElement('div');
            this.type = this.getRandomType();
            this.size = Math.random() * 100 + 20; // 20-120px
            this.x = Math.random() * (window.innerWidth - this.size);
            this.y = Math.random() * (window.innerHeight - this.size);
            this.vx = (Math.random() - 0.5) * 0.5; // скорость по X
            this.vy = (Math.random() - 0.5) * 0.5; // скорость по Y
            this.rotation = 0;
            this.rotationSpeed = (Math.random() - 0.5) * 2;
            this.opacity = Math.random() * 0.3 + 0.1; // 0.1-0.4
            this.pulseSpeed = Math.random() * 0.02 + 0.01;
            this.pulsePhase = Math.random() * Math.PI * 2;
            
            this.createElement();
            this.updatePosition();
            spaceContainer.appendChild(this.element);
        }
        
        getRandomType() {
            const types = ['star', 'planet', 'nebula', 'asteroid', 'comet'];
            return types[Math.floor(Math.random() * types.length)];
        }
        
        createElement() {
            this.element.className = `space-object space-${this.type}`;
            this.element.style.cssText = `
                position: absolute;
                left: ${this.x}px;
                top: ${this.y}px;
                width: ${this.size}px;
                height: ${this.size}px;
                opacity: ${this.opacity};
                transform: rotate(${this.rotation}deg);
                transition: none;
            `;
            
            // Создаем содержимое в зависимости от типа
            switch(this.type) {
                case 'star':
                    this.createStar();
                    break;
                case 'planet':
                    this.createPlanet();
                    break;
                case 'nebula':
                    this.createNebula();
                    break;
                case 'asteroid':
                    this.createAsteroid();
                    break;
                case 'comet':
                    this.createComet();
                    break;
            }
        }
        
        createStar() {
            this.element.innerHTML = `
                <div style="
                    width: 100%;
                    height: 100%;
                    background: radial-gradient(circle, #ffffff 0%, #4a9eff 30%, transparent 70%);
                    border-radius: 50%;
                    box-shadow: 0 0 ${this.size/2}px #4a9eff;
                    animation: twinkle 3s ease-in-out infinite alternate;
                "></div>
            `;
        }
        
        createPlanet() {
            const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3'];
            const color = colors[Math.floor(Math.random() * colors.length)];
            
            this.element.innerHTML = `
                <div style="
                    width: 100%;
                    height: 100%;
                    background: radial-gradient(circle at 30% 30%, 
                        ${color} 0%, 
                        ${color}dd 40%, 
                        ${color}88 70%, 
                        ${color}44 100%);
                    border-radius: 50%;
                    box-shadow: inset -${this.size/4}px -${this.size/4}px ${this.size/2}px rgba(0,0,0,0.3);
                "></div>
            `;
        }
        
        createNebula() {
            const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3'];
            const color1 = colors[Math.floor(Math.random() * colors.length)];
            const color2 = colors[Math.floor(Math.random() * colors.length)];
            
            this.element.innerHTML = `
                <div style="
                    width: 100%;
                    height: 100%;
                    background: radial-gradient(ellipse, 
                        ${color1}44 0%, 
                        ${color2}22 50%, 
                        transparent 100%);
                    border-radius: 50%;
                    filter: blur(2px);
                    animation: nebulaPulse 4s ease-in-out infinite alternate;
                "></div>
            `;
        }
        
        createAsteroid() {
            this.element.innerHTML = `
                <div style="
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(45deg, 
                        #8b4513 0%, 
                        #a0522d 25%, 
                        #cd853f 50%, 
                        #8b4513 75%, 
                        #654321 100%);
                    border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
                    box-shadow: inset -${this.size/6}px -${this.size/6}px ${this.size/3}px rgba(0,0,0,0.4);
                "></div>
            `;
        }
        
        createComet() {
            this.element.innerHTML = `
                <div style="
                    width: 100%;
                    height: 100%;
                    position: relative;
                ">
                    <div style="
                        width: 60%;
                        height: 60%;
                        background: radial-gradient(circle, #ffffff 0%, #87ceeb 50%, transparent 100%);
                        border-radius: 50%;
                        position: absolute;
                        top: 20%;
                        left: 20%;
                    "></div>
                    <div style="
                        width: 200%;
                        height: 20%;
                        background: linear-gradient(90deg, 
                            transparent 0%, 
                            #87ceeb 20%, 
                            #ffffff 50%, 
                            transparent 100%);
                        position: absolute;
                        top: 40%;
                        left: -50%;
                        border-radius: 50%;
                        filter: blur(1px);
                    "></div>
                </div>
            `;
        }
        
        updatePosition() {
            this.x += this.vx;
            this.y += this.vy;
            this.rotation += this.rotationSpeed;
            
            // Пульсация
            this.pulsePhase += this.pulseSpeed;
            const pulse = Math.sin(this.pulsePhase) * 0.1 + 1;
            
            // Проверяем границы экрана
            if (this.x < -this.size) this.x = window.innerWidth;
            if (this.x > window.innerWidth) this.x = -this.size;
            if (this.y < -this.size) this.y = window.innerHeight;
            if (this.y > window.innerHeight) this.y = -this.size;
            
            // Обновляем позицию
            this.element.style.left = this.x + 'px';
            this.element.style.top = this.y + 'px';
            this.element.style.transform = `
                rotate(${this.rotation}deg) 
                scale(${pulse})
            `;
        }
    }
    
    // Создаем космические объекты
    const objectCount = Math.min(15, Math.floor(window.innerWidth / 100));
    for (let i = 0; i < objectCount; i++) {
        const obj = new SpaceObject();
        spaceObjects.push(obj);
    }
    
    // Анимационный цикл
    function animate() {
        spaceObjects.forEach(obj => obj.updatePosition());
        requestAnimationFrame(animate);
    }
    
    // Запускаем анимацию
    animate();
    
    // Обработка изменения размера окна
    window.addEventListener('resize', function() {
        // Обновляем размер контейнера
        updateContainerSize();
        
        spaceObjects.forEach(obj => {
            // Пересчитываем позиции при изменении размера окна
            if (obj.x > window.innerWidth) obj.x = window.innerWidth - obj.size;
            if (obj.y > window.innerHeight) obj.y = window.innerHeight - obj.size;
        });
    });
    
    // Добавляем CSS анимации
    const style = document.createElement('style');
    style.textContent = `
        @keyframes twinkle {
            0% { 
                opacity: 0.3; 
                transform: scale(1);
            }
            100% { 
                opacity: 1; 
                transform: scale(1.2);
            }
        }
        
        @keyframes nebulaPulse {
            0% { 
                opacity: 0.2; 
                transform: scale(1);
            }
            100% { 
                opacity: 0.6; 
                transform: scale(1.1);
            }
        }
        
        .space-object {
            will-change: transform, opacity;
        }
        
        /* Адаптивность для мобильных устройств */
        @media (max-width: 768px) {
            .space-object {
                opacity: 0.5 !important;
            }
        }
        
        @media (max-width: 480px) {
            .space-object {
                opacity: 0.3 !important;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Пауза анимации при неактивной вкладке
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            spaceObjects.forEach(obj => {
                obj.element.style.animationPlayState = 'paused';
            });
        } else {
            spaceObjects.forEach(obj => {
                obj.element.style.animationPlayState = 'running';
            });
        }
    });
});
