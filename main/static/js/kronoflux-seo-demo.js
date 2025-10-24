/**
 * KRONOFLUX SEO DEMO
 * 3D анимации для сайта SEO студии
 */

// Ждем загрузки DOM и Three.js
document.addEventListener('DOMContentLoaded', function() {
  // Проверяем наличие THREE.js
  if (typeof THREE === 'undefined') {
    console.error('Three.js не загружен!');
    return;
  }

  // Создаем движок KronoFlux
  kronoflux = new KronoFlux({
    canvas: document.getElementById('webgl-canvas')
  });

  // ============================================
  // СЕКЦИЯ 1: HERO - Главный тор (0-800px)
  // ============================================
  const heroTorus = kronoflux.createTorus({
    radius: 2.5,
    tube: 0.8,
    radialSegments: 16,
    tubularSegments: 100,
    color: 0x6366f1,
    x: 0,
    y: 0,
    z: -2
  });

  kronoflux.animateOnScroll(heroTorus, 0, 800, (mesh, progress) => {
    mesh.rotation.x = progress * Math.PI * 2;
    mesh.rotation.y = progress * Math.PI * 4;
    mesh.scale.set(1 - progress * 0.5, 1 - progress * 0.5, 1 - progress * 0.5);
    mesh.position.z = -2 - progress * 8;
  });

  // ============================================
  // СЕКЦИЯ 2: WHY NO CLIENTS - Орбитальные сферы (800-2000px)
  // ============================================
  const sphereCount = 8;
  const sphereRadius = 0.3;
  const orbitRadius = 4;
  const orbitalSpheres = [];

  for (let i = 0; i < sphereCount; i++) {
    const angle = (i / sphereCount) * Math.PI * 2;
    const sphere = kronoflux.createSphere({
      radius: sphereRadius,
      color: 0xec4899,
      x: Math.cos(angle) * orbitRadius,
      y: Math.sin(angle) * orbitRadius,
      z: -5,
      widthSegments: 16,
      heightSegments: 16
    });
    orbitalSpheres.push({ mesh: sphere, angle, index: i });
  }

  orbitalSpheres.forEach(({ mesh, angle, index }) => {
    kronoflux.animateOnScroll(mesh, 800, 2000, (m, progress) => {
      const time = progress * Math.PI * 2;
      const currentAngle = angle + time;
      m.position.x = Math.cos(currentAngle) * orbitRadius;
      m.position.y = Math.sin(currentAngle) * orbitRadius;
      m.position.z = -5 + Math.sin(time + index) * 2;
      
      // Пульсация
      const scale = 1 + Math.sin(time * 3 + index) * 0.3;
      m.scale.set(scale, scale, scale);
    });
  });

  // ============================================
  // СЕКЦИЯ 3: HOW WE WORK - Вращающиеся кубы (2000-3200px)
  // ============================================
  const cubes = [
    { x: -3, y: 2, color: 0x6366f1 },
    { x: 3, y: 2, color: 0xec4899 },
    { x: -3, y: -2, color: 0x14b8a6 },
    { x: 3, y: -2, color: 0xf59e0b }
  ];

  cubes.forEach(({ x, y, color }, index) => {
    const cube = kronoflux.createBox({
      width: 1.5,
      height: 1.5,
      depth: 1.5,
      color,
      x,
      y,
      z: -8
    });

    kronoflux.animateOnScroll(cube, 2000, 3200, (mesh, progress) => {
      mesh.rotation.x = progress * Math.PI * 4 + index;
      mesh.rotation.y = progress * Math.PI * 6 + index;
      mesh.rotation.z = progress * Math.PI * 2 + index;
      
      const scale = 1 + Math.sin(progress * Math.PI * 4 + index) * 0.4;
      mesh.scale.set(scale, scale, scale);
    });
  });

  // ============================================
  // СЕКЦИЯ 4: NICHES - Шейдерная плоскость (3200-4500px)
  // ============================================
  const shaderPlane = kronoflux.createShaderPlane({
    width: 8,
    height: 8,
    widthSegments: 64,
    heightSegments: 64,
    x: 0,
    y: 0,
    z: -10
  });

  kronoflux.animateOnScroll(shaderPlane, 3200, 4500, (mesh, progress) => {
    mesh.rotation.z = progress * Math.PI * 2;
    mesh.position.z = -10 + progress * 5;
  });

  // ============================================
  // СЕКЦИЯ 5: LOCATIONS - Система частиц (4500-5800px)
  // ============================================
  const particles = kronoflux.createParticleSystem(2000, {
    size: 0.06,
    opacity: 0.7
  });

  particles.position.z = -15;

  kronoflux.animateOnScroll(particles, 4500, 5800, (mesh, progress) => {
    mesh.rotation.y = progress * Math.PI * 2;
    mesh.rotation.x = Math.sin(progress * Math.PI) * 0.5;
    mesh.position.z = -15 + progress * 8;
  });

  // ============================================
  // СЕКЦИЯ 6: TARIFFS - Спираль из торов (5800-7000px)
  // ============================================
  const spiralTori = [];
  const spiralCount = 12;

  for (let i = 0; i < spiralCount; i++) {
    const t = i / spiralCount;
    const angle = t * Math.PI * 4;
    const radius = 2 + t * 3;
    const height = t * 8 - 4;

    const hue = t * 360;
    const color = new THREE.Color(`hsl(${hue}, 70%, 60%)`);

    const torus = kronoflux.createTorus({
      radius: 0.8,
      tube: 0.2,
      radialSegments: 8,
      tubularSegments: 50,
      color: color.getHex(),
      wireframe: i % 2 === 0,
      x: Math.cos(angle) * radius,
      y: height,
      z: Math.sin(angle) * radius - 20
    });

    spiralTori.push(torus);
  }

  spiralTori.forEach((torus, index) => {
    kronoflux.animateOnScroll(torus, 5800, 7000, (mesh, progress) => {
      const baseRotation = (index / spiralCount) * Math.PI * 2;
      mesh.rotation.x = baseRotation + progress * Math.PI * 4;
      mesh.rotation.y = baseRotation + progress * Math.PI * 6;
    });
  });

  // ============================================
  // СЕКЦИЯ 7: TEAM - Туннель из колец (7000-8500px)
  // ============================================
  const tunnelRings = [];
  const ringCount = 20;

  for (let i = 0; i < ringCount; i++) {
    const z = -25 - i * 2;
    const scale = 1 + i * 0.1;

    const ring = kronoflux.createTorus({
      radius: 2 * scale,
      tube: 0.3,
      radialSegments: 8,
      tubularSegments: 32,
      color: 0x6366f1,
      wireframe: true,
      x: 0,
      y: 0,
      z: z
    });

    tunnelRings.push(ring);
  }

  tunnelRings.forEach((ring, index) => {
    kronoflux.animateOnScroll(ring, 7000, 8500, (mesh, progress) => {
      mesh.rotation.z = progress * Math.PI * 2 + index * 0.2;
      mesh.position.z = -25 - index * 2 + progress * 30;
      
      // Создаем эффект бесконечного туннеля
      if (mesh.position.z > 5) {
        mesh.position.z = -25 - ringCount * 2;
      }
    });
  });

  // ============================================
  // СЕКЦИЯ 8: REVIEWS - Икосаэдры (8500-10000px)
  // ============================================
  const icosahedrons = [];
  const icoCount = 15;

  for (let i = 0; i < icoCount; i++) {
    const geometry = new THREE.IcosahedronGeometry(0.5, 0);
    const material = new THREE.MeshStandardMaterial({
      color: Math.random() * 0xffffff,
      metalness: 0.8,
      roughness: 0.2,
      wireframe: i % 3 === 0
    });

    const ico = new THREE.Mesh(geometry, material);
    ico.position.set(
      (Math.random() - 0.5) * 10,
      (Math.random() - 0.5) * 10,
      -30 + (Math.random() - 0.5) * 10
    );

    kronoflux.scene.add(ico);
    icosahedrons.push({
      mesh: ico,
      speedX: Math.random() * 0.02 - 0.01,
      speedY: Math.random() * 0.02 - 0.01,
      speedZ: Math.random() * 0.02 - 0.01
    });
  }

  icosahedrons.forEach(({ mesh, speedX, speedY, speedZ }) => {
    kronoflux.animateOnScroll(mesh, 8500, 10000, (m, progress) => {
      m.rotation.x += speedX;
      m.rotation.y += speedY;
      m.rotation.z += speedZ;
      
      // Плавающее движение
      m.position.y += Math.sin(progress * Math.PI * 4 + m.position.x) * 0.02;
    });
  });

  // ============================================
  // СЕКЦИЯ 9: CONTACT - Финальная анимация (10000+)
  // ============================================
  const finalSphere = kronoflux.createSphere({
    radius: 3,
    color: 0x6366f1,
    x: 0,
    y: 0,
    z: -40,
    widthSegments: 64,
    heightSegments: 64
  });

  kronoflux.animateOnScroll(finalSphere, 10000, 12000, (mesh, progress) => {
    mesh.rotation.y = progress * Math.PI * 4;
    mesh.position.z = -40 + progress * 35;
    
    const scale = 1 + progress * 2;
    mesh.scale.set(scale, scale, scale);
    
    // Затухание
    mesh.material.opacity = 1 - progress;
    mesh.material.transparent = true;
  });

  console.log('🚀 KronoFlux SEO Demo загружен!');
});

