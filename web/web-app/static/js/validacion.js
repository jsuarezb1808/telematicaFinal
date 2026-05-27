// Validación del formulario de registro
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    const errorMessage = document.getElementById('errorMessage');
    const submitBtn = document.getElementById('submitBtn');

    // Validar formulario antes de enviar
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Limpiar mensajes anteriores
        errorMessage.textContent = '';
        errorMessage.classList.remove('show');
        
        // Resetear estilos de error
        document.querySelectorAll('.form-group').forEach(group => {
            group.classList.remove('form-error');
        });

        // Validaciones
        const nombre = document.getElementById('nombre');
        const comuna = document.getElementById('comuna');
        const fecha = document.getElementById('fecha');
        const carrera = document.querySelector('input[name="carrera"]:checked');

        let errors = [];

        // Validar nombre
        if (!nombre.value.trim()) {
            errors.push('Name is required');
            nombre.parentElement.classList.add('form-error');
        } else if (nombre.value.trim().length < 3) {
            errors.push('Name must be at least 3 characters');
            nombre.parentElement.classList.add('form-error');
        }

        // Validar comuna
        if (!comuna.value) {
            errors.push('You must select a zone');
            comuna.parentElement.classList.add('form-error');
        }

        // Validar fecha
        if (!fecha.value) {
            errors.push('Registration date is required');
            fecha.parentElement.classList.add('form-error');
        } else {
            const selectedDate = new Date(fecha.value);
            const today = new Date();
            if (selectedDate > today) {
                errors.push('Registration date cannot be in the future');
                fecha.parentElement.classList.add('form-error');
            }
        }

        // Validar carrera
        if (!carrera) {
            errors.push('You must select a career');
            document.querySelectorAll('input[name="carrera"]').forEach(input => {
                input.parentElement.parentElement.classList.add('form-error');
            });
        }

        // Mostrar errores o enviar formulario
        if (errors.length > 0) {
            errorMessage.innerHTML = '<i class="fas fa-exclamation-circle"></i> ' + errors.join('<br>');
            errorMessage.classList.add('show');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
            // Desabilitar botón y mostrar loading
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="loading-spinner"></span><span id="submitText">Registering...</span>';
            
            // Enviar formulario
            form.submit();
        }
    });

    // Limpiar errores cuando el usuario cambia los campos
    document.querySelectorAll('.form-control, .form-select, input[type="radio"]').forEach(field => {
        field.addEventListener('change', function() {
            this.closest('.form-group')?.classList.remove('form-error');
            if (document.querySelectorAll('.form-group.form-error').length === 0) {
                errorMessage.classList.remove('show');
            }
        });

        field.addEventListener('blur', function() {
            // Validar mientras se escribe
            if (this.id === 'nombre') {
                if (this.value.trim() && this.value.trim().length >= 3) {
                    this.closest('.form-group')?.classList.remove('form-error');
                }
            }
        });
    });

    // Permitir solo letras y espacios en el campo nombre
    document.getElementById('nombre').addEventListener('input', function(e) {
        this.value = this.value.replace(/[^a-zA-Z\s\u00E1\u00E9\u00ED\u00F3\u00FA\u00C1\u00C9\u00CD\u00D3\u00DA\u00F1\u00D1]/g, '');
    });

    // Formatear fecha automáticamente
    document.getElementById('fecha').addEventListener('blur', function() {
        if (this.value) {
            const date = new Date(this.value);
            if (!isNaN(date.getTime())) {
                const formattedDate = date.toISOString().split('T')[0];
                this.value = formattedDate;
            }
        }
    });
});
