from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import User, Room
import json
import os
from werkzeug.utils import secure_filename

bp = Blueprint('landlord', __name__, url_prefix='/landlord')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/rooms', methods=['POST'])
@jwt_required()
def create_room():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'landlord':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.form  # Use form to handle file uploads
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
    
    # Handle image upload
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        room.image_url = file_path  # Save the path to the image in the database
    
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
            'noise_level': room.noise_level,
            'image_url': room.image_url
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
        'noise_level': room.noise_level,
        'image_url': room.image_url
    }

    return jsonify(room_data)


@bp.route('/rooms/<int:room_id>', methods=['POST'])
@jwt_required()
def update_room(room_id):
    current_user_id = get_jwt_identity()
    room = Room.query.get_or_404(room_id)
    
   
    
    data = request.get_json()
    for key, value in data.items():
        if key == 'amenities':
            setattr(room, key, json.dumps(value))  # Store amenities as JSON string
        elif hasattr(room, key) and key != 'created_at':  # Skip created_at field
            setattr(room, key, value)
    
    db.session.commit()
    return jsonify({'message': 'Room updated successfully'})

@bp.route('/rooms/<int:room_id>/upload-image', methods=['POST'])
@jwt_required()
def upload_image(room_id):
    current_user_id = get_jwt_identity()
    room = Room.query.get_or_404(room_id)

    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Delete the old image if it exists
        if room.image_url and os.path.exists(room.image_url):
            os.remove(room.image_url)
        
        # Ensure that the file is not replaced if it already exists
        if not os.path.exists(file_path):
            file.save(file_path)
        
        room.image_url = file_path  # Update the room's image URL in the database
        db.session.commit()
        return jsonify({'message': 'Image uploaded successfully', 'image_url': room.image_url}), 200
    else:
        return jsonify({'error': 'Invalid image file'}), 400
