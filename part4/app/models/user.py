import re
import uuid
from sqlalchemy.orm import relationship, validates
from app.extensions import db, bcrypt
from app.models.base_model import BaseModel

class User(BaseModel, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # Relations
    places = relationship('Place', back_populates='owner', lazy='dynamic')
    reviews = relationship('Review', back_populates='user', lazy='dynamic')

    def __init__(self, first_name=None, last_name=None, email=None, password=None, is_admin=False):
        super().__init__()

        if not first_name or not last_name or not email or not password:
            raise ValueError("Tous les champs (prénom, nom, email, mot de passe) sont requis")

        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip().lower()
        self.is_admin = is_admin
        self.hash_password(password)

    @validates('email')
    def validate_email(self, key, email):
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email invalide")
        return email.lower()

    @validates('first_name', 'last_name')
    def validate_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError(f"{key} invalide ou trop long (max 50 caractères)")
        return value.strip()

    def hash_password(self, password):
        """Hash le mot de passe avant de le stocker"""
        if not password or len(password) < 6:
            raise ValueError("Le mot de passe doit contenir au moins 6 caractères")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Vérifie si le mot de passe correspond au hash stocké"""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Méthode utilitaire pour exposer les données utilisateur (sans mot de passe)"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }

    def __repr__(self):
        return f"<User {self.email}>"
