// Simple password protection for the construction management site
// This is basic security - for production, use server-side authentication

(function() {
  'use strict';
  
  // Configuration
  const SITE_PASSWORD = 'SilverCrowd2024'; // Change this to your desired password
  const AUTH_KEY = 'silvercrowdcraft_authenticated';
  const AUTH_EXPIRY_HOURS = 24; // How long authentication lasts
  
  // Check if user is already authenticated
  function isAuthenticated() {
    const authData = localStorage.getItem(AUTH_KEY);
    if (!authData) return false;
    
    try {
      const { timestamp } = JSON.parse(authData);
      const now = new Date().getTime();
      const expiryTime = AUTH_EXPIRY_HOURS * 60 * 60 * 1000;
      
      // Check if authentication has expired
      if (now - timestamp > expiryTime) {
        localStorage.removeItem(AUTH_KEY);
        return false;
      }
      
      return true;
    } catch (e) {
      return false;
    }
  }
  
  // Set authentication
  function setAuthenticated() {
    const authData = {
      timestamp: new Date().getTime()
    };
    localStorage.setItem(AUTH_KEY, JSON.stringify(authData));
  }
  
  // Show login screen
  function showLoginScreen() {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.id = 'auth-overlay';
    overlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
      z-index: 99999;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    `;
    
    // Create login box
    const loginBox = document.createElement('div');
    loginBox.style.cssText = `
      background: #12161b;
      border: 2px solid #667eea;
      border-radius: 12px;
      padding: 40px;
      max-width: 400px;
      width: 90%;
      box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    `;
    
    loginBox.innerHTML = `
      <div style="text-align: center; margin-bottom: 30px;">
        <div style="font-size: 48px; margin-bottom: 16px;">🔒</div>
        <h1 style="color: #9cc1ff; margin: 0 0 8px 0; font-size: 28px;">Protected Site</h1>
        <p style="color: #8a98ab; margin: 0; font-size: 14px;">SilverCrowd Construction Management</p>
      </div>
      
      <form id="auth-form" style="margin-bottom: 20px;">
        <label style="display: block; color: #e8eef5; margin-bottom: 8px; font-weight: 600;">
          Enter Password
        </label>
        <input 
          type="password" 
          id="password-input" 
          placeholder="Enter site password..."
          style="
            width: 100%;
            padding: 12px 16px;
            background: #0f1317;
            border: 2px solid #303947;
            border-radius: 6px;
            color: #e8eef5;
            font-size: 16px;
            outline: none;
            box-sizing: border-box;
            transition: border-color 0.2s;
          "
          autofocus
        />
        <button 
          type="submit"
          style="
            width: 100%;
            margin-top: 16px;
            padding: 12px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
          "
          onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(102, 126, 234, 0.4)'"
          onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'"
        >
          🔓 Unlock Site
        </button>
      </form>
      
      <div id="auth-error" style="
        display: none;
        padding: 12px;
        background: rgba(255, 107, 107, 0.1);
        border: 1px solid #ff6b6b;
        border-radius: 6px;
        color: #ff6b6b;
        font-size: 14px;
        text-align: center;
      "></div>
      
      <p style="color: #8a98ab; font-size: 12px; text-align: center; margin: 20px 0 0 0;">
        💡 Contact your administrator if you need access
      </p>
    `;
    
    overlay.appendChild(loginBox);
    document.body.appendChild(overlay);
    
    // Handle form submission
    const form = document.getElementById('auth-form');
    const input = document.getElementById('password-input');
    const errorDiv = document.getElementById('auth-error');
    
    // Style input on focus
    input.addEventListener('focus', () => {
      input.style.borderColor = '#667eea';
    });
    input.addEventListener('blur', () => {
      input.style.borderColor = '#303947';
    });
    
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const password = input.value;
      
      if (password === SITE_PASSWORD) {
        // Correct password
        setAuthenticated();
        overlay.style.opacity = '0';
        overlay.style.transition = 'opacity 0.3s';
        setTimeout(() => {
          overlay.remove();
        }, 300);
      } else {
        // Wrong password
        errorDiv.textContent = '❌ Incorrect password. Please try again.';
        errorDiv.style.display = 'block';
        input.value = '';
        input.style.borderColor = '#ff6b6b';
        
        // Shake animation
        loginBox.style.animation = 'shake 0.5s';
        setTimeout(() => {
          loginBox.style.animation = '';
        }, 500);
      }
    });
  }
  
  // Add shake animation
  const style = document.createElement('style');
  style.textContent = `
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
      20%, 40%, 60%, 80% { transform: translateX(10px); }
    }
  `;
  document.head.appendChild(style);
  
  // Check authentication on page load
  if (!isAuthenticated()) {
    showLoginScreen();
  }
  
  // Optional: Add logout function
  window.siteLogout = function() {
    if (confirm('Are you sure you want to log out?')) {
      localStorage.removeItem(AUTH_KEY);
      location.reload();
    }
  };
  
})();

