// ==========================================================================
// MetroCheck — Login & Signup JavaScript Controller
// Clean, Human-Readable, Beginner-Friendly Code for SIH PS-26034
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {

  // ------------------------------------------------------------------------
  // 1. Toast Notification System (Alert Popups)
  // ------------------------------------------------------------------------
  const toastContainer = document.getElementById('toastContainer');

  function showToast(title, message, type = 'info', duration = 3500) {
    if (!toastContainer) return;

    const toast = document.createElement('div');
    toast.className = `toast-card toast-${type}`;
    toast.innerHTML = `
      <div class="toast-body">
        <h4 class="toast-title">${title}</h4>
        <p class="toast-msg">${message}</p>
      </div>
      <button type="button" class="toast-close" aria-label="Close">&times;</button>
      <div class="toast-progress" style="transition: width ${duration}ms linear; width: 100%;"></div>
    `;

    toast.querySelector('.toast-close').onclick = () => toast.remove();
    toastContainer.appendChild(toast);

    // Animate progress bar countdown
    requestAnimationFrame(() => {
      const bar = toast.querySelector('.toast-progress');
      if (bar) bar.style.width = '0%';
    });

    setTimeout(() => { if (toast.parentNode) toast.remove(); }, duration);
  }

  // ------------------------------------------------------------------------
  // 2. Dark / Light Mode Theme Controller (Persistent via LocalStorage)
  // ------------------------------------------------------------------------
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon = document.getElementById('themeIcon');

  function updateThemeUI(isDark) {
    if (isDark) {
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
      // Sun icon when dark mode is active
      if (themeIcon) {
        themeIcon.innerHTML = `
          <circle cx="12" cy="12" r="5"/>
          <line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
          <line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>
        `;
      }
    } else {
      document.documentElement.removeAttribute('data-theme');
      localStorage.setItem('theme', 'light');
      // Moon icon when light mode is active
      if (themeIcon) {
        themeIcon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>';
      }
    }
  }

  // Initialize theme from saved preference or OS preference
  const savedTheme = localStorage.getItem('theme');
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  updateThemeUI(savedTheme === 'dark' || (!savedTheme && systemPrefersDark));

  themeToggle?.addEventListener('click', () => {
    const isCurrentlyDark = document.documentElement.getAttribute('data-theme') === 'dark';
    updateThemeUI(!isCurrentlyDark);
    showToast('Theme Changed', !isCurrentlyDark ? 'Switched to dark mode' : 'Switched to light mode', 'info', 2000);
  });

  // ------------------------------------------------------------------------
  // 3. Tab Switching (Log In vs Sign Up)
  // ------------------------------------------------------------------------
  const tabLogin = document.getElementById('tabLogin');
  const tabSignup = document.getElementById('tabSignup');
  const loginView = document.getElementById('loginView');
  const signupView = document.getElementById('signupView');

  function switchTab(showSignup) {
    tabSignup.classList.toggle('active', showSignup);
    tabLogin.classList.toggle('active', !showSignup);
    signupView.classList.toggle('hidden', !showSignup);
    loginView.classList.toggle('hidden', showSignup);
  }

  tabLogin?.addEventListener('click', () => switchTab(false));
  tabSignup?.addEventListener('click', () => switchTab(true));

  // ------------------------------------------------------------------------
  // 4. Password Show / Hide Toggle
  // ------------------------------------------------------------------------
  document.querySelectorAll('.toggle-pw').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetInput = document.getElementById(btn.dataset.target);
      if (targetInput) {
        targetInput.type = targetInput.type === 'password' ? 'text' : 'password';
      }
    });
  });

  // ------------------------------------------------------------------------
  // 5. Real-Time Password Strength Checker (for Sign Up)
  // ------------------------------------------------------------------------
  const signupPw = document.getElementById('signupPassword');
  const strengthBox = document.getElementById('pwStrengthContainer');
  const strengthBar = document.getElementById('strengthBar');
  const strengthText = document.getElementById('strengthText');

  signupPw?.addEventListener('input', () => {
    const val = signupPw.value;
    if (!val) {
      strengthBox?.classList.add('hidden');
      return;
    }
    strengthBox?.classList.remove('hidden');

    const criteria = {
      critLength: val.length >= 8,
      critUpper: /[A-Z]/.test(val),
      critNumber: /[0-9]/.test(val),
      critSpecial: /[^A-Za-z0-9]/.test(val)
    };

    let score = 0;
    for (const [id, passed] of Object.entries(criteria)) {
      const el = document.getElementById(id);
      if (el) el.className = passed ? 'valid' : '';
      if (passed) score++;
    }

    const levels = [
      { width: '25%', color: '#ef4444', label: 'Weak' },
      { width: '50%', color: '#f59e0b', label: 'Fair' },
      { width: '75%', color: '#3b82f6', label: 'Good' },
      { width: '100%', color: '#10b981', label: 'Strong' }
    ];

    const currentLevel = levels[Math.max(0, score - 1)] || levels[0];
    if (strengthBar) {
      strengthBar.style.width = currentLevel.width;
      strengthBar.style.backgroundColor = currentLevel.color;
    }
    if (strengthText) {
      strengthText.textContent = currentLevel.label;
      strengthText.style.color = currentLevel.color;
    }
  });

  // ------------------------------------------------------------------------
  // 6. Remember Me Checkbox & Reset Buttons
  // ------------------------------------------------------------------------
  const rememberMe = document.getElementById('rememberMe');
  const loginEmail = document.getElementById('loginEmail');
  const savedEmail = localStorage.getItem('metrocheck_remembered_email');

  if (savedEmail && loginEmail) {
    loginEmail.value = savedEmail;
    if (rememberMe) rememberMe.checked = true;
  }

  document.getElementById('resetLoginForm')?.addEventListener('click', () => {
    document.getElementById('loginForm')?.reset();
  });

  document.getElementById('resetSignupForm')?.addEventListener('click', () => {
    document.getElementById('signupForm')?.reset();
    strengthBox?.classList.add('hidden');
  });

  document.getElementById('dismissToast')?.addEventListener('click', () => {
    document.getElementById('cornerToast')?.remove();
  });

  // ------------------------------------------------------------------------
  // 7. Welcome Celebration Modal & Session Management
  // ------------------------------------------------------------------------
  function openWelcomeModal(name, email, role) {
    const cleanName = name || 'User';
    const cleanRole = role || 'Enforcement officer';
    const cleanEmail = email || 'user@metrocheck.in';

    // Store active user session for the dashboard
    localStorage.setItem('sih_user_name', cleanName);
    localStorage.setItem('sih_user_role', cleanRole);
    localStorage.setItem('sih_auth_token', 'token_' + Date.now());

    // Update Welcome modal details
    document.getElementById('welcomeHeading').textContent = `Welcome, ${cleanName.split(' ')[0]}!`;
    document.getElementById('welcomeUserName').textContent = cleanName;
    document.getElementById('welcomeUserEmail').textContent = cleanEmail;
    document.getElementById('welcomeUserRole').textContent = cleanRole;

    // Generate avatar initials (e.g., "Anuska Yadav" -> "AY")
    const initials = cleanName
      .split(' ')
      .filter(Boolean)
      .map(part => part[0])
      .join('')
      .slice(0, 2)
      .toUpperCase() || 'MC';

    document.getElementById('welcomeAvatar').textContent = initials;
    document.getElementById('welcomeModal')?.classList.remove('hidden');
  }

  // Continue to Compliance Dashboard
  document.getElementById('welcomeContinueBtn')?.addEventListener('click', () => {
    window.location.href = 'dashboard.html';
  });

  // Sign out / switch account
  document.getElementById('welcomeLogoutBtn')?.addEventListener('click', () => {
    localStorage.removeItem('sih_auth_token');
    document.getElementById('welcomeModal')?.classList.add('hidden');
  });

  // ------------------------------------------------------------------------
  // 8. Log In Form Submission Handler
  // ------------------------------------------------------------------------
  document.getElementById('loginForm')?.addEventListener('submit', (e) => {
    e.preventDefault();

    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    const role = document.getElementById('loginRole').value;

    if (!email || !password) {
      showToast('Validation Error', 'Please enter both email and password.', 'error');
      return;
    }

    // Save or remove remembered email
    if (rememberMe?.checked) {
      localStorage.setItem('metrocheck_remembered_email', email);
    } else {
      localStorage.removeItem('metrocheck_remembered_email');
    }

    // Check if user was registered previously
    const registeredUsers = JSON.parse(localStorage.getItem('metrocheck_registered_users') || '[]');
    const matchedUser = registeredUsers.find(u => u.email.toLowerCase() === email.toLowerCase());

    let finalName = '';
    if (matchedUser && matchedUser.name) {
      finalName = matchedUser.name;
    } else {
      // Derive a clean name from email prefix (e.g., "anuska.yadav@gmail.com" -> "Anuska Yadav")
      const prefix = email.split('@')[0];
      finalName = prefix.replace(/[._-]/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
    }

    openWelcomeModal(finalName, email, role);
  });

  // ------------------------------------------------------------------------
  // 9. Sign Up Form Submission Handler
  // ------------------------------------------------------------------------
  document.getElementById('signupForm')?.addEventListener('submit', (e) => {
    e.preventDefault();

    const name = document.getElementById('signupName').value.trim();
    const email = document.getElementById('signupEmail').value.trim();
    const role = document.getElementById('signupRole').value;
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('signupConfirmPassword').value;

    if (!name || !email || !password) {
      showToast('Form Error', 'Please fill in all required fields.', 'error');
      return;
    }

    if (password !== confirmPassword) {
      showToast('Password Mismatch', 'The passwords you entered do not match.', 'error');
      return;
    }

    // Save newly created user
    const registeredUsers = JSON.parse(localStorage.getItem('metrocheck_registered_users') || '[]');
    registeredUsers.push({ name, email, role, password });
    localStorage.setItem('metrocheck_registered_users', JSON.stringify(registeredUsers));

    showToast('Account Created', 'Your compliance account was created successfully!', 'success');
    openWelcomeModal(name, email, role);
  });

  // ------------------------------------------------------------------------
  // 10. Google Sign-In Modal Simulation
  // ------------------------------------------------------------------------
  const googleModal = document.getElementById('googleModal');
  const openGoogle = () => googleModal?.classList.remove('hidden');
  const closeGoogle = () => googleModal?.classList.add('hidden');

  document.getElementById('googleLoginBtn')?.addEventListener('click', openGoogle);
  document.getElementById('googleSignupBtn')?.addEventListener('click', openGoogle);
  document.getElementById('closeGoogleModal')?.addEventListener('click', closeGoogle);

  // Click on a saved Google account
  document.querySelectorAll('.google-account-item').forEach(item => {
    item.addEventListener('click', () => {
      closeGoogle();
      const currentRole = document.getElementById('loginRole')?.value || 'Enforcement officer';
      openWelcomeModal(item.dataset.name, item.dataset.email, currentRole);
    });
  });

  // Continue with custom Google email address
  document.getElementById('googleCustomSubmit')?.addEventListener('click', () => {
    const customEmail = document.getElementById('googleCustomEmail')?.value.trim();
    if (!customEmail) return;

    closeGoogle();
    const currentRole = document.getElementById('loginRole')?.value || 'Enforcement officer';
    const prefix = customEmail.split('@')[0];
    const derivedName = prefix.replace(/[._-]/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
    openWelcomeModal(derivedName, customEmail, currentRole);
  });

});