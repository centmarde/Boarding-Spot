from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'tenant' or 'landlord'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.Float)  # in square meters
    location = db.Column(db.String(200))
    amenities = db.Column(db.Text)  # JSON string of amenities
    availability = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Criteria for TOPSIS
    safety_score = db.Column(db.Float)  # 1-10
    cleanliness_score = db.Column(db.Float)  # 1-10
    accessibility_score = db.Column(db.Float)  # 1-10
    noise_level = db.Column(db.Float)  # 1-10 (lower is better)

class TenantPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    max_price = db.Column(db.Float)
    min_size = db.Column(db.Float)
    preferred_location = db.Column(db.String(200))
    required_amenities = db.Column(db.Text)  # JSON string of required amenities
    
    # Weights for TOPSIS criteria (0-1)
    safety_weight = db.Column(db.Float, default=0.25)
    cleanliness_weight = db.Column(db.Float, default=0.25)
    accessibility_weight = db.Column(db.Float, default=0.25)
    noise_level_weight = db.Column(db.Float, default=0.25)