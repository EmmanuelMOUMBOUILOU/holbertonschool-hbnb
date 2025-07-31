import uuid
from sqlalchemy.orm import relationship
from app.extensions import db  # Import depuis extensions pour éviter les cercles
from app.models.base_model import BaseModel

# Table d'association many-to-many entre places et amenities
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel, db.Model):
    __tablename__ = 'places'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    owner = relationship('User', backref='places')

    reviews = relationship('Review', backref='place', lazy=True)

    amenities = relationship('Amenity', secondary=place_amenity,
                             backref=db.backref('places', lazy='dynamic'),
                             lazy='subquery')

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        if not title or len(title) > 128:
            raise ValueError("Titre requis ou trop long (max 128 caractères)")
        if price <= 0:
            raise ValueError("Prix invalide")
        if latitude is not None and not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude invalide")
        if longitude is not None and not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude invalide")
        if not owner:
            raise ValueError("Propriétaire requis")

        # Import local pour éviter import circulaire
        from app.models.user import User
        if not isinstance(owner, User):
            raise ValueError("Propriétaire invalide")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

    def add_review(self, review):
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "user_id": self.user_id
        }
