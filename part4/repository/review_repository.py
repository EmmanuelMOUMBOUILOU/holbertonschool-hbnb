from models.review import Review
from models import db

class ReviewRepository:
    def __init__(self, session=db.session):
        self.session = session

    def add(self, review):
        self.session.add(review)
        self.session.commit()

    def get(self, review_id):
        return self.session.query(Review).filter_by(id=review_id).first()

    def get_all(self):
        return self.session.query(Review).all()

    def update(self):
        self.session.commit()

    def delete(self, review):
        self.session.delete(review)
        self.session.commit()
