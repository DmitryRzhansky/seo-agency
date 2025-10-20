// SEO-тематические анимации для заднего фона
document.addEventListener('DOMContentLoaded', function() {
    // Создаем контейнер для SEO-элементов
    const seoContainer = document.createElement('div');
    seoContainer.id = 'seo-animation-container';
    seoContainer.style.cssText = `
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
    document.body.appendChild(seoContainer);
    
    // Убеждаемся, что контейнер занимает всю область экрана
    function updateContainerSize() {
        seoContainer.style.width = window.innerWidth + 'px';
        seoContainer.style.height = window.innerHeight + 'px';
        seoContainer.style.minHeight = window.innerHeight + 'px';
    }
    
    // Обновляем размер при загрузке
    updateContainerSize();
    
    // Массив для хранения SEO-элементов
    const seoObjects = [];
    
    // Класс для SEO-элементов
    class SeoObject {
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
            seoContainer.appendChild(this.element);
        }
        
        getRandomType() {
            const types = ['circle', 'triangle', 'square', 'diamond', 'hexagon', 'star', 'wave', 'spiral', 'polygon', 'blob'];
            return types[Math.floor(Math.random() * types.length)];
        }
        
        createElement() {
            this.element.className = `seo-object seo-${this.type}`;
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
                case 'circle':
                    this.createCircle();
                    break;
                case 'triangle':
                    this.createTriangle();
                    break;
                case 'square':
                    this.createSquare();
                    break;
                case 'diamond':
                    this.createDiamond();
                    break;
                case 'hexagon':
                    this.createHexagon();
                    break;
                case 'star':
                    this.createStar();
                    break;
                case 'wave':
                    this.createWave();
                    break;
                case 'spiral':
                    this.createSpiral();
                    break;
                case 'polygon':
                    this.createPolygon();
                    break;
                case 'blob':
                    this.createBlob();
                    break;
            }
        }
        
        createCircle() {
            const colors = [
                'linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%)',
                'linear-gradient(135deg, #28a745 0%, #20c997 100%)',
                'linear-gradient(135deg, #ffc107 0%, #fd7e14 100%)',
                'linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%)',
                'linear-gradient(135deg, #17a2b8 0%, #0dcaf0 100%)'
            ];
            const color = colors[Math.floor(Math.random() * colors.length)];
            
            this.element.innerHTML = `
                <div style="
                    width: 100%;
                    height: 100%;
                    background: ${color};
                    border-radius: 50%;
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                "></div>
            `;
        }
        
        createTriangle() {
            const colors = [
                'linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%)',
                'linear-gradient(135deg, #28a745 0%, #20c997 100%)',
                'linear-gradient(135deg, #ffc107 0%, #fd7e14 100%)',
                'linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%)',
                'linear-gradient(135deg, #17a2b8 0%, #0dcaf0 100%)'
            ];
            const color = colors[Math.floor(Math.random() * colors.length)];
            
            this.element.innerHTML = `
                <div style="
                    width: 100%;
                    height: 100%;
                    background: ${color};
                    clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                "></div>
            `;
        }
        
        createSquare() {
            const colors = [
                'linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%)',
                'linear-gradient(135deg, #28a745 0%, #20c997 100%)',
                'linear-gradient(135deg, #ffc107 0%, #fd7e14 100%)',
                'linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%)',
                'linear-gradient(135deg, #17a2b8 0%, #0dcaf0 100%)'
            ];
            const color = colors[Math.floor(Math.random() * colors.length)];
            
            this.element.innerHTML = `
                <div style="
                    width: 100%;
                    height: 100%;
                    background: ${color};
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                "></div>
            `;
        }
        
        createDiamond() {
            const colors = [
                'linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%)',
                'linear-gradient(135deg, #28a745 0%, #20c997 100%)',
                'linear-gradient(135deg, #ffc107 0%, #fd7e14 100%)',
                'linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%)',
                'linear-gradient(135deg, #17a2b8 0%, #0dcaf0 100%)'
            ];
            const color = colors[Math.floor(Math.random() * colors.length)];
            
            this.element.innerHTML = `
                <div style="
                    width: 100%;
                    height: 100%;
                    background: ${color};
                    clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                "></div>
            `;
        }
        
        createHexagon() {
            const colors = [
                'linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%)',
                'linear-gradient(135deg, #28a745 0%, #20c997 100%)',
                'linear-gradient(135deg, #ffc107 0%, #fd7e14 100%)',
                'linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%)',
                'linear-gradient(135deg, #17a2b8 0%, #0dcaf0 100%)'
            ];
            const color = colors[Math.floor(Math.random() * colors.length)];
            
            this.element.innerHTML = `
                <div style="
                    width: 100%;
                    height: 100%;
                    background: ${color};
                    clip-path: polygon(30% 0%, 70% 0%, 100% 50%, 70% 100%, 30% 100%, 0% 50%);
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                "></div>
            `;
        }
        
        createStar() {
            const colors = [
                'linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%)',
                'linear-gradient(135deg, #28a745 0%, #20c997 100%)',
                'linear-gradient(135deg, #ffc107 0%, #fd7e14 100%)',
                'linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%)',
                'linear-gradient(135deg, #17a2b8 0%, #0dcaf0 100%)'
            ];
            const color = colors[Math.floor(Math.random() * colors.length)];
            
            this.element.innerHTML = `
                <div style="
                    width: 100%;
                    height: 100%;
                    background: ${color};
                    clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                "></div>
            `;
        }
        
        createWave() {
            const colors = [
                'linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%)',
                'linear-gradient(135deg, #28a745 0%, #20c997 100%)',
                'linear-gradient(135deg, #ffc107 0%, #fd7e14 100%)',
                'linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%)',
                'linear-gradient(135deg, #17a2b8 0%, #0dcaf0 100%)'
            ];
            const color = colors[Math.floor(Math.random() * colors.length)];
            
            this.element.innerHTML = `
                <div style="
                    width: 100%;
                    height: 100%;
                    background: ${color};
                    border-radius: 50% 30% 70% 40%;
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                "></div>
            `;
        }
        
        createSpiral() {
            const colors = [
                'linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%)',
                'linear-gradient(135deg, #28a745 0%, #20c997 100%)',
                'linear-gradient(135deg, #ffc107 0%, #fd7e14 100%)',
                'linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%)',
                'linear-gradient(135deg, #17a2b8 0%, #0dcaf0 100%)'
            ];
            const color = colors[Math.floor(Math.random() * colors.length)];
            
            this.element.innerHTML = `
                <div style="
                    width: 100%;
                    height: 100%;
                    background: ${color};
                    border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                "></div>
            `;
        }
        
        createPolygon() {
            const colors = [
                'linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%)',
                'linear-gradient(135deg, #28a745 0%, #20c997 100%)',
                'linear-gradient(135deg, #ffc107 0%, #fd7e14 100%)',
                'linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%)',
                'linear-gradient(135deg, #17a2b8 0%, #0dcaf0 100%)'
            ];
            const color = colors[Math.floor(Math.random() * colors.length)];
            const sides = Math.floor(Math.random() * 4) + 5; // 5-8 сторон
            const points = [];
            for (let i = 0; i < sides; i++) {
                const angle = (i * 360) / sides;
                const x = 50 + 40 * Math.cos(angle * Math.PI / 180);
                const y = 50 + 40 * Math.sin(angle * Math.PI / 180);
                points.push(`${x}% ${y}%`);
            }
            
            this.element.innerHTML = `
                <div style="
                    width: 100%;
                    height: 100%;
                    background: ${color};
                    clip-path: polygon(${points.join(', ')});
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                "></div>
            `;
        }
        
        createBlob() {
            const colors = [
                'linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%)',
                'linear-gradient(135deg, #28a745 0%, #20c997 100%)',
                'linear-gradient(135deg, #ffc107 0%, #fd7e14 100%)',
                'linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%)',
                'linear-gradient(135deg, #17a2b8 0%, #0dcaf0 100%)'
            ];
            const color = colors[Math.floor(Math.random() * colors.length)];
            
            this.element.innerHTML = `
                <div style="
                    width: 100%;
                    height: 100%;
                    background: ${color};
                    border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                "></div>
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
    
    // Создаем SEO-объекты
    const objectCount = Math.min(25, Math.floor(window.innerWidth / 80));
    for (let i = 0; i < objectCount; i++) {
        const obj = new SeoObject();
        seoObjects.push(obj);
    }
    
    // Создаем соединения между объектами
    function createConnections() {
        const connections = [];
        for (let i = 0; i < seoObjects.length; i++) {
            for (let j = i + 1; j < seoObjects.length; j++) {
                const obj1 = seoObjects[i];
                const obj2 = seoObjects[j];
                const distance = Math.sqrt(
                    Math.pow(obj1.x - obj2.x, 2) + Math.pow(obj1.y - obj2.y, 2)
                );
                
                // Создаем соединение если объекты близко
                if (distance < 200 && Math.random() < 0.3) {
                    const connection = document.createElement('div');
                    connection.className = 'seo-connection';
                    connection.style.cssText = `
                        position: absolute;
                        left: ${Math.min(obj1.x, obj2.x)}px;
                        top: ${Math.min(obj1.y, obj2.y)}px;
                        width: ${Math.abs(obj1.x - obj2.x)}px;
                        height: ${Math.abs(obj1.y - obj2.y)}px;
                        border: 1px solid rgba(13, 110, 253, 0.2);
                        pointer-events: none;
                        z-index: -1;
                    `;
                    
                    // Создаем SVG линию для соединения
                    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                    svg.style.cssText = `
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        pointer-events: none;
                    `;
                    
                    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                    line.setAttribute('x1', obj1.x - Math.min(obj1.x, obj2.x));
                    line.setAttribute('y1', obj1.y - Math.min(obj1.y, obj2.y));
                    line.setAttribute('x2', obj2.x - Math.min(obj1.x, obj2.x));
                    line.setAttribute('y2', obj2.y - Math.min(obj1.y, obj2.y));
                    line.setAttribute('stroke', 'rgba(13, 110, 253, 0.3)');
                    line.setAttribute('stroke-width', '1');
                    line.setAttribute('stroke-dasharray', '5,5');
                    
                    svg.appendChild(line);
                    connection.appendChild(svg);
                    seoContainer.appendChild(connection);
                    
                    connections.push({
                        element: connection,
                        obj1: obj1,
                        obj2: obj2
                    });
                }
            }
        }
        return connections;
    }
    
    // Создаем соединения
    let connections = createConnections();
    
    // Анимационный цикл
    function animate() {
        seoObjects.forEach(obj => obj.updatePosition());
        
        // Обновляем соединения
        connections.forEach(conn => {
            const obj1 = conn.obj1;
            const obj2 = conn.obj2;
            const distance = Math.sqrt(
                Math.pow(obj1.x - obj2.x, 2) + Math.pow(obj1.y - obj2.y, 2)
            );
            
            if (distance < 200) {
                conn.element.style.left = Math.min(obj1.x, obj2.x) + 'px';
                conn.element.style.top = Math.min(obj1.y, obj2.y) + 'px';
                conn.element.style.width = Math.abs(obj1.x - obj2.x) + 'px';
                conn.element.style.height = Math.abs(obj1.y - obj2.y) + 'px';
                conn.element.style.opacity = '1';
                
                // Обновляем SVG линию
                const line = conn.element.querySelector('line');
                if (line) {
                    line.setAttribute('x1', obj1.x - Math.min(obj1.x, obj2.x));
                    line.setAttribute('y1', obj1.y - Math.min(obj1.y, obj2.y));
                    line.setAttribute('x2', obj2.x - Math.min(obj1.x, obj2.x));
                    line.setAttribute('y2', obj2.y - Math.min(obj1.y, obj2.y));
                }
            } else {
                conn.element.style.opacity = '0';
            }
        });
        
        requestAnimationFrame(animate);
    }
    
    // Запускаем анимацию
    animate();
    
    // Обработка изменения размера окна
    window.addEventListener('resize', function() {
        // Обновляем размер контейнера
        updateContainerSize();
        
        seoObjects.forEach(obj => {
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
