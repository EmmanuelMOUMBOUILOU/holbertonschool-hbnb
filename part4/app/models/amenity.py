import uuid
from app.extensions import db  # Utiliser un module dédié aux extensions pour éviter circular import
from app.models.base_model import BaseModel

class Amenity(BaseModel, db.Model):
    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError("Nom requis ou trop long (max 50 caractères)")
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
