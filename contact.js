const API_BASE = 'http://localhost:5000';
const form = document.getElementById('contactForm');
const result = document.getElementById('result');

form.addEventListener('submit', async function(e) {
  e.preventDefault();
  
  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const phone = document.getElementById('phone').value;
  const message = document.getElementById('message').value;
  
  // Email validation
  if (!email.endsWith('@gmail.com')) {
    result.innerHTML = "Email must end with @gmail.com";
    result.style.color = "red";
    return;
  }
  
  // Phone validation
  if (!/^\d{10}$/.test(phone)) {
    result.innerHTML = "Phone number must be exactly 10 digits";
    result.style.color = "red";
    return;
  }
  
  result.innerHTML = "Sending message...";
  
  try {
    const response = await fetch(`${API_BASE}/api/contact`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name, email, message })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      result.innerHTML = "Message sent successfully! We'll get back to you soon.";
      result.style.color = "green";
      form.reset();
    } else {
      result.innerHTML = "Error: " + data.message;
      result.style.color = "red";
    }
  } catch (error) {
    console.error('Error:', error);
    result.innerHTML = "Something went wrong! Please try again.";
    result.style.color = "red";
  }
  
  setTimeout(() => {
    result.innerHTML = "";
  }, 5000);
});