/**
 * KRONOFLUX - WebGL 3D Engine
 * Аналог движка Кроно от Артемия Лебедева
 * Полноценный 3D движок с Three.js, шейдерами и scroll-based анимациями
 */

class KronoFlux {
  constructor(options = {}) {
    this.canvas = options.canvas || document.getElementById('webgl-canvas');
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.clock = new THREE.Clock();
    this.objects = [];
    this.animations = [];
    this.mouseX = 0;
    this.mouseY = 0;
    this.scrollY = 0;
    this.targetScrollY = 0;
    this.time = 0;
    
    // FPS counter
    this.fps = 60;
    this.lastTime = performance.now();
    this.frames = 0;
    
    this.init();
  }

  init() {
    this.setupScene();
    this.setupCamera();
    this.setupRenderer();
    this.setupLights();
    this.setupControls();
    this.setupPostProcessing();
    this.addEventListeners();
    this.animate();
  }

  setupScene() {
    this.scene = new THREE.Scene();
    this.scene.fog = new THREE.Fog(0x000000, 10, 50);
  }

  setupCamera() {
    this.camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    this.camera.position.z = 5;
  }

  setupRenderer() {
    this.renderer = new THREE.WebGLRenderer({
      canvas: this.canvas,
      antialias: true,
      alpha: true
    });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1;
  }

  setupLights() {
    // Ambient light
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    this.scene.add(ambientLight);

    // Directional light
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 5, 5);
    this.scene.add(directionalLight);

    // Point lights для эффекта
    const pointLight1 = new THREE.PointLight(0x6366f1, 2, 50);
    pointLight1.position.set(-10, 5, -5);
    this.scene.add(pointLight1);

    const pointLight2 = new THREE.PointLight(0xec4899, 2, 50);
    pointLight2.position.set(10, -5, -5);
    this.scene.add(pointLight2);

    const pointLight3 = new THREE.PointLight(0x14b8a6, 2, 50);
    pointLight3.position.set(0, 0, 10);
    this.scene.add(pointLight3);
  }

  setupControls() {
    // Mouse movement влияет на камеру
    document.addEventListener('mousemove', (e) => {
      this.mouseX = (e.clientX / window.innerWidth) * 2 - 1;
      this.mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
    });

    // Scroll для анимаций
    window.addEventListener('scroll', () => {
      this.targetScrollY = window.scrollY;
    });
  }

  setupPostProcessing() {
    // Можно добавить EffectComposer для постобработки
    // Bloom, glitch, film grain и т.д.
  }

  addEventListeners() {
    window.addEventListener('resize', () => this.onResize());
  }

  onResize() {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }

  // Создание 3D объектов
  createTorus(options = {}) {
    const geometry = new THREE.TorusGeometry(
      options.radius || 1,
      options.tube || 0.4,
      options.radialSegments || 16,
      options.tubularSegments || 100
    );
    
    const material = new THREE.MeshStandardMaterial({
      color: options.color || 0x6366f1,
      metalness: 0.8,
      roughness: 0.2,
      wireframe: options.wireframe || false
    });

    const torus = new THREE.Mesh(geometry, material);
    torus.position.set(
      options.x || 0,
      options.y || 0,
      options.z || 0
    );
    
    this.scene.add(torus);
    this.objects.push({ mesh: torus, type: 'torus', options });
    return torus;
  }

  createSphere(options = {}) {
    const geometry = new THREE.SphereGeometry(
      options.radius || 1,
      options.widthSegments || 32,
      options.heightSegments || 32
    );

    const material = new THREE.MeshStandardMaterial({
      color: options.color || 0xec4899,
      metalness: 0.9,
      roughness: 0.1,
      wireframe: options.wireframe || false
    });

    const sphere = new THREE.Mesh(geometry, material);
    sphere.position.set(
      options.x || 0,
      options.y || 0,
      options.z || 0
    );

    this.scene.add(sphere);
    this.objects.push({ mesh: sphere, type: 'sphere', options });
    return sphere;
  }

  createBox(options = {}) {
    const geometry = new THREE.BoxGeometry(
      options.width || 1,
      options.height || 1,
      options.depth || 1
    );

    const material = new THREE.MeshStandardMaterial({
      color: options.color || 0x14b8a6,
      metalness: 0.7,
      roughness: 0.3,
      wireframe: options.wireframe || false
    });

    const box = new THREE.Mesh(geometry, material);
    box.position.set(
      options.x || 0,
      options.y || 0,
      options.z || 0
    );

    this.scene.add(box);
    this.objects.push({ mesh: box, type: 'box', options });
    return box;
  }

  // Создание кастомного шейдерного материала
  createShaderMaterial(vertexShader, fragmentShader, uniforms = {}) {
    return new THREE.ShaderMaterial({
      vertexShader,
      fragmentShader,
      uniforms: {
        time: { value: 0 },
        ...uniforms
      }
    });
  }

  // Система частиц
  createParticleSystem(count = 1000, options = {}) {
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);

    for (let i = 0; i < count * 3; i += 3) {
      positions[i] = (Math.random() - 0.5) * 20;
      positions[i + 1] = (Math.random() - 0.5) * 20;
      positions[i + 2] = (Math.random() - 0.5) * 20;

      colors[i] = Math.random();
      colors[i + 1] = Math.random();
      colors[i + 2] = Math.random();
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: options.size || 0.05,
      vertexColors: true,
      transparent: true,
      opacity: options.opacity || 0.8,
      blending: THREE.AdditiveBlending
    });

    const particles = new THREE.Points(geometry, material);
    this.scene.add(particles);
    this.objects.push({ mesh: particles, type: 'particles', options });
    return particles;
  }

  // Создание плоскости с шейдером
  createShaderPlane(options = {}) {
    const geometry = new THREE.PlaneGeometry(
      options.width || 2,
      options.height || 2,
      options.widthSegments || 32,
      options.heightSegments || 32
    );

    const vertexShader = options.vertexShader || `
      varying vec2 vUv;
      varying vec3 vPosition;
      uniform float time;
      
      void main() {
        vUv = uv;
        vPosition = position;
        
        vec3 pos = position;
        float wave = sin(pos.x * 2.0 + time) * cos(pos.y * 2.0 + time) * 0.2;
        pos.z += wave;
        
        gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
      }
    `;

    const fragmentShader = options.fragmentShader || `
      varying vec2 vUv;
      varying vec3 vPosition;
      uniform float time;
      
      void main() {
        vec3 color1 = vec3(0.39, 0.40, 0.95); // #6366f1
        vec3 color2 = vec3(0.93, 0.28, 0.60); // #ec4899
        
        float gradient = sin(vUv.x * 3.14159 + time * 0.5) * 0.5 + 0.5;
        vec3 color = mix(color1, color2, gradient);
        
        gl_FragColor = vec4(color, 1.0);
      }
    `;

    const material = this.createShaderMaterial(vertexShader, fragmentShader);
    const plane = new THREE.Mesh(geometry, material);
    
    plane.position.set(
      options.x || 0,
      options.y || 0,
      options.z || 0
    );

    this.scene.add(plane);
    this.objects.push({ mesh: plane, type: 'shaderPlane', options, material });
    return plane;
  }

  // Анимация объектов на основе скролла
  animateOnScroll(mesh, scrollStart, scrollEnd, animation) {
    this.animations.push({
      mesh,
      scrollStart,
      scrollEnd,
      animation
    });
  }

  // Обновление анимаций
  updateAnimations() {
    const progress = this.scrollY / (document.body.scrollHeight - window.innerHeight);
    
    this.animations.forEach(({ mesh, scrollStart, scrollEnd, animation }) => {
      const scrollProgress = (this.scrollY - scrollStart) / (scrollEnd - scrollStart);
      const clampedProgress = Math.max(0, Math.min(1, scrollProgress));
      
      animation(mesh, clampedProgress, this.scrollY);
    });
  }

  // FPS счётчик
  updateFPS() {
    this.frames++;
    const now = performance.now();
    
    if (now >= this.lastTime + 1000) {
      this.fps = Math.round((this.frames * 1000) / (now - this.lastTime));
      this.frames = 0;
      this.lastTime = now;
      
      const fpsCounter = document.getElementById('fps-counter');
      if (fpsCounter) {
        fpsCounter.textContent = `FPS: ${this.fps}`;
      }
    }
  }

  // Главный цикл анимации
  animate() {
    requestAnimationFrame(() => this.animate());

    const delta = this.clock.getDelta();
    this.time += delta;

    // Плавный скролл
    this.scrollY += (this.targetScrollY - this.scrollY) * 0.05;

    // Движение камеры от мыши
    this.camera.position.x += (this.mouseX * 0.5 - this.camera.position.x) * 0.05;
    this.camera.position.y += (this.mouseY * 0.5 - this.camera.position.y) * 0.05;
    this.camera.lookAt(this.scene.position);

    // Обновление всех объектов
    this.objects.forEach(obj => {
      if (obj.mesh.rotation) {
        obj.mesh.rotation.x += 0.001;
        obj.mesh.rotation.y += 0.002;
      }

      // Обновление шейдеров
      if (obj.material && obj.material.uniforms && obj.material.uniforms.time) {
        obj.material.uniforms.time.value = this.time;
      }
    });

    // Обновление scroll-based анимаций
    this.updateAnimations();

    // FPS
    this.updateFPS();

    // Рендер
    this.renderer.render(this.scene, this.camera);
  }

  // Утилиты
  lerp(start, end, t) {
    return start * (1 - t) + end * t;
  }

  easeInOutCubic(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }
}

// Глобальный экземпляр
let kronoflux = null;

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { KronoFlux };
}


