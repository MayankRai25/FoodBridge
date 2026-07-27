// donor.js
const API_BASE = 'http://localhost:5000';

// -----------------------
// Signup Form Handling
// -----------------------
const signupFormContainer = document.querySelector(".signup-form");
if (signupFormContainer) {
  signupFormContainer.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Inputs are in order: Name, Email, Phone, Address, Password
    const inputs = signupFormContainer.querySelectorAll("input");
    const name = inputs[0].value.trim();
    const email = inputs[1].value.trim();
    const phone_number = inputs[2].value.trim();
    const address = inputs[3].value.trim();
    const password = inputs[4].value;

    // Basic validation
    if (!name || !email || !phone_number || !address || !password) {
      alert("Please fill in all fields.");
      return;
    }
    
    // Email validation
    if (!email.endsWith('@gmail.com')) {
      alert("Email must end with @gmail.com");
      return;
    }
    
    // Phone number validation
    if (!/^\d{10}$/.test(phone_number)) {
      alert("Phone number must be exactly 10 digits.");
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/api/donors`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, phone_number, address, password }),
      });

      const data = await response.json();

      if (response.ok) {
        alert("Donor registered successfully! Please login with your credentials.");
        inputs.forEach(input => input.value = "");
        // Switch to login tab
        document.getElementById('login').checked = true;
      } else {
        alert(data.message || "Registration failed. Try again.");
      }
    } catch (error) {
      console.error("Signup Error:", error);
      alert("Signup error: " + error.message);
    }
  });
}

// -----------------------
// Login Form Handling
// -----------------------
const loginFormContainer = document.querySelector(".login-form");
if (loginFormContainer) {
  loginFormContainer.addEventListener("submit", async (e) => {
    e.preventDefault();

    const inputs = loginFormContainer.querySelectorAll("input");
    const email = inputs[0].value.trim();
    const password = inputs[1].value;

    if (!email || !password) {
      alert("Please enter both email and password.");
      return;
    }
    
    // Email validation
    if (!email.endsWith('@gmail.com')) {
      alert("Email must end with @gmail.com");
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, type: 'donor' }),
      });

      const data = await response.json();

      if (data.success) {
        localStorage.setItem('userToken', 'donor-token');
        localStorage.setItem('userInfo', JSON.stringify(data.user));
        window.location.href = "donor_dashboard.html";
      } else {
        alert(data.message || "Invalid credentials");
      }
    } catch (error) {
      console.error("Login Error:", error);
      alert("Login failed. Please check your connection.");
    }
  });
}
