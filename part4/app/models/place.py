import uuid
from sqlalchemy.orm import relationship, validates
from app.extensions import db
from app.models.base_model import BaseModel

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
    owner = relationship('User', back_populates='places')

    reviews = relationship('Review', back_populates='place', lazy='select')

    amenities = relationship(
        'Amenity',
        secondary=place_amenity,
        back_populates='places',
        lazy='subquery'
    )

    def __init__(self, title, description, price, latitude=None, longitude=None, owner=None):
        super().__init__()

        if not title or len(title) > 128:
            raise ValueError("Titre requis ou trop long (max 128 caractères)")
        if price is None or price <= 0:
            raise ValueError("Prix invalide")
        if latitude is not None and not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude invalide")
        if longitude is not None and not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude invalide")
        if not owner:
            raise ValueError("Propriétaire requis")

        from app.models.user import User
        if not isinstance(owner, User):
            raise ValueError("Propriétaire invalide")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    @validates('title')
    def validate_title(self, key, value):
        if not value or len(value) > 128:
            raise ValueError("Titre requis ou trop long (max 128 caractères)")
        return value

    @validates('price')
    def validate_price(self, key, value):
        if value is None or value <= 0:
            raise ValueError("Prix invalide")
        return value

    @validates('latitude')
    def validate_latitude(self, key, value):
        if value is not None and not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude invalide")
        return value

    @validates('longitude')
    def validate_longitude(self, key, value):
        if value is not None and not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude invalide")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "user_id": self.user_id,
            "amenities": [amenity.id for amenity in self.amenities],
            # Pour les reviews, tu peux aussi faire [review.to_dict() for review in self.reviews] si besoin
        }
