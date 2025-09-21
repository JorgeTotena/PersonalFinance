// static/js/egresos.js

document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.getElementById('expenseCategory'); // ID del select de categorías de egreso
    const categoryModal = document.getElementById('categoryModal');   // El modal
    const newCategoryInput = document.getElementById('newCategoryInput');
    const addCategoryForm = document.getElementById('addCategoryForm'); // ¡Ahora sí con el ID correcto!
    const categoryList = document.getElementById('categoryList');     // Lista de categorías existentes

    // --- Funciones Auxiliares ---

    // Añade una opción al select principal del formulario de egresos
    function addOptionToSelect(id, nombre) {
        const newOption = new Option(nombre, id);
        categorySelect.add(newOption);
        categorySelect.value = id; // Seleccionar la nueva categoría automáticamente
    }

    // Añade un elemento a la lista de categorías dentro del modal
    function addToList(id, nombre) {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.textContent = nombre;

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'btn btn-danger btn-sm btn-delete-category';
        deleteBtn.innerHTML = '<i class="fas fa-trash-alt"></i>';
        deleteBtn.setAttribute('data-category-id', id); // Guardar el ID para eliminar
        // Asignar el evento click al botón de eliminar
        deleteBtn.addEventListener('click', handleDeleteCategory);

        li.appendChild(deleteBtn);
        categoryList.appendChild(li);
    }

    // --- Lógica para Añadir Categoría (dentro del Modal) ---

    if (addCategoryForm) { // Asegurarse de que el formulario existe
        addCategoryForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Detener el envío normal del formulario

            const newCategoryName = newCategoryInput.value.trim();

            if (newCategoryName) {
                // La URL de acción para añadir categorías de egreso.
                // Flask automáticamente genera la URL, no necesitas {{ url_for(...) }} aquí.
                // Es mejor dejar el action del form en HTML con url_for y en JS leerlo:
                const url = addCategoryForm.action; // Lee el action del formulario HTML

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({
                        'nombre': newCategoryName
                    })
                })
                .then(response => {
                    // Si la respuesta no es OK (ej. 409 Conflict por categoría existente)
                    if (!response.ok) {
                        // Intentar leer el error del JSON
                        return response.json().then(err => { throw new Error(err.message || 'Error desconocido al añadir categoría.'); });
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        addOptionToSelect(data.category.id, data.category.nombre); // Añadir al select
                        addToList(data.category.id, data.category.nombre);         // Añadir a la lista del modal
                        newCategoryInput.value = ''; // Limpiar el input
                        alert(data.message);
                    } else {
                        // Esto debería ser capturado por el !response.ok anterior, pero como fallback
                        alert('Error: ' + (data.message || 'No se pudo añadir la categoría.'));
                    }
                })
                .catch(error => {
                    console.error('Error al añadir categoría de egreso:', error);
                    alert('Ocurrió un error al añadir la categoría de egreso: ' + error.message);
                });
            } else {
                alert('Por favor, ingrese un nombre para la categoría de egreso.');
            }
        });
    }

    // --- Lógica para Eliminar Categoría (dentro del Modal) ---

    function handleDeleteCategory(event) {
        event.preventDefault();
        const categoryId = this.getAttribute('data-category-id');

        if (confirm('¿Está seguro de que desea eliminar esta categoría? Esto también eliminará los egresos asociados.')) {
            fetch(`/categorias/eliminar/${categoryId}`, { // Asegúrate de que esta ruta en Flask acepta DELETE
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
                    // Eliminar del SELECT principal del formulario de egresos
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
                console.error('Error al eliminar categoría de egreso:', error);
                alert('Ocurrió un error al eliminar la categoría de egreso: ' + error.message);
            });
        }
    }

    // Al abrir el modal, asegurar que los botones de eliminar tienen el listener
    if (categoryModal) {
        categoryModal.addEventListener('show.bs.modal', function () {
            document.querySelectorAll('#categoryList .btn-delete-category').forEach(button => {
                button.removeEventListener('click', handleDeleteCategory);
                button.addEventListener('click', handleDeleteCategory);
            });
        });
    }
});