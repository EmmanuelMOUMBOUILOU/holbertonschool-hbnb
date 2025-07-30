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



document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    setupPriceFilter();
});

// Récupère le cookie JWT
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Affiche ou cache le lien login
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        loginLink.style.display = 'inline-block'; // Affiche le lien
    } else {
        loginLink.style.display = 'none'; // Masque le lien
        fetchPlaces(token); // On récupère les lieux si connecté
    }
}

// Requête pour récupérer les lieux
async function fetchPlaces(token) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/places', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            displayPlaces(data);
        } else {
            alert('Failed to fetch places: ' + response.statusText);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        alert('Error connecting to the API.');
    }
}

// Affiche les lieux dynamiquement
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = ''; // Nettoie la liste actuelle

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.classList.add('place-card');
        placeCard.dataset.price = place.price_per_night; // utile pour le filtrage

        placeCard.innerHTML = `
            <h3>${place.name}</h3>
            <p>Price: $${place.price_per_night}/night</p>
            <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
        `;

        placesList.appendChild(placeCard);
    });
}

// Met en place le filtre de prix
document.getElementById('price-filter').addEventListener('change', (event) => {
    const selectedValue = event.target.value;
    const placeItems = document.querySelectorAll('.place-card');

    placeItems.forEach(place => {
        const price = parseFloat(place.dataset.price); // récupère le prix stocké dans l'attribut data-price

        // Affiche tous les lieux si "Tous" est sélectionné
        if (selectedValue === 'All' || price <= parseFloat(selectedValue)) {
            place.style.display = 'block';
        } else {
            place.style.display = 'none';
        }
    });
});

