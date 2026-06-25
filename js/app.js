import { Storage } from './storage.js';
import { calculateBasal } from './state.js';
import { switchView } from './ui.js';
import { renderHome } from './components/home.js';
import { renderDevelopment } from './components/development.js';
import { renderAnalysis } from './components/analysis.js';
import { renderEmergency } from './components/emergency.js';
import { openConfigModal } from './components/config.js';

let currentView = 'home';

document.addEventListener('DOMContentLoaded', () => {
  const config = Storage.getConfig();
  document.getElementById('pin-btn').addEventListener('click', () => {
    if (document.getElementById('pin-input').value === config.pin) {
      document.getElementById('pin-screen').classList.add('hidden');
      document.getElementById('app').classList.remove('hidden');
      initApp();
    } else {
      document.getElementById('pin-error').classList.remove('hidden');
      document.getElementById('pin-error').textContent = 'PIN incorrecto';
    }
  });

  document.querySelectorAll('.top-nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      switchView(btn.dataset.view);
      currentView = btn.dataset.view;
      navigate(currentView);
    });
  });

  document.getElementById('config-btn').addEventListener('click', openConfigModal);
});

function initApp() { navigate('home'); updateTopBar(); }

export function navigate(view) {
  switch(view) {
    case 'home': renderHome(); break;
    case 'development': renderDevelopment(); break;
    case 'analysis': renderAnalysis(); break;
    case 'emergency': renderEmergency(); break;
  }
  updateTopBar();
}

export function updateTopBar() {
  const basal = calculateBasal();
  const credits = Storage.getCredits();
  document.getElementById('status-dot').className = 'status-dot ' + basal.mode;
  document.getElementById('status-score').textContent = basal.score ?? '--';
  document.getElementById('credits-count').textContent = credits;

  // Modo Rojo: ocultar pestañas Desarrollo y Análisis
  const navDev = document.querySelector('.top-nav-btn[data-view="development"]');
  const navAnalysis = document.querySelector('.top-nav-btn[data-view="analysis"]');
  const navEmergency = document.getElementById('nav-emergency');

  if (basal.mode === 'red') {
    if (navDev) navDev.classList.add('hidden');
    if (navAnalysis) navAnalysis.classList.add('hidden');
    if (navEmergency) navEmergency.classList.remove('hidden');
    // Si estaba en Desarrollo o Análisis, forzar vista a home
    if (currentView === 'development' || currentView === 'analysis') {
      navigate('home');
      switchView('home');
    }
  } else {
    if (navDev) navDev.classList.remove('hidden');
    if (navAnalysis) navAnalysis.classList.remove('hidden');
  }
  currentView = document.querySelector('.top-nav-btn.active')?.dataset.view || 'home';
}
