from flask import request, jsonify
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.v1.views import api
from models import facade
from models.user import User
from extensions import bcrypt

@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()
        email = data.get('email')
        if not email:
            return {'error': 'Email is required'}, 400

        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        user = User(**data)
        facade.save_user(user)
        return {'message': 'User created successfully'}, 201


@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = request.get_json()
        email = data.get('email')
        if email:
            existing = facade.get_user_by_email(email)
            if existing and existing.id != user.id:
                return {'error': 'Email already in use'}, 400
            user.email = email

        if 'password' in data:
            user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']

        facade.save_user(user)
        return {'message': 'User updated'}, 200
