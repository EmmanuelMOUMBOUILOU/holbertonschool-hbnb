from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.services import facade
from app.models import Place

api = Namespace('places', description='Place operations')

# Related models
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String,
    'name': fields.String
})

user_model = api.model('PlaceUser', {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String
})

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True)
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        data = request.get_json()
        amenities = data.pop('amenities', None)
        current_user = get_jwt_identity()
        data["owner_id"] = current_user
        try:
            place = facade.create_place(data)
            if place.owner_id != current_user:
                return {'error': 'Unauthorized action'}, 403
            return {'id': place.id, 'title': place.title, 'description': place.description, 'price': place.price, 'latitude': place.latitude, 'longitude': place.longitude, 'owner_id': place.owner.id if place.owner else None}, 201
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        try:
            places = facade.get_list_places()
            return [{
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner.id if place.owner else None
            } for place in places], 200
        except Exception as e:
            print("🔥 ERREUR:", e)
            return {"error": str(e)}, 500

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return {'id': place.id, 'title': place.title, 'description': place.description, 'price': place.price, 'latitude': place.latitude, 'longitude': place.longitude, 'owner_id': place.owner.id if place.owner else None, 'amenities': [{'id': a.id, 'name': a.name} for a in place.amenities]}, 200

    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        data = request.get_json()
        current_user = get_jwt_identity()
        try:
            place = facade.update_place(place_id, data)
            if place.owner_id != current_user:
                return {'error': 'Unauthorized action'}, 403
            if not place:
                return {"error": "Place not found"}, 403
            return {"message": "Place updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 400
