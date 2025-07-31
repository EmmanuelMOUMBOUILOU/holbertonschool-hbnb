from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from flask_bcrypt import Bcrypt

api = Namespace('users', description='User operations')
bcrypt = Bcrypt()

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        if new_user.password:
            new_user.password = bcrypt.generate_password_hash(new_user.password).decode('utf-8')
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email, 'password': new_user.password}, 201

    @api.response(200, 'OK')
    def get(self):
        users = facade.get_all_users()
        return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.response(200, 'OK')
    @api.response(404, 'Not found')
    @api.response(400, 'Bad Request')
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        user = facade.get_user(user_id)
        if user is None:
            return {'error': 'User not found'}, 404

        current_user = facade.get_user(current_user_id)

        if current_user.id != user.id and not getattr(current_user, "is_admin", False):
            return {'error': 'Unauthorized action.'}, 403

        user_data = api.payload

        if not getattr(current_user, "is_admin", False):
            user_data.pop("email", None)
            user_data.pop("password", None)

        if "password" in user_data:
            user_data["password"] = bcrypt.generate_password_hash(user_data["password"]).decode('utf-8')

        updated_user = facade.update_user(user_id, user_data)

        return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email}, 200
