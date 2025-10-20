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
            const types = ['mandala', 'crystal', 'nebula', 'quantum', 'fractal', 'torus', 'helix', 'lattice', 'molecule', 'galaxy', 'vortex', 'prism'];
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
                case 'mandala':
                    this.createMandala();
                    break;
                case 'crystal':
                    this.createCrystal();
                    break;
                case 'nebula':
                    this.createNebula();
                    break;
                case 'quantum':
                    this.createQuantum();
                    break;
                case 'fractal':
                    this.createFractal();
                    break;
                case 'torus':
                    this.createTorus();
                    break;
                case 'helix':
                    this.createHelix();
                    break;
                case 'lattice':
                    this.createLattice();
                    break;
                case 'molecule':
                    this.createMolecule();
                    break;
                case 'galaxy':
                    this.createGalaxy();
                    break;
                case 'vortex':
                    this.createVortex();
                    break;
                case 'prism':
                    this.createPrism();
                    break;
            }
        }
        
        createMandala() {
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
                    position: relative;
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                ">
                    <div style="
                        position: absolute;
                        top: 20%;
                        left: 20%;
                        width: 60%;
                        height: 60%;
                        background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
                        border-radius: 50%;
                        clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
                    "></div>
                    <div style="
                        position: absolute;
                        top: 35%;
                        left: 35%;
                        width: 30%;
                        height: 30%;
                        background: radial-gradient(circle, rgba(255,255,255,0.5) 0%, transparent 70%);
                        border-radius: 50%;
                    "></div>
                </div>
            `;
        }
        
        createCrystal() {
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
                    clip-path: polygon(50% 0%, 100% 25%, 75% 100%, 25% 100%, 0% 25%);
                    position: relative;
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                ">
                    <div style="
                        position: absolute;
                        top: 20%;
                        left: 20%;
                        width: 60%;
                        height: 60%;
                        background: linear-gradient(45deg, rgba(255,255,255,0.4) 0%, transparent 50%);
                        clip-path: polygon(50% 0%, 100% 25%, 75% 100%, 25% 100%, 0% 25%);
                    "></div>
                </div>
            `;
        }
        
        createNebula() {
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
                    position: relative;
                    filter: blur(1px);
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                ">
                    <div style="
                        position: absolute;
                        top: 10%;
                        left: 10%;
                        width: 80%;
                        height: 80%;
                        background: radial-gradient(ellipse, rgba(255,255,255,0.3) 0%, transparent 70%);
                        border-radius: 50%;
                    "></div>
                    <div style="
                        position: absolute;
                        top: 30%;
                        left: 30%;
                        width: 40%;
                        height: 40%;
                        background: radial-gradient(circle, rgba(255,255,255,0.5) 0%, transparent 60%);
                        border-radius: 50%;
                    "></div>
                </div>
            `;
        }
        
        createQuantum() {
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
                    position: relative;
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                ">
                    <div style="
                        position: absolute;
                        top: 25%;
                        left: 25%;
                        width: 50%;
                        height: 50%;
                        background: radial-gradient(circle, rgba(255,255,255,0.6) 0%, transparent 70%);
                        border-radius: 50%;
                        clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
                    "></div>
                    <div style="
                        position: absolute;
                        top: 0%;
                        left: 0%;
                        width: 100%;
                        height: 100%;
                        background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.2) 0%, transparent 50%);
                        border-radius: 50%;
                    "></div>
                </div>
            `;
        }
        
        createFractal() {
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
                    clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
                    position: relative;
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                ">
                    <div style="
                        position: absolute;
                        top: 20%;
                        left: 20%;
                        width: 60%;
                        height: 60%;
                        background: linear-gradient(45deg, rgba(255,255,255,0.4) 0%, transparent 50%);
                        clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
                    "></div>
                    <div style="
                        position: absolute;
                        top: 40%;
                        left: 40%;
                        width: 20%;
                        height: 20%;
                        background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%);
                        border-radius: 50%;
                    "></div>
                </div>
            `;
        }
        
        createTorus() {
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
                    position: relative;
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                ">
                    <div style="
                        position: absolute;
                        top: 20%;
                        left: 20%;
                        width: 60%;
                        height: 60%;
                        background: transparent;
                        border: 3px solid rgba(255,255,255,0.6);
                        border-radius: 50%;
                    "></div>
                    <div style="
                        position: absolute;
                        top: 35%;
                        left: 35%;
                        width: 30%;
                        height: 30%;
                        background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
                        border-radius: 50%;
                    "></div>
                </div>
            `;
        }
        
        createHelix() {
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
                    position: relative;
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                ">
                    <div style="
                        position: absolute;
                        top: 15%;
                        left: 15%;
                        width: 70%;
                        height: 70%;
                        background: linear-gradient(45deg, rgba(255,255,255,0.3) 0%, transparent 50%);
                        border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
                    "></div>
                    <div style="
                        position: absolute;
                        top: 30%;
                        left: 30%;
                        width: 40%;
                        height: 40%;
                        background: radial-gradient(circle, rgba(255,255,255,0.5) 0%, transparent 70%);
                        border-radius: 50%;
                    "></div>
                </div>
            `;
        }
        
        createLattice() {
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
                    position: relative;
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                ">
                    <div style="
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background: linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px),
                                    linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px);
                        background-size: 20px 20px;
                    "></div>
                    <div style="
                        position: absolute;
                        top: 25%;
                        left: 25%;
                        width: 50%;
                        height: 50%;
                        background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
                        border-radius: 50%;
                    "></div>
                </div>
            `;
        }
        
        createMolecule() {
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
                    position: relative;
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                ">
                    <div style="
                        position: absolute;
                        top: 20%;
                        left: 20%;
                        width: 60%;
                        height: 60%;
                        background: radial-gradient(circle, rgba(255,255,255,0.4) 0%, transparent 70%);
                        border-radius: 50%;
                    "></div>
                    <div style="
                        position: absolute;
                        top: 10%;
                        left: 10%;
                        width: 20%;
                        height: 20%;
                        background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%);
                        border-radius: 50%;
                    "></div>
                    <div style="
                        position: absolute;
                        top: 70%;
                        left: 70%;
                        width: 20%;
                        height: 20%;
                        background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%);
                        border-radius: 50%;
                    "></div>
                    <div style="
                        position: absolute;
                        top: 10%;
                        left: 70%;
                        width: 20%;
                        height: 20%;
                        background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%);
                        border-radius: 50%;
                    "></div>
                    <div style="
                        position: absolute;
                        top: 70%;
                        left: 10%;
                        width: 20%;
                        height: 20%;
                        background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%);
                        border-radius: 50%;
                    "></div>
                </div>
            `;
        }
        
        createGalaxy() {
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
                    position: relative;
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                ">
                    <div style="
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background: radial-gradient(ellipse at 30% 30%, rgba(255,255,255,0.3) 0%, transparent 50%);
                        border-radius: 50%;
                    "></div>
                    <div style="
                        position: absolute;
                        top: 20%;
                        left: 20%;
                        width: 60%;
                        height: 60%;
                        background: radial-gradient(ellipse at 70% 70%, rgba(255,255,255,0.2) 0%, transparent 60%);
                        border-radius: 50%;
                    "></div>
                    <div style="
                        position: absolute;
                        top: 40%;
                        left: 40%;
                        width: 20%;
                        height: 20%;
                        background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%);
                        border-radius: 50%;
                    "></div>
                </div>
            `;
        }
        
        createVortex() {
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
                    position: relative;
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                ">
                    <div style="
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background: conic-gradient(from 0deg, rgba(255,255,255,0.3) 0%, transparent 50%, rgba(255,255,255,0.3) 100%);
                        border-radius: 50%;
                    "></div>
                    <div style="
                        position: absolute;
                        top: 30%;
                        left: 30%;
                        width: 40%;
                        height: 40%;
                        background: radial-gradient(circle, rgba(255,255,255,0.6) 0%, transparent 70%);
                        border-radius: 50%;
                    "></div>
                </div>
            `;
        }
        
        createPrism() {
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
                    clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
                    position: relative;
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
                ">
                    <div style="
                        position: absolute;
                        top: 20%;
                        left: 20%;
                        width: 60%;
                        height: 60%;
                        background: linear-gradient(45deg, rgba(255,255,255,0.4) 0%, transparent 50%);
                        clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
                    "></div>
                    <div style="
                        position: absolute;
                        top: 40%;
                        left: 40%;
                        width: 20%;
                        height: 20%;
                        background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%);
                        border-radius: 50%;
                    "></div>
                </div>
            `;
        }
        
        updatePosition() {
            // Магнитные взаимодействия с другими объектами
            let magneticForceX = 0;
            let magneticForceY = 0;
            
            seoObjects.forEach(other => {
                if (other !== this) {
                    const dx = other.x - this.x;
                    const dy = other.y - this.y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    
                    if (distance < 150 && distance > 0) {
                        // Притяжение на близком расстоянии
                        const force = (150 - distance) / 150 * 0.02;
                        magneticForceX += (dx / distance) * force;
                        magneticForceY += (dy / distance) * force;
                    } else if (distance < 50 && distance > 0) {
                        // Отталкивание на очень близком расстоянии
                        const force = (50 - distance) / 50 * 0.05;
                        magneticForceX -= (dx / distance) * force;
                        magneticForceY -= (dy / distance) * force;
                    }
                }
            });
            
            // Применяем магнитные силы
            this.vx += magneticForceX;
            this.vy += magneticForceY;
            
            // Ограничиваем скорость
            const maxSpeed = 1;
            const speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
            if (speed > maxSpeed) {
                this.vx = (this.vx / speed) * maxSpeed;
                this.vy = (this.vy / speed) * maxSpeed;
            }
            
            // Добавляем небольшое случайное движение
            this.vx += (Math.random() - 0.5) * 0.01;
            this.vy += (Math.random() - 0.5) * 0.01;
            
            // Обновляем позицию
            this.x += this.vx;
            this.y += this.vy;
            this.rotation += this.rotationSpeed;
            
            // Пульсация с реакцией на соседей
            this.pulsePhase += this.pulseSpeed;
            let pulse = Math.sin(this.pulsePhase) * 0.1 + 1;
            
            // Усиливаем пульсацию при приближении к другим объектам
            const nearbyObjects = seoObjects.filter(other => {
                if (other === this) return false;
                const dx = other.x - this.x;
                const dy = other.y - this.y;
                return Math.sqrt(dx * dx + dy * dy) < 100;
            });
            
            if (nearbyObjects.length > 0) {
                pulse += nearbyObjects.length * 0.05;
            }
            
            // Проверяем границы экрана с затуханием
            if (this.x < -this.size) {
                this.x = window.innerWidth;
                this.vx *= 0.8;
            }
            if (this.x > window.innerWidth) {
                this.x = -this.size;
                this.vx *= 0.8;
            }
            if (this.y < -this.size) {
                this.y = window.innerHeight;
                this.vy *= 0.8;
            }
            if (this.y > window.innerHeight) {
                this.y = -this.size;
                this.vy *= 0.8;
            }
            
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
        const maxConnections = Math.min(seoObjects.length * 2, 30); // Ограничиваем количество соединений
        let connectionCount = 0;
        
        for (let i = 0; i < seoObjects.length && connectionCount < maxConnections; i++) {
            for (let j = i + 1; j < seoObjects.length && connectionCount < maxConnections; j++) {
                const obj1 = seoObjects[i];
                const obj2 = seoObjects[j];
                const distance = Math.sqrt(
                    Math.pow(obj1.x - obj2.x, 2) + Math.pow(obj1.y - obj2.y, 2)
                );
                
                // Создаем соединение если объекты близко
                if (distance < 180 && Math.random() < 0.4) {
                    const connection = document.createElement('div');
                    connection.className = 'seo-connection';
                    connection.style.cssText = `
                        position: absolute;
                        left: ${Math.min(obj1.x, obj2.x)}px;
                        top: ${Math.min(obj1.y, obj2.y)}px;
                        width: ${Math.abs(obj1.x - obj2.x)}px;
                        height: ${Math.abs(obj1.y - obj2.y)}px;
                        pointer-events: none;
                        z-index: -1;
                        transition: opacity 0.3s ease;
                        opacity: 0;
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
                    
                    // Разные стили соединений в зависимости от расстояния
                    if (distance < 100) {
                        line.setAttribute('stroke', 'rgba(13, 110, 253, 0.6)');
                        line.setAttribute('stroke-width', '2');
                        line.setAttribute('stroke-dasharray', '3,3');
                    } else {
                        line.setAttribute('stroke', 'rgba(13, 110, 253, 0.3)');
                        line.setAttribute('stroke-width', '1');
                        line.setAttribute('stroke-dasharray', '8,4');
                    }
                    
                    svg.appendChild(line);
                    connection.appendChild(svg);
                    seoContainer.appendChild(connection);
                    
                    connections.push({
                        element: connection,
                        obj1: obj1,
                        obj2: obj2,
                        line: line,
                        distance: distance
                    });
                    
                    connectionCount++;
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
            
            if (distance < 180) {
                conn.element.style.left = Math.min(obj1.x, obj2.x) + 'px';
                conn.element.style.top = Math.min(obj1.y, obj2.y) + 'px';
                conn.element.style.width = Math.abs(obj1.x - obj2.x) + 'px';
                conn.element.style.height = Math.abs(obj1.y - obj2.y) + 'px';
                
                // Плавное появление соединения
                const opacity = Math.max(0, 1 - (distance / 180));
                conn.element.style.opacity = opacity;
                
                // Обновляем SVG линию
                if (conn.line) {
                    conn.line.setAttribute('x1', obj1.x - Math.min(obj1.x, obj2.x));
                    conn.line.setAttribute('y1', obj1.y - Math.min(obj1.y, obj2.y));
                    conn.line.setAttribute('x2', obj2.x - Math.min(obj1.x, obj2.x));
                    conn.line.setAttribute('y2', obj2.y - Math.min(obj1.y, obj2.y));
                    
                    // Обновляем стиль линии в зависимости от расстояния
                    if (distance < 100) {
                        conn.line.setAttribute('stroke', `rgba(13, 110, 253, ${0.6 * opacity})`);
                        conn.line.setAttribute('stroke-width', '2');
                        conn.line.setAttribute('stroke-dasharray', '3,3');
                    } else {
                        conn.line.setAttribute('stroke', `rgba(13, 110, 253, ${0.3 * opacity})`);
                        conn.line.setAttribute('stroke-width', '1');
                        conn.line.setAttribute('stroke-dasharray', '8,4');
                    }
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
