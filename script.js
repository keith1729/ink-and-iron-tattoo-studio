const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav-links');
const filterButtons = document.querySelectorAll('.filter-btn');
const cards = document.querySelectorAll('.gallery-card');
const form = document.getElementById('booking-form');
const status = document.getElementById('form-status');

if (toggle && nav) {
  toggle.addEventListener('click', () => nav.classList.toggle('open'));
  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => nav.classList.remove('open'));
  });
}

filterButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    filterButtons.forEach((btn) => btn.classList.remove('active'));
    button.classList.add('active');

    cards.forEach((card) => {
      const isVisible = filter === 'all' || card.dataset.category === filter;
      card.style.display = isVisible ? 'block' : 'none';
    });
  });
});

if (form) {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!form.checkValidity()) {
      status.textContent = 'Please complete all required fields before submitting.';
      form.reportValidity();
      return;
    }

    const selectedDate = new Date(form.date.value);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    if (selectedDate < today) {
      status.textContent = 'Please choose a future date for your appointment request.';
      return;
    }

    status.textContent = 'Request received. Our team will contact you within 24 hours.';
    form.reset();
  });
}

const year = document.getElementById('year');
if (year) {
  year.textContent = String(new Date().getFullYear());
}

const revealElements = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.2 });

revealElements.forEach((element) => observer.observe(element));
