from flask_restx import Api

# Objet API global
api = Api(
    title='HBnB API',
    version='1.0',
    description='API for the HBnB project (CRUD for users, places, reviews, etc.)',
    doc='/docs'  # Swagger UI accessible à /docs
)

# save namespaces
from .v1.reviews import api as reviews_ns
from .v1.users import api as users_ns
from .v1.places import api as places_ns
from .v1.amenities import api as amenities_ns
from .v1.auth import api as auth_ns


# root
api.add_namespace(users_ns, path="/api/v1/users")
api.add_namespace(places_ns, path="/api/v1/places")
api.add_namespace(reviews_ns, path="/api/v1/reviews")
api.add_namespace(amenities_ns, path="/api/v1/amenities")
api.add_namespace(auth_ns, path='/api/v1/auth')