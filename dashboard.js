// dashboard.js - Connect dashboard forms to database
const API_BASE = 'http://localhost:5000';

// Handle donor food donation form
document.addEventListener('DOMContentLoaded', function() {
    const donationForm = document.getElementById('donationForm');
    if (donationForm) {
        donationForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const inputs = this.querySelectorAll('input, textarea');
            
            const donationData = {
                name: inputs[0].value.trim(), // Donor name
                phone_number: inputs[5].value.trim(), // Contact number
                food_name: inputs[1].value.trim(), // Food name
                quantity: inputs[2].value.trim(), // Quantity
                food_description: inputs[3].value.trim(), // Food description
                pickup_address: inputs[4].value.trim() // Pickup address
            };
            
            console.log('Donation data:', donationData); // Debug log
            
            if (!donationData.name || !donationData.phone_number || !donationData.food_name || !donationData.quantity || !donationData.food_description || !donationData.pickup_address) {
                alert('Please fill in all required fields.');
                return;
            }
            
            try {
                console.log('Sending request to:', `${API_BASE}/api/donations`);
                console.log('Request data:', donationData);
                
                const response = await fetch(`${API_BASE}/api/donations`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(donationData)
                });
                
                console.log('Response status:', response.status);
                console.log('Response headers:', response.headers.get('content-type'));
                
                const responseText = await response.text();
                console.log('Raw response:', responseText);
                
                let result;
                try {
                    result = JSON.parse(responseText);
                } catch (parseError) {
                    console.error('JSON parse error:', parseError);
                    console.error('Response was:', responseText.substring(0, 200));
                    alert('Server returned invalid response. Check if Flask server is running.');
                    return;
                }
                
                if (response.ok) {
                    alert('Food donation submitted successfully!');
                    this.reset();
                    loadDonorStats();
                } else {
                    alert('Error: ' + (result.message || 'Unknown server error'));
                }
            } catch (error) {
                console.error('Error submitting donation:', error);
                if (error.message.includes('Failed to fetch')) {
                    alert('Cannot connect to server. Please start Flask backend: python app.py');
                } else {
                    alert('Error submitting donation: ' + error.message);
                }
            }
        });
    }
    
    // Load donor statistics
    loadDonorStats();
    loadNGOStats();
    loadAvailableDonations();
});

// Load donor dashboard statistics
async function loadDonorStats() {
    try {
        const response = await fetch(`${API_BASE}/api/donations`);
        const donations = await response.json();
        
        const totalDonations = donations.length;
        const acceptedDonations = donations.filter(d => d.status === 'accepted').length;
        const pendingDonations = donations.filter(d => d.status === 'pending').length;
        
        // Update dashboard cards
        const cards = document.querySelectorAll('.card p');
        if (cards.length >= 3) {
            cards[0].textContent = totalDonations;
            cards[1].textContent = acceptedDonations;
            cards[2].textContent = pendingDonations;
        }
        
        // Update recent donations table
        updateRecentDonationsTable(donations.slice(-5).reverse());
        
    } catch (error) {
        console.error('Error loading donor stats:', error);
    }
}

// Load NGO dashboard statistics
async function loadNGOStats() {
    try {
        const response = await fetch(`${API_BASE}/api/donations`);
        const donations = await response.json();
        
        const acceptedByNGO = donations.filter(d => d.status === 'accepted').length;
        const pendingRequests = donations.filter(d => d.status === 'pending').length;
        
        // Update NGO dashboard cards if on NGO dashboard
        const ngoCards = document.querySelectorAll('.card p');
        if (ngoCards.length >= 3 && document.title.includes('NGO')) {
            ngoCards[0].textContent = acceptedByNGO; // Food requests made
            ngoCards[1].textContent = acceptedByNGO; // Food received
            ngoCards[2].textContent = pendingRequests; // Pending requests
        }
        
    } catch (error) {
        console.error('Error loading NGO stats:', error);
    }
}

// Update recent donations table
function updateRecentDonationsTable(donations) {
    const tbody = document.querySelector('.recent table tbody');
    if (tbody) {
        tbody.innerHTML = donations.map(donation => `
            <tr>
                <td>${donation.food_name || donation.name}</td>
                <td>${donation.quantity || 'Not specified'}</td>
                <td><span class="status ${donation.status}">${donation.status}</span></td>
                <td>${donation.accepted_by || '—'}</td>
            </tr>
        `).join('');
    }
}

// Load available donations for NGO dashboard
async function loadAvailableDonations() {
    if (!document.title.includes('NGO')) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/donations`);
        const donations = await response.json();
        const availableDonations = donations.filter(d => d.status === 'pending');
        
        const foodList = document.querySelector('.food-list');
        if (foodList) {
            foodList.innerHTML = availableDonations.map(donation => `
                <div class="food-item" data-id="${donation.id}">
                    <h4>${donation.food_name}</h4>
                    <p><strong>Donor:</strong> ${donation.name}</p>
                    <p><strong>Quantity:</strong> ${donation.quantity}</p>
                    <p><strong>Description:</strong> ${donation.food_description}</p>
                    <p><strong>Pickup Address:</strong> ${donation.pickup_address}</p>
                    <p><strong>Contact:</strong> ${donation.phone_number}</p>
                    <div class="btn-group">
                        <button class="btn accept-btn" onclick="acceptFood(${donation.id})">Accept</button>
                        <button class="btn reject-btn" onclick="rejectFood(${donation.id})">Reject</button>
                    </div>
                </div>
            `).join('');
        }
        
    } catch (error) {
        console.error('Error loading available donations:', error);
    }
}

// Accept food donation (NGO function)
async function acceptFood(donationId) {
    const user = getCurrentUser();
    const ngoName = user ? user.name : 'NGO Organization';
    
    try {
        const response = await fetch(`${API_BASE}/api/donations/${donationId}/accept`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ accepted_by: ngoName })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            alert('Food donation accepted successfully!');
            loadAvailableDonations();
            loadNGOStats();
        } else {
            alert('Error accepting donation: ' + result.message);
        }
    } catch (error) {
        console.error('Error accepting donation:', error);
        alert('Error accepting donation. Please try again.');
    }
}

// Reject food donation (NGO function)
function rejectFood(donationId) {
    const foodItem = document.querySelector(`[data-id="${donationId}"]`);
    if (foodItem) {
        foodItem.style.display = 'none';
        alert('Food donation rejected.');
    }
}