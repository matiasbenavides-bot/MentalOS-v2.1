import { Storage } from './storage.js';
import { calculateBasal, getCredits } from './state.js';
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
  document.querySelectorAll('.nav-btn').forEach(btn => {
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
  const credits = getCredits();
  document.getElementById('status-dot').className = 'status-dot ' + basal.mode;
  document.getElementById('status-score').textContent = basal.score ?? '--';
  document.getElementById('status-label').textContent = basal.mode === 'green' ? 'Explotación' : (basal.mode === 'yellow' ? 'Limitado' : 'Protección');
  document.getElementById('credits-count').textContent = credits;
  document.getElementById('nav-emergency').classList.toggle('atenuado', basal.mode !== 'red');
}
