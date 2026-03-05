(function () {
    function triggerLoading(btn, event) {
        if (event) {
            event.preventDefault();
        }
        if (!btn || btn.disabled) {
            return;
        }

        const btnText = btn.querySelector('.btn-text-container');
        const spinner = btn.querySelector('.btn-spinner-container');

        if (btnText && spinner) {
            btnText.classList.add('hidden');
            spinner.classList.remove('hidden');
            spinner.classList.add('flex');
        }

        btn.disabled = true;

        const form = btn.closest('form');
        if (form) {
            setTimeout(() => form.submit(), 500);
        }
    }

    function togglePasswordVisibility(inputId, iconId) {
        const input = document.getElementById(inputId);
        const icon = document.getElementById(iconId);
        if (!input || !icon) {
            return;
        }

        if (input.type === 'password') {
            input.type = 'text';
            icon.textContent = 'visibility_off';
        } else {
            input.type = 'password';
            icon.textContent = 'visibility';
        }
    }

    function toggleTermsDropdown() {
        const dropdown = document.getElementById('terms-dropdown');
        const chevron = document.getElementById('terms-chevron');
        if (!dropdown || !chevron) {
            return;
        }

        if (dropdown.style.maxHeight && dropdown.style.maxHeight !== '0px') {
            dropdown.style.maxHeight = '0px';
            dropdown.style.opacity = '0';
            chevron.style.transform = 'rotate(0deg)';
        } else {
            dropdown.style.maxHeight = '250px';
            dropdown.style.opacity = '1';
            chevron.style.transform = 'rotate(180deg)';
        }
    }

    function resetLoginForm() {
        const loginForm = document.getElementById('login-form');
        const loginSubmitBtn = document.getElementById('login-submit-btn');
        const loginIcon = document.getElementById('login-p-icon');
        const passwordInput = document.getElementById('id_password');
        const errorFlag = document.getElementById('login-error-flag');

        if (loginForm) {
            loginForm.reset();
        }

        if (errorFlag) {
            errorFlag.classList.add('hidden');
        }

        if (passwordInput && loginIcon) {
            passwordInput.type = 'password';
            loginIcon.textContent = 'visibility';
        }

        if (loginSubmitBtn) {
            loginSubmitBtn.disabled = true;
        }
    }

    function resetSignupForm() {
        const signupForm = document.getElementById('signup-form');
        const signupBtn = document.getElementById('signup-submit-btn');
        const termsDropdown = document.getElementById('terms-dropdown');
        const termsChevron = document.getElementById('terms-chevron');

        if (signupForm) {
            signupForm.reset();
            signupForm.querySelectorAll('input').forEach((input) => {
                input.classList.remove('input-match-success', 'input-match-error');
            });
        }

        ['username-hint', 'email-hint', 'pass-hint', 'match-hint'].forEach((hintId) => {
            const hintEl = document.getElementById(hintId);
            if (hintEl) {
                hintEl.classList.add('hidden');
            }
        });

        const passHint = document.getElementById('pass-hint');
        if (passHint) {
            passHint.classList.remove('hidden');
            passHint.textContent = 'At least 8 characters required';
            passHint.style.color = '#94a3b8';
        }

        if (termsDropdown && termsChevron) {
            termsDropdown.style.maxHeight = '0px';
            termsDropdown.style.opacity = '0';
            termsChevron.style.transform = 'rotate(0deg)';
        }

        if (signupBtn) {
            signupBtn.disabled = true;
        }
    }

    function toggleAuthMode(mode) {
        const loginContainer = document.getElementById('login-form-container');
        const signupContainer = document.getElementById('signup-form-container');

        if (!loginContainer || !signupContainer) {
            return;
        }

        loginContainer.classList.toggle('hidden', mode !== 'login');
        signupContainer.classList.toggle('hidden', mode !== 'signup');

        setTimeout(() => {
            const selector = mode === 'login'
                ? '#login-form-container input[name="username"]'
                : '#signup-form-container input[name="username"]';
            const input = document.querySelector(selector);
            if (input) {
                input.focus();
            }
        }, 50);
    }

    function openAuthModal(mode) {
        const modal = document.getElementById('auth-modal');
        if (!modal) {
            return;
        }

        modal.classList.remove('hidden');
        modal.classList.add('flex');
        document.body.style.overflow = 'hidden';
        toggleAuthMode(mode || 'login');

        setTimeout(() => {
            const selector = mode === 'signup'
                ? '#signup-form-container input[name="username"]'
                : '#login-form-container input[name="username"]';
            const input = document.querySelector(selector);
            if (input) {
                input.focus();
            }
        }, 250);
    }

    function closeAuthModal() {
        const modal = document.getElementById('auth-modal');
        if (!modal) {
            return;
        }

        modal.classList.add('hidden');
        modal.classList.remove('flex');
        document.body.style.overflow = 'auto';

        resetLoginForm();
        resetSignupForm();

        const url = new URL(window.location.href);
        if (url.searchParams.has('signup_success') || url.searchParams.has('reset_success')) {
            url.searchParams.delete('signup_success');
            url.searchParams.delete('reset_success');
            window.history.replaceState({}, document.title, url.pathname + url.search);
        }
    }

    function initMessageAutoDismiss() {
        const messages = document.querySelectorAll('#message-container > div');
        messages.forEach((message) => {
            setTimeout(() => {
                message.classList.add('opacity-0', '-translate-y-4');
                setTimeout(() => message.remove(), 500);
            }, 5000);
        });
    }

    function initLoginFormValidation() {
        const form = document.getElementById('login-form');
        const submitBtn = document.getElementById('login-submit-btn');
        if (!form || !submitBtn) {
            return;
        }

        const username = form.querySelector('input[name="username"]');
        const password = form.querySelector('input[name="password"]');
        if (!username || !password) {
            return;
        }

        const validate = () => {
            const isReady = username.value.trim().length > 0 && password.value.trim().length > 0;
            submitBtn.disabled = !isReady;
        };

        [username, password].forEach((input) => {
            input.addEventListener('input', validate);
        });

        validate();
    }

    function initSignupFormValidation() {
        const form = document.getElementById('signup-form');
        const submitBtn = document.getElementById('signup-submit-btn');
        const termsCheck = document.getElementById('terms_check');
        if (!form || !submitBtn || !termsCheck) {
            return;
        }

        const username = form.querySelector('input[name="username"]');
        const email = form.querySelector('input[name="email"]');
        const password1 = form.querySelector('input[name="password1"]');
        const password2 = form.querySelector('input[name="password2"]');

        if (!username || !email || !password1 || !password2) {
            return;
        }

        function applyStyle(el, hintId, message, isSuccess) {
            const hint = document.getElementById(hintId);
            el.classList.remove('input-match-success', 'input-match-error');
            el.classList.add(isSuccess ? 'input-match-success' : 'input-match-error');

            if (hint) {
                hint.textContent = message;
                hint.style.color = isSuccess ? '#10b981' : '#ef4444';
                hint.classList.remove('hidden');
            }
        }

        function clearStyle(el, hintId) {
            el.classList.remove('input-match-success', 'input-match-error');
            const hint = document.getElementById(hintId);
            if (hint) {
                hint.classList.add('hidden');
            }
        }

        const validate = () => {
            let isValid = true;

            if (username.value.length > 0 && username.value.length < 3) {
                applyStyle(username, 'username-hint', 'Too short', false);
                isValid = false;
            } else if (username.value.length >= 3) {
                applyStyle(username, 'username-hint', 'Looks good!', true);
            } else {
                clearStyle(username, 'username-hint');
            }

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (email.value.length > 0) {
                if (!emailRegex.test(email.value)) {
                    applyStyle(email, 'email-hint', 'Invalid email format', false);
                    isValid = false;
                } else {
                    applyStyle(email, 'email-hint', 'Valid email', true);
                }
            } else {
                clearStyle(email, 'email-hint');
            }

            if (password1.value.length > 0) {
                if (password1.value.length < 8) {
                    applyStyle(password1, 'pass-hint', 'Minimum 8 characters required', false);
                    isValid = false;
                } else {
                    applyStyle(password1, 'pass-hint', 'Strong password', true);
                }
            } else {
                const passHint = document.getElementById('pass-hint');
                password1.classList.remove('input-match-success', 'input-match-error');
                if (passHint) {
                    passHint.classList.remove('hidden');
                    passHint.textContent = 'At least 8 characters required';
                    passHint.style.color = '#94a3b8';
                }
            }

            if (password1.value.length > 0 && password2.value.length > 0) {
                if (password1.value !== password2.value) {
                    applyStyle(password2, 'match-hint', 'Passwords do not match', false);
                    isValid = false;
                } else {
                    applyStyle(password2, 'match-hint', 'Passwords match', true);
                }
            } else {
                clearStyle(password2, 'match-hint');
            }

            const allFilled = username.value && email.value && password1.value && password2.value && termsCheck.checked;
            submitBtn.disabled = !(isValid && allFilled);
        };

        [username, email, password1, password2].forEach((input) => {
            input.addEventListener('input', validate);
        });
        termsCheck.addEventListener('change', validate);

        submitBtn.disabled = true;
    }

    function initModalStatesFromFlags() {
        const loginError = document.getElementById('login-error-flag');
        if (loginError) {
            openAuthModal('login');
            loginError.classList.add('shake-error');
            return;
        }

        const signupError = document.getElementById('signup-error-flag');
        if (signupError) {
            openAuthModal('signup');
            signupError.classList.add('shake-error');
            return;
        }

        const urlParams = new URLSearchParams(window.location.search);
        const signupSuccess = urlParams.get('signup_success') === 'true';
        const resetSuccess = urlParams.get('reset_success') === 'true';
        if (signupSuccess || resetSuccess) {
            setTimeout(() => openAuthModal('login'), 150);
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        initMessageAutoDismiss();
        initLoginFormValidation();
        initSignupFormValidation();
        initModalStatesFromFlags();
    });

    window.triggerLoading = triggerLoading;
    window.togglePasswordVisibility = togglePasswordVisibility;
    window.toggleTermsDropdown = toggleTermsDropdown;
    window.openAuthModal = openAuthModal;
    window.closeAuthModal = closeAuthModal;
    window.toggleAuthMode = toggleAuthMode;
})();
