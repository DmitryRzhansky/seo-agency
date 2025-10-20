// Простая анимация "Паутина данных" для SEO-агентства
document.addEventListener('DOMContentLoaded', function() {
    // Создаем контейнер для анимации
    const dataContainer = document.createElement('div');
    dataContainer.id = 'seo-animation-container';
    dataContainer.style.cssText = `
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
    
    document.body.appendChild(dataContainer);

    // Сеть отключена — работаем только с крупными плавными точками
    
    // Обновляем размер контейнера
    function updateContainerSize() {
        dataContainer.style.width = window.innerWidth + 'px';
        dataContainer.style.height = window.innerHeight + 'px';
        dataContainer.style.minHeight = window.innerHeight + 'px';
    }
    
    updateContainerSize();
    
    // Массив для хранения узлов
    const dataNodes = [];
    // Соединения не используются
    
    // Класс для узлов данных
    class DataNode {
        constructor() {
            this.element = document.createElement('div');
            this.x = Math.random() * window.innerWidth;
            this.y = Math.random() * window.innerHeight;
            this.vx = (Math.random() - 0.5) * 0.12; // немного быстрее движение
            this.vy = (Math.random() - 0.5) * 0.12;
            this.size = Math.random() * 170 + 100; // 100-270px — крупнее точки
            this.opacity = Math.random() * 0.2 + 0.15; // 0.15-0.35 — мягкая видимость
            this.pulsePhase = Math.random() * Math.PI * 2;
            this.pulseSpeed = Math.random() * 0.02 + 0.01;
            
            this.createElement();
            this.updatePosition();
            dataContainer.appendChild(this.element);
        }
        
        createElement() {
            this.element.className = 'data-node';
            this.element.style.cssText = `
                position: absolute;
                left: ${this.x}px;
                top: ${this.y}px;
                width: ${this.size}px;
                height: ${this.size}px;
                background: radial-gradient(circle, rgba(13, 110, 253, 0.9) 0%, rgba(13, 110, 253, 0.5) 50%, rgba(13, 110, 253, 0.15) 80%, transparent 100%);
                border-radius: 50%;
                box-shadow: 0 0 ${Math.round(this.size * 0.8)}px rgba(13, 110, 253, 0.35), 0 0 ${Math.round(this.size * 1.4)}px rgba(13, 110, 253, 0.2);
                opacity: ${this.opacity};
                transition: none;
            `;
        }
        
        updatePosition() {
            // Легкая случайность для плавного дрейфа
            this.vx += (Math.random() - 0.5) * 0.003;
            this.vy += (Math.random() - 0.5) * 0.003;
            const maxV = 0.18;
            if (this.vx > maxV) this.vx = maxV; if (this.vx < -maxV) this.vx = -maxV;
            if (this.vy > maxV) this.vy = maxV; if (this.vy < -maxV) this.vy = -maxV;

            this.x += this.vx;
            this.y += this.vy;
            
            // Пульсация
            this.pulsePhase += this.pulseSpeed;
            const pulse = Math.sin(this.pulsePhase) * 0.2 + 1;
            
            // Проверяем границы экрана с учетом размера
            const margin = this.size * 0.5;
            if (this.x < -margin) this.x = window.innerWidth + margin;
            if (this.x > window.innerWidth + margin) this.x = -margin;
            if (this.y < -margin) this.y = window.innerHeight + margin;
            if (this.y > window.innerHeight + margin) this.y = -margin;
            
            // Обновляем позицию
            this.element.style.left = this.x + 'px';
            this.element.style.top = this.y + 'px';
            this.element.style.transform = `scale(${pulse})`;
        }
    }
    
    // Создаем немного крупных узлов
    const nodeCount = Math.max(6, Math.min(10, Math.floor(window.innerWidth / 300)));
    for (let i = 0; i < nodeCount; i++) {
        const node = new DataNode();
        dataNodes.push(node);
    }
    // Сети нет — соединения не создаем
    
    // Анимационный цикл
    function animate() {
        // Обновляем позиции узлов
        dataNodes.forEach(node => node.updatePosition());
        
        // Соединений нет
        
        // Пересоздавать нечего
        
        requestAnimationFrame(animate);
    }
    
    // Запускаем анимацию
    animate();
    
    // Обработка изменения размера окна
    window.addEventListener('resize', function() {
        updateContainerSize();
        // Пересчитываем позиции узлов
        dataNodes.forEach(node => {
            if (node.x > window.innerWidth) node.x = window.innerWidth - node.size;
            if (node.y > window.innerHeight) node.y = window.innerHeight - node.size;
        });
        // Соединения отсутствуют
    });
    
    // Пауза анимации при неактивной вкладке
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            dataNodes.forEach(node => {
                node.element.style.animationPlayState = 'paused';
            });
        } else {
            dataNodes.forEach(node => {
                node.element.style.animationPlayState = 'running';
            });
        }
    });
});