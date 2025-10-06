// static/js/nueva_meta.js

document.addEventListener('DOMContentLoaded', function () {
    const newMetaForm = document.getElementById('newMetaForm');
    const alertContainer = document.getElementById('meta-alert-container');

    // Función para mostrar alertas de Bootstrap
    function showAlert(message, type = 'success') {
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        alertContainer.innerHTML = alertHtml;
        // Opcional: desaparecer la alerta después de unos segundos
        setTimeout(() => {
            const currentAlert = alertContainer.querySelector('.alert');
            if (currentAlert) {
                new bootstrap.Alert(currentAlert).close();
            }
        }, 5000); // 5 segundos
    }



    if (newMetaForm) {
        newMetaForm.addEventListener('submit', function (event) {
            event.preventDefault(); // ¡Detener el envío normal del formulario!

            const formData = new FormData(newMetaForm); // Capturar todos los datos del formulario

            // Convierte FormData a un objeto de URLSearchParams si tu Flask espera application/x-www-form-urlencoded
            const params = new URLSearchParams();
            for (const pair of formData) {
                params.append(pair[0], pair[1]);
            }

            fetch(newMetaForm.action, { // Usar la URL definida en el 'action' del formulario
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: params // Enviar los datos del formulario
            })
            .then(response => {
                // Verificar si la respuesta fue exitosa (status 2xx)
                if (!response.ok) {
                    // Si no es OK, intenta leer el error del JSON
                    return response.json().then(err => {
                        throw new Error(err.message || 'Error desconocido del servidor.');
                    });
                }
                return response.json(); // Si es OK, parsear el JSON
            })
            .then(data => {
                if (data.success) {
                    showAlert(data.message, 'success');
                    newMetaForm.reset(); // Limpiar el formulario
                    // Opcional: redirigir a la página de metas después de un éxito
                    // setTimeout(() => {
                    //     window.location.href = '{{ url_for("metas") }}'; // Redirigir a la lista de metas
                    // }, 2000);
                } else {
                    showAlert('Error: ' + (data.message || 'No se pudo crear la meta.'), 'danger');
                }
            })
            .catch(error => {
                console.error('Error al crear la meta:', error);
                showAlert('Ocurrió un error al crear la meta: ' + error.message, 'danger');
            });
        });
    }

    // Opcional: establecer la fecha de creación por defecto a hoy
    const fechaCreacionInput = document.getElementById('fechaCreacion');
    if (fechaCreacionInput && !fechaCreacionInput.value) {
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0'); // Enero es 0
        const dd = String(today.getDate()).padStart(2, '0');
        fechaCreacionInput.value = `${yyyy}-${mm}-${dd}`;
    }
});