from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place
from app import db
from .base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place: Place, user: User):
        super().__init__()
        if not text:
            raise ValueError("Le texte de l'avis est requis")
        if not (1 <= rating <= 5):
            raise ValueError("La note doit être entre 1 et 5")
        if not isinstance(place, Place):
            raise ValueError("Place invalide")
        if not isinstance(user, User):
            raise ValueError("Utilisateur invalide")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
        }
