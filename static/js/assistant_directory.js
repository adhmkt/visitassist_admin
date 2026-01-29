// assistant_directory.js

document.addEventListener('DOMContentLoaded', function() {
    // Add click effect for assistant cards
    document.querySelectorAll('.assistant-card-link').forEach(function(card) {
        card.addEventListener('mousedown', function() {
            card.classList.add('active');
        });
        card.addEventListener('mouseup', function() {
            card.classList.remove('active');
        });
        card.addEventListener('mouseleave', function() {
            card.classList.remove('active');
        });
    });

    // Preview Assistant Modal
    window.previewAssistant = function(assistantId) {
        const modal = document.getElementById('previewModal');
        const content = document.getElementById('previewContent');
        content.innerHTML = '<div style="text-align:center;padding:2em;">Loading assistant preview...</div>';
        modal.style.display = 'block';
        fetch(`/api/assistants/${assistantId}`)
            .then(response => response.json())
            .then(data => {
                if (data.success && data.assistant) {
                    content.innerHTML = `
                        <h3>${data.assistant.assistant_name}</h3>
                        <p>${data.assistant.assistant_desc}</p>
                        <p><b>Type:</b> ${data.assistant.assistant_type}</p>
                    `;
                } else {
                    content.innerHTML = '<div style="color:red;">Failed to load assistant details.</div>';
                }
            })
            .catch(() => {
                content.innerHTML = '<div style="color:red;">Error loading assistant details.</div>';
            });
    };

    // Close modal
    document.querySelectorAll('.close-modal').forEach(function(btn) {
        btn.addEventListener('click', function() {
            document.getElementById('previewModal').style.display = 'none';
        });
    });

    // Close modal on outside click
    window.onclick = function(event) {
        const modal = document.getElementById('previewModal');
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };
});
