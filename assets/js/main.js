/* Global Key Partners — main.js */

// ── Sticky header shadow ──────────────────────────────────
const header = document.querySelector('.site-header');
if (header) {
  window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', window.scrollY > 20);
  }, { passive: true });
}

// ── Mobile nav toggle ─────────────────────────────────────
const hamburger = document.querySelector('.hamburger');
const mobileNav = document.querySelector('.mobile-nav');
if (hamburger && mobileNav) {
  hamburger.addEventListener('click', () => {
    const open = mobileNav.classList.toggle('open');
    hamburger.classList.toggle('open', open);
    hamburger.setAttribute('aria-expanded', open);
    hamburger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.style.overflow = open ? 'hidden' : '';
  });
  // Close the drawer when a nav link inside it is tapped (e.g. same-page anchor)
  mobileNav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      mobileNav.classList.remove('open');
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', false);
      hamburger.setAttribute('aria-label', 'Open menu');
      document.body.style.overflow = '';
    });
  });
}

// ── FAQ accordion ─────────────────────────────────────────
document.querySelectorAll('.faq-question').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq-item');
    const isOpen = item.classList.contains('open');
    // Close all
    document.querySelectorAll('.faq-item.open').forEach(el => el.classList.remove('open'));
    // Open clicked (unless it was already open)
    if (!isOpen) item.classList.add('open');
  });
});

// ── Animate elements on scroll ────────────────────────────
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver(
    entries => entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('animate-in');
        io.unobserve(e.target);
      }
    }),
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );
  document.querySelectorAll('.card, .trust-item, .team-card, .stat-item')
    .forEach(el => io.observe(el));
}

// ── Active nav link ───────────────────────────────────────
const currentPath = window.location.pathname.replace(/\/$/, '') || '/';
document.querySelectorAll('.nav-link').forEach(link => {
  const href = link.getAttribute('href')?.replace(/\/$/, '') || '';
  if (href && currentPath.startsWith(href) && href !== '/' && href !== '/de') {
    link.classList.add('active');
  } else if ((href === '/' || href === '/de') && currentPath === href) {
    link.classList.add('active');
  }
});

// ── Form success message ───────────────────────────────────
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
  contactForm.addEventListener('submit', async e => {
    const action = contactForm.getAttribute('action') || '';
    if (action.includes('formspree')) return; // let Formspree redirect handle it
  });
}
