from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import User, Room, TenantPreference
import json
import numpy as np
from topsispy import topsis

bp = Blueprint('tenant', __name__, url_prefix='/tenant')

@bp.route('/preferences', methods=['POST'])
@jwt_required()
def set_preferences():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'tenant':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Delete existing preferences if any
    TenantPreference.query.filter_by(tenant_id=current_user_id).delete()
    
    preference = TenantPreference(
        tenant_id=current_user_id,
        max_price=data.get('max_price'),
        min_size=data.get('min_size'),
        preferred_location=data.get('preferred_location'),
        required_amenities=json.dumps(data.get('required_amenities', [])),
        safety_weight=data.get('safety_weight', 0.25),
        cleanliness_weight=data.get('cleanliness_weight', 0.25),
        accessibility_weight=data.get('accessibility_weight', 0.25),
        noise_level_weight=data.get('noise_level_weight', 0.25)
    )
    
    db.session.add(preference)
    db.session.commit()
    
    return jsonify({'message': 'Preferences saved successfully'})

@bp.route('/search', methods=['GET'])
@jwt_required()
def search_rooms():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'tenant':
        return jsonify({'error': 'Unauthorized'}), 403
    
    preference = TenantPreference.query.filter_by(tenant_id=current_user_id).first()
    if not preference:
        return jsonify({'error': 'Please set your preferences first'}), 400
    
    # Filter rooms based on basic criteria
    query = Room.query.filter_by(availability=True)
    
    if preference.max_price:
        query = query.filter(Room.price <= preference.max_price)
    if preference.min_size:
        query = query.filter(Room.size >= preference.min_size)
    if preference.preferred_location:
        query = query.filter(Room.location.ilike(f'%{preference.preferred_location}%'))
    
    rooms = query.all()
    if not rooms:
        return jsonify({'message': 'No rooms found matching your criteria'})
    
    # Prepare data for TOPSIS
    decision_matrix = np.array([[
        room.safety_score,
        room.cleanliness_score,
        room.accessibility_score,
        -room.noise_level,  # Negative because lower is better
    ] for room in rooms])
    
    weights = np.array([
        preference.safety_weight,
        preference.cleanliness_weight,
        preference.accessibility_weight,
        preference.noise_level_weight
    ])
    
    # All criteria are beneficial (1 for beneficial, 0 for non-beneficial)
    impacts = np.array([1, 1, 1, 1])
    
    # Calculate TOPSIS scores
    topsis_scores = topsis(decision_matrix, weights, impacts)
    
    # Sort rooms by TOPSIS score
    ranked_rooms = sorted(zip(rooms, topsis_scores), key=lambda x: x[1], reverse=True)
    
    return jsonify([{
        'id': room.id,
        'title': room.title,
        'description': room.description,
        'price': room.price,
        'size': room.size,
        'location': room.location,
        'amenities': json.loads(room.amenities),
        'safety_score': room.safety_score,
        'cleanliness_score': room.cleanliness_score,
        'accessibility_score': room.accessibility_score,
        'noise_level': room.noise_level,
        'topsis_score': float(score)
    } for room, score in ranked_rooms]) 