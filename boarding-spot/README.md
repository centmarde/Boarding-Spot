# Boarding Spot API

A Flask-based API server for matching tenants with rental rooms using TOPSIS algorithm for preference-based recommendations.

## Features

- JWT Authentication
- Landlord and Tenant user types
- Room management for landlords
- Preference-based room search for tenants
- TOPSIS algorithm for room ranking based on multiple criteria

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables (optional):
```bash
export SECRET_KEY=your-secret-key
export JWT_SECRET_KEY=your-jwt-secret
export DATABASE_URL=your-database-url
```

4. Run the server:
```bash
python app.py
```

## API Endpoints

### Authentication
- POST `/auth/register` - Register new user (landlord/tenant)
- POST `/auth/login` - Login and get JWT token

### Landlord Routes
- POST `/landlord/rooms` - Create a new room
- GET `/landlord/rooms` - Get all rooms owned by landlord
- PUT `/landlord/rooms/<room_id>` - Update room details

### Tenant Routes
- POST `/tenant/preferences` - Set room preferences
- GET `/tenant/search` - Search and rank rooms based on preferences

## Testing with Postman

1. Register a user (landlord/tenant)
2. Login to get the JWT token
3. Use the JWT token in the Authorization header for all protected routes:
   `Authorization: Bearer <your-token>`

### Example Requests

#### Register User
```json
POST /auth/register
{
    "email": "user@example.com",
    "password": "password123",
    "user_type": "landlord"
}
```

#### Create Room (Landlord)
```json
POST /landlord/rooms
{
    "title": "Cozy Studio",
    "description": "Modern studio apartment",
    "price": 1000,
    "size": 30,
    "location": "Downtown",
    "amenities": ["wifi", "ac", "parking"],
    "safety_score": 8.5,
    "cleanliness_score": 9.0,
    "accessibility_score": 7.5,
    "noise_level": 3.0
}
```

#### Set Preferences (Tenant)
```json
POST /tenant/preferences
{
    "max_price": 1200,
    "min_size": 25,
    "preferred_location": "Downtown",
    "required_amenities": ["wifi"],
    "safety_weight": 0.3,
    "cleanliness_weight": 0.3,
    "accessibility_weight": 0.2,
    "noise_level_weight": 0.2
}
``` 