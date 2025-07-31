from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.v1.views import api
from models import facade

@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        data = request.get_json()
        if 'name' in data:
            place.name = data['name']
        if 'description' in data:
            place.description = data['description']

        facade.save_place(place)
        return {'message': 'Place updated'}, 200
