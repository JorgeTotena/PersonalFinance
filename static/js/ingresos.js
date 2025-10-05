document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.getElementById('incomeCategory'); // ID corregido para el select principal
    const categoryModal = document.getElementById('categoryModal');
    const categoryList = document.getElementById('categoryList');

    // --- NUEVAS REFERENCIAS PARA EL FORMULARIO DE AÑADIR CATEGORÍA DE INGRESOS ---
    const addIncomeCategoryForm = document.getElementById('addIncomeCategoryForm'); // Capturar el formulario
    const newCategoryInput = document.getElementById('newCategoryInput'); // Capturar el input de nueva categoría
    // --- FIN NUEVAS REFERENCIAS ---


    // --- Funciones Auxiliares (Asegurarse de que tienen nombres únicos si los tienes en otros JS) ---
    function addOptionToSelect(id, nombre) {
        const newOption = new Option(nombre, id); // Usamos el ID como valor, el nombre como texto
        categorySelect.add(newOption);
        categorySelect.value = id; // Opcional: seleccionar la nueva categoría automáticamente
    }

    function addToList(id, nombre) {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.textContent = nombre;

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'btn btn-danger btn-sm btn-delete-category';
        deleteBtn.innerHTML = '<i class="fas fa-trash-alt"></i>';
        deleteBtn.setAttribute('data-category-id', id);
        deleteBtn.addEventListener('click', handleDeleteCategory); // Asignar el evento

        li.appendChild(deleteBtn);
        categoryList.appendChild(li);
    }
    // --- Fin Funciones Auxiliares ---


    // --- Lógica para AÑADIR CATEGORÍA (NUEVA PARTE) ---
    if (addIncomeCategoryForm) {
        addIncomeCategoryForm.addEventListener('submit', function (event) {
            event.preventDefault(); // ¡PREVENIR EL ENVÍO NORMAL DEL FORMULARIO!

            const newCategoryName = newCategoryInput.value.trim();

            if (newCategoryName) {
                const url = addIncomeCategoryForm.action; // Obtener la URL del atributo action del formulario

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded', // Necesario para FormData si no usas FormData directamente
                    },
                    body: new URLSearchParams({ // Construye el cuerpo como un formulario URL-encoded
                        'nombre': newCategoryName
                    })
                })
                .then(response => {
                    // Si la respuesta no es OK (ej. 409 Conflict, 400 Bad Request)
                    if (!response.ok) {
                        return response.json().then(err => {
                            throw new Error(err.message || 'Error desconocido al añadir categoría de ingreso.');
                        });
                    }
                    return response.json(); // Parsea la respuesta JSON
                })
                .then(data => {
                    if (data.success) {
                        alert(data.message);
                        addOptionToSelect(data.category.id, data.category.nombre); // Añadir al select principal
                        addToList(data.category.id, data.category.nombre);         // Añadir a la lista del modal
                        newCategoryInput.value = ''; // Limpiar el input

                        // Opcional: Cerrar el modal después de añadir
                        // const modalInstance = bootstrap.Modal.getInstance(categoryModal);
                        // if (modalInstance) modalInstance.hide();

                        // Recargar la página para que el select principal de ingresos se actualice completamente
                        window.location.reload();

                    } else {
                        alert('Error: ' + (data.message || 'No se pudo añadir la categoría de ingreso.'));
                    }
                })
                .catch(error => {
                    console.error('Error al añadir categoría de ingreso:', error);
                    alert('Ocurrió un error al añadir la categoría de ingreso: ' + error.message);
                });
            } else {
                alert('Por favor, ingrese un nombre para la categoría de ingreso.');
            }
        });
    }
    // --- FIN Lógica para AÑADIR CATEGORÍA ---


    // --- Lógica para ELIMINAR CATEGORÍA (esta ya la tenías, solo ajusto referencias) ---
    function handleDeleteCategory(event) {
        event.preventDefault();
        const categoryId = this.getAttribute('data-category-id');

        if (confirm('¿Está seguro de que desea eliminar esta categoría? Esto también eliminará los ingresos asociados.')) {
            fetch(`/categorias/eliminar/${categoryId}`, { // La URL DE TU RUTA DELETE
                method: 'DELETE',
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.message || 'Error desconocido al eliminar categoría.'); });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Eliminar del SELECT principal del formulario de ingresos
                    // IMPORTANTE: Si tu option value es el ID, esto funciona. Si es el nombre, tendrías que buscar por nombre.
                    const optionToRemove = categorySelect.querySelector(`option[value="${categoryId}"]`);
                    if (optionToRemove) {
                        optionToRemove.remove();
                    }
                    // Eliminar del LISTADO del modal
                    this.closest('li').remove();
                    alert(data.message);
                } else {
                    alert('Error: ' + (data.message || 'No se pudo eliminar la categoría.'));
                }
            })
            .catch(error => {
                console.error('Error al eliminar categoría:', error);
                alert('Ocurrió un error al eliminar la categoría. Intente de nuevo.');
            });
        }
    }

    // Al abrir el modal, asegurar que los botones de eliminar tienen el listener
    if (categoryModal) {
        categoryModal.addEventListener('show.bs.modal', function () {
            document.querySelectorAll('#categoryList .btn-delete-category').forEach(button => {
                button.removeEventListener('click', handleDeleteCategory); // Prevenir listeners duplicados
                button.addEventListener('click', handleDeleteCategory);
            });
        });
    }
});