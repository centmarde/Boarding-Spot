from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from extensions import db
from models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    user = User(
        email=data['email'],
        user_type=data['user_type']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'access_token': access_token,
        'user_type': user.user_type,
        'id': user.id
    }) 

@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [
        {
            'id': user.id,
            'email': user.email,
            'user_type': user.user_type
        }
        for user in users
    ]
    return jsonify(user_list), 200

@bp.route('/tenants', methods=['GET'])
def get_tenants():
    tenants = User.query.filter_by(user_type='tenant').all()
    tenant_list = [
        {
            'id': tenant.id,
            'email': tenant.email,
            'user_type': tenant.user_type
        }
        for tenant in tenants
    ]
    return jsonify(tenant_list), 200

@bp.route('/landlords', methods=['GET'])
def get_landlords():
    landlords = User.query.filter_by(user_type='landlord').all()
    landlord_list = [
        {
            'id': landlord.id,
            'email': landlord.email,
            'user_type': landlord.user_type
        }
        for landlord in landlords
    ]
    return jsonify(landlord_list), 200