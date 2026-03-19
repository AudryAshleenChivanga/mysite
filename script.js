/**
 * AUDRY ASHLEEN CHIVANGA - Portfolio
 * Enhanced JavaScript for interactions and animations
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize all modules
    initNavigation();
    initScrollEffects();
    initAnimations();
    initCounters();
    initContactForm();
    initCursorFollower();
    initGallery();
    loadExperience();
    loadProjects();
    
    console.log('%c✨ Welcome to Audry\'s Portfolio', 'color: #d4a853; font-size: 16px; font-weight: bold;');
    console.log('%cBuilding technology that transforms lives across Africa.', 'color: #a0a0a8; font-size: 14px;');
});

/**
 * Navigation Module
 */
function initNavigation() {
    const navbar = document.getElementById('navbar');
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Mobile menu toggle
    navToggle?.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        navToggle.classList.toggle('active');
        document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
    });
    
    // Close menu on link click
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            // Close mobile menu
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
            document.body.style.overflow = '';
            
            // Smooth scroll to section
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Navbar scroll effect
    let lastScrollY = window.scrollY;
    
    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;
        
        // Add scrolled class
        if (currentScrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        lastScrollY = currentScrollY;
    });
    
    // Active link highlighting
    const sections = document.querySelectorAll('section[id]');
    
    function setActiveLink() {
        const scrollPosition = window.scrollY + 150;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }
    
    window.addEventListener('scroll', throttle(setActiveLink, 100));
    setActiveLink();
    
    // Close menu on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
}

/**
 * Scroll Effects Module
 */
function initScrollEffects() {
    // Back to top button
    const backToTop = document.getElementById('backToTop');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 500) {
            backToTop?.classList.add('show');
        } else {
            backToTop?.classList.remove('show');
        }
    });
    
    backToTop?.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Parallax effect for hero
    const hero = document.querySelector('.hero');
    
    window.addEventListener('scroll', () => {
        if (hero && window.scrollY < window.innerHeight) {
            const scrolled = window.scrollY;
            hero.style.transform = `translateY(${scrolled * 0.3}px)`;
        }
    });
}

/**
 * Animations Module
 */
function initAnimations() {
    // Intersection Observer for reveal animations
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -100px 0px',
        threshold: 0.1
    };
    
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                
                // Stagger children animations
                const children = entry.target.querySelectorAll('.stagger-child');
                children.forEach((child, index) => {
                    child.style.transitionDelay = `${index * 0.1}s`;
                    child.classList.add('active');
                });
            }
        });
    }, observerOptions);
    
    // Observe elements
    const revealElements = document.querySelectorAll(`
        .timeline-item,
        .achievement-card,
        .skill-category,
        .gallery-item,
        .contact-card,
        .education-card,
        .startup-content,
        .research-callout,
        .experience-item,
        .project-card
    `);
    
    revealElements.forEach(el => {
        el.classList.add('reveal');
        revealObserver.observe(el);
    });
    
    // Section headers
    const sectionHeaders = document.querySelectorAll('.section-header');
    sectionHeaders.forEach(header => {
        header.classList.add('reveal');
        revealObserver.observe(header);
    });
    
    // About content
    const aboutContent = document.querySelector('.about-content');
    if (aboutContent) {
        aboutContent.classList.add('reveal');
        revealObserver.observe(aboutContent);
    }
}

/**
 * Counter Animation Module
 */
function initCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-count'));
                
                if (target) {
                    animateCounter(counter, target);
                }
                
                counterObserver.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
}

function animateCounter(element, target) {
    const duration = 2000;
    const steps = 60;
    const stepDuration = duration / steps;
    const increment = target / steps;
    let current = 0;
    
    const timer = setInterval(() => {
        current += increment;
        
        if (current >= target) {
            element.textContent = target + '+';
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current) + '+';
        }
    }, stepDuration);
}

/**
 * Load Experience Data Module
 */
async function loadExperience() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        const experiences = data.experience || [];
        
        // Find the container where you want to display experience
        const experienceContainer = document.getElementById('experience-section');
        if (!experienceContainer) {
            console.warn('Experience section container not found');
            return;
        }
        
        if (experiences.length === 0) {
            experienceContainer.innerHTML = '<p class="text-muted text-center py-5">No experience entries yet.</p>';
            return;
        }
        
        let html = '';
        experiences.forEach(exp => {
            html += `
                <div class="experience-item">
                    <div class="experience-header">
                        <h5 class="mb-1">${exp.title || 'Position'}</h5>
                        <h6 class="text-muted">${exp.organization || 'Organization'}</h6>
                    </div>
                    <div class="experience-meta mb-2">
                        <span class="badge bg-primary">${(exp.type || 'experience').toUpperCase()}</span>
                        <small class="text-muted">
                            <i class="fas fa-calendar"></i> ${exp.date || 'Date'} | 
                            <i class="fas fa-map-marker-alt"></i> ${exp.location || 'Location'}
                        </small>
                    </div>
                    <p class="experience-description">${exp.description || 'No description'}</p>
                </div>
            `;
        });
        
        experienceContainer.innerHTML = html;
        
        // Trigger animations for newly added elements
        const experienceItems = experienceContainer.querySelectorAll('.experience-item');
        experienceItems.forEach(item => {
            item.classList.add('reveal');
            const observerOptions = {
                root: null,
                rootMargin: '0px 0px -100px 0px',
                threshold: 0.1
            };
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('active');
                    }
                });
            }, observerOptions);
            observer.observe(item);
        });
    } catch (error) {
        console.error('Error loading experience:', error);
        const experienceContainer = document.getElementById('experience-section');
        if (experienceContainer) {
            experienceContainer.innerHTML = '<p class="text-danger text-center">Error loading experience data</p>';
        }
    }
}

/**
 * Load Projects Data Module
 */
async function loadProjects() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        const projects = data.projects || [];
        
        // Find the container where you want to display projects
        const projectsContainer = document.getElementById('projects-section');
        if (!projectsContainer) {
            console.warn('Projects section container not found');
            return;
        }
        
        if (projects.length === 0) {
            projectsContainer.innerHTML = '<p class="text-muted text-center py-5">No projects yet.</p>';
            return;
        }
        
        let html = '';
        projects.forEach(project => {
            const featuredBadge = project.featured ? `<span class="badge bg-warning text-dark"><i class="fas fa-star"></i> Featured</span>` : '';
            const awardBadge = project.award ? `<span class="badge bg-success">${project.award}</span>` : '';
            const projectUrl = project.url ? `<a href="${project.url}" target="_blank" class="btn btn-sm btn-outline-primary mt-3"><i class="fas fa-external-link-alt"></i> View Project</a>` : '';
            
            html += `
                <div class="col-lg-6 mb-4">
                    <div class="project-card h-100">
                        <div class="project-header">
                            <h5>${project.name || 'Project'}</h5>
                            <div class="project-badges">
                                ${featuredBadge}
                                ${awardBadge}
                            </div>
                        </div>
                        <p class="project-description">${project.description || 'No description'}</p>
                        <div class="project-tags mb-3">
                            ${(project.tags || []).map(tag => `<span class="badge bg-light text-dark">${tag}</span>`).join('')}
                        </div>
                        ${projectUrl}
                    </div>
                </div>
            `;
        });
        
        projectsContainer.innerHTML = `<div class="row">${html}</div>`;
        
        // Trigger animations for newly added elements
        const projectItems = projectsContainer.querySelectorAll('.project-card');
        projectItems.forEach(item => {
            item.classList.add('reveal');
            const observerOptions = {
                root: null,
                rootMargin: '0px 0px -100px 0px',
                threshold: 0.1
            };
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('active');
                    }
                });
            }, observerOptions);
            observer.observe(item);
        });
    } catch (error) {
        console.error('Error loading projects:', error);
        const projectsContainer = document.getElementById('projects-section');
        if (projectsContainer) {
            projectsContainer.innerHTML = '<p class="text-danger text-center">Error loading projects data</p>';
        }
    }
}

/**
 * Contact Form Module
 */
function initContactForm() {
    const form = document.getElementById('contact-form');
    
    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            subject: formData.get('subject'),
            message: formData.get('message')
        };
        
        // Validate
        if (!data.name || !data.email || !data.subject || !data.message) {
            showNotification('Please fill in all fields.', 'error');
            return;
        }
        
        if (!isValidEmail(data.email)) {
            showNotification('Please enter a valid email address.', 'error');
            return;
        }
        
        // Submit button state
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalHTML = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        submitBtn.disabled = true;
        
        // Send to backend API
        try {
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                showNotification(result.message || 'Thank you! Your message has been sent successfully.', 'success');
                form.reset();
            } else {
                showNotification(result.error || 'Failed to send message. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            showNotification('Failed to send message. Please check your connection and try again.', 'error');
        } finally {
            submitBtn.innerHTML = originalHTML;
            submitBtn.disabled = false;
        }
    });
    
    // Input focus effects
    const inputs = form?.querySelectorAll('input, textarea');
    inputs?.forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', () => {
            if (!input.value) {
                input.parentElement.classList.remove('focused');
            }
        });
    });
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showNotification(message, type = 'info') {
    // Remove existing notification
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button class="notification-close">&times;</button>
    `;
    
    // Styles
    Object.assign(notification.style, {
        position: 'fixed',
        top: '100px',
        right: '20px',
        padding: '16px 24px',
        paddingRight: '50px',
        borderRadius: '10px',
        color: '#fff',
        fontWeight: '500',
        fontSize: '15px',
        zIndex: '10000',
        opacity: '0',
        transform: 'translateX(100%)',
        transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
        maxWidth: '400px',
        boxShadow: '0 10px 40px rgba(0, 0, 0, 0.3)'
    });
    
    // Colors based on type
    const colors = {
        success: 'linear-gradient(135deg, #10b981, #059669)',
        error: 'linear-gradient(135deg, #ef4444, #dc2626)',
        info: 'linear-gradient(135deg, #d4a853, #b8943f)'
    };
    
    notification.style.background = colors[type] || colors.info;
    
    // Close button styles
    const closeBtn = notification.querySelector('.notification-close');
    Object.assign(closeBtn.style, {
        position: 'absolute',
        right: '16px',
        top: '50%',
        transform: 'translateY(-50%)',
        background: 'none',
        border: 'none',
        color: '#fff',
        fontSize: '24px',
        cursor: 'pointer',
        opacity: '0.7'
    });
    
    document.body.appendChild(notification);
    
    // Animate in
    requestAnimationFrame(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    });
    
    // Close handlers
    const closeNotification = () => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => notification.remove(), 400);
    };
    
    closeBtn.addEventListener('click', closeNotification);
    setTimeout(closeNotification, 5000);
}

/**
 * Cursor Follower Module
 */
function initCursorFollower() {
    const cursor = document.querySelector('.cursor-follower');
    
    if (!cursor || window.matchMedia('(max-width: 768px)').matches) {
        if (cursor) cursor.style.display = 'none';
        return;
    }
    
    let mouseX = 0, mouseY = 0;
    let cursorX = 0, cursorY = 0;
    
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        
        if (cursor.style.opacity === '0') {
            cursor.style.opacity = '1';
        }
    });
    
    // Smooth cursor following
    function animateCursor() {
        const dx = mouseX - cursorX;
        const dy = mouseY - cursorY;
        
        cursorX += dx * 0.15;
        cursorY += dy * 0.15;
        
        cursor.style.left = cursorX + 'px';
        cursor.style.top = cursorY + 'px';
        
        requestAnimationFrame(animateCursor);
    }
    
    animateCursor();
    
    // Hover effects
    const interactiveElements = document.querySelectorAll('a, button, .gallery-item, .achievement-card, .timeline-content, .experience-item, .project-card');
    
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => cursor.classList.add('active'));
        el.addEventListener('mouseleave', () => cursor.classList.remove('active'));
    });
    
    // Hide on mouse leave window
    document.addEventListener('mouseleave', () => {
        cursor.style.opacity = '0';
    });
    
    document.addEventListener('mouseenter', () => {
        cursor.style.opacity = '1';
    });
}

/**
 * Gallery Module
 */
function initGallery() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    galleryItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            galleryItems.forEach(other => {
                if (other !== item) {
                    other.style.opacity = '0.5';
                }
            });
        });
        
        item.addEventListener('mouseleave', () => {
            galleryItems.forEach(other => {
                other.style.opacity = '1';
            });
        });
    });
}

/**
 * Utility Functions
 */
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

function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

/**
 * Loading State
 */
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
    
    // Trigger initial animations
    const heroContent = document.querySelector('.hero-content');
    const heroImage = document.querySelector('.hero-image');
    
    if (heroContent) {
        heroContent.style.animation = 'fadeInUp 1s ease forwards';
    }
    
    if (heroImage) {
        heroImage.style.animation = 'fadeInRight 1s ease 0.3s forwards';
    }
});

/**
 * Smooth Scroll Polyfill for older browsers
 */
if (!('scrollBehavior' in document.documentElement.style)) {
    const smoothScroll = (target) => {
        const targetPosition = target.offsetTop - 80;
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        const duration = 800;
        let start = null;
        
        const animation = (currentTime) => {
            if (start === null) start = currentTime;
            const timeElapsed = currentTime - start;
            const progress = Math.min(timeElapsed / duration, 1);
            const ease = easeInOutCubic(progress);
            
            window.scrollTo(0, startPosition + distance * ease);
            
            if (timeElapsed < duration) {
                requestAnimationFrame(animation);
            }
        };
        
        requestAnimationFrame(animation);
    };
    
    const easeInOutCubic = (t) => {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    };
}

/**
 * Accessibility: Keyboard Navigation
 */
document.addEventListener('keydown', (e) => {
    // Skip to main content on Tab
    if (e.key === 'Tab' && !e.shiftKey) {
        const skipLink = document.querySelector('.skip-link');
        if (skipLink && document.activeElement === document.body) {
            skipLink.focus();
        }
    }
    
    // Scroll to top on Home key
    if (e.key === 'Home' && e.ctrlKey) {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    // Scroll to bottom on End key
    if (e.key === 'End' && e.ctrlKey) {
        e.preventDefault();
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }
});