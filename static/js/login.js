document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('error-message');

    loginForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Get form data
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (data.success) {
                // Redirect to dashboard
                window.location.href = data.redirect;
            } else {
                // Show error message
                if (errorMessage) {
                    errorMessage.textContent = data.message || 'Invalid credentials';
                    errorMessage.style.display = 'block';
                } else {
                    alert(data.message || 'Invalid credentials');
                }
            }
        } catch (error) {
            console.error('Login error:', error);
            if (errorMessage) {
                errorMessage.textContent = 'An error occurred during login. Please try again.';
                errorMessage.style.display = 'block';
            } else {
                alert('An error occurred during login. Please try again.');
            }
        }
    });
});