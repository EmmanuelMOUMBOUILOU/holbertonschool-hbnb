Bien sûr ! Pour t’aider au mieux, je vais te faire un README clair et complet pour ton projet HBnB (avec JWT, API Flask, pages HTML, gestion des lieux, avis, etc.) incluant :

* Description du projet
* Prérequis
* Installation
* Lancement de l’application
* Identifiants de test (login) pour chaque rôle/utilisateur
* Fonctionnalités principales / tâches réalisées
* Comment tester chaque fonctionnalité (avec exemples curl ou instructions)
* Notes complémentaires / conseils pour faciliter l’accès et les tests

---

# README - Projet HBnB (Hébergement de type Airbnb)

---

## Description

Ce projet est une application web de gestion de locations immobilières (HBnB), inspirée d’Airbnb.
L’application est composée :

* D’une API REST sécurisée avec Flask, utilisant JWT (JSON Web Tokens) pour l’authentification et la gestion des rôles (utilisateurs, admins).
* D’une interface front-end en HTML/CSS/JavaScript permettant de consulter les lieux, se connecter, ajouter des avis, etc.
* D’un système complet de gestion des utilisateurs, lieux, équipements (amenities), et avis.

L’objectif est d’apprendre à intégrer une API sécurisée avec JWT, gérer des ressources REST, et construire une interface utilisateur dynamique.

---

## Prérequis

* Python 3.9+
* Pip
* Virtualenv recommandé
* MySQL (configuré avec une base de données vide prête à l’emploi)
* Navigateurs modernes (Chrome, Firefox, Edge)

---

## Installation

1. **Cloner le dépôt :**

```bash
git clone https://github.com/EmmanuelMOUMBOUILOU/holbertonschool-hbnb.git
cd holbertonschool-hbnb
```

2. **Créer un environnement virtuel et installer les dépendances :**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configurer la base de données :**

* Créer une base MySQL nommée `hbnb_db`
* Modifier le fichier de configuration `config.py` (ou `.env`) pour adapter les paramètres de connexion à ta base (hôte, user, mot de passe)

4. **Initialiser la base de données et les tables :**

```bash
flask db upgrade  # ou exécuter le script de création des tables selon le projet
```

---

## Lancement de l’application

Lancer le serveur Flask :

```bash
flask run
```

L’application sera accessible à l’adresse : `http://localhost:5000`

---

## Identifiants de test (login)

| Rôle        | Email                                           | Mot de passe        | Description                     |
| ----------- | ---------------------------------------------   | ------------------- | ------------------------------- |
| Admin       | [admin@example.com](mailto:admin@example.com)   | AdminPass123        | Utilisateur avec droits admin   |
| Utilisateur | [john.doe@gmail.com](mailto:john.doe@gmail.com) | jesuisunecornichon  | Utilisateur standard            |

---

## Fonctionnalités principales

* **Authentification JWT** : login et génération de token
* **Consultation des lieux** : affichage liste et détails
* **Création, modification et suppression de lieux** (selon rôle et propriété)
* **Ajout d’avis aux lieux**
* **Gestion des équipements (amenities)**
* **Pages front-end : login, index, place, add\_review**
* **Gestion des rôles : accès sécurisé aux ressources selon JWT**

---

## Comment tester

### 1. Se connecter (login)

Envoyer une requête POST à `/api/login` avec un JSON :

```json
{
  "email": "user1@example.com",
  "password": "UserPass123"
}
```

Réponse :

```json
{
  "access_token": "jwt-token-ici",
  "user": {
    "id": 1,
    "email": "user1@example.com",
    "is_admin": false
  }
}
```

---

### 2. Utiliser le token pour accéder aux endpoints sécurisés

Exemple pour obtenir la liste des lieux :

```bash
curl -H "Authorization: Bearer jwt-token-ici" http://localhost:5000/api/places
```

---

### 3. Ajouter un lieu (Admin ou propriétaire)

```bash
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer jwt-token-ici" \
     -d '{"name": "Nouvelle maison", "description": "Belle maison", "price": 120}' \
     http://localhost:5000/api/places
```

---

### 4. Ajouter un avis

Depuis la page `add_review.html`, remplir le formulaire et envoyer l’avis via le script JS qui utilise le token stocké dans `localStorage`.

---

### 5. Modifier ou supprimer un lieu ou un avis

Seul l’admin ou le propriétaire peut modifier/supprimer.

---

## Notes & conseils

* Pour faciliter les tests, le frontend stocke le JWT dans `localStorage`. Pour simuler en curl, récupérer ce token via login puis l’utiliser dans l’en-tête Authorization.
* Les rôles et droits sont gérés côté serveur via JWT et décorateurs `@jwt_required()`.
* Les utilisateurs peuvent consulter tous les lieux et avis, mais seuls les admins/propriétaires peuvent modifier ou supprimer.
* Pour créer rapidement des comptes, une route admin d’init peut être prévue (à activer uniquement en dev).

---

## Tests automatisés (exemples)

Voici quelques commandes curl pour tester les principales fonctionnalités :

* **Login admin :**

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "admin@example.com", "password": "AdminPass123"}' \
     http://localhost:5000/api/login
```

* **Lister lieux (avec token) :**

```bash
curl -H "Authorization: Bearer <token>" http://localhost:5000/api/places
```

* **Ajouter lieu (admin) :**

```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <token>" \
     -d '{"name":"Maison test","description":"Test","price":100}' \
     http://localhost:5000/api/places
```

* **Ajouter avis :**

```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <token>" \
     -d '{"text":"Super endroit!","rating":5,"place_id":1}' \
     http://localhost:5000/api/reviews
```

---

Si tu veux, je peux te générer un fichier `README.md` complet prêt à l’usage. Veux-tu ?
