document.addEventListener('DOMContentLoaded', function () {
    const agentForm = document.getElementById('agentForm');
    const agentSelect = document.getElementById('agent-select');
    const deleteAgentBtn = document.getElementById('deleteAgentBtn');
    const newAgentBtn = document.getElementById('newAgentBtn');
    const searchInput = document.querySelector('.search-bar input');

    // Store all agents for search functionality
    let allAgents = [];

    // Initialize agents data
    async function initializeAgents() {
        try {
            const response = await fetch('/agents');
            const data = await response.json();
            if (data.success) {
                allAgents = data.agents;
                updateAgentSelect(allAgents);
            }
        } catch (error) {
            console.error('Error loading agents:', error);
        }
    }

    // Update agent select dropdown
    function updateAgentSelect(agents) {
        agentSelect.innerHTML = '';

        if (agents.length === 1) {
            // Single result - auto-select and populate form
            const option = document.createElement('option');
            option.value = agents[0].id;
            option.textContent = agents[0].name;
            option.selected = true;
            agentSelect.appendChild(option);

            // Trigger change event to populate form
            agentSelect.value = agents[0].id;
            agentSelect.dispatchEvent(new Event('change'));
        } else if (agents.length > 1) {
            // Multiple results - show message and list
            const defaultOption = document.createElement('option');
            defaultOption.value = "";
            defaultOption.textContent = "Please Choose the Assistant";
            defaultOption.selected = true;
            agentSelect.appendChild(defaultOption);

            // Add all matching agents
            agents.forEach(agent => {
                const option = document.createElement('option');
                option.value = agent.id;
                option.textContent = agent.name;
                agentSelect.appendChild(option);
            });

            // Clear form if something was selected before
            if (agentForm) {
                agentForm.reset();
                deleteAgentBtn.style.display = 'none';
            }
        } else {
            // No results
            const defaultOption = document.createElement('option');
            defaultOption.value = "";
            defaultOption.textContent = "No matching assistants found";
            defaultOption.selected = true;
            agentSelect.appendChild(defaultOption);

            // Clear form if something was selected before
            if (agentForm) {
                agentForm.reset();
                deleteAgentBtn.style.display = 'none';
            }
        }
    }

    // Handle search with debounce
    let searchTimeout;
    searchInput.addEventListener('input', function (e) {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            const searchTerm = e.target.value.toLowerCase();
            const filteredAgents = allAgents.filter(agent =>
                agent.name.toLowerCase().includes(searchTerm)
            );
            updateAgentSelect(filteredAgents);
        }, 300); // 300ms delay to prevent too frequent updates
    });

    // Initialize agents on page load
    initializeAgents();

    // Function to format JSON in textareas
    function formatJsonField(value) {
        try {
            return JSON.stringify(value, null, 2);
        } catch (e) {
            return value || '';
        }
    }

    // Function to update assistant website link
    function updateAssistantWebsiteLink() {
        const assistantId = document.getElementById('assistant_id').value;
        const assistantName = document.getElementById('name').value;
        const assistantType = document.getElementById('type').value;

        if (assistantId && assistantName) {
            const baseUrl = 'https://apis-ia-app-28obw.ondigitalocean.app';
            const encodedName = encodeURIComponent(assistantName);
            const encodedType = encodeURIComponent(assistantType || 'classic');
            const url = `${baseUrl}/${assistantId}?assistant_name=${encodedName}&type=${encodedType}&default_language=en`;

            const link = document.getElementById('assistantWebsiteLink');
            link.href = url;
            link.style.display = 'inline-flex';
        } else {
            document.getElementById('assistantWebsiteLink').style.display = 'none';
        }
    }

    // Function to update language selector based on assistant_languages
    function updateLanguageSelector(assistantLanguages) {
        const languageSelect = document.getElementById('language-select');
        languageSelect.innerHTML = '';

        try {
            // Get languages from assistant_languages field
            const languages = assistantLanguages?.languages || [];

            if (languages.length === 0) {
                // Add default English if no languages defined
                const defaultOption = document.createElement('option');
                defaultOption.value = 'en';
                defaultOption.textContent = 'English (1.0)';
                languageSelect.appendChild(defaultOption);
            } else {
                // Add each language from the assistant's configuration
                languages.forEach(lang => {
                    const option = document.createElement('option');
                    option.value = lang.language_code;
                    option.textContent = `${lang.language_name} (${lang.version})`;
                    languageSelect.appendChild(option);
                });
            }

            // Update configuration fields for the first language
            const firstLang = languages[0]?.language_code || 'en';
            updateConfigurationFields(firstLang);
        } catch (error) {
            console.error('Error updating language selector:', error);
            // Fallback to English
            const defaultOption = document.createElement('option');
            defaultOption.value = 'en';
            defaultOption.textContent = 'English (1.0)';
            languageSelect.appendChild(defaultOption);
        }
    }

    // Handle agent selection
    agentSelect.addEventListener('change', async function () {
        const agentId = this.value;
        if (agentId) {
            try {
                const response = await fetch(`/agent/${agentId}`);
                const data = await response.json();

                if (data.success) {
                    // Fill form with agent data
                    const agent = data.agent;
                    document.getElementById('assistant_id').value = agent.id || '';
                    document.getElementById('name').value = agent.name || '';
                    document.getElementById('description').value = agent.description || '';
                    document.getElementById('prompt').value = agent.prompt || '';
                    document.getElementById('type').value = agent.type || 'classic';
                    document.getElementById('image').value = agent.image || '';
                    document.getElementById('sponsor_id').value = agent.sponsor_id || '';
                    document.getElementById('questions').value = formatJsonField(agent.questions);
                    document.getElementById('config').value = formatJsonField(agent.config);
                    document.getElementById('functions').value = agent.functions || 'not_defined';
                    document.getElementById('languages').value = formatJsonField(agent.languages);
                    document.getElementById('subtype').value = agent.subtype || 'subtype';
                    document.getElementById('sponsor_logo').value = agent.sponsor_logo || 'sponsor_default.png';
                    document.getElementById('sponsor_url').value = agent.sponsor_url || 'https://apis-ia.com';

                    // Update language selector with assistant's languages
                    updateLanguageSelector(agent.languages);

                    // Update assistant website link
                    updateAssistantWebsiteLink();

                    // Show delete button
                    deleteAgentBtn.style.display = 'inline-block';
                } else {
                    alert('Error loading agent: ' + data.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error loading agent details');
            }
        } else {
            // Clear form when no agent is selected
            agentForm.reset();
            deleteAgentBtn.style.display = 'none';
            // Reset language selector to default
            updateLanguageSelector({ languages: [] });
            // Hide assistant website link
            document.getElementById('assistantWebsiteLink').style.display = 'none';
        }
    });

    // Handle new agent button
    newAgentBtn.addEventListener('click', function () {
        agentSelect.value = '';
        agentForm.reset();
        deleteAgentBtn.style.display = 'none';
        // Reset language selector to default
        updateLanguageSelector({ languages: [] });
        // Hide assistant website link
        document.getElementById('assistantWebsiteLink').style.display = 'none';
    });

    // Add event listeners for link updates
    document.getElementById('name').addEventListener('input', updateAssistantWebsiteLink);
    document.getElementById('type').addEventListener('input', updateAssistantWebsiteLink);

    // Function to safely parse JSON fields
    function parseJsonField(value) {
        try {
            return value ? JSON.parse(value) : null;
        } catch (e) {
            console.error('Error parsing JSON:', e);
            return null;
        }
    }

    // Handle form submission
    agentForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Update the config field with the current configuration data
        const configData = collectConfigurationData();
        document.getElementById('config').value = JSON.stringify(configData, null, 2);

        const agentData = {
            assistant_id: document.getElementById('assistant_id').value,
            name: document.getElementById('name').value,
            description: document.getElementById('description').value,
            prompt: document.getElementById('prompt').value,
            type: document.getElementById('type').value,
            image: document.getElementById('image').value,
            sponsor_id: document.getElementById('sponsor_id').value,
            questions: parseJsonField(document.getElementById('questions').value),
            config: configData,
            functions: document.getElementById('functions').value,
            languages: parseJsonField(document.getElementById('languages').value),
            subtype: document.getElementById('subtype').value,
            sponsor_logo: document.getElementById('sponsor_logo').value,
            sponsor_url: document.getElementById('sponsor_url').value
        };

        // Remove empty values
        Object.keys(agentData).forEach(key => {
            if (agentData[key] === '' || agentData[key] === null) {
                delete agentData[key];
            }
        });

        try {
            const response = await fetch('/edit-agent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(agentData)
            });

            const data = await response.json();

            if (data.success) {
                alert('Assistant saved successfully!');
                // Reload page to update the agent list
                window.location.reload();
            } else {
                alert('Error saving assistant: ' + data.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error saving assistant');
        }
    });

    // Handle delete button
    deleteAgentBtn.addEventListener('click', async function () {
        const agentId = document.getElementById('assistant_id').value;
        if (!agentId) return;

        if (confirm('Are you sure you want to delete this agent?')) {
            try {
                const response = await fetch(`/agent/${agentId}/delete`, {
                    method: 'POST'
                });

                const data = await response.json();

                if (data.success) {
                    alert('Agent deleted successfully!');
                    window.location.reload();
                } else {
                    alert('Error deleting agent: ' + data.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error deleting agent');
            }
        }
    });

    // Manage Functionalities button click handler
    document.getElementById('manageFunctionalities').addEventListener('click', function () {
        const assistantId = document.getElementById('assistant_id').value;
        if (!assistantId) {
            alert('Please select an assistant first');
            return;
        }

        // Get the current config data
        const configData = parseJsonField(document.getElementById('config').value) || {};
        const assistantLanguages = parseJsonField(document.getElementById('languages').value) || {};

        // Get languages from assistant_languages field
        const languages = assistantLanguages.languages || [{
            language_code: 'en',
            language_name: 'English',
            version: '1.0'
        }];

        // Create functionalities map for each language
        const functionalities = {};
        languages.forEach(lang => {
            const langCode = lang.language_code;
            const langConfig = configData.languages?.[langCode] || {};
            functionalities[langCode] = (langConfig.functionalities || []).map(func => ({
                id: parseInt(func.id || func.functionality_id),
                text: func.text || func.functionality_text || '',
                value: func.value || func.functionality_value || ''
            }));
        });

        console.log('Opening modal with:', {
            languages,
            functionalities,
            assistantId
        });

        // Open modal with language data and functionalities
        window.functionalityModal.open(languages, functionalities, assistantId);
    });

    // Helper function to get language display names
    function getLanguageDisplayName(code) {
        const languageNames = {
            'en': 'English',
            'es': 'Español',
            'fr': 'Français',
            'de': 'Deutsch',
            'ar': 'العربية',
            'lb': 'Lëtzebuergesch',
            'pt': 'Português',
            'zh': '中文'
        };
        return languageNames[code] || code.toUpperCase();
    }

    // Listen for functionality updates from the modal
    window.addEventListener('functionalityUpdate', function (event) {
        const functionalities = event.detail.functionalities;

        // Get current configuration
        const configData = parseJsonField(document.getElementById('config').value) || {};
        if (!configData.languages) {
            configData.languages = {};
        }

        // Update functionalities for each language
        Object.entries(functionalities).forEach(([langCode, funcs]) => {
            if (!configData.languages[langCode]) {
                configData.languages[langCode] = {};
            }
            configData.languages[langCode].functionalities = funcs;
        });

        // Update the hidden config field
        document.getElementById('config').value = JSON.stringify(configData, null, 2);

        // Update the UI to show changes
        updateFunctionalitySummary(configData);
    });

    function updateFunctionalitySummary(configData) {
        const currentLang = document.getElementById('languageSelect').value;
        const functionalities = configData.languages?.[currentLang]?.functionalities || [];

        document.getElementById('functionalityCount').textContent = functionalities.length;
        document.getElementById('lastUpdated').textContent = new Date().toLocaleString();
    }

    // Handle language selection
    const languageSelect = document.getElementById('language-select');
    languageSelect.addEventListener('change', function () {
        updateConfigurationFields(this.value);
    });

    // Function to update configuration fields based on selected language
    function updateConfigurationFields(languageCode) {
        const configData = parseJsonField(document.getElementById('config').value) || {};
        const langConfig = configData.languages?.[languageCode] || {};

        // Update basic information
        document.getElementById('assistant_name').value = langConfig.assistant_name || '';
        document.getElementById('assistant_desc').value = langConfig.assistant_desc || '';

        // Update design features
        const designFeatures = langConfig.design_features || {};
        document.getElementById('assistant_img_url').value = langConfig.assistant_img_url || designFeatures.assistant_img_url || '';
        document.getElementById('assistant_sidebar_img').value = langConfig.assistant_sidebar_img || designFeatures.assistant_sidebar_img || '';
        document.getElementById('assistant_splash_img').value = langConfig.assistant_splash_img || designFeatures.assistant_splash_img || '';
        document.getElementById('bg_image').value = designFeatures.bg_image || '';
        document.getElementById('bubble_bg_color').value = designFeatures.bubble_bg_color || '#ffffff';
        document.getElementById('bubble_font_color').value = designFeatures.bubble_font_color || '#000000';

        // Update welcome messages
        document.getElementById('assistant_splash_txt').value = langConfig.assistant_splash_txt || '';
        document.getElementById('assistant_splash_mobile_txt').value = langConfig.assistant_splash_mobile_txt || '';

        // Update functionalities count
        const functionalities = langConfig.functionalities || [];
        document.getElementById('functionalityCount').textContent = functionalities.length;
    }

    // Function to collect configuration data from form fields
    function collectConfigurationData() {
        const configData = parseJsonField(document.getElementById('config').value) || {};
        if (!configData.languages) configData.languages = {};

        const currentLang = languageSelect.value;
        if (!configData.languages[currentLang]) configData.languages[currentLang] = {};

        const langConfig = configData.languages[currentLang];

        // Update basic information
        langConfig.assistant_name = document.getElementById('assistant_name').value;
        langConfig.assistant_desc = document.getElementById('assistant_desc').value;

        // Update design features
        langConfig.design_features = {
            assistant_sidebar_img: document.getElementById('assistant_sidebar_img').value,
            assistant_splash_img: document.getElementById('assistant_splash_img').value,
            bg_image: document.getElementById('bg_image').value,
            bubble_bg_color: document.getElementById('bubble_bg_color').value,
            bubble_font_color: document.getElementById('bubble_font_color').value
        };

        // Update URLs at root level for backward compatibility
        langConfig.assistant_sidebar_img = document.getElementById('assistant_sidebar_img').value;
        langConfig.assistant_splash_img = document.getElementById('assistant_splash_img').value;

        // Update welcome messages
        langConfig.assistant_splash_txt = document.getElementById('assistant_splash_txt').value;
        langConfig.assistant_splash_mobile_txt = document.getElementById('assistant_splash_mobile_txt').value;

        // Keep existing functionalities
        if (!langConfig.functionalities) langConfig.functionalities = [];

        return configData;
    }
}); 