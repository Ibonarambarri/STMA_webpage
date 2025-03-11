// main.js

document.addEventListener('DOMContentLoaded', function() {
    // Añadir clase activa a la navegación según la página actual
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentLocation ||
            (href !== '/' && currentLocation.startsWith(href))) {
            link.classList.add('active');
        }
    });

    // Inicializar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Animaciones al hacer scroll
    const animateElements = document.querySelectorAll('.animate-on-scroll');

    if (animateElements.length > 0) {
        // Función para verificar si un elemento está en el viewport
        function isInViewport(el) {
            const rect = el.getBoundingClientRect();
            return (
                rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.bottom >= 0
            );
        }

        // Inicialmente, verificar elementos visibles
        animateElements.forEach(el => {
            if (isInViewport(el)) {
                el.classList.add('animate-fade-in');
            }
        });

        // Escuchar el evento scroll
        window.addEventListener('scroll', function() {
            animateElements.forEach(el => {
                if (isInViewport(el) && !el.classList.contains('animate-fade-in')) {
                    el.classList.add('animate-fade-in');
                }
            });
        });
    }

    // Validación personalizada del formulario de contacto
    const contactForm = document.querySelector('#contactForm');

    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            const nombre = document.querySelector('#nombre').value.trim();
            const email = document.querySelector('#email').value.trim();
            const asunto = document.querySelector('#asunto').value.trim();
            const mensaje = document.querySelector('#mensaje').value.trim();
            const privacidad = document.querySelector('#privacidad').checked;

            let isValid = true;

            // Validar campos requeridos
            if (!nombre || !email || !asunto || !mensaje || !privacidad) {
                isValid = false;
                alert('Por favor, completa todos los campos obligatorios.');
            }

            // Validar formato de email
            const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;

            if (!emailRegex.test(email)) {
                isValid = false;
                alert('Por favor, introduce un email válido.');
            }

            if (!isValid) {
                event.preventDefault();
            }
        });
    }

    // Mostrar detalles de proyectos en modal
    const projectLinks = document.querySelectorAll('.project-modal-link');

    if (projectLinks.length > 0) {
        projectLinks.forEach(link => {
            link.addEventListener('click', function(event) {
                event.preventDefault();

                const projectId = this.getAttribute('data-project-id');
                const modalTitle = document.querySelector('#projectModalLabel');
                const modalBody = document.querySelector('#projectModalBody');

                // Aquí normalmente harías una petición AJAX para obtener los detalles del proyecto
                // Por simplicidad, usamos los datos que ya tenemos en la página
                const projectTitle = this.closest('.card').querySelector('.card-title').textContent;
                const projectDesc = this.closest('.card').querySelector('.card-text').textContent;

                modalTitle.textContent = projectTitle;
                modalBody.innerHTML = `<p>${projectDesc}</p>`;

                const projectModal = new bootstrap.Modal(document.getElementById('projectModal'));
                projectModal.show();
            });
        });
    }

    // Contador de estadísticas animado
    const statCounters = document.querySelectorAll('.stat-counter');

    if (statCounters.length > 0) {
        // Función para animar contadores
        function animateCounter(counter) {
            const target = parseInt(counter.getAttribute('data-target'));
            const duration = 2000; // duración en milisegundos
            const step = Math.ceil(target / (duration / 16)); // 60fps aproximadamente

            let current = 0;
            const timer = setInterval(() => {
                current += step;
                if (current >= target) {
                    clearInterval(timer);
                    counter.textContent = target;
                } else {
                    counter.textContent = current;
                }
            }, 16);
        }

        // Observador de intersección para iniciar animación cuando sea visible
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        statCounters.forEach(counter => {
            observer.observe(counter);
        });
    }
});

// Función para mostrar la barra de progreso mientras se envía el formulario
function mostrarProgreso() {
    document.getElementById('form-progress').style.display = 'block';
    document.getElementById('submit-button').disabled = true;
}

// Función para volver al inicio de la página suavemente
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}