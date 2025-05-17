// Función para mostrar y ocultar la sidebar
document.addEventListener('DOMContentLoaded', function() {
    // Agregar botón toggle para la sidebar si no existe
    if (!document.querySelector('.sidebar-toggle')) {
        const toggleButton = document.createElement('button');
        toggleButton.className = 'sidebar-toggle';
        toggleButton.innerHTML = '<i class="fas fa-bars"></i>'; // Usa Font Awesome o agrega el icono que prefieras
        document.body.appendChild(toggleButton);
        
        // Evento para el botón toggle
        toggleButton.addEventListener('click', function() {
            document.querySelector('.sidebar').classList.toggle('sidebar-visible');
            document.querySelector('.content').classList.toggle('content-shifted');
        });
    }
    
    // Cerrar sidebar al hacer clic en un enlace (en dispositivos móviles)
    const sidebarLinks = document.querySelectorAll('.sidebar .nav-link');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth < 992) {
                document.querySelector('.sidebar').classList.remove('sidebar-visible');
                document.querySelector('.content').classList.remove('content-shifted');
            }
        });
    });
    
    // Cerrar sidebar al hacer clic fuera de ella
    document.addEventListener('click', function(event) {
        const sidebar = document.querySelector('.sidebar');
        const toggleButton = document.querySelector('.sidebar-toggle');
        
        if (sidebar.classList.contains('sidebar-visible') && 
            !sidebar.contains(event.target) && 
            event.target !== toggleButton &&
            !toggleButton.contains(event.target)) {
            sidebar.classList.remove('sidebar-visible');
            document.querySelector('.content').classList.remove('content-shifted');
        }
    });
});