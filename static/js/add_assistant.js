document.addEventListener('DOMContentLoaded', function () {
    const addAssistantForm = document.getElementById('addAssistantForm');
    const assistantIdInput = document.getElementById('assistant_id');
    const promptInput = document.getElementById('prompt');
    const languagesSelect = document.getElementById('languages');

    // Store the default instructions
    const defaultInstructions = promptInput.value;

    // Function to update destination in instructions
    function updateDestination(destination) {
        let instructions = promptInput.value;
        instructions = instructions.replace(/^Destination:.*$/m, `Destination: ${destination}`);
        promptInput.value = instructions;
    }

    // Reset instructions to default
    function resetInstructions() {
        promptInput.value = defaultInstructions;
    }

    // Validate assistant ID format
    assistantIdInput.addEventListener('input', function () {
        const value = this.value;
        const isValid = /^[a-zA-Z0-9_-]+$/.test(value);

        if (!isValid && value !== '') {
            this.setCustomValidity('Assistant ID can only contain letters, numbers, hyphens, and underscores');
        } else {
            this.setCustomValidity('');
        }
    });

    // Auto-generate assistant ID from name
    document.getElementById('name').addEventListener('input', function () {
        if (!assistantIdInput.value) {
            const suggestedId = this.value
                .toLowerCase()
                .replace(/[^a-z0-9]+/g, '-')
                .replace(/^-+|-+$/g, '');
            assistantIdInput.value = suggestedId;
        }
    });

    // Handle form submission
    addAssistantForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        console.log('Form submission started');

        // Validate that at least one language is selected
        if (languagesSelect.selectedOptions.length === 0) {
            alert('Please select at least one language');
            return;
        }

        // Get selected languages and create the languages structure
        const selectedLanguages = Array.from(languagesSelect.selectedOptions).map(option => {
            return JSON.parse(option.value);
        });

        const formData = {
            assistant_id: document.getElementById('assistant_id').value,
            assistant_name: document.getElementById('name').value,
            assistant_desc: document.getElementById('description').value,
            assistant_instructions: document.getElementById('prompt').value,
            assistant_type: document.getElementById('type').value,
            assistant_img: document.getElementById('assistant_img').value,
            sponsor_id: document.getElementById('sponsor_id').value || null,
            assistant_questions: {},
            assistant_functions: document.getElementById('functions').value,
            assistant_languages: {
                languages: selectedLanguages
            },
            subtype: document.getElementById('subtype').value,
            sponsor_logo: document.getElementById('sponsor_logo').value || 'sponsor_default.png',
            sponsor_url: document.getElementById('sponsor_url').value || 'https://apis-ia.com'
        };

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
                alert('Assistant created successfully!');
                // Redirect to edit page for the new assistant
                window.location.href = `/edit-agent?id=${data.agent.assistant_id}`;
            } else {
                console.error('Error creating assistant:', data.message);
                alert('Error creating assistant: ' + data.message);
            }
        } catch (error) {
            console.error('Error submitting form:', error);
            alert('Error creating assistant');
        }
    });
}); 