document.addEventListener('DOMContentLoaded', function () {
    // DOM Elements
    const searchInput = document.getElementById('searchEvents');
    const startDateFilter = document.getElementById('startDate');
    const endDateFilter = document.getElementById('endDate');
    const venueFilter = document.getElementById('venueFilter');
    const organizerFilter = document.getElementById('organizerFilter');
    const eventsTable = document.getElementById('eventsTable');
    const loadingMessage = document.getElementById('loadingMessage');
    const eventModal = document.getElementById('eventModal');
    const eventForm = document.getElementById('eventForm');
    const createEventBtn = document.getElementById('createEventBtn');
    const closeBtn = document.querySelector('.close-btn');
    const saveBtn = document.getElementById('saveBtn');
    const cancelBtn = document.getElementById('cancelBtn');

    let currentEventId = null;

    // Load initial data
    loadEvents();

    // Event Listeners
    searchInput.addEventListener('input', debounce(filterEvents, 300));
    startDateFilter.addEventListener('change', filterEvents);
    endDateFilter.addEventListener('change', filterEvents);
    venueFilter.addEventListener('change', filterEvents);
    organizerFilter.addEventListener('change', filterEvents);
    createEventBtn.addEventListener('click', showCreateEventModal);
    closeBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);
    saveBtn.addEventListener('click', saveEvent);
    eventForm.addEventListener('submit', (e) => e.preventDefault());

    // Functions
    async function loadEvents() {
        try {
            showLoading(true);
            const response = await fetch('/api/events');
            if (!response.ok) {
                throw new Error('Failed to load events');
            }
            const events = await response.json();
            renderEvents(events);
        } catch (error) {
            console.error('Error loading events:', error);
            showError('Failed to load events');
        } finally {
            showLoading(false);
        }
    }

    function renderEvents(events) {
        const tbody = eventsTable.querySelector('tbody');
        tbody.innerHTML = '';

        if (!events.length) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td colspan="6" class="text-center">No events found</td>
            `;
            tbody.appendChild(row);
            return;
        }

        events.forEach(event => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${escapeHtml(event.title)}</td>
                <td>${formatDate(event.start_date)}</td>
                <td>${escapeHtml(event.ev_venues?.name || 'N/A')}</td>
                <td>${escapeHtml(event.ev_organizers?.name || 'N/A')}</td>
                <td>${formatPrice(event.ticket_price)}</td>
                <td class="action-buttons">
                    <button class="btn btn-primary btn-sm edit-btn" data-id="${event.event_id}">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-danger btn-sm delete-btn" data-id="${event.event_id}">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;

            // Add event listeners for edit and delete buttons
            const editBtn = row.querySelector('.edit-btn');
            const deleteBtn = row.querySelector('.delete-btn');
            editBtn.addEventListener('click', () => showEditEventModal(event.event_id));
            deleteBtn.addEventListener('click', () => deleteEvent(event.event_id));

            tbody.appendChild(row);
        });
    }

    async function filterEvents() {
        const searchTerm = searchInput.value.trim();
        const startDate = startDateFilter.value;
        const endDate = endDateFilter.value;
        const venueId = venueFilter.value;
        const organizerId = organizerFilter.value;

        try {
            showLoading(true);
            const params = new URLSearchParams();

            if (searchTerm) params.append('search', searchTerm);
            if (startDate) params.append('start_date', startDate);
            if (endDate) params.append('end_date', endDate);
            if (venueId) params.append('venue_id', venueId);
            if (organizerId) params.append('organizer_id', organizerId);

            const response = await fetch(`/api/events/search?${params}`);
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to filter events');
            }
            const events = await response.json();
            renderEvents(events);
        } catch (error) {
            console.error('Error filtering events:', error);
            showError(error.message || 'Failed to filter events');
        } finally {
            showLoading(false);
        }
    }

    function showCreateEventModal() {
        currentEventId = null;
        eventForm.reset();
        document.getElementById('modalTitle').textContent = 'Create Event';
        eventModal.style.display = 'block';
    }

    async function showEditEventModal(eventId) {
        try {
            showLoading(true);
            const response = await fetch(`/api/events/${eventId}`);
            const event = await response.json();

            currentEventId = eventId;
            document.getElementById('modalTitle').textContent = 'Edit Event';

            // Populate form fields
            eventForm.title.value = event.title;
            eventForm.description.value = event.description;
            eventForm.start_date.value = formatDateTimeForInput(event.start_date);
            eventForm.end_date.value = formatDateTimeForInput(event.end_date);
            eventForm.venue_id.value = event.venue_id;
            eventForm.organizer_id.value = event.organizer_id;
            eventForm.ticket_price.value = event.ticket_price;
            eventForm.image_url.value = event.image_url || '';

            // Handle tags
            const tagSelect = eventForm.tags;
            Array.from(tagSelect.options).forEach(option => {
                option.selected = event.tags.includes(parseInt(option.value));
            });

            eventModal.style.display = 'block';
        } catch (error) {
            console.error('Error loading event details:', error);
            showError('Failed to load event details');
        } finally {
            showLoading(false);
        }
    }

    async function saveEvent() {
        const formData = new FormData(eventForm);
        const eventData = {
            title: formData.get('title'),
            description: formData.get('description'),
            start_date: formData.get('start_date'),
            end_date: formData.get('end_date'),
            venue_id: parseInt(formData.get('venue_id')),
            organizer_id: parseInt(formData.get('organizer_id')),
            ticket_price: parseFloat(formData.get('ticket_price')) || 0,
            image_url: formData.get('image_url'),
            tags: Array.from(eventForm.tags.selectedOptions).map(option => parseInt(option.value))
        };

        try {
            const url = currentEventId ? `/api/events/${currentEventId}` : '/api/events';
            const method = currentEventId ? 'PUT' : 'POST';

            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(eventData)
            });

            if (!response.ok) {
                throw new Error('Failed to save event');
            }

            closeModal();
            loadEvents();
            showSuccess(currentEventId ? 'Event updated successfully' : 'Event created successfully');
        } catch (error) {
            console.error('Error saving event:', error);
            showError('Failed to save event');
        }
    }

    async function deleteEvent(eventId) {
        if (!confirm('Are you sure you want to delete this event?')) {
            return;
        }

        try {
            const response = await fetch(`/api/events/${eventId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Failed to delete event');
            }

            loadEvents();
            showSuccess('Event deleted successfully');
        } catch (error) {
            console.error('Error deleting event:', error);
            showError('Failed to delete event');
        }
    }

    // Utility Functions
    function closeModal() {
        eventModal.style.display = 'none';
        eventForm.reset();
        currentEventId = null;
    }

    function showLoading(show) {
        loadingMessage.style.display = show ? 'flex' : 'none';
        eventsTable.style.opacity = show ? '0.5' : '1';
    }

    function formatDate(dateString) {
        if (!dateString) return 'N/A';
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    function formatDateTimeForInput(dateString) {
        return new Date(dateString).toISOString().slice(0, 16);
    }

    function formatPrice(price) {
        if (!price) return 'Free';
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(price);
    }

    function showSuccess(message) {
        // Implement your preferred success notification method
        alert(message);
    }

    function showError(message) {
        // Implement your preferred error notification method
        alert(message);
    }

    function escapeHtml(unsafe) {
        if (!unsafe) return '';
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}); 