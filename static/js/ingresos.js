document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.getElementById('incomeCategory');
    const categoryModal = document.getElementById('categoryModal');
    const categoryList = document.getElementById('categoryList');

    function handleDeleteCategory(event) {
        event.preventDefault();
        const categoryId = this.getAttribute('data-category-id');

        if (confirm('¿Está seguro de que desea eliminar esta categoría?')) {
            fetch(`/categorias/eliminar/${categoryId}`, { // La URL DE TU RUTA DELETE
                method: 'DELETE',
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const optionToRemove = categorySelect.querySelector(`option[value="${categoryId}"]`);
                    if (optionToRemove) {
                        optionToRemove.remove();
                    }
                    this.closest('li').remove();
                    alert(data.message);
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error al eliminar categoría:', error);
                alert('Ocurrió un error al eliminar la categoría. Intente de nuevo.');
            });
        }
    }

    categoryModal.addEventListener('show.bs.modal', function () {
        document.querySelectorAll('#categoryList .btn-delete-category').forEach(button => {
            button.removeEventListener('click', handleDeleteCategory);
            button.addEventListener('click', handleDeleteCategory);
        });
    });

    // ... (Tu lógica para añadir categorías, quizás también usando fetch) ...
});