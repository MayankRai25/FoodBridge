from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    date_of_register = db.Column(db.DateTime, default=datetime.utcnow)

class NGO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    date_of_register = db.Column(db.DateTime, default=datetime.utcnow)

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    food_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(100), nullable=False)
    food_description = db.Column(db.String(200), nullable=False)
    pickup_address = db.Column(db.String(200), nullable=False)
    donation_date = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_by = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='pending')

