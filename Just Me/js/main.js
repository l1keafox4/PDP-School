// Hi, my name is Jasurbek, i am 17 years old and i am from Uzbekistan 
// This html file contains the front-end code of my personal portfolio website. 
// Also take a look to my github to find more projects :-) https://github.com/l1keafox4 

let currentProject = 0;
let projectInterval;
let cooldownTimeout;
let currentRotation = 0;
let isInCooldown = false;
const totalProjects = 6;

function initProjectCarousel() {
    currentRotation = 0;
    
    startAutoRotation();
    
    const carousel = document.querySelector('.carousel-container');
    if (carousel) {
        carousel.addEventListener('mouseenter', stopAutoRotation);
        carousel.addEventListener('mouseleave', startAutoRotation);
    }
}

function startAutoRotation() {
    if (isInCooldown) {
        console.log('Auto rotation blocked - in cooldown');
        return;
    }
    projectInterval = setInterval(() => {
        currentProject = (currentProject + 1) % totalProjects;
        updateCarousel();
    }, 3000); // Every 3 seconds
    console.log('Auto rotation started');
}

function stopAutoRotation() {
    if (projectInterval) {
        clearInterval(projectInterval);
    }
}

function updateCarousel() {
    const carousel = document.querySelector('.carousel-3d');
    const items = document.querySelectorAll('.carousel-item');
    const indicators = document.querySelectorAll('.indicator');
    
    if (!carousel) return;
    
    const targetRotation = -currentProject * 60;
    
    let rotationDiff = targetRotation - currentRotation;
    
    while (rotationDiff > 180) rotationDiff -= 360;
    while (rotationDiff < -180) rotationDiff += 360;
    
    currentRotation += rotationDiff;
    
    carousel.style.transform = `rotateY(${currentRotation}deg)`;
    
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

function nextProjectWithCooldown() {
    console.log('Next button clicked!');
    stopAutoRotation();
    
    isInCooldown = true;
    
    if (cooldownTimeout) {
        clearTimeout(cooldownTimeout);
    }
    
    currentProject = (currentProject + 1) % totalProjects;
    console.log('Moving to project:', currentProject);
    updateCarousel();
    
    cooldownTimeout = setTimeout(() => {
        console.log('Cooldown finished, restarting auto rotation');
        isInCooldown = false;
        startAutoRotation();
    }, 5000); // 5 seconds cooldown
}

function prevProjectWithCooldown() {
    console.log('Prev button clicked!');
    stopAutoRotation();
    
    isInCooldown = true;
    
    if (cooldownTimeout) {
        clearTimeout(cooldownTimeout);
    }
    
    currentProject = (currentProject - 1 + totalProjects) % totalProjects;
    console.log('Moving to project:', currentProject);
    updateCarousel();
    
    cooldownTimeout = setTimeout(() => {
        console.log('Cooldown finished, restarting auto rotation');
        isInCooldown = false;
        startAutoRotation();
    }, 5000); // 5 seconds cooldown
}

function goToProject(index) {
    if (index >= 0 && index < totalProjects) {
        console.log('Indicator clicked for project:', index);
        
        stopAutoRotation();
        
        isInCooldown = true;
        
        if (cooldownTimeout) {
            clearTimeout(cooldownTimeout);
        }
        
        currentProject = index;
        updateCarousel();
        

        cooldownTimeout = setTimeout(() => {
            console.log('Cooldown finished, restarting auto rotation');
            isInCooldown = false;
            startAutoRotation();
        }, 5000); // 5 seconds cooldown
    }
}

window.nextProject = nextProjectWithCooldown;
window.prevProject = prevProjectWithCooldown;
window.goToProject = goToProject;

window.nextProjectOriginal = nextProject;
window.prevProjectOriginal = prevProject;

document.addEventListener('DOMContentLoaded', () => {
    const y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
    
    const contactBtn = document.querySelector('.contact-btn');
    if (contactBtn) {
        contactBtn.addEventListener('click', () => {
            const contactSection = document.querySelector('#contact');
            if (contactSection) {
                contactSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
    
    initProjectCarousel();
    
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
                    
                    const navToggle = document.querySelector('.nav-toggle');
                    const navMenu = document.querySelector('.nav-menu');
                    if (navToggle && navMenu && navToggle.getAttribute('aria-expanded') === 'true') {
                        navToggle.setAttribute('aria-expanded', 'false');
                        navMenu.style.display = 'none';
                    }
                }
            });
        });
    }
    
    smoothScroll();
  
    const toggle = document.querySelector('.nav-toggle');
    if (toggle) {
      const navMenu = document.querySelector('.nav-menu');
      
      function closeMenu() {
        toggle.setAttribute('aria-expanded', 'false');
        if (navMenu) navMenu.style.display = 'none';
      }
      
      function openMenu() {
        toggle.setAttribute('aria-expanded', 'true');
        if (navMenu) navMenu.style.display = 'flex';
      }
      
      toggle.addEventListener('click', (e) => {
        e.stopPropagation();
        const expanded = toggle.getAttribute('aria-expanded') === 'true';
        if (expanded) {
          closeMenu();
        } else {
          openMenu();
        }
      });
      
      document.addEventListener('click', (e) => {
        const expanded = toggle.getAttribute('aria-expanded') === 'true';
        if (expanded && !navMenu.contains(e.target) && !toggle.contains(e.target)) {
          closeMenu();
        }
      });
      
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
          closeMenu();
        }
      });
    }
  
    const tokenEl = document.getElementById('form_token');
    if (tokenEl) {
      tokenEl.value = btoa(Date.now().toString()).slice(0, 32);
    }
  
    if (window.gsap) {
      gsap.registerPlugin(ScrollTrigger);
  
      gsap.from('.hero-left .hero-title', {y: 30, opacity: 0, duration: 0.8, ease: 'power3.out'});
      gsap.from('.hero-left .hero-lead', {y: 18, opacity: 0, duration: 0.8, delay: 0.15});
      gsap.from('.hero-left .hero-cta', {y: 10, opacity: 0, duration: 0.6, delay: 0.3});
      gsap.from('.hero-left .meta', {y: 10, opacity: 0, duration: 0.6, delay: 0.4});
  
      gsap.from('.profile-card', {scale: 0.96, opacity: 0, duration: 0.8, ease: 'elastic.out(1, 0.6)', delay: 0.35});
  
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
      
      gsap.utils.toArray('.work-card').forEach((card, index) => {
        gsap.set(card, {opacity: 1, y: 0});
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
  
      gsap.to('.hero-decor', {
        backgroundPosition: '0 50px',
        scrollTrigger: { scrub: true },
        duration: 2
      });
    }
  
    const form = document.getElementById('contactForm');
    if (form) {
      form.addEventListener('submit', (e) => {
        const name = form.querySelector('[name="name"]');
        const email = form.querySelector('[name="email"]');
        const msg = form.querySelector('[name="message"]');
        if (!name.value.trim() || !email.value.trim() || !msg.value.trim()) {
          e.preventDefault();
          alert('Please fill in all fields before submitting.');
        }
      });
    }
    
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
    
    window.addEventListener('scroll', updateActiveNav);
    updateActiveNav(); 
  });
  
  function copyToClipboard(text, element) {
    navigator.clipboard.writeText(text).then(function() {

      const originalText = element.textContent;
      element.textContent = 'Copied!';
      element.style.color = 'white';
      element.style.fontWeight = 'bold';
      
      setTimeout(() => {
        element.textContent = originalText;
        element.style.color = '';
        element.style.fontWeight = '';
      }, 2000);
    }).catch(function(err) {
      console.error('Failed to copy text: ', err);

      const textArea = document.createElement('textarea');
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
    
      const originalText = element.textContent;
      element.textContent = 'Copied!';
      element.style.color = 'white';
      
      setTimeout(() => {
        element.textContent = originalText;
        element.style.color = '';
      }, 2000);
    });
  }
  
