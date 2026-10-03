(function () {
  'use strict';

  // Calendrier des disponibilités : la section reste masquée tant que
  // les données ne sont pas chargées.
  var section = document.querySelector('[data-availability]');
  if (!section || !window.fetch) return;

  var english = document.documentElement.lang === 'en';
  var locale = english ? 'en-GB' : 'fr-FR';
  var labels = english
    ? { free: 'available', booked: 'unavailable' }
    : { free: 'disponible', booked: 'indisponible' };
  var MONTHS_SHOWN = 2;
  var MAX_OFFSET = 11;

  var monthsEl = section.querySelector('.cal-months');
  var prevBtn = section.querySelector('.cal-prev');
  var nextBtn = section.querySelector('.cal-next');
  var monthFormat = new Intl.DateTimeFormat(locale, { month: 'long', year: 'numeric' });
  var weekdayFormat = new Intl.DateTimeFormat(locale, { weekday: 'narrow' });
  var booked = {};
  var offset = 0;

  function pad(n) { return n < 10 ? '0' + n : String(n); }
  function iso(date) { return date.getFullYear() + '-' + pad(date.getMonth() + 1) + '-' + pad(date.getDate()); }
  function parse(text) {
    var parts = text.split('-');
    return new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
  }

  // Chaque plage va du jour d'arrivée (inclus) au jour de départ (exclu).
  function indexBooked(ranges) {
    ranges.forEach(function (range) {
      var day = parse(range[0]);
      var end = parse(range[1]);
      for (var guard = 0; day < end && guard < 800; guard++) {
        booked[iso(day)] = true;
        day.setDate(day.getDate() + 1);
      }
    });
  }

  function renderMonth(year, month, todayIso) {
    var first = new Date(year, month, 1);
    var wrapper = document.createElement('div');
    wrapper.className = 'cal-month';

    var title = document.createElement('h3');
    title.textContent = monthFormat.format(first);
    wrapper.appendChild(title);

    var grid = document.createElement('div');
    grid.className = 'cal-grid';
    for (var w = 0; w < 7; w++) {
      var head = document.createElement('span');
      head.className = 'cal-weekday';
      head.setAttribute('aria-hidden', 'true');
      head.textContent = weekdayFormat.format(new Date(2024, 0, 1 + w)); // le 1er janvier 2024 est un lundi
      grid.appendChild(head);
    }

    var blanks = (first.getDay() + 6) % 7; // semaine commençant le lundi
    for (var b = 0; b < blanks; b++) grid.appendChild(document.createElement('span'));

    var daysInMonth = new Date(year, month + 1, 0).getDate();
    for (var d = 1; d <= daysInMonth; d++) {
      var key = year + '-' + pad(month + 1) + '-' + pad(d);
      var cell = document.createElement('span');
      cell.textContent = d;
      if (key < todayIso) {
        cell.className = 'cal-day past';
      } else if (booked[key]) {
        cell.className = 'cal-day booked';
        cell.setAttribute('aria-label', d + ' : ' + labels.booked);
      } else {
        cell.className = 'cal-day free';
        cell.setAttribute('aria-label', d + ' : ' + labels.free);
      }
      grid.appendChild(cell);
    }

    wrapper.appendChild(grid);
    return wrapper;
  }

  function render() {
    var today = new Date();
    var todayIso = iso(today);
    monthsEl.textContent = '';
    for (var i = 0; i < MONTHS_SHOWN; i++) {
      var month = new Date(today.getFullYear(), today.getMonth() + offset + i, 1);
      monthsEl.appendChild(renderMonth(month.getFullYear(), month.getMonth(), todayIso));
    }
    prevBtn.disabled = offset === 0;
    nextBtn.disabled = offset >= MAX_OFFSET;
  }

  function load(urls) {
    if (!urls.length) return Promise.reject(new Error('no availability data'));
    return fetch(urls[0], { cache: 'no-store' })
      .then(function (response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.json();
      })
      .then(function (data) {
        if (!data || !Array.isArray(data.booked)) throw new Error('unexpected data');
        return data;
      })
      .catch(function () { return load(urls.slice(1)); });
  }

  prevBtn.addEventListener('click', function () { if (offset > 0) { offset--; render(); } });
  nextBtn.addEventListener('click', function () { if (offset < MAX_OFFSET) { offset++; render(); } });

  // La copie du dépôt est la plus fraîche ; celle du site sert de secours.
  load([section.getAttribute('data-remote'), section.getAttribute('data-src')].filter(Boolean))
    .then(function (data) {
      indexBooked(data.booked);
      render();
      section.hidden = false;
    })
    .catch(function () { /* pas de données : la section reste masquée */ });
})();
