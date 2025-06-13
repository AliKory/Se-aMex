document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const hamburger = document.querySelector('.hamburger');
    const navItems = document.querySelector('.nav-items');
    const currentPage = window.location.pathname.split('/').pop() || 'inicio.html';
    
    // Marcar página activa
    document.querySelectorAll('.nav-link').forEach(link => {
        const linkPage = link.getAttribute('href').split('/').pop();
        if (linkPage === currentPage) {
            link.classList.add('active');
        }
    });
    
    // Toggle del menú hamburguesa
    hamburger.addEventListener('click', function() {
        this.classList.toggle('active');
        navItems.classList.toggle('active');
    });
    
    // Cerrar menú al hacer clic en un enlace (solo mobile)
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                hamburger.classList.remove('active');
                navItems.classList.remove('active');
            }
        });
    });
    
    // Ajustar hero height (manteniendo tu función original)
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