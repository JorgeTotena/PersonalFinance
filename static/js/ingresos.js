// static/js/ingresos.js

document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.getElementById('incomeCategory');
    const categoryModal = document.getElementById('categoryModal');
    const newCategoryInput = document.getElementById('newCategoryInput');
    const addCategoryBtn = document.getElementById('addCategoryBtn');
    const categoryList = document.getElementById('categoryList');
    const categoryForm = newCategoryInput.closest('form'); // Obtener el formulario

    // Función para renderizar la lista de categorías en el modal
    function renderCategoryList() {
        categoryList.innerHTML = ''; // Limpiar la lista
        const options = Array.from(categorySelect.options);

        options.forEach(option => {
            if (option.value) {
                const li = document.createElement('li');
                li.className = 'list-group-item';
                li.textContent = option.textContent;

                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'btn btn-danger btn-sm btn-delete-category';
                deleteBtn.innerHTML = '<i class="fas fa-trash-alt"></i>';
                deleteBtn.onclick = function() {
                    option.remove(); // Eliminar del select
                    li.remove();     // Eliminar de la lista del modal
                    // Opcional: Enviar solicitud al servidor para eliminar la categoría
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
    addCategoryBtn.addEventListener('click', function (event) {
        event.preventDefault(); // Evitar el envío inmediato del formulario
        const newCategoryName = newCategoryInput.value.trim();

        if (newCategoryName) {
            // Crear la nueva opción para el select
            const newOption = new Option(newCategoryName, newCategoryName);
            categorySelect.add(newOption);

            // Actualizar la lista en el modal
            renderCategoryList();

            // Enviar el formulario al servidor
            categoryForm.submit();
        } else {
            alert('Por favor, ingrese un nombre para la categoría.');
        }
    });
});