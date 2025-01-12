document.addEventListener('DOMContentLoaded', function () {
    const cardsContainer = document.getElementById('cardsContainer');
    const searchInput = document.getElementById('assistantSearch');
    const prevPageBtn = document.getElementById('prevPage');
    const nextPageBtn = document.getElementById('nextPage');
    const pageInfo = document.getElementById('pageInfo');
    const loadingMessage = document.getElementById('loadingMessage');

    let allAssistants = [];
    let currentPage = 1;
    const itemsPerPage = 8;
    let filteredAssistants = [];

    // Fetch assistants from the server
    async function fetchAssistants() {
        try {
            const response = await fetch('/agents');
            const data = await response.json();
            if (data.success) {
                console.log('Fetched assistants:', data.agents);
                // Filter assistants by subtype and sort alphabetically by name
                allAssistants = data.agents
                    .filter(assistant =>
                        assistant.subtype === 'VisitAssist' ||
                        assistant.subtype === 'GuestAssist'
                    )
                    .sort((a, b) => (a.assistant_name || '').localeCompare(b.assistant_name || ''));

                filteredAssistants = [...allAssistants];
                updateDisplay();
            } else {
                console.error('Error fetching assistants:', data.message);
                cardsContainer.innerHTML = '<p class="error-message">Unable to load assistants. Please try again later.</p>';
            }
        } catch (error) {
            console.error('Error fetching assistants:', error);
            cardsContainer.innerHTML = '<p class="error-message">Unable to load assistants. Please try again later.</p>';
        }
    }

    // Create assistant card HTML
    function createAssistantCard(assistant) {
        const baseUrl = 'https://apis-ia-app-28obw.ondigitalocean.app';
        const cdnBaseUrl = 'https://apis-ia.nyc3.digitaloceanspaces.com/static/images/assistant_imgs';
        const encodedName = encodeURIComponent(assistant.assistant_name || '');
        const encodedType = encodeURIComponent(assistant.assistant_type || 'classic');
        const url = `${baseUrl}/${assistant.assistant_id}?assistant_name=${encodedName}&type=${encodedType}&default_language=en`;

        // Construct full image URL using CDN
        const imageUrl = assistant.assistant_img ? `${cdnBaseUrl}/${assistant.assistant_img}` : '';

        const imageHtml = imageUrl ?
            `<img src="${imageUrl}" alt="${assistant.assistant_name || 'Assistant'}" onerror="this.parentElement.innerHTML='<div class=\'image-placeholder\'><i class=\'fas fa-robot\'></i></div>'">` :
            `<div class="image-placeholder"><i class="fas fa-robot"></i></div>`;

        return `
            <div class="assistant-card">
                <div class="assistant-image">
                    ${imageHtml}
                </div>
                <div class="assistant-content">
                    <h3>${assistant.assistant_name || 'Unnamed Assistant'}</h3>
                    <p>${assistant.assistant_desc || 'No description available'}</p>
                    <a href="${url}" target="_blank" class="assistant-link">
                        Open Assistant <i class="fas fa-external-link-alt"></i>
                    </a>
                </div>
            </div>
        `;
    }

    // Update display with current page of assistants
    function updateDisplay() {
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        const pageAssistants = filteredAssistants.slice(startIndex, endIndex);

        // Remove loading message if it exists
        if (loadingMessage) {
            loadingMessage.style.display = 'none';
        }

        if (pageAssistants.length === 0) {
            cardsContainer.innerHTML = '<p class="no-results">No assistants found.</p>';
        } else {
            // Update cards
            cardsContainer.innerHTML = pageAssistants.map(createAssistantCard).join('');
        }

        // Update pagination
        const totalPages = Math.ceil(filteredAssistants.length / itemsPerPage);
        pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;

        // Update button states
        prevPageBtn.disabled = currentPage === 1;
        nextPageBtn.disabled = currentPage === totalPages;
    }

    // Handle search input
    searchInput.addEventListener('input', function (e) {
        const searchTerm = e.target.value.toLowerCase();
        filteredAssistants = allAssistants.filter(assistant =>
            (assistant.assistant_name || '').toLowerCase().includes(searchTerm) ||
            (assistant.assistant_desc || '').toLowerCase().includes(searchTerm)
        );
        currentPage = 1;
        updateDisplay();
    });

    // Handle pagination
    prevPageBtn.addEventListener('click', function () {
        if (currentPage > 1) {
            currentPage--;
            updateDisplay();
        }
    });

    nextPageBtn.addEventListener('click', function () {
        const totalPages = Math.ceil(filteredAssistants.length / itemsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            updateDisplay();
        }
    });

    // Initial fetch
    fetchAssistants();
}); 