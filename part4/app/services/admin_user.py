from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.services.facade import get_user_by_email, create_user, update_user

api = Namespace('admin_users', path='/api/v1/users')

@api.route('/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        if get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        new_user = create_user(user_data)
        return {'message': 'User created', 'user': new_user.to_dict()}, 201

@api.route('/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        if email:
            existing_user = get_user_by_email(email)
            if existing_user and str(existing_user.id) != user_id:
                return {'error': 'Email already in use'}, 400

        updated_user = update_user(user_id, data)
        return {'message': 'User updated', 'user': updated_user.to_dict()}, 200
