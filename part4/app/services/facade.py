from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

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

    def put_update_users(self, user_id):
        return self.user_repo.put(user_id)

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
        self.amenity_repo.update()
        return amenity

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

        if float(data["price_by_night"]) < 0:
            raise ValueError("Price must be non-negative")
        if not (-90 <= float(data["latitude"]) <= 90):
            raise ValueError("Invalid latitude")
        if not (-180 <= float(data["longitude"]) <= 180):
            raise ValueError("Invalid longitude")

        place = Place(
            name=data["name"],
            description=data["description"],
            city=data["city"],
            user=user,
            price_by_night=float(data["price_by_night"]),
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"]),
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
        self.place_repo.update()
        return place

    # ---------- Reviews ----------
    def create_review(self, review_data):
        user = self.user_repo.get(review_data["user_id"])
        place = self.place_repo.get(review_data["place_id"])
        if not user or not place:
            raise ValueError("User or Place not found")

        rating = review_data.get("rating")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

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
        self.review_repo.update()
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review)
        return True
