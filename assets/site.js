document.documentElement.classList.add('js');
document.querySelectorAll('.menu-toggle').forEach(button => {
  const nav = document.getElementById(button.getAttribute('aria-controls'));
  button.addEventListener('click', () => {
    const expanded = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(expanded));
    nav.classList.toggle('is-open', expanded);
  });
  nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    button.setAttribute('aria-expanded', 'false');
    nav.classList.remove('is-open');
  }));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') {
      button.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
      button.focus();
    }
  });
});
document.querySelectorAll('.reveal-email').forEach(button => {
  button.addEventListener('click', () => {
    const address = ['chris', 'staikos', 'psychotherapy'].join('.') + '@' + ['proton', 'me'].join('.');
    const link = document.createElement('a');
    link.href = 'mailto:' + address;
    link.textContent = address;
    const result = button.closest('[data-email-container]').querySelector('.email-result');
    result.replaceChildren(link);
    button.hidden = true;
    link.focus();
  });
});
