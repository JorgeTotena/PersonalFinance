// static/js/movimientos.js

document.addEventListener('DOMContentLoaded', function () {
    // Obtenemos las referencias a los elementos de filtro y la tabla
    const searchInput = document.getElementById('searchInput');
    const typeFilter = document.getElementById('typeFilter');
    const monthFilter = document.getElementById('monthFilter');
    const tableBody = document.querySelector('#movementsTable tbody');
    const tableRows = tableBody.querySelectorAll('tr:not(#no-results-row)'); // Todas las filas de datos
    const noResultsRow = document.getElementById('no-results-row');

    // Función principal que aplica todos los filtros
    function applyFilters() {
        const searchTerm = searchInput.value.toLowerCase();
        const typeValue = typeFilter.value;
        const monthValue = monthFilter.value; // Formato YYYY-MM

        let visibleRows = 0;

        // Recorremos cada fila de la tabla para decidir si mostrarla u ocultarla
        tableRows.forEach(row => {
            const description = row.cells[1].textContent.toLowerCase();
            const rowType = row.dataset.type;
            const rowDate = row.dataset.date.substring(0, 7); // Obtenemos YYYY-MM de la fecha de la fila

            // Condiciones de visibilidad
            const matchesSearch = description.includes(searchTerm);
            const matchesType = typeValue === 'all' || rowType === typeValue;
            const matchesMonth = monthValue === '' || rowDate === monthValue;

            // Si la fila cumple todas las condiciones, se muestra. Si no, se oculta.
            if (matchesSearch && matchesType && matchesMonth) {
                row.style.display = ''; // Muestra la fila
                visibleRows++;
            } else {
                row.style.display = 'none'; // Oculta la fila
            }
        });

        // Muestra u oculta el mensaje de "no hay resultados"
        if (visibleRows === 0) {
            noResultsRow.style.display = '';
        } else {
            noResultsRow.style.display = 'none';
        }
    }

    // Añadimos "escuchadores" de eventos a los filtros.
    // Cada vez que el usuario interactúa con un filtro, se llama a la función applyFilters.
    searchInput.addEventListener('keyup', applyFilters);
    typeFilter.addEventListener('change', applyFilters);
    monthFilter.addEventListener('change', applyFilters);
});
