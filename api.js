// api.js - API integration for FoodBridge
const API_BASE = 'http://localhost:5000';

// Create donation
async function createDonation(donationData) {
  try {
    const response = await fetch(`${API_BASE}/api/donations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(donationData)
    });
    return await response.json();
  } catch (error) {
    console.error('Error creating donation:', error);
    throw error;
  }
}

// Get all donations
async function getDonations() {
  try {
    const response = await fetch(`${API_BASE}/api/donations`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching donations:', error);
    throw error;
  }
}

// Accept donation
async function acceptDonation(donationId, acceptedBy) {
  try {
    const response = await fetch(`${API_BASE}/api/donations/${donationId}/accept`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ accepted_by: acceptedBy })
    });
    return await response.json();
  } catch (error) {
    console.error('Error accepting donation:', error);
    throw error;
  }
}

// Example usage functions
function showDonationForm() {
  const form = `
    <div id="donationForm" style="padding: 20px; border: 1px solid #ccc; margin: 20px;">
      <h3>Create Donation</h3>
      <input type="text" id="donorName" placeholder="Your Name" required><br><br>
      <input type="tel" id="donorPhone" placeholder="Phone Number" required><br><br>
      <input type="text" id="foodQuantity" placeholder="Quantity of Food" required><br><br>
      <button onclick="submitDonation()">Submit Donation</button>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', form);
}

async function submitDonation() {
  const name = document.getElementById('donorName').value;
  const phone_number = document.getElementById('donorPhone').value;
  const quantity_of_food = document.getElementById('foodQuantity').value;

  if (!name || !phone_number || !quantity_of_food) {
    alert('Please fill all fields');
    return;
  }

  try {
    const result = await createDonation({ name, phone_number, quantity_of_food });
    alert('Donation created successfully!');
    document.getElementById('donationForm').remove();
  } catch (error) {
    alert('Error creating donation');
  }
}

async function loadDonations() {
  try {
    const donations = await getDonations();
    console.log('Donations:', donations);
    return donations;
  } catch (error) {
    console.error('Failed to load donations');
  }
}