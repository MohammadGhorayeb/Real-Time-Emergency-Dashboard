from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=True)  # Add location field

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID
    name = db.Column(db.String(100), nullable=False)  # Name of the location
    latitude = db.Column(db.Float, nullable=False)  # Latitude
    longitude = db.Column(db.Float, nullable=False)  # Longitude
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())  # Timestamp



