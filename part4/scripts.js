/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

// Script pour la page de connexion (login.html)

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

// Script pour la page d'accueil (index.html)

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

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication(); // Démarre le processus
});

// Script pour la page de détails d'un lieu (place.html)

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

function checkAuthentication(placeId) {
  const token = getCookie('token');
  const addReviewSection = document.getElementById('add-review');

  if (!token) {
    addReviewSection.style.display = 'none';
  } else {
    addReviewSection.style.display = 'block';
  }

  // Même sans token, on affiche les détails publics du lieu
  fetchPlaceDetails(token, placeId);
}

async function fetchPlaceDetails(token, placeId) {
  try {
    const response = await fetch(`http://localhost:5001/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    });

    if (!response.ok) {
      throw new Error(`Erreur: ${response.status}`);
    }

    const place = await response.json();
    displayPlaceDetails(place);
  } catch (error) {
    console.error('Erreur lors de la récupération des détails du lieu :', error);
  }
}

function displayPlaceDetails(place) {
  const detailsSection = document.getElementById('place-details');
  detailsSection.innerHTML = '';  // Nettoyage

  const name = document.createElement('h2');
  name.textContent = place.name;

  const description = document.createElement('p');
  description.textContent = place.description;

  const price = document.createElement('p');
  price.textContent = `Prix: ${place.price} €`;

  const amenities = document.createElement("ul");
  place.amenities.forEach(amenity => {
      const li = document.createElement("li");
      li.textContent = amenity.name;
      amenities.appendChild(li);
  });

  const reviews = document.createElement("ul");
  place.reviews.forEach(review => {
      const li = document.createElement("li");
      li.textContent = `${review.user_name}: ${review.text}`;
      reviews.appendChild(li);
  });

  detailsSection.append(name, description, price, document.createElement("hr"), amenities, document.createElement("hr"), reviews);
}


document.addEventListener('DOMContentLoaded', () => {
  const placeId = getPlaceIdFromURL();
  if (placeId) {
    checkAuthentication(placeId);
  } else {
    alert("Aucun identifiant de lieu trouvé dans l'URL.");
  }
});

// Script pour la page d'ajout de lieu (add_review.html)

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        // Redirige vers la page d'accueil si non connecté
        window.location.href = 'index.html';
    }
    return token;  // retourne le token pour l'utiliser plus tard
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('place_id'); // Exemple : ?id=42
}

document.addEventListener('DOMContentLoaded', () => {
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();
    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review-text').value;
            await submitReview(token, placeId, reviewText);
        });
    }
});

async function submitReview(token, placeId, reviewText) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/reviews', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                text: reviewText
            })
        });

        handleResponse(response);
    } catch (error) {
        alert('Erreur lors de la soumission : ' + error.message);
    }
}

async function handleResponse(response) {
    if (response.ok) {
        alert('Avis envoyé avec succès !');
        document.getElementById('review-text').value = '';
    } else {
        const data = await response.json();
        alert(`Erreur : ${data.message || 'Échec de l’envoi'}`);
    }
}

