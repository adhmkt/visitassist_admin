document.addEventListener('DOMContentLoaded', function () {
    // Get DOM elements with error checking
    const agentForm = document.getElementById('agentForm');
    const agentSelect = document.getElementById('agent-select');
    const deleteAgentBtn = document.getElementById('deleteAgentBtn');
    const searchInput = document.getElementById('agentSearch');
    const assistantWebsiteLink = document.getElementById('assistantWebsiteLink');

    // Check if required elements exist
    if (!agentForm || !agentSelect) {
        console.error('Required elements not found:', {
            agentForm: !!agentForm,
            agentSelect: !!agentSelect
        });
        return;
    }

    // Store all agents for search functionality
    let allAgents = [];
    let currentAgent = null;
    let filteredAgents = [];

    // Load agent details from server
    async function loadAgentDetails(agentId) {
        console.log('Loading agent details for:', agentId);
        try {
            const response = await fetch(`/agent/${agentId}`, {
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Agent details from server:', data);

            if (data.success && data.agent) {
                if (!data.agent.assistant_id) {
                    console.warn('Warning: Agent data is missing assistant_id:', data.agent);
                }
                currentAgent = data.agent;
                populateForm(currentAgent);
            } else {
                console.error('Invalid response format:', data);
                throw new Error(data.message || 'Failed to load agent details');
            }
        } catch (error) {
            console.error('Error loading agent details:', error);
            alert('Error loading assistant details. Please try again.');
        }
    }

    // Populate form with agent data
    function populateForm(agent) {
        console.log('Populating form with agent data:', agent);

        // Basic Information
        document.getElementById('assistant_id').value = agent.assistant_id || '';
        document.getElementById('name').value = agent.assistant_name || '';
        document.getElementById('description').value = agent.assistant_desc || '';
        document.getElementById('assistant_img_url').value = agent.assistant_img || '';
        document.getElementById('prompt').value = agent.assistant_instructions || '';

        // Configuration
        document.getElementById('type').value = agent.assistant_type || 'classic';
        document.getElementById('subtype').value = agent.subtype || 'subtype';

        // Additional Settings
        document.getElementById('functions').value = agent.assistant_functions || 'not_defined';
        document.getElementById('languages').value =
            typeof agent.assistant_languages === 'object'
                ? JSON.stringify(agent.assistant_languages, null, 2)
                : agent.assistant_languages || '';

        // Sponsor Information
        document.getElementById('sponsor_id').value = agent.sponsor_id || '';
        document.getElementById('sponsor_logo').value = agent.sponsor_logo || 'sponsor_default.png';
        document.getElementById('sponsor_url').value = agent.sponsor_url || 'https://apis-ia.com';

        // Update assistant website link if it exists
        if (assistantWebsiteLink && agent.sponsor_url) {
            assistantWebsiteLink.href = agent.sponsor_url;
        }

        // Update config if it exists
        const configField = document.getElementById('config');
        if (configField && agent.assistant_json) {
            configField.value = typeof agent.assistant_json === 'object'
                ? JSON.stringify(agent.assistant_json, null, 2)
                : agent.assistant_json;
        }

        console.log('Form populated successfully');
    }

    // Initialize agents data
    async function initializeAgents() {
        console.log('Initializing agents...');
        try {
            const response = await fetch('/agents', {
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Server response:', data);

            if (data.success && Array.isArray(data.agents)) {
                allAgents = data.agents;
                filteredAgents = [...allAgents];
                console.log(`Loaded ${allAgents.length} agents:`, allAgents);
                updateAgentSelect(filteredAgents);
            } else {
                throw new Error(data.message || 'Invalid response format');
            }
        } catch (error) {
            console.error('Error loading agents:', error);
            agentSelect.innerHTML = '<option value="">Error loading assistants</option>';
        }
    }

    // Update agent select dropdown
    function updateAgentSelect(agents) {
        console.log('Updating select with agents:', agents);
        if (!agentSelect) return;

        agentSelect.innerHTML = '<option value="">Choose an assistant...</option>';

        if (Array.isArray(agents) && agents.length > 0) {
            agents.forEach(agent => {
                if (agent?.assistant_id && agent?.assistant_name) {
                    const option = document.createElement('option');
                    option.value = agent.assistant_id;
                    option.textContent = agent.assistant_name;
                    agentSelect.appendChild(option);
                    console.log('Added option:', option.value, option.textContent);
                }
            });
        }
    }

    // Handle search functionality
    if (searchInput) {
        searchInput.addEventListener('input', function (e) {
            const searchTerm = e.target.value.toLowerCase().trim();
            console.log('Search term:', searchTerm);
            console.log('Available agents:', allAgents.length);

            if (searchTerm === '') {
                filteredAgents = [...allAgents];
            } else {
                filteredAgents = allAgents.filter(agent => {
                    const name = agent?.assistant_name?.toLowerCase() || '';
                    const match = name.includes(searchTerm);
                    console.log(`Checking "${name}" against "${searchTerm}":`, match);
                    return match;
                });
            }

            console.log(`Found ${filteredAgents.length} matches`);
            updateAgentSelect(filteredAgents);
        });
    }

    // Handle agent selection
    if (agentSelect) {
        agentSelect.addEventListener('change', function () {
            const selectedId = this.value;
            if (selectedId) {
                loadAgentDetails(selectedId);
            }
        });
    }

    // Initialize the page
    initializeAgents();
}); 