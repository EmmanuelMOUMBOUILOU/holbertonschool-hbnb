import uuid
from sqlalchemy.orm import relationship
from app.extensions import db
from app.models.base_model import BaseModel

class Amenity(BaseModel, db.Model):
    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False, unique=True)

    # Relation réciproque avec Place (Many-to-Many via place_amenity)
    places = relationship(
        'Place',
        secondary='place_amenity',  # Nom exact de la table d'association
        back_populates='amenities',
        lazy='subquery'
    )

    def __init__(self, name):
        super().__init__()
        if not name or len(name.strip()) == 0:
            raise ValueError("Nom requis")
        if len(name) > 50:
            raise ValueError("Nom trop long (max 50 caractères)")
        self.name = name.strip()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def __repr__(self):
        return f"<Amenity {self.name}>"
