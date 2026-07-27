document.addEventListener('DOMContentLoaded', () => {
  const donateBtn = document.querySelector('.btn-group .btn');
  const acceptBtn = document.querySelector('.btn-group .btn.secondary');
  const dashboardLink = document.querySelector('a[href="dashboard.html"]');
  
  // Protect dashboard access
  dashboardLink.addEventListener('click', (e) => {
    e.preventDefault();
    const user = getCurrentUser();
    if (!user) {
      showLoginModal();
    } else {
      window.location.href = user.type === 'donor' ? 'donor_dashboard.html' : 'ngo_dashboard.html';
    }
  });
  
  donateBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const user = getCurrentUser();
    if (user && user.type === 'donor') {
      window.location.href = 'donor_dashboard.html';
    } else {
      window.location.href = 'donor-portal.html';
    }
  });
  
  acceptBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const user = getCurrentUser();
    if (user && user.type === 'ngo') {
      window.location.href = 'ngo_dashboard.html';
    } else {
      window.location.href = 'ngo-portal.html';
    }
  });
  

});

function showLoginModal() {
  document.getElementById('loginModal').style.display = 'block';
}

function hideLoginModal() {
  document.getElementById('loginModal').style.display = 'none';
}



function goToSignup(type) {
  hideLoginModal();
  if (type === 'donor') {
    window.location.href = 'donor-portal.html';
  } else {
    window.location.href = 'ngo-portal.html';
  }
}