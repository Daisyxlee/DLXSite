/**
 * DLX Solution - main.js
 * Promo banner, language picker, smooth scroll for anchors
 */
(function () {
  const messages = [
    "Founder's Launch Kit is now available at an introductory rate for early clients.",
    "Launch your website, branded business email, and LinkedIn company page in one streamlined package.",
    "Build a credible digital presence faster with DLX Solution's startup-ready launch support."
  ];

  const banner = document.getElementById("promoBanner");
  const messageEl = document.getElementById("promoMessage");
  const closeEl = document.getElementById("promoClose");

  if (!banner || !messageEl || !closeEl) return;

  document.body.classList.add("has-promo-banner");

  let index = 0;
  let intervalId = null;

  function renderMessage(nextIndex) {
    messageEl.classList.add("is-exiting");

    setTimeout(function () {
      messageEl.textContent = messages[nextIndex];
      messageEl.classList.remove("is-exiting");
      messageEl.classList.add("is-entering");

      setTimeout(function () {
        messageEl.classList.remove("is-entering");
      }, 350);
    }, 220);
  }

  messageEl.textContent = messages[index];

  if (messages.length > 1) {
    intervalId = setInterval(function () {
      index = (index + 1) % messages.length;
      renderMessage(index);
    }, 4000);
  }

  closeEl.addEventListener("click", function () {
    banner.style.display = "none";
    document.body.classList.remove("has-promo-banner");
    if (intervalId) clearInterval(intervalId);
  });
})();

document.addEventListener('DOMContentLoaded', function () {
  const langSelect = document.getElementById('lang-select');
  if (langSelect) {
    langSelect.addEventListener('change', function () {
      const lang = this.value;
      const url = new URL(window.location.href);
      url.searchParams.set('lang', lang);
      window.location.href = url.toString();
    });
  }

  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
});
