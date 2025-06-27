// JavaScript principal para Dashboards UTL

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Animaciones de entrada para las cards
    observeElements();
    
    // Configurar búsqueda en tiempo real
    setupSearch();
    
    // Manejar errores de carga de gráficos
    handleChartErrors();
});

// Observer para animaciones de entrada
function observeElements() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });
    
    document.querySelectorAll('.dashboard-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

// Configurar búsqueda mejorada
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(this.value);
            }, 300); // Debounce de 300ms
        });
    }
}

// Realizar búsqueda
function performSearch(query) {
    const dashboardCards = document.querySelectorAll('.dashboard-card');
    const noResults = document.getElementById('noResults');
    let visibleCount = 0;
    
    dashboardCards.forEach(card => {
        const name = card.getAttribute('data-name') || '';
        const description = card.getAttribute('data-description') || '';
        const category = card.getAttribute('data-category') || '';
        
        const matches = name.includes(query.toLowerCase()) || 
                       description.includes(query.toLowerCase()) ||
                       category.toLowerCase().includes(query.toLowerCase());
        
        if (matches) {
            card.style.display = 'block';
            visibleCount++;
            // Animación de aparición
            card.style.animation = 'fadeIn 0.5s ease-in-out';
        } else {
            card.style.display = 'none';
        }
    });
    
    // Mostrar/ocultar mensaje de "no resultados"
    if (noResults) {
        if (visibleCount === 0 && query.trim() !== '') {
            noResults.classList.remove('d-none');
        } else {
            noResults.classList.add('d-none');
        }
    }
}

// Manejar errores de carga de gráficos
function handleChartErrors() {
    // Verificar si Plotly está disponible
    if (typeof Plotly === 'undefined') {
        console.warn('Plotly no está cargado');
        return;
    }
    
    // Configurar gráficos responsivos
    window.addEventListener('resize', function() {
        const charts = document.querySelectorAll('.plotly-graph-div');
        charts.forEach(chart => {
            if (chart.data && chart.layout) {
                Plotly.Plots.resize(chart);
            }
        });
    });
}

// Utilidades para los dashboards
const DashboardUtils = {
    // Mostrar loading spinner
    showLoading: function(containerId) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `
                <div class="text-center p-4">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Cargando...</span>
                    </div>
                    <p class="mt-2">Cargando datos...</p>
                </div>
            `;
        }
    },
    
    // Ocultar loading spinner
    hideLoading: function(containerId) {
        const spinner = document.querySelector(`#${containerId} .spinner-border`);
        if (spinner) {
            spinner.closest('.text-center').remove();
        }
    },
    
    // Mostrar mensaje de error
    showError: function(containerId, message) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    <i class="fas fa-exclamation-triangle"></i>
                    <strong>Error:</strong> ${message}
                </div>
            `;
        }
    },
    
    // Formatear números
    formatNumber: function(num) {
        return new Intl.NumberFormat('es-MX').format(num);
    },
    
    // Formatear porcentajes
    formatPercentage: function(num) {
        return new Intl.NumberFormat('es-MX', {
            style: 'percent',
            minimumFractionDigits: 1
        }).format(num / 100);
    },
    
    // Formatear fechas
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat('es-MX', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(date);
    }
};

// Funciones para filtros avanzados
const FilterManager = {
    // Aplicar múltiples filtros
    applyFilters: function(filters) {
        const cards = document.querySelectorAll('.dashboard-card');
        let visibleCount = 0;
        
        cards.forEach(card => {
            let shouldShow = true;
            
            // Aplicar cada filtro
            Object.keys(filters).forEach(filterKey => {
                const filterValue = filters[filterKey];
                if (filterValue && shouldShow) {
                    const cardValue = card.getAttribute(`data-${filterKey}`);
                    if (cardValue !== filterValue) {
                        shouldShow = false;
                    }
                }
            });
            
            if (shouldShow) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        return visibleCount;
    },
    
    // Limpiar todos los filtros
    clearAllFilters: function() {
        const cards = document.querySelectorAll('.dashboard-card');
        cards.forEach(card => {
            card.style.display = 'block';
        });
        
        // Limpiar campos de filtro
        const filterInputs = document.querySelectorAll('.filter-input');
        filterInputs.forEach(input => {
            input.value = '';
        });
    }
};

// Funciones para exportación de datos
const ExportManager = {
    // Exportar datos a CSV
    exportToCSV: function(data, filename) {
        const csv = this.convertToCSV(data);
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        
        if (link.download !== undefined) {
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            link.setAttribute('download', filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    },
    
    // Convertir datos a formato CSV
    convertToCSV: function(data) {
        if (!data || data.length === 0) return '';
        
        const headers = Object.keys(data[0]);
        const csvContent = [
            headers.join(','),
            ...data.map(row => 
                headers.map(header => {
                    const value = row[header];
                    // Escapar comillas y comas
                    return typeof value === 'string' && (value.includes(',') || value.includes('"'))
                        ? `"${value.replace(/"/g, '""')}"` 
                        : value;
                }).join(',')
            )
        ].join('\n');
        
        return csvContent;
    }
};

// Hacer las utilidades disponibles globalmente
window.DashboardUtils = DashboardUtils;
window.FilterManager = FilterManager;
window.ExportManager = ExportManager;