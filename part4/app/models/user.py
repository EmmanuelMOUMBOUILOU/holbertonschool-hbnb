import re
import uuid
from sqlalchemy.orm import relationship
from app.extensions import db, bcrypt
from app.models.base_model import BaseModel

class User(BaseModel, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = relationship('Place', backref='owner', lazy=True)
    reviews = relationship('Review', backref='author', lazy=True)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()

        # Validation
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email invalide")
        if len(first_name) > 50 or len(last_name) > 50:
            raise ValueError("Nom trop long (max 50 caractères)")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        # Hashage du mot de passe
        self.hash_password(password)

    def hash_password(self, password):
        """Hash le mot de passe avant de le stocker."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Vérifie si le mot de passe correspond au hash stocké."""
        return bcrypt.check_password_hash(self.password, password)
