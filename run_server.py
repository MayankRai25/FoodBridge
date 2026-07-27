from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# File to store data
DATA_FILE = 'foodbridge_data.json'

def get_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'donors': [], 'ngos': [], 'donations': []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def home():
    return '<h1>FoodBridge Server Running!</h1><p>Server is working at http://localhost:5000</p>'

@app.route('/api/donors', methods=['POST'])
def register_donor():
    try:
        data = request.json
        db_data = get_data()
        
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ngos', methods=['POST'])
def register_ngo():
    try:
        data = request.json
        db_data = get_data()
        
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/donors', methods=['GET'])
def get_all_donors():
    db_data = get_data()
    return jsonify(db_data['donors'])

@app.route('/api/admin/ngos', methods=['GET'])
def get_all_ngos():
    db_data = get_data()
    return jsonify(db_data['ngos'])

@app.route('/api/donations', methods=['GET'])
def get_donations():
    db_data = get_data()
    return jsonify(db_data['donations'])

@app.route('/admin')
def admin_panel():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>FoodBridge Admin Panel</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #0288d1; text-align: center; }
        .stats { display: flex; gap: 20px; margin: 20px 0; }
        .stat-card { background: #0288d1; color: white; padding: 20px; border-radius: 8px; flex: 1; text-align: center; }
        .tabs { display: flex; gap: 10px; margin: 20px 0; }
        .tab-btn { background: #0288d1; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
        .tab-btn.active { background: #01579b; }
        .section { display: none; background: white; padding: 20px; border-radius: 8px; }
        .section.active { display: block; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #0288d1; color: white; }
        .refresh-btn { background: #4CAF50; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🍽️ FoodBridge Admin Panel</h1>
        
        <div class="stats">
            <div class="stat-card">
                <h3>Total Donors</h3>
                <p id="donorCount">0</p>
            </div>
            <div class="stat-card">
                <h3>Total NGOs</h3>
                <p id="ngoCount">0</p>
            </div>
            <div class="stat-card">
                <h3>Total Donations</h3>
                <p id="donationCount">0</p>
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab-btn active" onclick="showTab('donors')">👥 Donors</button>
            <button class="tab-btn" onclick="showTab('ngos')">🏢 NGOs</button>
            <button class="tab-btn" onclick="showTab('donations')">🍽️ Donations</button>
        </div>
        
        <div id="donors" class="section active">
            <h2>Registered Donors</h2>
            <button class="refresh-btn" onclick="loadDonors()">Refresh</button>
            <table id="donorsTable">
                <thead>
                    <tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Address</th><th>Registration Date</th></tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
        
        <div id="ngos" class="section">
            <h2>Registered NGOs</h2>
            <button class="refresh-btn" onclick="loadNGOs()">Refresh</button>
            <table id="ngosTable">
                <thead>
                    <tr><th>ID</th><th>Organization</th><th>Email</th><th>Phone</th><th>Address</th><th>Registration Date</th></tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
        
        <div id="donations" class="section">
            <h2>Food Donations</h2>
            <button class="refresh-btn" onclick="loadDonations()">Refresh</button>
            <table id="donationsTable">
                <thead>
                    <tr><th>ID</th><th>Donor</th><th>Phone</th><th>Food Details</th><th>Date</th><th>Status</th></tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
    </div>
    
    <script>
        function showTab(tabName) {
            document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            if (tabName === 'donors') loadDonors();
            else if (tabName === 'ngos') loadNGOs();
            else if (tabName === 'donations') loadDonations();
        }
        
        async function loadDonors() {
            try {
                const response = await fetch('/api/admin/donors');
                const donors = await response.json();
                const tbody = document.querySelector('#donorsTable tbody');
                tbody.innerHTML = donors.map(d => `
                    <tr>
                        <td>${d.id}</td>
                        <td>${d.name}</td>
                        <td>${d.email}</td>
                        <td>${d.phone_number}</td>
                        <td>${d.address || 'Not provided'}</td>
                        <td>${new Date(d.date_of_register).toLocaleDateString()}</td>
                    </tr>
                `).join('');
                document.getElementById('donorCount').textContent = donors.length;
            } catch (error) {
                console.error('Error loading donors:', error);
            }
        }
        
        async function loadNGOs() {
            try {
                const response = await fetch('/api/admin/ngos');
                const ngos = await response.json();
                const tbody = document.querySelector('#ngosTable tbody');
                tbody.innerHTML = ngos.map(n => `
                    <tr>
                        <td>${n.id}</td>
                        <td>${n.organization_name}</td>
                        <td>${n.email}</td>
                        <td>${n.phone_number}</td>
                        <td>${n.address || 'Not provided'}</td>
                        <td>${new Date(n.date_of_register).toLocaleDateString()}</td>
                    </tr>
                `).join('');
                document.getElementById('ngoCount').textContent = ngos.length;
            } catch (error) {
                console.error('Error loading NGOs:', error);
            }
        }
        
        async function loadDonations() {
            try {
                const response = await fetch('/api/donations');
                const donations = await response.json();
                const tbody = document.querySelector('#donationsTable tbody');
                tbody.innerHTML = donations.map(d => `
                    <tr>
                        <td>${d.id}</td>
                        <td>${d.name}</td>
                        <td>${d.phone_number}</td>
                        <td>${d.quantity_of_food}</td>
                        <td>${new Date(d.donation_date).toLocaleDateString()}</td>
                        <td>${d.status}</td>
                    </tr>
                `).join('');
                document.getElementById('donationCount').textContent = donations.length;
            } catch (error) {
                console.error('Error loading donations:', error);
            }
        }
        
        // Load data on page load
        window.onload = function() {
            loadDonors();
        };
    </script>
</body>
</html>'''

if __name__ == '__main__':
    print("=" * 50)
    print("🍽️ FoodBridge Server Starting...")
    print("Server URL: http://localhost:5000")
    print("Admin Panel: http://localhost:5000/admin")
    print("Keep this window open!")
    print("=" * 50)
    app.run(host='127.0.0.1', port=5000, debug=True)