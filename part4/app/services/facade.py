from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository

from app.extensions import db

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository(db.session)
        self.place_repo = PlaceRepository(db.session)
        self.review_repo = ReviewRepository(db.session)
        self.amenity_repo = AmenityRepository(db.session)

    # ---------- Users ----------
    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        for key, value in user_data.items():
            if key == "password":
                user.hash_password(value)
            else:
                setattr(user, key, value)
        self.user_repo.update(user_id, user_data)
        return user

    def delete_user(self, user_id):
        success = self.user_repo.delete(user_id)
        return success

    # ---------- Amenities ----------
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        for key, value in amenity_data.items():
            setattr(amenity, key, value)
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)

    # ---------- Places ----------
    def create_place(self, data):
        required = [
            "name", "description", "city", "user_id",
            "price_by_night", "latitude", "longitude"
        ]
        for field in required:
            if field not in data:
                raise ValueError(f"Missing field: {field}")

        user = self.user_repo.get(data["user_id"])
        if not user:
            raise ValueError("Invalid user_id")

        amenities = []
        for amenity_id in data.get("amenity_ids", []):
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                amenities.append(amenity)

        price = float(data["price_by_night"])
        lat = float(data["latitude"])
        lng = float(data["longitude"])

        if price < 0:
            raise ValueError("Price must be non-negative")
        if not (-90 <= lat <= 90):
            raise ValueError("Invalid latitude")
        if not (-180 <= lng <= 180):
            raise ValueError("Invalid longitude")

        place = Place(
            name=data["name"],
            description=data["description"],
            city=data["city"],
            user=user,
            price_by_night=price,
            latitude=lat,
            longitude=lng,
            amenities=amenities
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def list_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        for key in [
            "name", "description", "city",
            "price_by_night", "latitude", "longitude"
        ]:
            if key in data:
                setattr(place, key, data[key])
        self.place_repo.update(place_id, data)
        return place

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    # ---------- Reviews ----------
    def create_review(self, review_data):
        user = self.user_repo.get(review_data["user_id"])
        place = self.place_repo.get(review_data["place_id"])
        if not user or not place:
            raise ValueError("User or Place not found")

        rating = review_data.get("rating")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [
            r for r in self.review_repo.get_all()
            if r.place_id == place_id
        ]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        for key, value in review_data.items():
            setattr(review, key, value)
        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)


# --- Fonctions globales exposées ---

_facade = HBnBFacade()

# Users
def create_user(user_data):
    return _facade.create_user(user_data)

def get_user(user_id):
    return _facade.get_user(user_id)

def get_user_by_email(email):
    return _facade.get_user_by_email(email)

def get_all_users():
    return _facade.get_all_users()

def update_user(user_id, user_data):
    return _facade.update_user(user_id, user_data)

def delete_user(user_id):
    return _facade.delete_user(user_id)

# Amenities
def create_amenity(amenity_data):
    return _facade.create_amenity(amenity_data)

def get_amenity(amenity_id):
    return _facade.get_amenity(amenity_id)

def get_all_amenities():
    return _facade.get_all_amenities()

def update_amenity(amenity_id, amenity_data):
    return _facade.update_amenity(amenity_id, amenity_data)

def delete_amenity(amenity_id):
    return _facade.delete_amenity(amenity_id)

# Places
def create_place(data):
    return _facade.create_place(data)

def get_place(place_id):
    return _facade.get_place(place_id)

def list_places():
    return _facade.list_places()

def update_place(place_id, data):
    return _facade.update_place(place_id, data)

def delete_place(place_id):
    return _facade.delete_place(place_id)

# Reviews
def create_review(review_data):
    return _facade.create_review(review_data)

def get_review(review_id):
    return _facade.get_review(review_id)

def get_all_reviews():
    return _facade.get_all_reviews()

def get_reviews_by_place(place_id):
    return _facade.get_reviews_by_place(place_id)

def update_review(review_id, review_data):
    return _facade.update_review(review_id, review_data)

def delete_review(review_id):
    return _facade.delete_review(review_id)
