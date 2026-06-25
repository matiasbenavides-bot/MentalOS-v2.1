import { Storage } from './storage.js';
import { todayStr, calculateBasal, getCredits } from './state.js';
import { switchView } from './ui.js';
import { renderHome } from './components/home.js';
import { renderExploit } from './components/exploit.js';
import { renderAnalysis } from './components/analysis.js';
import { renderEmergency } from './components/emergency.js';
import { openConfigModal } from './components/config.js';

let currentView = 'home';

document.addEventListener('DOMContentLoaded', () => {
  // PIN screen
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

  // Bottom nav
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      switchView(btn.dataset.view);
      currentView = btn.dataset.view;
      navigate(currentView);
    });
  });

  // Config button
  document.getElementById('config-btn').addEventListener('click', openConfigModal);
});

function initApp() {
  navigate('home');
  updateTopBar();
}

export function navigate(view) {
  switch(view) {
    case 'home': renderHome(); break;
    case 'exploit': renderExploit(); break;
    case 'analysis': renderAnalysis(); break;
    case 'emergency': renderEmergency(); break;
  }
  updateTopBar();
}

export function updateTopBar() {
  const basal = calculateBasal();
  const credits = Storage.getCredits();
  const dot = document.getElementById('status-dot');
  dot.className = 'status-dot ' + basal.mode;
  document.getElementById('status-score').textContent = basal.score !== null ? basal.score : '--';
  const label = basal.mode === 'green' ? 'Explotación disponible' : (basal.mode === 'yellow' ? 'Limitado' : 'Protección');
  document.getElementById('status-label').textContent = label;
  document.getElementById('credits-count').textContent = credits;
  // Emergency nav visibility
  const navEm = document.getElementById('nav-emergency');
  if (basal.mode === 'red') navEm.classList.remove('atenuado');
  else navEm.classList.add('atenuado');
}
