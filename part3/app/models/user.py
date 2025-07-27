import re
from app import db, bcrypt
import uuid
from datetime import datetime
from app.models.base_model import BaseModel
from .base_model import BaseModel
from sqlalchemy.orm import relationship


class User(BaseModel, db.Model):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    id = db.Column(db.Integer, primary_key=True)
    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)


    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email invalide")
        if len(first_name) > 50 or len(last_name) > 50:
            raise ValueError("Nom trop long (max 50 caractères)")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = password

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
