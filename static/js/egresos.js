// static/js/egresos.js

document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.getElementById('expenseCategory');
    const categoryModal = document.getElementById('categoryModal');
    const newCategoryInput = document.getElementById('newCategoryInput');
    const addCategoryBtn = document.getElementById('addCategoryBtn');
    const categoryList = document.getElementById('categoryList');

    // Función para renderizar la lista de categorías en el modal
    function renderCategoryList() {
        // Limpiamos la lista actual para evitar duplicados
        categoryList.innerHTML = '';

        // Obtenemos todas las opciones del select principal
        const options = Array.from(categorySelect.options);

        options.forEach(option => {
            // Ignoramos la primera opción ("Selecciona una categoría...")
            if (option.value) {
                const li = document.createElement('li');
                li.className = 'list-group-item';
                li.textContent = option.textContent;

                // Botón para eliminar (funcionalidad futura)
                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'btn btn-danger btn-sm btn-delete-category';
                deleteBtn.innerHTML = '<i class="fas fa-trash-alt"></i>';
                deleteBtn.onclick = function() {
                    // Lógica para eliminar la categoría (tanto del modal como del select)
                    option.remove(); // Elimina del select
                    li.remove();     // Elimina de la lista del modal
                };

                li.appendChild(deleteBtn);
                categoryList.appendChild(li);
            }
        });
    }

    // Evento que se dispara cuando el modal de categorías se abre
    categoryModal.addEventListener('show.bs.modal', function () {
        renderCategoryList();
    });

    // Evento para el botón de añadir nueva categoría
    addCategoryBtn.addEventListener('click', function () {
        const newCategoryName = newCategoryInput.value.trim();

        if (newCategoryName) {
            // Crear la nueva opción para el select
            const newOption = new Option(newCategoryName, newCategoryName);
            categorySelect.add(newOption);

            // Limpiar el input
            newCategoryInput.value = '';

            // Actualizar la lista en el modal
            renderCategoryList();
        }
    });
});
