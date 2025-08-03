// static/js/dashboard.js

// Espera a que el contenido del DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function () {

    // --- GRÁFICO DE GASTOS ---
    // Busca el elemento canvas en el HTML
    const ctx = document.getElementById('expenseChart');

    // Si el elemento existe, crea el gráfico
    if (ctx) {
        new Chart(ctx, {
            type: 'doughnut', // Tipo de gráfico (dona)
            data: {
                // Etiquetas para cada sección del gráfico
                labels: ['Comida', 'Transporte', 'Servicios', 'Ocio', 'Hogar'],
                datasets: [{
                    label: 'Gastos del Mes',
                    // Datos de ejemplo (asegúrate que sumen el total de egresos)
                    data: [450000, 200000, 350000, 250000, 600000],
                    // Colores para cada sección
                    backgroundColor: [
                        '#FF6384', // Rojo
                        '#36A2EB', // Azul
                        '#FFCE56', // Amarillo
                        '#4BC0C0', // Turquesa
                        '#9966FF'  // Morado
                    ],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true, // Hace que el gráfico se adapte al tamaño del contenedor
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom', // Posición de la leyenda
                    }
                }
            }
        });
    }
});
