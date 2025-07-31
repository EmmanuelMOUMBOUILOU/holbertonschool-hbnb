from models.place import Place
from models import db

class PlaceRepository:
    def __init__(self, session=db.session):
        self.session = session

    def add(self, place):
        self.session.add(place)
        self.session.commit()

    def get(self, place_id):
        return self.session.query(Place).filter_by(id=place_id).first()

    def get_all(self):
        return self.session.query(Place).all()

    def update(self):
        self.session.commit()

    def delete(self, place):
        self.session.delete(place)
        self.session.commit()
