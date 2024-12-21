document.addEventListener('DOMContentLoaded', function () {
    const agentForm = document.getElementById('agentForm');
    const agentSelect = document.getElementById('agent-select');
    const deleteAgentBtn = document.getElementById('deleteAgentBtn');
    const newAgentBtn = document.getElementById('newAgentBtn');
    const searchInput = document.querySelector('.search-bar input');
    const assistantWebsiteLink = document.getElementById('assistantWebsiteLink');
    const manageFunctionalities = document.getElementById('manageFunctionalities');
    const functionalityModal = window.functionalityModal;
    const languageSelect = document.getElementById('language-select');

    // Store all agents for search functionality
    let allAgents = [];
    let currentAgent = null;
    let currentLanguageData = {};

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
        agentSelect.innerHTML = '<option value="">Choose an assistant...</option>';

        if (agents.length === 1) {
            const option = document.createElement('option');
            option.value = agents[0].id;
            option.textContent = agents[0].name;
            agentSelect.appendChild(option);
            agentSelect.value = agents[0].id;
            loadAgentDetails(agents[0].id);
        } else if (agents.length > 1) {
            agents.forEach(agent => {
                const option = document.createElement('option');
                option.value = agent.id;
                option.textContent = agent.name;
                agentSelect.appendChild(option);
            });
        }
    }

    // Load agent details
    async function loadAgentDetails(agentId) {
        try {
            console.log('Loading agent details for ID:', agentId);
            const response = await fetch(`/agent/${agentId}`);
            const data = await response.json();

            if (data.success) {
                console.log('Agent data received:', data.agent);
                currentAgent = data.agent;
                populateForm(currentAgent);
                updateAssistantWebsiteLink(currentAgent);
                updateLanguageSelector(currentAgent.languages);
                console.log('Current agent config:', currentAgent.config);
                loadLanguageSpecificData(currentAgent.config);
                deleteAgentBtn.style.display = 'inline-block';
            }
        } catch (error) {
            console.error('Error loading agent details:', error);
        }
    }

    // Populate form with agent data
    function populateForm(agent) {
        document.getElementById('assistant_id').value = agent.id || '';
        document.getElementById('name').value = agent.name || '';
        document.getElementById('description').value = agent.description || '';
        document.getElementById('prompt').value = agent.prompt || '';
        document.getElementById('type').value = agent.type || 'classic';
        document.getElementById('functions').value = agent.functions || 'not_defined';
        document.getElementById('languages').value = formatJsonField(agent.languages);
        document.getElementById('subtype').value = agent.subtype || 'subtype';
        document.getElementById('sponsor_id').value = agent.sponsor_id || '';
        document.getElementById('sponsor_logo').value = agent.sponsor_logo || 'sponsor_default.png';
        document.getElementById('sponsor_url').value = agent.sponsor_url || 'https://apis-ia.com';
    }

    // Load language-specific data from assistant_json
    function loadLanguageSpecificData(config) {
        console.log('Loading language-specific data with config:', config);

        currentLanguageData = {};
        const languages = currentAgent.languages?.languages || [];
        console.log('Available languages:', languages);

        // Initialize data structure for each language
        languages.forEach(lang => {
            const langCode = lang.language_code;
            // Check if language data exists in config.languages first
            if (config && config.languages && config.languages[langCode]) {
                currentLanguageData[langCode] = config.languages[langCode];
            } else {
                // Initialize with empty structure
                currentLanguageData[langCode] = {
                    assistant_name: currentAgent.name || '',
                    assistant_desc: currentAgent.description || '',
                    assistant_img_url: currentAgent.image || '',
                    assistant_sidebar_img: '',
                    assistant_splash_img: '',
                    bg_image: '',
                    bubble_bg_color: '#FFFFFF',
                    bubble_font_color: '#000000',
                    assistant_splash_txt: '',
                    assistant_splash_mobile_txt: ''
                };
            }
            console.log(`Initialized data for language ${langCode}:`, currentLanguageData[langCode]);
        });

        // Load data for current language
        const currentLang = languageSelect.value;
        console.log('Current selected language:', currentLang);
        if (currentLang) {
            updateConfigurationFields(currentLang);
        } else {
            console.warn('No language selected');
        }
    }

    // Update configuration fields for specific language
    function updateConfigurationFields(languageCode) {
        console.log('Updating configuration fields for language:', languageCode);
        const langData = currentLanguageData[languageCode] || {};
        console.log('Language-specific data:', langData);

        const fields = [
            'assistant_name',
            'assistant_desc',
            'assistant_img_url',
            'assistant_sidebar_img',
            'assistant_splash_img',
            'bg_image',
            'bubble_bg_color',
            'bubble_font_color',
            'assistant_splash_txt',
            'assistant_splash_mobile_txt'
        ];

        fields.forEach(field => {
            const element = document.getElementById(field);
            if (element) {
                // Set default values for color inputs
                if (field === 'bubble_bg_color' && !langData[field]) {
                    element.value = '#FFFFFF';
                } else if (field === 'bubble_font_color' && !langData[field]) {
                    element.value = '#000000';
                } else {
                    element.value = langData[field] || '';
                }
                console.log(`Setting ${field} to:`, element.value);
            } else {
                console.warn(`Field element not found: ${field}`);
            }
        });

        // Update functionality count and last updated
        if (currentAgent && currentAgent.config && currentAgent.config.languages) {
            const langConfig = currentAgent.config.languages[languageCode] || {};
            const functionalities = langConfig.functionalities || [];
            document.getElementById('functionalityCount').textContent = functionalities.length;
            document.getElementById('lastUpdated').textContent =
                currentAgent.config.last_updated || 'Never';
            console.log('Updated functionality count:', functionalities.length);
            console.log('Updated last updated:', currentAgent.config.last_updated);
        } else {
            console.warn('No current agent or config data available');
            document.getElementById('functionalityCount').textContent = '0';
            document.getElementById('lastUpdated').textContent = 'Never';
        }
    }

    // Update assistant website link
    function updateAssistantWebsiteLink(agent) {
        if (agent && agent.id) {
            const baseUrl = 'https://apis-ia-app-28obw.ondigitalocean.app';
            const encodedName = encodeURIComponent(agent.name || '');
            const encodedType = encodeURIComponent(agent.type || 'classic');
            const url = `${baseUrl}/${agent.id}?assistant_name=${encodedName}&type=${encodedType}&default_language=en`;
            assistantWebsiteLink.href = url;
            assistantWebsiteLink.style.display = 'inline-flex';
        } else {
            assistantWebsiteLink.style.display = 'none';
        }
    }

    // Update language selector
    function updateLanguageSelector(languagesData) {
        console.log('Updating language selector with data:', languagesData);
        languageSelect.innerHTML = '';

        const languages = languagesData?.languages || [{
            language_code: 'en',
            language_name: 'English',
            version: '1.0'
        }];

        console.log('Available languages for selector:', languages);

        languages.forEach(lang => {
            const option = document.createElement('option');
            option.value = lang.language_code;
            option.textContent = `${lang.language_name} (${lang.version})`;
            languageSelect.appendChild(option);
            console.log(`Added language option: ${lang.language_name} (${lang.version})`);
        });

        // Select first language by default
        if (languages.length > 0) {
            languageSelect.value = languages[0].language_code;
            console.log('Selected default language:', languages[0].language_code);
            updateConfigurationFields(languages[0].language_code);
        } else {
            console.warn('No languages available to select');
        }
    }

    // Handle language selection change
    languageSelect.addEventListener('change', function () {
        const selectedLanguage = this.value;
        if (selectedLanguage) {
            updateConfigurationFields(selectedLanguage);
        }
    });

    // Save configuration data for current language
    function saveCurrentLanguageData() {
        const currentLang = languageSelect.value;
        console.log('Saving data for language:', currentLang);
        if (!currentLang) {
            console.warn('No language selected for saving');
            return;
        }

        const fields = [
            'assistant_name',
            'assistant_desc',
            'assistant_img_url',
            'assistant_sidebar_img',
            'assistant_splash_img',
            'bg_image',
            'bubble_bg_color',
            'bubble_font_color',
            'assistant_splash_txt',
            'assistant_splash_mobile_txt'
        ];

        currentLanguageData[currentLang] = {};
        fields.forEach(field => {
            const element = document.getElementById(field);
            if (element) {
                currentLanguageData[currentLang][field] = element.value;
                console.log(`Saved ${field}:`, element.value);
            } else {
                console.warn(`Field element not found while saving: ${field}`);
            }
        });

        console.log('Updated currentLanguageData:', currentLanguageData);
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
        }, 300);
    });

    // Handle agent selection
    agentSelect.addEventListener('change', function () {
        const agentId = this.value;
        if (agentId) {
            loadAgentDetails(agentId);
        } else {
            clearForm();
        }
    });

    // Handle new agent button
    newAgentBtn.addEventListener('click', clearForm);

    // Handle manage functionalities button
    manageFunctionalities.addEventListener('click', function () {
        if (currentAgent) {
            const languages = currentAgent.languages?.languages || [];
            const functionalitiesByLang = {};

            // Extract functionalities by language from config
            if (currentAgent.config && currentAgent.config.languages) {
                Object.entries(currentAgent.config.languages).forEach(([langCode, langData]) => {
                    if (langData.functionalities) {
                        functionalitiesByLang[langCode] = langData.functionalities;
                    }
                });
            }

            functionalityModal.open(languages, functionalitiesByLang, currentAgent.id);
        }
    });

    // Clear form
    function clearForm() {
        agentForm.reset();
        currentAgent = null;
        currentLanguageData = {};
        deleteAgentBtn.style.display = 'none';
        assistantWebsiteLink.style.display = 'none';
        updateLanguageSelector();
        document.getElementById('functionalityCount').textContent = '0';
        document.getElementById('lastUpdated').textContent = 'Never';
    }

    // Format JSON fields
    function formatJsonField(value) {
        try {
            return JSON.stringify(value, null, 2);
        } catch (e) {
            return value || '';
        }
    }

    // Handle form submission
    agentForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        console.log('Form submission started');

        // Save current language data before submitting
        saveCurrentLanguageData();

        const formData = {
            assistant_id: document.getElementById('assistant_id').value,
            name: document.getElementById('name').value,
            description: document.getElementById('description').value,
            prompt: document.getElementById('prompt').value,
            type: document.getElementById('type').value,
            functions: document.getElementById('functions').value,
            languages: JSON.parse(document.getElementById('languages').value),
            subtype: document.getElementById('subtype').value,
            sponsor_id: document.getElementById('sponsor_id').value || null,
            sponsor_logo: document.getElementById('sponsor_logo').value,
            sponsor_url: document.getElementById('sponsor_url').value,
            config: {
                languages: {},
                last_updated: new Date().toISOString()
            }
        };

        // Preserve existing language-specific data
        Object.entries(currentLanguageData).forEach(([langCode, langData]) => {
            formData.config.languages[langCode] = {
                ...langData,
                functionalities: currentAgent?.config?.languages?.[langCode]?.functionalities || []
            };
        });

        console.log('Submitting form data:', formData);

        try {
            const response = await fetch('/edit-agent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            console.log('Server response:', data);
            if (data.success) {
                alert('Assistant saved successfully!');
                // Refresh the agents list
                initializeAgents();
            } else {
                console.error('Error saving assistant:', data.message);
                alert('Error saving assistant: ' + data.message);
            }
        } catch (error) {
            console.error('Error submitting form:', error);
            alert('Error saving assistant');
        }
    });

    // Handle delete button
    deleteAgentBtn.addEventListener('click', async function () {
        const agentId = document.getElementById('assistant_id').value;
        if (!agentId || !confirm('Are you sure you want to delete this assistant?')) {
            return;
        }

        try {
            const response = await fetch(`/agent/${agentId}/delete`, {
                method: 'POST'
            });

            const data = await response.json();
            if (data.success) {
                alert('Assistant deleted successfully!');
                clearForm();
                initializeAgents();
            } else {
                alert('Error deleting assistant: ' + data.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error deleting assistant');
        }
    });

    // Initialize page
    initializeAgents();
}); 