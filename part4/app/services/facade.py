from app.models.user import User
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.persistence.repository import UserRepository
from repository.place_repository import PlaceRepository
from repository.review_repository import ReviewRepository
from repository.amenity_repository import AmenityRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)  # Switched to SQLAlchemyRepository
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

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

    
    def create_amenity(self, amenity_data):
        # Placeholder for logic to create an amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        return self.all_amenity_repo.get(amenity)

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        amenity = amenity.get_by_id(amenity_id)
        if not review:
            return None
        for key, value in amenity_data.items():
            setattr(review, key, value)
        amenity.save()
        return amenity

    def create_place(self, data):
        # Valider les attributs requis
        required = [
            "name", "description", "city", "user_id",
            "price_by_night", "latitude", "longitude"
        ]

        for field in required:
            if field not in data:
                raise ValueError(f"Missing field: {field}")

        # Récupérer l'utilisateur propriétaire
        user = self.repo.get("User", data["user_id"])
        if not user:
            raise ValueError("Invalid user_id")

        # Récupérer les amenities s'ils sont fournis
        amenities = []
        for amenity_id in data.get("amenity_ids", []):
            amenity = self.repo.get("Amenity", amenity_id)
            if amenity:
                amenities.append(amenity)

        # Validation de base
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
        self.repo.add("Place", place)
        return place

    def get_place(self, place_id):
        return self.repo.get("Place", place_id)

    def list_places(self):
        return self.repo.all("Place")

    def update_place(self, place_id, data):
        place = self.repo.get("Place", place_id)
        if not place:
            return None

        for key in [
            "name", "description", "city",
            "price_by_night", "latitude", "longitude"
        ]:
            if key in data:
                setattr(place, key, data[key])
        return place

    def create_review(self, review_data):
        user = User.get_by_id(review_data["user_id"])
        place = Place.get_by_id(review_data["place_id"])

        if not user or not place:
            raise ValueError("User or Place not found")

        rating = review_data.get("rating")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        review = Review(**review_data)
        review.save()
        return review

    def get_review(self, review_id):
        return Review.get_by_id(review_id)

    def get_all_reviews(self):
        return Review.all()

    def get_reviews_by_place(self, place_id):
        place = Place.get_by_id(place_id)
        if not place:
            raise ValueError("Place not found")
        return [r for r in Review.all() if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = Review.get_by_id(review_id)
        if not review:
            return None
        for key, value in review_data.items():
            setattr(review, key, value)
        review.save()
        return review

    def delete_review(self, review_id):
        review = Review.get_by_id(review_id)
        if not review:
            return None
        review.delete()
        return True
