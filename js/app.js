import { Storage } from './storage.js';
import { calculateBasal } from './state.js';
import { switchView } from './ui.js';
import { renderHome } from './components/home.js';
import { renderExploit } from './components/exploit.js';
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

  // Navegación superior
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
    case 'exploit': renderExploit(); break;
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
  // Oculta etiqueta de modo en esta versión (opcional)
  document.getElementById('credits-count').textContent = credits;
  // Atenuación de Emergencia si no es rojo
  const navEm = document.getElementById('nav-emergency');
  if (navEm) navEm.classList.toggle('atenuado', basal.mode !== 'red');
}
