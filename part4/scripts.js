/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('http://localhost:5000/api/v1/auth/login', {  // <-- adapte l'URL si besoin
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    // Stocker le token dans un cookie (expirant dans 1 jour)
                    document.cookie = `token=${data.access_token}; path=/; max-age=86400; SameSite=Lax`;

                    // Rediriger vers la page principale
                    window.location.href = 'index.html';
                } else {
                    const errorText = await response.text();
                    alert('Login failed: ' + errorText);
                }

            } catch (error) {
                console.error('Login error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }
});
