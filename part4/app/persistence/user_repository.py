from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email: str):
        """Return user instance matching the email."""
        return self.session.query(User).filter_by(email=email).first()

    def get_by_id(self, user_id: str):
        """Return user by ID."""
        return self.session.query(User).filter_by(id=user_id).first()

    def get_all(self):
        """Return all users."""
        return self.session.query(User).all()

    def delete_by_id(self, user_id: str):
        """Delete user by ID."""
        user = self.get_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def update(self, user_id: str, data: dict):
        """Update user with new data."""
        user = self.get_by_id(user_id)
        if not user:
            return None
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        self.session.commit()
        return user
