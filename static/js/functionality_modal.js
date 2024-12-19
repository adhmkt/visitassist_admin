class FunctionalityModal {
    constructor() {
        this.modal = null;
        this.currentLanguage = '';
        this.allLanguages = [];
        this.functionalitiesByLanguage = {};
        this.dbFunctionalities = [];
        this.assistantId = null;
        this.selectedItems = new Set();
        this.isLoading = false;
        this.init();
    }

    init() {
        this.createModal();
        this.attachEventListeners();
    }

    createModal() {
        const modalHTML = `
            <div id="functionalityModal" class="modal">
                <div class="modal-content">
                    <!-- Header -->
                    <div class="modal-header">
                        <div class="header-top">
                            <h2>Manage Conversation Starters</h2>
                            <div class="language-selector">
                                <label for="languageSelect">Language:</label>
                                <select id="languageSelect" class="language-select"></select>
                            </div>
                        </div>
                        <div class="header-controls">
                            <div class="search-filter">
                                <input type="text" id="searchFunctionalities" placeholder="Search conversation starters...">
                                <select id="sortFunctionalities">
                                    <option value="id">Sort by ID</option>
                                    <option value="text">Sort by Text</option>
                                </select>
                            </div>
                            <div class="bulk-actions">
                                <button class="bulk-action-btn">Bulk Actions ▼</button>
                                <div class="bulk-action-menu">
                                    <button data-action="copy">Copy to Language...</button>
                                    <button data-action="export">Export Selected...</button>
                                    <button data-action="delete">Delete Selected</button>
                                    <button data-action="import">Import from File</button>
                                    <button data-action="reorder">Reorder...</button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Main Content -->
                    <div class="modal-body">
                        <div class="table-container">
                            <table id="functionalitiesTable">
                                <thead>
                                    <tr>
                                        <th><input type="checkbox" id="selectAll"></th>
                                        <th>ID</th>
                                        <th>Text</th>
                                        <th>Value</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody></tbody>
                            </table>
                        </div>
                        <div class="edit-form">
                            <h3>Edit Conversation Starter</h3>
                            <form id="editFunctionalityForm">
                                <div class="form-group">
                                    <label for="editId">ID</label>
                                    <input type="number" id="editId" readonly>
                                </div>
                                <div class="form-group">
                                    <label for="editText">Text</label>
                                    <input type="text" id="editText" required>
                                </div>
                                <div class="form-group">
                                    <label for="editValue">Value</label>
                                    <textarea id="editValue" required></textarea>
                                </div>
                            </form>
                        </div>
                    </div>

                    <!-- Footer -->
                    <div class="modal-footer">
                        <div class="selection-info">Selected: <span class="selected-count">0</span> items</div>
                        <div class="action-buttons">
                            <button class="cancel-btn">Cancel</button>
                            <button class="save-btn">Save Changes</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHTML);
        this.modal = document.getElementById('functionalityModal');
    }

    attachEventListeners() {
        // Close modal
        this.modal.querySelector('.cancel-btn').addEventListener('click', () => this.close());

        // Select all functionality
        const selectAll = this.modal.querySelector('#selectAll');
        selectAll.addEventListener('change', (e) => this.handleSelectAll(e.target.checked));

        // Search functionality
        const searchInput = this.modal.querySelector('#searchFunctionalities');
        searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value));

        // Sort functionality
        const sortSelect = this.modal.querySelector('#sortFunctionalities');
        sortSelect.addEventListener('change', (e) => this.handleSort(e.target.value));

        // Bulk actions
        const bulkActionBtn = this.modal.querySelector('.bulk-action-btn');
        bulkActionBtn.addEventListener('click', () => this.toggleBulkActionMenu());

        // Save changes
        this.modal.querySelector('.save-btn').addEventListener('click', () => this.saveChanges());

        // Edit functionality
        this.modal.addEventListener('click', (e) => {
            const editBtn = e.target.closest('.edit-btn');
            if (editBtn) {
                const id = editBtn.dataset.id;
                this.editFunctionality(id);
            }
        });

        // Delete functionality
        this.modal.addEventListener('click', (e) => {
            const deleteBtn = e.target.closest('.delete-btn');
            if (deleteBtn) {
                const id = deleteBtn.dataset.id;
                this.deleteFunctionality(id);
            }
        });

        // Handle checkbox changes
        this.modal.querySelector('tbody').addEventListener('change', (e) => {
            if (e.target.type === 'checkbox') {
                this.handleItemSelection(e.target.dataset.id, e.target.checked);
            }
        });

        // Language selection change
        const languageSelect = this.modal.querySelector('#languageSelect');
        languageSelect.addEventListener('change', (e) => this.switchLanguage(e.target.value));
    }

    async open(languages, functionalitiesByLang, assistantId) {
        console.log('Opening modal with config:', { languages, functionalitiesByLang, assistantId });

        // Store assistant ID
        this.assistantId = assistantId;

        // Store the full language objects
        this.languageData = Array.isArray(languages) ? languages : [];

        // If no languages, initialize with English
        if (this.languageData.length === 0) {
            this.languageData = [{
                language_code: 'en',
                language_name: 'English',
                version: '1.0'
            }];
        }

        // Store functionalities by language
        this.functionalitiesByLanguage = functionalitiesByLang || {};

        // Ensure each language has a functionalities array
        this.languageData.forEach(lang => {
            if (!this.functionalitiesByLanguage[lang.language_code]) {
                this.functionalitiesByLanguage[lang.language_code] = [];
            }
        });

        // Set current language to first available language
        this.currentLanguage = this.languageData[0]?.language_code || 'en';
        this.functionalities = this.functionalitiesByLanguage[this.currentLanguage] || [];

        // Clear selection
        this.selectedItems.clear();

        // Update UI
        this.updateLanguageSelector();
        this.updateTable();
        this.updateLanguageStats();

        // Show modal
        this.modal.style.display = 'block';
    }

    updateLanguageSelector() {
        const languageSelect = this.modal.querySelector('#languageSelect');
        languageSelect.innerHTML = '';

        // Add options for each language
        this.languageData.forEach(lang => {
            const option = document.createElement('option');
            option.value = lang.language_code;
            option.textContent = `${lang.language_name} (${lang.version})`;
            option.selected = lang.language_code === this.currentLanguage;
            languageSelect.appendChild(option);
        });
    }

    updateLanguageStats() {
        // Add language statistics to the header
        const headerTop = this.modal.querySelector('.header-top');
        const statsDiv = headerTop.querySelector('.language-stats') || document.createElement('div');
        statsDiv.className = 'language-stats';

        // Calculate statistics
        const totalLanguages = this.languageData.length;
        const completedLanguages = Object.values(this.functionalitiesByLanguage)
            .filter(funcs => funcs.length > 0).length;

        statsDiv.innerHTML = `
            <div class="stat">
                <span class="stat-label">Languages:</span>
                <span class="stat-value">${totalLanguages}</span>
            </div>
            <div class="stat">
                <span class="stat-label">With Content:</span>
                <span class="stat-value">${completedLanguages}</span>
            </div>
        `;

        if (!headerTop.querySelector('.language-stats')) {
            headerTop.appendChild(statsDiv);
        }
    }

    close() {
        this.modal.style.display = 'none';
    }

    updateTable(items = this.functionalities) {
        const tbody = this.modal.querySelector('tbody');
        tbody.innerHTML = '';

        items.forEach(func => {
            const row = document.createElement('tr');
            const isEditing = document.querySelector('#editId')?.value === func.id.toString();
            if (isEditing) {
                row.classList.add('editing');
            }
            row.innerHTML = `
                <td><input type="checkbox" data-id="${func.id}" ${this.selectedItems.has(func.id) ? 'checked' : ''}></td>
                <td>${func.id}</td>
                <td>${this.escapeHtml(func.text)}</td>
                <td>${this.escapeHtml(func.value)}</td>
                <td class="action-buttons">
                    <button class="edit-btn ${isEditing ? 'active' : ''}" data-id="${func.id}" title="Edit">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="delete-btn" data-id="${func.id}" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });

        this.updateSelectedCount();
    }

    handleSelectAll(checked) {
        const checkboxes = this.modal.querySelectorAll('tbody input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = checked;
            this.handleItemSelection(checkbox.dataset.id, checked);
        });
    }

    handleItemSelection(id, selected) {
        if (selected) {
            this.selectedItems.add(id);
        } else {
            this.selectedItems.delete(id);
        }
        this.updateSelectedCount();
    }

    handleSearch(query) {
        const searchTerm = query.toLowerCase();
        const filteredItems = this.functionalities.filter(func =>
            func.text.toLowerCase().includes(searchTerm) ||
            func.value.toLowerCase().includes(searchTerm) ||
            func.id.toString().includes(searchTerm)
        );
        this.updateTable(filteredItems);
    }

    handleSort(criteria) {
        const sortedItems = [...this.functionalities].sort((a, b) => {
            if (criteria === 'id') {
                return a.id - b.id;
            } else if (criteria === 'text') {
                return a.text.localeCompare(b.text);
            }
            return 0;
        });
        this.updateTable(sortedItems);
    }

    async editFunctionality(id) {
        const func = this.functionalities.find(f => f.id.toString() === id.toString());
        if (!func) {
            this.showError('Functionality not found');
            return;
        }

        try {
            // Show loading state in the form area only
            const form = this.modal.querySelector('#editFunctionalityForm');
            const editArea = this.modal.querySelector('.edit-form');
            editArea.classList.add('loading');

            // Fetch functionality data from database
            const response = await fetch(
                `/api/assistant-functionalities/${this.assistantId}/${id}/${this.currentLanguage}`
            );
            const data = await response.json();

            console.log('Fetched functionality data:', data);

            if (!data.success) {
                throw new Error(data.error || 'Failed to load functionality data');
            }

            // Get the database functionality data
            const dbFunc = data.functionality;

            // Store the fetched functionality in dbFunctionalities array
            if (dbFunc) {
                const existingIndex = this.dbFunctionalities.findIndex(f =>
                    f.functionality_id === dbFunc.functionality_id &&
                    f.language === dbFunc.language
                );
                if (existingIndex !== -1) {
                    this.dbFunctionalities[existingIndex] = dbFunc;
                } else {
                    this.dbFunctionalities.push(dbFunc);
                }
            }

            // Update form fields
            form.querySelector('#editId').value = func.id;
            form.querySelector('#editText').value = func.text;
            form.querySelector('#editValue').value = func.value;

            // Highlight the selected row
            const rows = this.modal.querySelectorAll('tbody tr');
            rows.forEach(row => row.classList.remove('editing'));
            const selectedRow = this.modal.querySelector(`tr input[data-id="${id}"]`)?.closest('tr');
            if (selectedRow) selectedRow.classList.add('editing');

            // Show edit feedback
            this.showSuccess('Editing conversation starter');

            // Add event listener for form changes
            const editText = form.querySelector('#editText');
            const editValue = form.querySelector('#editValue');

            const updateHandler = () => {
                const updatedFunc = {
                    id: parseInt(form.querySelector('#editId').value),
                    text: editText.value,
                    value: editValue.value
                };

                // Update the functionality in the current language array
                const index = this.functionalities.findIndex(f => f.id.toString() === updatedFunc.id.toString());
                if (index !== -1) {
                    this.functionalities[index] = updatedFunc;

                    // Update the table
                    this.updateTable();

                    // Store in the language-specific data
                    this.functionalitiesByLanguage[this.currentLanguage] = this.functionalities;

                    // Update in dbFunctionalities
                    const dbIndex = this.dbFunctionalities.findIndex(f =>
                        f.functionality_id === updatedFunc.id &&
                        f.language === this.currentLanguage
                    );
                    if (dbIndex !== -1) {
                        this.dbFunctionalities[dbIndex] = {
                            ...this.dbFunctionalities[dbIndex],
                            functionality_text: updatedFunc.text,
                            functionality_value: updatedFunc.value
                        };
                    }
                }
            };

            // Remove existing event listeners to prevent duplicates
            editText.removeEventListener('input', updateHandler);
            editValue.removeEventListener('input', updateHandler);

            // Add new event listeners
            editText.addEventListener('input', updateHandler);
            editValue.addEventListener('input', updateHandler);

        } catch (error) {
            console.error('Error fetching functionality:', error);
            this.showError(error.message || 'Error loading functionality data');
        } finally {
            // Remove loading state from the form area
            const editArea = this.modal.querySelector('.edit-form');
            editArea.classList.remove('loading');
        }
    }

    updatePreview(func) {
        const previewContent = this.modal.querySelector('.preview-content');
        previewContent.innerHTML = `
            <div class="preview-item">
                <strong>ID:</strong> ${func.id}<br>
                <strong>Text:</strong> ${this.escapeHtml(func.text)}<br>
                <strong>Value:</strong> ${this.escapeHtml(func.value)}<br>
                <strong>Additional Data:</strong><br>
                <pre>${this.escapeHtml(func.blob || '{}')}</pre>
            </div>
        `;
    }

    async deleteFunctionality(id) {
        if (!confirm('Are you sure you want to delete this functionality?')) {
            return;
        }

        try {
            // Remove from current language only
            const index = this.functionalities.findIndex(f => f.id.toString() === id.toString());
            if (index === -1) {
                throw new Error('Functionality not found');
            }

            // Remove from current language array
            this.functionalities.splice(index, 1);

            // Update the language-specific data
            this.functionalitiesByLanguage[this.currentLanguage] = this.functionalities;

            // Update the table
            this.updateTable();

            // Show success message
            this.showSuccess('Functionality deleted successfully');

            // Save changes to persist the deletion
            await this.saveChanges();
        } catch (error) {
            console.error('Delete error:', error);
            this.showError('Error deleting functionality. Please try again.');
            // Refresh the table to ensure consistent state
            this.updateTable();
        }
    }

    async saveChanges() {
        try {
            this.setLoading(true);

            // Get the current edited functionality ID
            const editForm = this.modal.querySelector('#editFunctionalityForm');
            const currentEditId = editForm.querySelector('#editId')?.value;

            if (!currentEditId) {
                throw new Error('No functionality is currently being edited');
            }

            // Get the updated values
            const updatedFunc = {
                id: parseInt(currentEditId),
                text: editForm.querySelector('#editText').value,
                value: editForm.querySelector('#editValue').value
            };

            // Find existing functionality in current language
            const existingFunc = this.functionalities.find(f => f.id === updatedFunc.id);
            if (!existingFunc) {
                throw new Error('Functionality not found in current language');
            }

            // Check if there are actual changes
            if (existingFunc.text === updatedFunc.text && existingFunc.value === updatedFunc.value) {
                this.showSuccess('No changes to save');
                setTimeout(() => this.close(), 1500);
                return;
            }

            // Update in current language array
            const index = this.functionalities.findIndex(f => f.id === updatedFunc.id);
            this.functionalities[index] = updatedFunc;
            this.functionalitiesByLanguage[this.currentLanguage] = this.functionalities;

            // Get current configuration from dbFunctionalities
            const dbFunc = this.dbFunctionalities.find(f =>
                f.functionality_id === updatedFunc.id &&
                f.language === this.currentLanguage
            );

            // Prepare configuration updates only for the current functionality
            const configUpdates = {
                languages: {
                    [this.currentLanguage]: {
                        functionalities: [{
                            functionality_id: updatedFunc.id,
                            functionality_text: updatedFunc.text,
                            functionality_value: updatedFunc.value
                        }]
                    }
                }
            };

            // Prepare database update
            const dbUpdates = [{
                assistant_id: this.assistantId,
                language: this.currentLanguage,
                functionality_id: updatedFunc.id,
                functionality_text: updatedFunc.text,
                functionality_value: updatedFunc.value,
                functionality_type: dbFunc?.functionality_type || 'default'
            }];

            console.log('Sending updates:', {
                assistantId: this.assistantId,
                configUpdates,
                dbUpdates
            });

            // Send updates to server
            const response = await fetch('/api/update-functionalities', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    assistantId: this.assistantId,
                    configUpdates,
                    dbUpdates
                })
            });

            const data = await response.json();
            if (!data.success) {
                throw new Error(data.error || 'Failed to save changes');
            }

            // Update dbFunctionalities after successful save
            const dbIndex = this.dbFunctionalities.findIndex(f =>
                f.functionality_id === updatedFunc.id &&
                f.language === this.currentLanguage
            );
            if (dbIndex !== -1) {
                this.dbFunctionalities[dbIndex] = {
                    ...this.dbFunctionalities[dbIndex],
                    functionality_text: updatedFunc.text,
                    functionality_value: updatedFunc.value
                };
            }

            this.showSuccess('Changes saved successfully!');
            setTimeout(() => this.close(), 1500);
        } catch (error) {
            console.error('Save error:', error);
            this.showError(error.message || 'Error saving changes. Please try again.');
        } finally {
            this.setLoading(false);
        }
    }

    escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    toggleBulkActionMenu() {
        const menu = this.modal.querySelector('.bulk-action-menu');
        menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
    }

    updateSelectedCount() {
        this.modal.querySelector('.selected-count').textContent = this.selectedItems.size;
    }

    switchLanguage(newLanguage) {
        // Save current functionalities before switching
        this.functionalitiesByLanguage[this.currentLanguage] = [...this.functionalities];

        // Switch to new language
        this.currentLanguage = newLanguage;
        this.functionalities = [...(this.functionalitiesByLanguage[newLanguage] || [])];

        // Clear selection
        this.selectedItems.clear();

        // Update UI
        this.updateTable();
        this.updateLanguageStats();
    }

    getLanguageDisplayName(langCode) {
        const languageNames = {
            'en': 'English',
            'es': 'Español',
            'fr': 'Français',
            'de': 'Deutsch',
            'it': 'Italiano',
            'pt': 'Português',
            'ar': 'العربية',
            'zh': '中文',
            'ja': '日本',
            'ko': '한국어',
            'ru': 'Русский',
            'nl': 'Nederlands',
            'pl': 'Polski',
            'tr': 'Türkçe',
            'hi': 'हिन्दी',
            'bn': 'বাংলা',
            'th': 'ไทย',
            'vi': 'Tiếng Việt',
            'id': 'Bahasa Indonesia',
            'ms': 'Bahasa Melayu',
            'fa': 'فارسی',
            'he': 'עברית',
            'lb': 'Lëtzebuergesch'
        };
        return languageNames[langCode] || langCode.toUpperCase();
    }

    // Add loading state management
    setLoading(loading) {
        this.isLoading = loading;
        const saveBtn = this.modal.querySelector('.save-btn');
        const modalContent = this.modal.querySelector('.modal-content');

        if (loading) {
            saveBtn.disabled = true;
            saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
            modalContent.classList.add('loading');
        } else {
            saveBtn.disabled = false;
            saveBtn.innerHTML = 'Save Changes';
            modalContent.classList.remove('loading');
        }
    }

    // Add success feedback
    showSuccess(message) {
        const feedback = document.createElement('div');
        feedback.className = 'feedback-message success';
        feedback.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
        this.modal.querySelector('.modal-header').appendChild(feedback);

        setTimeout(() => feedback.remove(), 3000);
    }

    // Add error feedback
    showError(message) {
        const feedback = document.createElement('div');
        feedback.className = 'feedback-message error';
        feedback.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
        this.modal.querySelector('.modal-header').appendChild(feedback);

        setTimeout(() => feedback.remove(), 3000);
    }
}

// Initialize the modal
const functionalityModal = new FunctionalityModal();

// Export for use in other files
window.functionalityModal = functionalityModal; 