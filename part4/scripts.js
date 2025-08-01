/* 
  Fichier JS centralisé pour les pages login.html, index.html, place.html et add_review.html
*/

// ========== UTILITAIRES COMMUNS ==========

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id') || params.get('place_id');
}

// ========== PAGE DE CONNEXION ==========
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/; max-age=86400; SameSite=Lax`;
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

// ========== PAGE D'ACCUEIL ==========
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('places-list')) {
        const token = getCookie('token');
        checkAuthenticationIndex(token);
        setupPriceFilter();
    }
});

function checkAuthenticationIndex(token) {
    const loginLink = document.getElementById('login-link');
    if (!token) {
        if (loginLink) loginLink.style.display = 'inline-block';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

async function fetchPlaces(token) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/places', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            const data = await response.json();
            displayPlaces(data);
        } else {
            alert('Failed to fetch places: ' + response.statusText);
        }
    } catch (error) {
        alert('Error connecting to the API.');
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';
    places.forEach(place => {
        const card = document.createElement('div');
        card.classList.add('place-card');
        card.dataset.price = place.price_per_night;
        card.innerHTML = `
            <h3>${place.name}</h3>
            <p>Price: $${place.price_per_night}/night</p>
            <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
        `;
        placesList.appendChild(card);
    });
}

function setupPriceFilter() {
    const filter = document.getElementById('price-filter');
    if (!filter) return;
    filter.addEventListener('change', () => {
        const value = filter.value;
        const cards = document.querySelectorAll('.place-card');
        cards.forEach(card => {
            const price = parseFloat(card.dataset.price);
            card.style.display = (value === 'All' || price <= parseFloat(value)) ? 'block' : 'none';
        });
    });
}

// ========== PAGE DETAILS (place.html) ==========
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('place-details')) {
        const placeId = getPlaceIdFromURL();
        if (!placeId) return alert("Aucun identifiant de lieu trouvé dans l'URL.");
        const token = getCookie('token');
        checkPlaceAuthentication(token);
        fetchPlaceDetails(token, placeId);
    }
});

function checkPlaceAuthentication(token) {
    const section = document.getElementById('add-review');
    if (section) section.style.display = token ? 'block' : 'none';
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`http://localhost:5001/api/v1/places/${placeId}`, {
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });
        if (!response.ok) throw new Error(`Erreur: ${response.status}`);
        const place = await response.json();
        displayPlaceDetails(place);
    } catch (error) {
        alert('Erreur lors de la récupération du lieu.');
    }
}

function displayPlaceDetails(place) {
    const details = document.getElementById('place-details');
    details.innerHTML = '';
    const name = document.createElement('h2');
    name.textContent = place.name;
    const description = document.createElement('p');
    description.textContent = place.description;
    const price = document.createElement('p');
    price.textContent = `Prix: ${place.price} €`;

    const amenities = document.createElement('ul');
    place.amenities.forEach(a => {
        const li = document.createElement('li');
        li.textContent = a.name;
        amenities.appendChild(li);
    });

    const reviews = document.createElement('ul');
    place.reviews.forEach(r => {
        const li = document.createElement('li');
        li.textContent = `${r.user_name}: ${r.text}`;
        reviews.appendChild(li);
    });

    details.append(name, description, price, document.createElement('hr'), amenities, document.createElement('hr'), reviews);
}

// ========== PAGE D'AJOUT DE REVIEW ==========
document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        const token = getCookie('token');
        if (!token) return window.location.href = 'index.html';

        const placeId = getPlaceIdFromURL();
        if (!placeId) return alert("Identifiant de lieu manquant dans l'URL.");

        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const text = document.getElementById('review').value;
            const rating = document.getElementById('rating').value;
            await submitReview(token, placeId, text, rating);
        });
    }
});

async function submitReview(token, placeId, text, rating) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/reviews', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ place_id: placeId, text, rating: parseInt(rating) })
        });
        await handleReviewResponse(response);
    } catch (error) {
        alert('Erreur lors de la soumission : ' + error.message);
    }
}

async function handleReviewResponse(response) {
    if (response.ok) {
        alert('Avis envoyé avec succès !');
        document.getElementById('review').value = '';
    } else {
        const data = await response.json();
        alert(`Erreur : ${data.message || 'Échec de l’envoi'}`);
    }
}