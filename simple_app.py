from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Simple file-based storage
DATA_FILE = 'data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'donors': [], 'ngos': [], 'donations': [], 'contacts': []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/api/donors', methods=['POST'])
def register_donor():
    data = request.json
    db_data = load_data()
    
    donor = {
        'id': len(db_data['donors']) + 1,
        'name': data['name'],
        'email': data['email'],
        'phone_number': data['phone_number'],
        'address': data.get('address', ''),
        'date_of_register': datetime.now().isoformat()
    }
    
    db_data['donors'].append(donor)
    save_data(db_data)
    
    return jsonify({'message': 'Donor registered successfully'}), 201

@app.route('/api/ngos', methods=['POST'])
def register_ngo():
    data = request.json
    db_data = load_data()
    
    ngo = {
        'id': len(db_data['ngos']) + 1,
        'organization_name': data['organization_name'],
        'email': data['email'],
        'phone_number': data['phone_number'],
        'address': data.get('address', ''),
        'date_of_register': datetime.now().isoformat()
    }
    
    db_data['ngos'].append(ngo)
    save_data(db_data)
    
    return jsonify({'message': 'NGO registered successfully'}), 201

@app.route('/api/donations', methods=['POST'])
def create_donation():
    data = request.json
    db_data = load_data()
    
    donation = {
        'id': len(db_data['donations']) + 1,
        'name': data['name'],
        'phone_number': data['phone_number'],
        'quantity_of_food': data['quantity_of_food'],
        'donation_date': datetime.now().isoformat(),
        'accepted_by': None,
        'status': 'pending'
    }
    
    db_data['donations'].append(donation)
    save_data(db_data)
    
    return jsonify({'message': 'Donation created successfully'}), 201

@app.route('/api/donations', methods=['GET'])
def get_donations():
    db_data = load_data()
    return jsonify(db_data['donations'])

@app.route('/api/admin/donors', methods=['GET'])
def get_all_donors():
    db_data = load_data()
    return jsonify(db_data['donors'])

@app.route('/api/admin/ngos', methods=['GET'])
def get_all_ngos():
    db_data = load_data()
    return jsonify(db_data['ngos'])

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.json
    db_data = load_data()
    
    contact = {
        'id': len(db_data['contacts']) + 1,
        'name': data['name'],
        'email': data['email'],
        'message': data['message'],
        'contact_date': datetime.now().isoformat()
    }
    
    db_data['contacts'].append(contact)
    save_data(db_data)
    
    return jsonify({'message': 'Contact form submitted successfully'}), 201

@app.route('/')
def home():
    return '<h1>FoodBridge API is Running!</h1><p>Server is working correctly.</p>'

if __name__ == '__main__':
    print("Starting FoodBridge Flask Server...")
    print("Server will run on: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)