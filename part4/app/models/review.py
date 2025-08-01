import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from app.extensions import db
from app.models.base_model import BaseModel

class Review(BaseModel, db.Model):
    __tablename__ = 'reviews'
    __table_args__ = (
        UniqueConstraint('user_id', 'place_id', name='uix_user_place_review'),
    )

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    place = relationship('Place', back_populates='reviews')
    user = relationship('User', back_populates='reviews')

    def __init__(self, text, rating, place, user):
        super().__init__()

        if not text:
            raise ValueError("Le texte de l'avis est requis")
        if not (1 <= rating <= 5):
            raise ValueError("La note doit être entre 1 et 5")

        # Import local pour éviter l'import circulaire
        from app.models.place import Place
        from app.models.user import User

        if not isinstance(place, Place):
            raise ValueError("Place invalide")
        if not isinstance(user, User):
            raise ValueError("Utilisateur invalide")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id
        }
