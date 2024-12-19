// Dashboard initialization
document.addEventListener('DOMContentLoaded', function () {
    // Initialize search functionality
    const searchInput = document.querySelector('.search-bar input');
    if (searchInput) {
        searchInput.addEventListener('input', handleSearch);
    }

    // Initialize action buttons
    const createAgentBtn = document.querySelector('.action-card:nth-child(1) .action-button');
    const editAgentBtn = document.getElementById('editAgentBtn');

    if (createAgentBtn) {
        createAgentBtn.addEventListener('click', () => {
            window.location.href = '/edit-agent';
        });
    }

    if (editAgentBtn) {
        editAgentBtn.addEventListener('click', () => {
            window.location.href = '/edit-agent';
        });
    }
});

// Handle search input
function handleSearch(e) {
    const searchTerm = e.target.value.toLowerCase();
    // TODO: Implement search functionality
    console.log('Searching for:', searchTerm);
} 