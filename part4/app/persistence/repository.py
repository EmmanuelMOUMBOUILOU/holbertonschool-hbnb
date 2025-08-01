from abc import ABC, abstractmethod
from app import db  # Instance SQLAlchemy (db)
from app.models import User, Place, Review, Amenity  # tes modèles


class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class SQLAlchemyRepository(Repository):
    def __init__(self, model, session=None):
        self.model = model
        self.session = session or db.session  # On accepte une session personnalisée ou on prend la session globale

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()

    def get(self, obj_id):
        return self.session.query(self.model).get(obj_id)

    def get_all(self):
        return self.session.query(self.model).all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            self.session.commit()
        return obj

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        attr = getattr(self.model, attr_name, None)
        if attr is None:
            return None
        return self.session.query(self.model).filter(attr == attr_value).first()


class UserRepository(SQLAlchemyRepository):
    def __init__(self, session=None):
        super().__init__(User, session)

    def get_user_by_email(self, email):
        return self.session.query(self.model).filter_by(email=email).first()
