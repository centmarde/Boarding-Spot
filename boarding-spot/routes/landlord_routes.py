from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import User, Room
import json

bp = Blueprint('landlord', __name__, url_prefix='/landlord')

@bp.route('/rooms', methods=['POST'])
@jwt_required()
def create_room():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'landlord':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    room = Room(
        landlord_id=current_user_id,
        title=data['title'],
        description=data['description'],
        price=data['price'],
        size=data.get('size'),
        location=data['location'],
        amenities=json.dumps(data.get('amenities', [])),
        safety_score=data.get('safety_score', 5.0),
        cleanliness_score=data.get('cleanliness_score', 5.0),
        accessibility_score=data.get('accessibility_score', 5.0),
        noise_level=data.get('noise_level', 5.0)
    )
    
    db.session.add(room)
    db.session.commit()
    
    return jsonify({'message': 'Room created successfully', 'room_id': room.id}), 201

@bp.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    room_data = []
    for room in rooms:
        try:
            amenities = json.loads(room.amenities) if room.amenities else []
        except json.JSONDecodeError:
            amenities = []  # Default to an empty list if JSON decoding fails

        room_data.append({
            'id': room.id,
            'title': room.title,
            'description': room.description,
            'created_at': room.created_at,
            'price': room.price,
            'size': room.size,
            'location': room.location,
            'amenities': amenities,
            'availability': room.availability,
            'safety_score': room.safety_score,
            'cleanliness_score': room.cleanliness_score,
            'accessibility_score': room.accessibility_score,
            'noise_level': room.noise_level
        })

    return jsonify(room_data)

@bp.route('/rooms/<int:room_id>', methods=['GET'])
def get_specific_room(room_id):
    room = Room.query.get(room_id)  # Fetch room by the specific ID
    if not room:
        return jsonify({'error': 'Room not found'}), 404  # Return error if the room does not exist
    
    try:
        amenities = json.loads(room.amenities) if room.amenities else []
    except json.JSONDecodeError:
        amenities = []  # Default to an empty list if JSON decoding fails

    room_data = {
        'id': room.id,
        'title': room.title,
        'description': room.description,
        'created_at': room.created_at,
        'price': room.price,
        'size': room.size,
        'location': room.location,
        'amenities': amenities,
        'availability': room.availability,
        'safety_score': room.safety_score,
        'cleanliness_score': room.cleanliness_score,
        'accessibility_score': room.accessibility_score,
        'noise_level': room.noise_level
    }

    return jsonify(room_data)


@bp.route('/rooms/<int:room_id>', methods=['POST'])
@jwt_required()
def update_room(room_id):
    current_user_id = get_jwt_identity()
    room = Room.query.get_or_404(room_id)
    
    # if room.landlord_id == current_user_id:
    #     return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    for key, value in data.items():
        if key == 'amenities':
            setattr(room, key, json.dumps(value))
        elif hasattr(room, key):
            setattr(room, key, value)
    
    db.session.commit()
    return jsonify({'message': 'Room updated successfully'})
