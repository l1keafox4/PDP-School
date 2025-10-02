// Hi, my name is Jasurbek, i am 17 years old and i am from Uzbekistan 
// This html file contains the front-end code of my personal portfolio website. 
// Also take a look to my github to find more projects :-) https://github.com/l1keafox4 

// main.js — GSAP animations + small interactions

// 3D CAROUSEL FUNCTIONALITY
let currentProject = 0;
let projectInterval;
const totalProjects = 6;

function initProjectCarousel() {
    // Initialize rotation
    currentRotation = 0;
    
    // Start auto-rotation
    startAutoRotation();
    
    // Pause on hover
    const carousel = document.querySelector('.carousel-container');
    if (carousel) {
        carousel.addEventListener('mouseenter', stopAutoRotation);
        carousel.addEventListener('mouseleave', startAutoRotation);
    }
}

function startAutoRotation() {
    projectInterval = setInterval(() => {
        nextProject();
    }, 3000); // Every 3 seconds
}

function stopAutoRotation() {
    if (projectInterval) {
        clearInterval(projectInterval);
    }
}

let currentRotation = 0;

function updateCarousel() {
    const carousel = document.querySelector('.carousel-3d');
    const items = document.querySelectorAll('.carousel-item');
    const indicators = document.querySelectorAll('.indicator');
    
    if (!carousel) return;
    
    // Calculate target rotation angle (60 degrees per item for 6 items)
    const targetRotation = -currentProject * 60;
    
    // Find the shortest rotation path
    let rotationDiff = targetRotation - currentRotation;
    
    // Normalize the difference to be within -180 to 180 degrees
    while (rotationDiff > 180) rotationDiff -= 360;
    while (rotationDiff < -180) rotationDiff += 360;
    
    // Update current rotation
    currentRotation += rotationDiff;
    
    carousel.style.transform = `rotateY(${currentRotation}deg)`;
    
    // Update active states
    items.forEach((item, index) => {
        item.classList.toggle('active', index === currentProject);
    });
    
    indicators.forEach((indicator, index) => {
        indicator.classList.toggle('active', index === currentProject);
    });
}

function nextProject() {
    currentProject = (currentProject + 1) % totalProjects;
    updateCarousel();
}

function prevProject() {
    currentProject = (currentProject - 1 + totalProjects) % totalProjects;
    updateCarousel();
}

function goToProject(index) {
    if (index >= 0 && index < totalProjects) {
        currentProject = index;
        updateCarousel();
        
        // Restart auto-rotation
        stopAutoRotation();
        setTimeout(startAutoRotation, 1000);
    }
}

// Make functions global for onclick handlers
window.nextProject = nextProject;
window.prevProject = prevProject;
window.goToProject = goToProject;

document.addEventListener('DOMContentLoaded', () => {
    // refresh year
    const y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
    
    // Hero contact form interaction
    const contactBtn = document.querySelector('.contact-btn');
    if (contactBtn) {
        contactBtn.addEventListener('click', () => {
            // Можно добавить модальное окно или переход к секции контактов
            const contactSection = document.querySelector('#contact');
            if (contactSection) {
                contactSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
    
    // 3D Carousel initialization
    initProjectCarousel();
    
    // Smooth scrolling for navigation links
    function smoothScroll() {
        const navLinks = document.querySelectorAll('a[href^="#"]');
        
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                
                const targetId = link.getAttribute('href');
                const targetSection = document.querySelector(targetId);
                
                if (targetSection) {
                    const headerHeight = document.querySelector('.site-header').offsetHeight;
                    const targetPosition = targetSection.offsetTop - headerHeight;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                    
                    // Close mobile menu if open
                    const navToggle = document.querySelector('.nav-toggle');
                    const navMenu = document.querySelector('.nav-menu');
                    if (navToggle && navMenu) {
                        navToggle.setAttribute('aria-expanded', 'false');
                        navMenu.style.display = 'none';
                    }
                }
            });
        });
    }
    
    // Initialize smooth scrolling
    smoothScroll();
  
    // simple nav toggle for small screens
    const toggle = document.querySelector('.nav-toggle');
    if (toggle) {
      const nav = document.querySelector('.nav');
      const navMenu = document.querySelector('.nav-menu');
      toggle.addEventListener('click', () => {
        const expanded = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', String(!expanded));
        if (nav) nav.style.display = expanded ? 'none' : 'flex';
        if (navMenu) navMenu.style.display = expanded ? 'none' : 'flex';
      });
    }
  
    // generate and set a simple token for form (basic anti-bot)
    const tokenEl = document.getElementById('form_token');
    if (tokenEl) {
      tokenEl.value = btoa(Date.now().toString()).slice(0, 32);
    }
  
    // GSAP animations (if loaded)
    if (window.gsap) {
      gsap.registerPlugin(ScrollTrigger);
  
      // hero elements animation
      gsap.from('.hero-left .hero-title', {y: 30, opacity: 0, duration: 0.8, ease: 'power3.out'});
      gsap.from('.hero-left .hero-lead', {y: 18, opacity: 0, duration: 0.8, delay: 0.15});
      gsap.from('.hero-left .hero-cta', {y: 10, opacity: 0, duration: 0.6, delay: 0.3});
      gsap.from('.hero-left .meta', {y: 10, opacity: 0, duration: 0.6, delay: 0.4});
  
      // profile card pop
      gsap.from('.profile-card', {scale: 0.96, opacity: 0, duration: 0.8, ease: 'elastic.out(1, 0.6)', delay: 0.35});
  
      // fade in sections (excluding work cards)
      gsap.utils.toArray('.section').forEach((el) => {
        gsap.from(el, {
          scrollTrigger: {
            trigger: el,
            start: 'top 85%',
          },
          y: 20,
          opacity: 0,
          duration: 0.7,
          ease: 'power2.out'
        });
      });
      
      // separate animation for work cards
      gsap.utils.toArray('.work-card').forEach((card, index) => {
        gsap.set(card, {opacity: 1, y: 0}); // ensure cards are visible initially
        gsap.from(card, {
          scrollTrigger: {
            trigger: card,
            start: 'top 90%',
          },
          y: 30,
          opacity: 0,
          duration: 0.6,
          delay: index * 0.1,
          ease: 'power2.out'
        });
      });
  
      // little parallax on hero-decor (if present)
      gsap.to('.hero-decor', {
        backgroundPosition: '0 50px',
        scrollTrigger: { scrub: true },
        duration: 2
      });
    }
  
    // form validation enhancement
    const form = document.getElementById('contactForm');
    if (form) {
      form.addEventListener('submit', (e) => {
        // simple client-side required check
        const name = form.querySelector('[name="name"]');
        const email = form.querySelector('[name="email"]');
        const msg = form.querySelector('[name="message"]');
        if (!name.value.trim() || !email.value.trim() || !msg.value.trim()) {
          e.preventDefault();
          alert('Please fill in all fields before submitting.');
        }
      });
    }
    
    // Active navigation highlighting
    function updateActiveNav() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav a, .nav-menu a');
        
        const scrollPosition = window.scrollY + 100;
        
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
    
    // Update active nav on scroll
    window.addEventListener('scroll', updateActiveNav);
    updateActiveNav(); // Initial call
  });
  
  // Copy to clipboard function
  function copyToClipboard(text, element) {
    navigator.clipboard.writeText(text).then(function() {
      // Show success feedback
      const originalText = element.textContent;
      element.textContent = 'Copied!';
      element.style.color = '#10B981';
      element.style.fontWeight = 'bold';
      
      // Reset after 2 seconds
      setTimeout(() => {
        element.textContent = originalText;
        element.style.color = '';
        element.style.fontWeight = '';
      }, 2000);
    }).catch(function(err) {
      console.error('Failed to copy text: ', err);
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      
      // Show feedback
      const originalText = element.textContent;
      element.textContent = 'Copied!';
      element.style.color = '#10B981';
      
      setTimeout(() => {
        element.textContent = originalText;
        element.style.color = '';
      }, 2000);
    });
  }
  
