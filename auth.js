// auth.js - Authentication management

// Check if user is logged in
function isLoggedIn() {
  return localStorage.getItem('userToken') !== null;
}

// Get current user info
function getCurrentUser() {
  const userInfo = localStorage.getItem('userInfo');
  return userInfo ? JSON.parse(userInfo) : null;
}

// Login function - removed dummy credentials
// Use donor.js and ngo.js for actual authentication



// Logout function
function logout() {
  localStorage.removeItem('userToken');
  localStorage.removeItem('userInfo');
  window.location.href = 'newhome.html';
}

// Show login modal
function showLoginModal() {
  document.getElementById('loginModal').style.display = 'block';
}

// Hide login modal
function hideLoginModal() {
  document.getElementById('loginModal').style.display = 'none';
}


// Get dashboard URL based on user type
function getDashboardUrl() {
  const user = getCurrentUser();
  if (!user) return 'dashboard.html'; // Default fallback
  return user.type === 'donor' ? 'donor_dashboard.html' : 'ngo_dashboard.html';
}

// Update navbar dashboard link
function updateNavbarDashboardLink() {
  const dashboardLinks = document.querySelectorAll('a[href*="dashboard"]');
  const dashboardUrl = getDashboardUrl();
  dashboardLinks.forEach(link => {
    if (link.textContent.trim() === 'Dashboard') {
      link.href = dashboardUrl;
    }
  });
}
