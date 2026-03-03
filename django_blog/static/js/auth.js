// Authentication JavaScript Functions

// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    initializeAuthForms();
});

// Initialize Authentication Forms
function initializeAuthForms() {
    // Login form validation
    const loginForm = document.querySelector('.login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLoginFormSubmit);
    }
    
    // Register form validation
    const registerForm = document.querySelector('.register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegisterFormSubmit);
        addPasswordValidation();
    }
    
    // Profile form validation
    const profileForm = document.querySelector('form[action*="profile"]');
    if (profileForm) {
        profileForm.addEventListener('submit', handleProfileFormSubmit);
    }
}

// Handle Login Form Submission
function handleLoginFormSubmit(e) {
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Basic validation
    const username = form.querySelector('#id_username').value.trim();
    const password = form.querySelector('#id_password').value.trim();
    
    if (!username || !password) {
        e.preventDefault();
        showMessage('Please fill in all fields.', 'error');
        return false;
    }
    
    // Disable submit button to prevent double submission
    submitBtn.disabled = true;
    submitBtn.textContent = 'Logging in...';
    
    // Re-enable after a timeout (in case of errors)
    setTimeout(() => {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Login';
    }, 5000);
}

// Handle Register Form Submission
function handleRegisterFormSubmit(e) {
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Basic validation
    const username = form.querySelector('#id_username').value.trim();
    const email = form.querySelector('#id_email').value.trim();
    const password1 = form.querySelector('#id_password1').value.trim();
    const password2 = form.querySelector('#id_password2').value.trim();
    
    if (!username || !email || !password1 || !password2) {
        e.preventDefault();
        showMessage('Please fill in all fields.', 'error');
        return false;
    }
    
    if (password1 !== password2) {
        e.preventDefault();
        showMessage('Passwords do not match.', 'error');
        return false;
    }
    
    if (password1.length < 8) {
        e.preventDefault();
        showMessage('Password must be at least 8 characters long.', 'error');
        return false;
    }
    
    // Disable submit button to prevent double submission
    submitBtn.disabled = true;
    submitBtn.textContent = 'Registering...';
    
    // Re-enable after a timeout (in case of errors)
    setTimeout(() => {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Register';
    }, 5000);
}

// Handle Profile Form Submission
function handleProfileFormSubmit(e) {
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Basic validation
    const username = form.querySelector('#id_username').value.trim();
    const email = form.querySelector('#id_email').value.trim();
    
    if (!username || !email) {
        e.preventDefault();
        showMessage('Please fill in all fields.', 'error');
        return false;
    }
    
    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        e.preventDefault();
        showMessage('Please enter a valid email address.', 'error');
        return false;
    }
    
    // Disable submit button to prevent double submission
    submitBtn.disabled = true;
    submitBtn.textContent = 'Updating...';
    
    // Re-enable after a timeout (in case of errors)
    setTimeout(() => {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Update Profile';
    }, 5000);
}

// Add Password Validation
function addPasswordValidation() {
    const password1 = document.querySelector('#id_password1');
    const password2 = document.querySelector('#id_password2');
    
    if (password1 && password2) {
        password1.addEventListener('input', function() {
            validatePasswordStrength(this.value);
            checkPasswordMatch();
        });
        
        password2.addEventListener('input', checkPasswordMatch);
    }
}

// Validate Password Strength
function validatePasswordStrength(password) {
    const requirements = {
        length: password.length >= 8,
        uppercase: /[A-Z]/.test(password),
        lowercase: /[a-z]/.test(password),
        numbers: /\d/.test(password),
        special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
    };
    
    let strength = 0;
    if (requirements.length) strength++;
    if (requirements.uppercase) strength++;
    if (requirements.lowercase) strength++;
    if (requirements.numbers) strength++;
    if (requirements.special) strength++;
    
    updatePasswordStrengthIndicator(strength);
}

// Check Password Match
function checkPasswordMatch() {
    const password1 = document.querySelector('#id_password1').value;
    const password2 = document.querySelector('#id_password2').value;
    const matchIndicator = document.querySelector('#password-match-indicator');
    
    if (matchIndicator) {
        if (password1 === password2 && password1.length > 0) {
            matchIndicator.textContent = 'Passwords match!';
            matchIndicator.className = 'password-match success';
        } else if (password2.length > 0) {
            matchIndicator.textContent = 'Passwords do not match.';
            matchIndicator.className = 'password-match error';
        } else {
            matchIndicator.textContent = '';
            matchIndicator.className = 'password-match';
        }
    }
}

// Update Password Strength Indicator
function updatePasswordStrengthIndicator(strength) {
    const indicator = document.querySelector('#password-strength-indicator');
    
    if (indicator) {
        const strengthTexts = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
        const strengthClasses = ['very-weak', 'weak', 'fair', 'good', 'strong'];
        
        indicator.textContent = `Password Strength: ${strengthTexts[strength]}`;
        indicator.className = `password-strength ${strengthClasses[strength]}`;
    }
}

// Show Message Function
function showMessage(message, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.auth-message');
    existingMessages.forEach(msg => msg.remove());
    
    // Create new message element
    const messageElement = document.createElement('div');
    messageElement.className = `auth-message ${type}`;
    messageElement.textContent = message;
    
    // Add styles
    messageElement.style.cssText = `
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 4px;
        background-color: ${type === 'error' ? '#f8d7da' : '#d4edda'};
        color: ${type === 'error' ? '#721c24' : '#155724'};
        border: 1px solid ${type === 'error' ? '#f5c6cb' : '#c3e6cb'};
    `;
    
    // Insert at the top of the form container
    const container = document.querySelector('.login-container, .register-container, .form-container');
    if (container) {
        container.insertBefore(messageElement, container.firstChild);
    }
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        messageElement.remove();
    }, 5000);
}

// Add password strength indicator to register form
document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.querySelector('.register-form');
    if (registerForm) {
        const password1 = registerForm.querySelector('#id_password1');
        const password2 = registerForm.querySelector('#id_password2');
        
        // Add strength indicator
        const strengthIndicator = document.createElement('div');
        strengthIndicator.id = 'password-strength-indicator';
        strengthIndicator.className = 'password-strength';
        strengthIndicator.style.cssText = `
            margin-top: 0.5rem;
            font-size: 0.875rem;
            font-weight: bold;
        `;
        
        const matchIndicator = document.createElement('div');
        matchIndicator.id = 'password-match-indicator';
        matchIndicator.className = 'password-match';
        matchIndicator.style.cssText = `
            margin-top: 0.5rem;
            font-size: 0.875rem;
            font-weight: bold;
        `;
        
        if (password1 && password1.parentNode) {
            password1.parentNode.appendChild(strengthIndicator);
        }
        
        if (password2 && password2.parentNode) {
            password2.parentNode.appendChild(matchIndicator);
        }
    }
});
