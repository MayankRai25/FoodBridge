from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Donor, NGO, Donation
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foodbridge.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
try:
    from email_config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS
except ImportError:
    # Fallback configuration
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USER = 'your_email@gmail.com'
    EMAIL_PASS = 'your_app_password'
    print("Warning: Using default email config. Please set up email_config.py")

db.init_app(app)
CORS(app)

def send_notification_to_ngos(donation_data):
    """Send email notification to all registered NGOs about new food donation"""
    try:
        # Get all NGO emails
        ngos = NGO.query.all()
        if not ngos:
            print("No NGOs registered to notify")
            return False
        
        # Check if email is configured
        if EMAIL_USER == 'your_email@gmail.com' or EMAIL_PASS == 'your_app_password':
            print(f"Email not configured. Would notify {len(ngos)} NGOs about: {donation_data['food_name']}")
            return False
        
        # Create email content
        subject = "🍽️ New Food Donation Available - FoodBridge"
        
        text_body = f"""
🍽️ NEW FOOD DONATION AVAILABLE!

=== DONATION DETAILS ===
Food Name: {donation_data['food_name']}
Quantity: {donation_data['quantity']}
Description: {donation_data['food_description']}
Pickup Address: {donation_data['pickup_address']}

🌟 MAKE A DIFFERENCE TODAY!
This food donation can help feed many people in need. Your quick action can prevent food waste and bring smiles to hungry faces.

⚡ ACT FAST! Fresh food donations are time-sensitive.

🚀 To accept this donation, visit: http://localhost:5000

Together, we can reduce food waste and feed the hungry.
Thank you for being part of FoodBridge! 💚

---
FoodBridge - Connecting donors and NGOs to reduce food waste
        """
        
        # Check if email is configured
        if EMAIL_USER == 'your_email@gmail.com' or EMAIL_PASS == 'your_app_password':
            print(f"⚠️  Email not configured. Please update email_config.py")
            print(f"📧 Would notify {len(ngos)} NGOs about: {donation_data['food_name']}")
            return
        
        # Send email to each NGO
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        
        for ngo in ngos:
            msg = MIMEText(text_body, 'plain')
            msg['Subject'] = subject
            msg['From'] = EMAIL_USER
            msg['To'] = ngo.email
            
            server.send_message(msg)
        
        server.quit()
        print(f"✅ Email notifications sent to {len(ngos)} NGOs")
        print(f"📧 Notified about: {donation_data['food_name']} - {donation_data['quantity']}")
        return True
        
    except Exception as e:
        print(f"Error sending email notifications: {str(e)}")
        return False

with app.app_context():
    # Create tables if they don't exist
    db.create_all()

@app.route('/api/donors', methods=['POST'])
def register_donor():
    try:
        data = request.json
        
        # Check if donor already exists
        existing_donor = Donor.query.filter_by(email=data['email']).first()
        if existing_donor:
            return jsonify({'message': 'Email already registered'}), 400
        
        donor = Donor(
            name=data['name'],
            email=data['email'],
            phone_number=data['phone_number'],
            address=data.get('address', ''),
            password=data['password']
        )
        db.session.add(donor)
        db.session.commit()
        return jsonify({'message': 'Donor registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error registering donor: {str(e)}")
        return jsonify({'message': f'Registration failed: {str(e)}'}), 400

@app.route('/api/ngos', methods=['POST'])
def register_ngo():
    try:
        data = request.json
        ngo = NGO(
            organization_name=data['organization_name'],
            email=data['email'],
            phone_number=data['phone_number'],
            address=data.get('address', ''),
            password=data['password']
        )
        db.session.add(ngo)
        db.session.commit()
        return jsonify({'message': 'NGO registered successfully'}), 201
    except Exception as e:
        return jsonify({'message': f'Registration failed: {str(e)}'}), 400

@app.route('/api/donations', methods=['POST'])
def create_donation():
    try:
        data = request.json
        donation = Donation(
            name=data['name'],
            phone_number=data['phone_number'],
            food_name=data['food_name'],
            quantity=data['quantity'],
            food_description=data['food_description'],
            pickup_address=data['pickup_address']
        )
        db.session.add(donation)
        db.session.commit()
        
        # Send email notifications to all NGOs (don't let email errors stop donation)
        try:
            send_notification_to_ngos(data)
        except Exception as email_error:
            print(f"Email notification failed: {email_error}")
        
        return jsonify({'message': 'Donation created successfully!'}), 201
    except Exception as e:
        print(f"Error creating donation: {str(e)}")
        return jsonify({'message': f'Error creating donation: {str(e)}'}), 400

@app.route('/api/donations', methods=['GET'])
def get_donations():
    donations = Donation.query.all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'phone_number': d.phone_number,
        'food_name': d.food_name,
        'quantity': d.quantity,
        'food_description': d.food_description,
        'pickup_address': d.pickup_address,
        'donation_date': d.donation_date.isoformat(),
        'accepted_by': d.accepted_by,
        'status': d.status
    } for d in donations])

@app.route('/api/donations/<int:donation_id>/accept', methods=['PUT'])
def accept_donation(donation_id):
    data = request.json
    donation = Donation.query.get(donation_id)
    donation.accepted_by = data['accepted_by']
    donation.status = 'accepted'
    db.session.commit()
    return jsonify({'message': 'Donation accepted successfully'})

# Admin routes
@app.route('/api/admin/donors', methods=['GET'])
def get_all_donors():
    donors = Donor.query.all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'email': d.email,
        'phone_number': d.phone_number,
        'address': d.address or 'Not provided',
        'date_of_register': d.date_of_register.isoformat()
    } for d in donors])

@app.route('/api/admin/ngos', methods=['GET'])
def get_all_ngos():
    ngos = NGO.query.all()
    return jsonify([{
        'id': n.id,
        'organization_name': n.organization_name,
        'email': n.email,
        'phone_number': n.phone_number,
        'address': n.address or 'Not provided',
        'date_of_register': n.date_of_register.isoformat()
    } for n in ngos])

@app.route('/admin')
def admin_panel():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FoodBridge Admin Panel</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: "Segoe UI", Arial, sans-serif; background: #f9f9f9; color: #333; line-height: 1.6; }
        .navbar { display: flex; justify-content: center; align-items: center; padding: 15px 30px; background-color: #0288d1; border-radius: 12px; width: max-content; margin: 15px auto; }
        .nav-links { display: flex; list-style: none; gap: 20px; }
        .nav-links a { color: white; text-decoration: none; font-weight: 500; padding: 8px 15px; border-radius: 25px; transition: background 0.3s; }
        .nav-links a.active, .nav-links a:hover { background: #fff; color: #0288d1; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .admin-title { text-align: center; color: #0288d1; font-size: 2.5em; margin: 30px 0; }
        .stats { display: flex; justify-content: center; gap: 30px; margin: 40px 0; flex-wrap: wrap; }
        .stat-card { background: #0288d1; color: #fff; padding: 30px; border-radius: 12px; width: 250px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; }
        .stat-card h3 { font-size: 1.5em; margin-bottom: 15px; }
        .stat-card p { font-size: 2em; font-weight: bold; }
        .tab-buttons { display: flex; justify-content: center; gap: 20px; margin: 40px 0; flex-wrap: wrap; }
        .tab-btn { background-color: #0288d1; color: #fff; border: none; padding: 15px 30px; border-radius: 25px; cursor: pointer; font-weight: 500; font-size: 1.1em; transition: all 0.3s; }
        .tab-btn:hover { background-color: #01579b; transform: translateY(-2px); }
        .tab-btn.active { background-color: #0277bd; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
        .section { background: #fff; margin: 30px 0; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); display: none; }
        .section.active { display: block; }
        .section h2 { color: #0277bd; font-size: 1.8em; margin-bottom: 20px; }
        button { background-color: #0288d1; color: #fff; border: none; padding: 12px 25px; border-radius: 25px; cursor: pointer; font-weight: 500; margin-bottom: 20px; transition: background 0.3s; }
        button:hover { background-color: #01579b; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        th { background-color: #0277bd; color: white; padding: 15px 12px; text-align: left; font-weight: 600; }
        td { padding: 12px; border-bottom: 1px solid #eee; }
        tr:hover { background-color: #f5f5f5; }
        tr:nth-child(even) { background-color: #fafafa; }
        footer { background: #0277bd; color: #fff; padding: 20px; text-align: center; margin-top: 50px; border-radius: 12px; }
    </style>
</head>
<body>
    <nav class="navbar">
        <ul class="nav-links">
            <li><a href="#" class="active">Admin Panel</a></li>
        </ul>
    </nav>
    <div class="container">
        <h1 class="admin-title">🍽️ FoodBridge Admin Panel</h1>
        <div class="stats">
            <div class="stat-card"><h3>Total Donors</h3><p id="donorCount">Loading...</p></div>
            <div class="stat-card"><h3>Total NGOs</h3><p id="ngoCount">Loading...</p></div>
            <div class="stat-card"><h3>Total Donations</h3><p id="donationCount">Loading...</p></div>
        </div>
        <div class="tab-buttons">
            <button class="tab-btn active" onclick="showTab('donors')">👥 View Donors</button>
            <button class="tab-btn" onclick="showTab('ngos')">🏢 View NGOs</button>
            <button class="tab-btn" onclick="showTab('donations')">🍽️ View Donations</button>
            <button class="tab-btn" onclick="showTab('reset')">🔑 Reset Password</button>
        </div>
        <div id="donors" class="section active">
            <h2>Donors</h2>
            <button onclick="loadDonors()">Refresh Donors</button>
            <table id="donorsTable"><thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Address</th><th>Registration Date</th><th>Action</th></tr></thead><tbody></tbody></table>
        </div>
        <div id="ngos" class="section">
            <h2>NGOs</h2>
            <button onclick="loadNGOs()">Refresh NGOs</button>
            <table id="ngosTable"><thead><tr><th>ID</th><th>Organization</th><th>Email</th><th>Phone</th><th>Address</th><th>Registration Date</th><th>Action</th></tr></thead><tbody></tbody></table>
        </div>
        <div id="donations" class="section">
            <h2>Donations</h2>
            <button onclick="loadDonations()">Refresh Donations</button>
            <table id="donationsTable"><thead><tr><th>ID</th><th>Donor Name</th><th>Phone</th><th>Food Name</th><th>Quantity</th><th>Description</th><th>Pickup Address</th><th>Date</th><th>Accepted By</th><th>Status</th></tr></thead><tbody></tbody></table>
        </div>
        <div id="reset" class="section">
            <h2>Reset User Password</h2>
            <div style="max-width: 400px; margin: 20px 0;">
                <label>User Type:</label>
                <select id="userType" style="width: 100%; padding: 8px; margin: 5px 0;">
                    <option value="donor">Donor</option>
                    <option value="ngo">NGO</option>
                </select>
                <label>Email:</label>
                <input type="email" id="resetEmail" placeholder="Enter user email" style="width: 100%; padding: 8px; margin: 5px 0;">
                <label>New Password:</label>
                <input type="password" id="newPassword" placeholder="Enter new password" style="width: 100%; padding: 8px; margin: 5px 0;">
                <button onclick="resetUserPassword()" style="width: 100%; padding: 10px; margin: 10px 0;">Reset Password</button>
            </div>
        </div>
    </div>
    <footer><p>&copy; 2025 FoodBridge Admin Panel. All rights reserved.</p></footer>
    <script>
        const API_BASE = window.location.origin;
        async function loadDonors() {
            try {
                const response = await fetch(`${API_BASE}/api/admin/donors`);
                const donors = await response.json();
                const tbody = document.querySelector('#donorsTable tbody');
                tbody.innerHTML = donors.map(d => `<tr><td>${d.id}</td><td>${d.name}</td><td>${d.email}</td><td>${d.phone_number}</td><td>${d.address}</td><td>${new Date(d.date_of_register).toLocaleDateString()}</td><td><button onclick="deleteDonor(${d.id})" style="background: #f44336; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">Delete</button></td></tr>`).join('');
                document.getElementById('donorCount').textContent = donors.length;
            } catch (error) { console.error('Error loading donors:', error); }
        }
        async function loadNGOs() {
            try {
                const response = await fetch(`${API_BASE}/api/admin/ngos`);
                const ngos = await response.json();
                const tbody = document.querySelector('#ngosTable tbody');
                tbody.innerHTML = ngos.map(n => `<tr><td>${n.id}</td><td>${n.organization_name}</td><td>${n.email}</td><td>${n.phone_number}</td><td>${n.address}</td><td>${new Date(n.date_of_register).toLocaleDateString()}</td><td><button onclick="deleteNGO(${n.id})" style="background: #f44336; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">Delete</button></td></tr>`).join('');
                document.getElementById('ngoCount').textContent = ngos.length;
            } catch (error) { console.error('Error loading NGOs:', error); }
        }
        async function loadDonations() {
            try {
                const response = await fetch(`${API_BASE}/api/donations`);
                const donations = await response.json();
                const tbody = document.querySelector('#donationsTable tbody');
                tbody.innerHTML = donations.map(d => `<tr><td>${d.id}</td><td>${d.name}</td><td>${d.phone_number}</td><td>${d.food_name || 'Not specified'}</td><td>${d.quantity || 'Not specified'}</td><td>${d.food_description || 'No description'}</td><td>${d.pickup_address || 'No address'}</td><td>${new Date(d.donation_date).toLocaleDateString()}</td><td>${d.accepted_by || 'Not accepted'}</td><td>${d.status}</td></tr>`).join('');
                document.getElementById('donationCount').textContent = donations.length;
            } catch (error) { console.error('Error loading donations:', error); }
        }
        function showTab(tabName) {
            // Hide all sections
            document.querySelectorAll('.section').forEach(section => {
                section.classList.remove('active');
            });
            // Remove active class from all buttons
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            // Show selected section
            document.getElementById(tabName).classList.add('active');
            // Add active class to clicked button
            event.target.classList.add('active');
            // Load data for the selected tab
            if (tabName === 'donors') loadDonors();
            else if (tabName === 'ngos') loadNGOs();
            else if (tabName === 'donations') loadDonations();
        }
        async function resetUserPassword() {
            const userType = document.getElementById('userType').value;
            const email = document.getElementById('resetEmail').value;
            const newPassword = document.getElementById('newPassword').value;
            
            if (!email || !newPassword) {
                alert('Please fill in all fields');
                return;
            }
            
            try {
                const response = await fetch(`${API_BASE}/api/admin/reset-password`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, new_password: newPassword, type: userType })
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    alert('Password reset successfully!');
                    document.getElementById('resetEmail').value = '';
                    document.getElementById('newPassword').value = '';
                } else {
                    alert('Error: ' + result.message);
                }
            } catch (error) {
                alert('Error resetting password: ' + error.message);
            }
        }
        async function deleteDonor(donorId) {
            if (confirm('Are you sure you want to delete this donor?')) {
                try {
                    const response = await fetch(`${API_BASE}/api/admin/donors/${donorId}`, {
                        method: 'DELETE'
                    });
                    const result = await response.json();
                    if (response.ok) {
                        alert('Donor deleted successfully!');
                        loadDonors();
                    } else {
                        alert('Error: ' + result.message);
                    }
                } catch (error) {
                    alert('Error deleting donor: ' + error.message);
                }
            }
        }
        
        async function deleteNGO(ngoId) {
            if (confirm('Are you sure you want to delete this NGO?')) {
                try {
                    const response = await fetch(`${API_BASE}/api/admin/ngos/${ngoId}`, {
                        method: 'DELETE'
                    });
                    const result = await response.json();
                    if (response.ok) {
                        alert('NGO deleted successfully!');
                        loadNGOs();
                    } else {
                        alert('Error: ' + result.message);
                    }
                } catch (error) {
                    alert('Error deleting NGO: ' + error.message);
                }
            }
        }
        
        window.onload = function() { loadDonors(); };
    </script>
</body>
</html>'''

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('type')
    
    print(f"Login attempt: {email}, {password}, {user_type}")  # Debug log
    
    if user_type == 'donor':
        user = Donor.query.filter_by(email=email, password=password).first()
        print(f"Donor found: {user}")  # Debug log
        if user:
            return jsonify({
                'success': True,
                'user': {
                    'email': user.email,
                    'name': user.name,
                    'type': 'donor'
                }
            })
    elif user_type == 'ngo':
        user = NGO.query.filter_by(email=email, password=password).first()
        print(f"NGO found: {user}")  # Debug log
        if user:
            return jsonify({
                'success': True,
                'user': {
                    'email': user.email,
                    'name': user.organization_name,
                    'type': 'ngo'
                }
            })
    
    return jsonify({'success': False, 'message': 'Invalid credentials or user not found'}), 401



@app.route('/api/admin/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')
    new_password = data.get('new_password')
    user_type = data.get('type')
    
    print(f"Password reset attempt: {email}, {user_type}")  # Debug log
    
    if user_type == 'donor':
        user = Donor.query.filter_by(email=email).first()
        print(f"Donor found for reset: {user}")  # Debug log
        if user:
            user.password = new_password
            db.session.commit()
            return jsonify({'message': 'Donor password reset successfully'})
    elif user_type == 'ngo':
        user = NGO.query.filter_by(email=email).first()
        print(f"NGO found for reset: {user}")  # Debug log
        if user:
            user.password = new_password
            db.session.commit()
            return jsonify({'message': 'NGO password reset successfully'})
    
    return jsonify({'message': 'User not found'}), 404

@app.route('/api/admin/donors/<int:donor_id>', methods=['DELETE'])
def delete_donor(donor_id):
    try:
        donor = Donor.query.get(donor_id)
        if donor:
            db.session.delete(donor)
            db.session.commit()
            return jsonify({'message': 'Donor deleted successfully'})
        return jsonify({'message': 'Donor not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error deleting donor: {str(e)}'}), 400

@app.route('/api/admin/ngos/<int:ngo_id>', methods=['DELETE'])
def delete_ngo(ngo_id):
    try:
        ngo = NGO.query.get(ngo_id)
        if ngo:
            db.session.delete(ngo)
            db.session.commit()
            return jsonify({'message': 'NGO deleted successfully'})
        return jsonify({'message': 'NGO not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error deleting NGO: {str(e)}'}), 400

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    try:
        data = request.json
        name = data['name']
        email = data['email']
        message = data['message']
        
        # Send email to your address
        subject = f"🍽️ FoodBridge Contact Form - Message from {name}"
        
        email_body = f"""
📧 NEW CONTACT FORM SUBMISSION

👤 Name: {name}
📧 Email: {email}

💬 Message:
{message}

---
Sent via FoodBridge Contact Form
        """
        
        # Check if email is configured
        if EMAIL_USER == 'your_email@gmail.com' or EMAIL_PASS == 'your_app_password':
            print(f"📧 Contact form submission from {name} ({email}): {message}")
            return jsonify({'message': 'Message received! (Email not configured)'}), 201
        
        # Send email
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        
        msg = MIMEText(email_body, 'plain')
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_USER  # Send to your own email
        msg['Reply-To'] = email  # User can reply directly
        
        server.send_message(msg)
        server.quit()
        
        return jsonify({'message': 'Message sent successfully!'}), 201
        
    except Exception as e:
        print(f"Contact form error: {str(e)}")
        return jsonify({'message': 'Failed to send message. Please try again.'}), 500

@app.route('/')
def home():
    return '<h1>FoodBridge API</h1><p><a href="/admin">Go to Admin Panel</a></p>'

if __name__ == '__main__':
    app.run(debug=True)