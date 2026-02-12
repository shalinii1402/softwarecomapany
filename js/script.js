document.addEventListener('DOMContentLoaded', () => {

    /* =========================================
       1. THEME TOGGLE (Local Storage + System Pref)
       ========================================= */
    const themeToggle = document.getElementById('theme-toggle');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

    // Check for saved user preference, if any, on load
    const currentTheme = localStorage.getItem('theme');

    if (currentTheme) {
        document.documentElement.setAttribute('data-theme', currentTheme);
        updateToggleIcon(currentTheme);
    } else if (prefersDarkScheme.matches) {
        document.documentElement.setAttribute('data-theme', 'dark');
        updateToggleIcon('dark');
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            let theme = document.documentElement.getAttribute('data-theme');
            let newTheme = theme === 'dark' ? 'light' : 'dark';

            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateToggleIcon(newTheme);
        });
    }

    function updateToggleIcon(theme) {
        if (!themeToggle) return;
        if (theme === 'dark') {
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        }
    }

    /* =========================================
       2. MOBILE MENU HANDLING
       ========================================= */
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileBtn && navLinks) {
        mobileBtn.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent click from bubbling to body
            toggleMobileMenu();
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (navLinks.classList.contains('open') &&
                !navLinks.contains(e.target) &&
                !mobileBtn.contains(e.target)) {
                toggleMobileMenu();
            }
        });
    }

    function toggleMobileMenu() {
        navLinks.classList.toggle('open');
        document.body.classList.toggle('menu-open');
        const icon = mobileBtn.querySelector('i');
        if (navLinks.classList.contains('open')) {
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        } else {
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    }

    /* =========================================
       3. DROPDOWN HANDLING (Mobile Fix)
       ========================================= */
    // On mobile, clicking a dropdown parent should toggle the submenu
    const dropdowns = document.querySelectorAll('.dropdown > a');

    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', (e) => {
            if (window.innerWidth <= 991) {
                e.preventDefault();
                const parent = dropdown.parentElement;
                parent.classList.toggle('active');
            }
        });
    });

    // Close menu when clicking a link
    const navItems = document.querySelectorAll('.nav-links a:not(.dropdown > a)');
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            if (navLinks.classList.contains('open')) {
                toggleMobileMenu();
            }
        });
    });

    /* =========================================
       4. SCROLL ANIMATIONS (Intersection Observer)
       ========================================= */
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15 // Trigger when 15% visible
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Force opacity 1 immediately to ensure visibility if animation fails
                entry.target.style.opacity = '1';
                entry.target.classList.add('active');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => observer.observe(el));

    // Fallback: If intersection observer is not supported or fails, check visibility manually on load
    if (animatedElements.length > 0) {
        setTimeout(() => {
            animatedElements.forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.top < window.innerHeight) {
                    el.style.opacity = '1';
                    el.classList.add('active');
                }
            });
        }, 500);
    }

    /* =========================================
       5. BACK TO TOP BUTTON
       ========================================= */
    const backToTopBtn = document.getElementById('back-to-top');

    if (backToTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        });

        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    /* =========================================
       6. FORM VALIDATION (Simple)
       ========================================= */
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            let isValid = true;

            // Basic Input Validation
            const inputs = form.querySelectorAll('input, textarea');
            inputs.forEach(input => {
                if (input.type !== 'submit') {
                    // Remove existing error styles
                    input.style.borderColor = 'var(--border-color)';

                    if (!input.value.trim()) {
                        isValid = false;
                        input.style.borderColor = 'red';
                        // Optional: Add shake animation or error message
                    } else if (input.type === 'email' && !validateEmail(input.value)) {
                        isValid = false;
                        input.style.borderColor = 'red';
                    }
                }
            });

            if (isValid) {
                // Simulate submission
                const btn = form.querySelector('button[type="submit"]');
                const originalText = btn.innerHTML;

                btn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Processing...';
                btn.disabled = true;

                setTimeout(() => {
                    alert('Success! Form submitted.');
                    form.reset();
                    btn.innerHTML = originalText;
                    btn.disabled = false;
                }, 1500);
            } else {
                alert('Please fill in all fields correctly.');
            }
        });
    });

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

});

/* =========================================
   7. PROJECT FILTERING LOGIC
   ========================================= */
function filterProjects(category) {
    const buttons = document.querySelectorAll('.filter-btn');
    const projects = document.querySelectorAll('.project-card');

    // Update active button state
    buttons.forEach(btn => {
        btn.classList.remove('active');
        // Handle onclick event structure by text fallback
        if (btn.innerText.toLowerCase() === category
            || (category === 'all' && btn.innerText.toLowerCase() === 'all')
            || (btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(`'${category}'`))) {
            btn.classList.add('active');
        }
    });

    // Filter projects
    projects.forEach(card => {
        const projectCategory = card.getAttribute('data-category');

        // Reset animation for smoothness
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';

        setTimeout(() => {
            if (category === 'all' || (projectCategory && projectCategory === category)) {
                card.style.display = 'block';
                // Trigger reflow
                void card.offsetWidth;
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            } else {
                card.style.display = 'none';
            }
        }, 300); // Wait for fade out
    });
}