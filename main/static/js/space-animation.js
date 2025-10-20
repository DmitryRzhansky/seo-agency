// Анимация "Паутина данных" для SEO-агентства
document.addEventListener('DOMContentLoaded', function() {
    // Создаем контейнер для анимации (сохраняем все важные настройки)
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
    
    // Добавляем контейнер в body
    document.body.appendChild(dataContainer);
    
    // Убеждаемся, что контейнер занимает всю область экрана
    function updateContainerSize() {
        dataContainer.style.width = window.innerWidth + 'px';
        dataContainer.style.height = window.innerHeight + 'px';
        dataContainer.style.minHeight = window.innerHeight + 'px';
    }
    
    // Обновляем размер при загрузке
    updateContainerSize();
    
    // Массив для хранения узлов данных
    const dataNodes = [];
    const connections = [];
    
    // Класс для узлов данных
    class DataNode {
        constructor() {
            this.element = document.createElement('div');
            this.x = Math.random() * window.innerWidth;
            this.y = Math.random() * window.innerHeight;
            this.vx = (Math.random() - 0.5) * 0.3; // медленное движение
            this.vy = (Math.random() - 0.5) * 0.3;
            this.size = Math.random() * 8 + 4; // 4-12px
            this.opacity = Math.random() * 0.4 + 0.2; // 0.2-0.6
            this.pulsePhase = Math.random() * Math.PI * 2;
            this.pulseSpeed = Math.random() * 0.02 + 0.01;
            this.glowIntensity = Math.random() * 0.5 + 0.3;
            
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
                background: radial-gradient(circle, rgba(13, 110, 253, 0.8) 0%, rgba(13, 110, 253, 0.3) 50%, transparent 100%);
                border-radius: 50%;
                box-shadow: 0 0 ${this.size * 2}px rgba(13, 110, 253, ${this.glowIntensity});
                opacity: ${this.opacity};
                transition: none;
            `;
        }
        
        updatePosition() {
            // Медленное дрейфование
            this.x += this.vx;
            this.y += this.vy;
            
            // Пульсация
            this.pulsePhase += this.pulseSpeed;
            const pulse = Math.sin(this.pulsePhase) * 0.2 + 1;
            
            // Проверяем границы экрана
            if (this.x < 0) this.x = window.innerWidth;
            if (this.x > window.innerWidth) this.x = 0;
            if (this.y < 0) this.y = window.innerHeight;
            if (this.y > window.innerHeight) this.y = 0;
            
            // Обновляем позицию
            this.element.style.left = this.x + 'px';
            this.element.style.top = this.y + 'px';
            this.element.style.transform = `scale(${pulse})`;
        }
    }
    
    // Создаем узлы данных
    const nodeCount = Math.min(25, Math.floor(window.innerWidth / 100));
    for (let i = 0; i < nodeCount; i++) {
        const node = new DataNode();
        dataNodes.push(node);
    }
    
    // Создаем соединения между узлами
    function createConnections() {
        // Очищаем старые соединения
        connections.forEach(conn => {
            if (conn.element && conn.element.parentNode) {
                conn.element.parentNode.removeChild(conn.element);
            }
        });
        connections.length = 0;
        
        // Создаем новые соединения
        for (let i = 0; i < dataNodes.length; i++) {
            for (let j = i + 1; j < dataNodes.length; j++) {
                const node1 = dataNodes[i];
                const node2 = dataNodes[j];
                const distance = Math.sqrt(
                    Math.pow(node1.x - node2.x, 2) + Math.pow(node1.y - node2.y, 2)
                );
                
                // Создаем соединение если узлы близко
                if (distance < 150 && Math.random() < 0.4) {
                    const connection = document.createElement('div');
                    connection.className = 'data-connection';
                    
                    // Создаем SVG линию
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
                    line.setAttribute('x1', node1.x);
                    line.setAttribute('y1', node1.y);
                    line.setAttribute('x2', node2.x);
                    line.setAttribute('y2', node2.y);
                    
                    // Стиль линии зависит от расстояния
                    const opacity = Math.max(0, 1 - (distance / 150));
                    if (distance < 80) {
                        line.setAttribute('stroke', `rgba(13, 110, 253, ${0.6 * opacity})`);
                        line.setAttribute('stroke-width', '2');
                        line.setAttribute('stroke-dasharray', '2,4');
                    } else {
                        line.setAttribute('stroke', `rgba(13, 110, 253, ${0.3 * opacity})`);
                        line.setAttribute('stroke-width', '1');
                        line.setAttribute('stroke-dasharray', '5,10');
                    }
                    
                    svg.appendChild(line);
                    connection.appendChild(svg);
                    dataContainer.appendChild(connection);
                    
                    connections.push({
                        element: connection,
                        svg: svg,
                        line: line,
                        node1: node1,
                        node2: node2,
                        distance: distance
                    });
                }
            }
        }
    }
    
    // Создаем начальные соединения
    createConnections();
    
    // Анимационный цикл
    function animate() {
        // Обновляем позиции узлов
        dataNodes.forEach(node => node.updatePosition());
        
        // Обновляем соединения
        connections.forEach(conn => {
            const node1 = conn.node1;
            const node2 = conn.node2;
            const distance = Math.sqrt(
                Math.pow(node1.x - node2.x, 2) + Math.pow(node1.y - node2.y, 2)
            );
            
            if (distance < 150) {
                // Обновляем позиции линии
                conn.line.setAttribute('x1', node1.x);
                conn.line.setAttribute('y1', node1.y);
                conn.line.setAttribute('x2', node2.x);
                conn.line.setAttribute('y2', node2.y);
                
                // Обновляем прозрачность
                const opacity = Math.max(0, 1 - (distance / 150));
                if (distance < 80) {
                    conn.line.setAttribute('stroke', `rgba(13, 110, 253, ${0.6 * opacity})`);
                } else {
                    conn.line.setAttribute('stroke', `rgba(13, 110, 253, ${0.3 * opacity})`);
                }
            } else {
                // Скрываем соединение если узлы далеко
                conn.element.style.opacity = '0';
            }
        });
        
        // Периодически пересоздаем соединения для динамичности
        if (Math.random() < 0.001) {
            createConnections();
        }
        
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
        
        // Пересоздаем соединения
        createConnections();
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