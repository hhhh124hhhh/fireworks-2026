// =====================
// Cyberpunk Portfolio JavaScript
// =====================

// =====================
// CONFIGURATION
// =====================
const CONFIG = {
    // Typewriter Effect
    typing: {
        text: "构建智能技能生态 · 重新定义人机协作",
        speed: 100,
        delay: 1000,
        cursor: "█",
        glitch: true
    },

    // Number Counter
    counter: {
        duration: 2000,
        easing: 'easeOutQuart'
    },

    // Matrix Rain
    matrix: {
        chars: 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789ABCDEF',
        fontSize: 14,
        speed: 50,
        opacity: 0.15
    },

    // Cursor
    cursor: {
        size: 20,
        hoverScale: 2,
        transition: 100
    },

    // Ripple
    ripple: {
        duration: 600
    }
};

// =====================
// UTILITIES
// =====================
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

// Easing Functions
const easingFunctions = {
    easeOutQuart: (t) => 1 - (--t) * t * t * t,
    easeOutCubic: (t) => (--t) * t * t + 1,
    easeOutQuad: (t) => t * (2 - t)
};

// Request Animation Frame Wrapper
function raf(callback) {
    return window.requestAnimationFrame(callback);
}

// =====================
// MATRIX RAIN EFFECT
// =====================
function initMatrixRain() {
    const canvas = $('#matrix-rain');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let drops = [];
    let animationId;

    // Set canvas size
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const columns = Math.floor(canvas.width / CONFIG.matrix.fontSize);
        drops = Array(columns).fill(0);
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Draw matrix rain
    function draw() {
        ctx.fillStyle = 'rgba(10, 14, 10, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#00ff88';
        ctx.font = `${CONFIG.matrix.fontSize}px monospace`;

        for (let i = 0; i < drops.length; i++) {
            const char = CONFIG.matrix.chars.charAt(
                Math.floor(Math.random() * CONFIG.matrix.chars.length)
            );

            ctx.fillText(char, i * CONFIG.matrix.fontSize, drops[i] * CONFIG.matrix.fontSize);

            if (drops[i] * CONFIG.matrix.fontSize > canvas.height &&
                Math.random() > 0.975) {
                drops[i] = 0;
            }

            drops[i]++;
        }

        animationId = raf(draw);
    }

    draw();

    // Pause animation when not visible (performance optimization)
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            cancelAnimationFrame(animationId);
        } else {
            draw();
        }
    });
}

// =====================
// TYPEWRITER EFFECT
// =====================
function initTypewriter() {
    const element = $('#typewriter');
    if (!element) return;

    let charIndex = 0;
    let isDeleting = false;
    let isPaused = false;

    function type() {
        const currentText = CONFIG.typing.text;
        let displayText = currentText.substring(0, charIndex);

        // Add cursor
        element.innerHTML = displayText + '<span class="typewriter-cursor">' + CONFIG.typing.cursor + '</span>';

        if (!isPaused) {
            if (isDeleting) {
                charIndex--;
            } else {
                charIndex++;
            }
        }

        let speed = CONFIG.typing.speed;

        if (!isDeleting && charIndex === currentText.length) {
            isPaused = true;
            speed = CONFIG.typing.delay;

            setTimeout(() => {
                isPaused = false;
                type();
            }, speed);

            return;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            speed = 500;
        }

        if (isPaused) {
            isPaused = false;
        }

        setTimeout(type, speed);
    }

    type();
}

// =====================
// NUMBER COUNTER
// =====================
function initNumberCounter() {
    const counters = $$('.stat-number[data-target]');

    const observerOptions = {
        threshold: 0.5
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const target = parseInt(element.dataset.target);
                animateCounter(element, target);
                observer.unobserve(element);
            }
        });
    }, observerOptions);

    counters.forEach(counter => observer.observe(counter));
}

function animateCounter(element, target) {
    const duration = CONFIG.counter.duration;
    const easing = easingFunctions[CONFIG.counter.easing];
    let startTime = null;

    function update(currentTime) {
        if (!startTime) startTime = currentTime;
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easedProgress = easing(progress);

        element.textContent = Math.floor(target * easedProgress);

        if (progress < 1) {
            raf(update);
        } else {
            element.textContent = target;
        }
    }

    raf(update);
}

// =====================
// CUSTOM CURSOR
// =====================
function initCustomCursor() {
    const cursor = $('.custom-cursor');
    if (!cursor) return;

    let mouseX = 0;
    let mouseY = 0;
    let cursorX = 0;
    let cursorY = 0;

    // Track mouse position
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // Smooth cursor movement
    function updateCursor() {
        const dx = mouseX - cursorX;
        const dy = mouseY - cursorY;

        cursorX += dx * 0.2;
        cursorY += dy * 0.2;

        cursor.style.left = cursorX + 'px';
        cursor.style.top = cursorY + 'px';

        raf(updateCursor);
    }

    updateCursor();

    // Hover effect
    const hoverElements = $$('a, button, .neon-card, .project-card');

    hoverElements.forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursor.classList.add('hover');
        });

        el.addEventListener('mouseleave', () => {
            cursor.classList.remove('hover');
        });
    });

    // Hide cursor when leaving window
    document.addEventListener('mouseleave', () => {
        cursor.style.opacity = '0';
    });

    document.addEventListener('mouseenter', () => {
        cursor.style.opacity = '1';
    });
}

// =====================
// RIPPLE EFFECT
// =====================
function initRippleEffect() {
    const cards = $$('.neon-card');

    cards.forEach(card => {
        card.addEventListener('click', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';

            card.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, CONFIG.ripple.duration);
        });
    });
}

// =====================
// SMOOTH SCROLL
// =====================
function initSmoothScroll() {
    const links = $$('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = $(link.getAttribute('href'));

            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// =====================
 PERFORMANCE OPTIMIZATION
// =====================
function initPerformanceOptimization() {
    // Debounce function
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Throttle function
    function throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // Lazy load images (if any)
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            });
        });

        const lazyImages = $$('img[data-src]');
        lazyImages.forEach(img => imageObserver.observe(img));
    }

    // Optimize scroll events
    window.addEventListener('scroll', throttle(() => {
        // Any scroll-related optimizations
    }, 100));

    // Optimize resize events
    window.addEventListener('resize', debounce(() => {
        // Any resize-related optimizations
    }, 250));
}

// =====================
// ACCESSIBILITY
// =====================
function initAccessibility() {
    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

    function handleReducedMotion() {
        if (prefersReducedMotion.matches) {
            // Disable animations
            document.body.classList.add('reduced-motion');
        } else {
            document.body.classList.remove('reduced-motion');
        }
    }

    handleReducedMotion();
    prefersReducedMotion.addEventListener('change', handleReducedMotion);

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-nav');
        }
    });

    document.addEventListener('mousedown', () => {
        document.body.classList.remove('keyboard-nav');
    });

    // Focus visible styles
    const style = document.createElement('style');
    style.textContent = `
        body.keyboard-nav *:focus-visible {
            outline: 3px solid #00ff88 !important;
            outline-offset: 2px;
        }
    `;
    document.head.appendChild(style);
}

// =====================
// INITIALIZE ALL EFFECTS
// =====================
function initAll() {
    // Phase 2: Visual Effects
    initMatrixRain();

    // Phase 3: Animation Effects
    initTypewriter();
    initNumberCounter();

    // Phase 4: Interaction Effects
    initCustomCursor();
    initRippleEffect();

    // Utilities
    initSmoothScroll();

    // Performance & Accessibility
    initPerformanceOptimization();
    initAccessibility();

    console.log('🚀 Cyberpunk Portfolio Initialized');
    console.log('📊 Matrix Rain: Active');
    console.log('⌨️  Typewriter: Active');
    console.log('🔢 Counter: Active');
    console.log('🖱️  Cursor: Active');
    console.log('💫 Ripple: Active');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
} else {
    initAll();
}

// =====================
// EXPORT (for potential module usage)
// =====================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        CONFIG,
        initMatrixRain,
        initTypewriter,
        initNumberCounter,
        initCustomCursor,
        initRippleEffect
    };
}
