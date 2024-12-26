let searchTimeout;

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('results-container');
    const paginationContainer = document.getElementById('pagination-container');

    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            clearTimeout(searchTimeout);
            
            searchTimeout = setTimeout(() => {
                const searchQuery = e.target.value;
                performSearch(searchQuery);
            }, 300); // Délai de 300ms pour éviter trop de requêtes
        });
    }

    function performSearch(query) {
        fetch(`/api/search/?search=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = data.html;
                updatePagination(data);
            })
            .catch(error => console.error('Erreur:', error));
    }

    function updatePagination(data) {
        if (data.total_pages <= 1) {
            paginationContainer.style.display = 'none';
            return;
        }

        paginationContainer.style.display = 'flex';
        // Mise à jour de la pagination...
    }
});