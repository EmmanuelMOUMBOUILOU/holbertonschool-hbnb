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
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    places = relationship('Place', back_populates='owner', lazy='dynamic')
    reviews = relationship('Review', back_populates='user', lazy='dynamic')

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.hash_password(password)

    @validates('email')
    def validate_email(self, key, email):
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email invalide")
        return email

    @validates('first_name', 'last_name')
    def validate_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError(f"{key} invalide ou trop long (max 50 caractères)")
        return value

    def hash_password(self, password):
        """Hash le mot de passe avant de le stocker."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Vérifie si le mot de passe correspond au hash stocké."""
        return bcrypt.check_password_hash(self.password, password)
