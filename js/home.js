document.addEventListener('DOMContentLoaded', function() {
    // Menú hamburguesa
    const hamburger = document.createElement('div');
    hamburger.className = 'hamburger';
    hamburger.innerHTML = `
        <span></span>
        <span></span>
        <span></span>
    `;
    
    const navbar = document.querySelector('.container_navbar');
    const navItems = document.querySelector('.nav-items');
    
    // Insertar hamburguesa antes de los nav-items
    navbar.insertBefore(hamburger, navItems);
    
    // Toggle del menú
    hamburger.addEventListener('click', function() {
        this.classList.toggle('active');
        navItems.classList.toggle('active');
    });
    
    // Cerrar menú al hacer clic en un enlace
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function() {
            hamburger.classList.remove('active');
            navItems.classList.remove('active');
        });
    });
    
    // Ajustar altura del hero section
    function adjustHeroHeight() {
        const hero = document.querySelector('.hero');
        if (window.innerWidth >= 820 && window.innerWidth <= 1180) {
            hero.style.minHeight = 'calc(100vh - 120px)';
        } else {
            hero.style.minHeight = '';
        }
    }
    
    // Ejecutar al cargar y al redimensionar
    adjustHeroHeight();
    window.addEventListener('resize', adjustHeroHeight);
});