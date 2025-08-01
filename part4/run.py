from app import create_app
from app.extensions import db
from app.models import User, Place, Review, Amenity, place_amenity  # importe tous les modèles

app = create_app()

def setup_database():
    with app.app_context():
        # Création des tables si elles n'existent pas déjà
        db.create_all()
        print("✔️  Toutes les tables ont été créées.")

if __name__ == '__main__':
    setup_database()
    app.run(host='0.0.0.0', port=5000, debug=True)
