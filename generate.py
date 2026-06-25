#!/usr/bin/env python3
"""
MentalOS — Arquitectura fisiológica completa
Genera los archivos directamente en la carpeta actual.
"""

import os

FILES = {}

# ==================== index.html ====================
FILES["index.html"] = '''<!DOCTYPE html>
<html lang="es" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>MentalOS</title>
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="css/style.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body>
  <div id="pin-screen" class="fullscreen-center">
    <div class="pin-card">
      <h1>MentalOS</h1>
      <input type="password" id="pin-input" maxlength="4" placeholder="••••" inputmode="numeric" pattern="[0-9]*">
      <button id="pin-btn" class="btn-primary full-width">Entrar</button>
      <p id="pin-error" class="text-error hidden"></p>
    </div>
  </div>

  <div id="app" class="app-container hidden">
    <header class="topbar" id="topbar">
      <div class="topbar-row">
        <div class="status-badge" id="status-badge">
          <div class="status-dot" id="status-dot"></div>
          <span id="status-score">--</span>
        </div>
        <nav class="top-nav" id="top-nav">
          <button class="top-nav-btn active" data-view="home">Hoy</button>
          <button class="top-nav-btn" data-view="development">Desarrollo</button>
          <button class="top-nav-btn" data-view="analysis">Análisis</button>
          <button class="top-nav-btn" data-view="emergency" id="nav-emergency">Emergencia</button>
        </nav>
        <div class="topbar-actions">
          <span class="credits-badge">⚡<span id="credits-count">0</span></span>
          <button class="icon-btn" id="config-btn" title="Configuración">⚙</button>
        </div>
      </div>
    </header>

    <main id="viewport" class="viewport"></main>
  </div>

  <div id="modal-overlay" class="modal-overlay hidden">
    <div class="modal-container" id="modal-container">
      <div class="modal-header"><h2 id="modal-title"></h2><button class="modal-close" id="modal-close">✕</button></div>
      <div class="modal-body" id="modal-body"></div>
      <div class="modal-footer" id="modal-footer"></div>
    </div>
  </div>
  <div id="toast" class="toast hidden"></div>

  <script type="module" src="js/app.js"></script>
</body>
</html>'''

# ==================== css/style.css ====================
FILES["css/style.css"] = '''/* MentalOS — Neutralidad sensorial, móvil primero */
:root {
  --bg: #121212;
  --surface: #1c1c1c;
  --text: #d0d0d0;
  --text-secondary: #888;
  --border: #2a2a2a;
  --accent: #5c8aff;
  --green: #4caf50;
  --yellow: #ffc107;
  --red: #f44336;
  --radius: 10px;
  --transition: 0.2s ease;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Inter', system-ui, sans-serif;
  background: var(--bg); color: var(--text);
  height: 100vh; overflow: hidden;
  -webkit-tap-highlight-color: transparent;
}
.fullscreen-center { display: flex; align-items: center; justify-content: center; height: 100vh; background: var(--bg); }
.hidden { display: none !important; }

.pin-card { text-align: center; padding: 2rem; width: 260px; }
.pin-card h1 { margin-bottom: 1.5rem; font-size: 2rem; color: var(--text); }
#pin-input {
  width: 100%; padding: 0.7rem; font-size: 1.4rem; text-align: center;
  background: var(--surface); border: 1px solid var(--border); color: var(--text);
  border-radius: var(--radius); letter-spacing: 0.5em;
}
.text-error { color: var(--red); margin-top: 0.5rem; font-size: 0.85rem; }

.app-container { display: flex; flex-direction: column; height: 100vh; overflow: hidden; }

/* Topbar */
.topbar {
  background: var(--surface); border-bottom: 1px solid var(--border);
  padding: 0.4rem 0.6rem; flex-shrink: 0;
}
.topbar-row { display: flex; align-items: center; justify-content: space-between; gap: 0.3rem; }
.status-badge { display: flex; align-items: center; gap: 0.3rem; }
.status-dot { width: 12px; height: 12px; border-radius: 50%; background: var(--border); }
.status-dot.green { background: var(--green); }
.status-dot.yellow { background: var(--yellow); }
.status-dot.red { background: var(--red); }
.status-score { font-weight: 700; font-size: 0.9rem; }

.top-nav { display: flex; gap: 0.2rem; }
.top-nav-btn {
  background: none; border: none; color: var(--text-secondary); font-size: 0.7rem;
  padding: 0.2rem 0.4rem; border-radius: 4px; cursor: pointer;
}
.top-nav-btn.active { color: var(--accent); background: rgba(92,138,255,0.12); }
.topbar-actions { display: flex; align-items: center; gap: 0.4rem; }
.credits-badge { font-weight: 600; font-size: 0.8rem; }
.icon-btn { background: none; border: none; color: var(--text); font-size: 1.1rem; cursor: pointer; }

/* Viewport */
.viewport {
  flex: 1; overflow-y: auto; padding: 0.6rem;
  max-width: 600px; margin: 0 auto; width: 100%;
}

/* Chips Core */
.core-quick-panel { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-bottom: 0.8rem; }
.core-chip {
  display: flex; align-items: center; gap: 0.2rem;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 16px; padding: 0.3rem 0.6rem; cursor: pointer;
  font-size: 0.75rem;
}
.chip-value { font-weight: 500; }

/* Secciones de hábitos */
.habit-section { margin-bottom: 1rem; }
.section-title { font-size: 0.85rem; margin-bottom: 0.3rem; font-weight: 600; color: var(--text-secondary); }
.habit-list { display: flex; flex-direction: column; gap: 0.3rem; min-height: 30px; }

.habit-item {
  display: flex; align-items: center; gap: 0.4rem;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 0.5rem 0.6rem;
  cursor: pointer; user-select: none;
  transition: transform 0.15s, opacity 0.15s;
}
.habit-item.dragging { opacity: 0.5; transform: scale(0.96); }
.habit-item.completed { opacity: 0.6; }
.habit-checkbox {
  width: 18px; height: 18px; border-radius: 50%;
  border: 2px solid var(--border); flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.6rem; color: transparent;
}
.habit-item.completed .habit-checkbox {
  background: var(--green); border-color: var(--green); color: white;
}
.habit-info { flex: 1; display: flex; justify-content: space-between; align-items: center; }
.habit-name { font-size: 0.8rem; }
.habit-duration { font-size: 0.7rem; color: var(--text-secondary); }

.btn-add-habit {
  background: none; border: 1px dashed var(--border); color: var(--text-secondary);
  padding: 0.4rem; border-radius: var(--radius); cursor: pointer;
  text-align: center; font-size: 0.75rem; margin-top: 0.2rem;
}

/* Calendario semanal */
.mini-calendar { display: flex; gap: 0.3rem; margin: 0.8rem 0; justify-content: center; }
.calendar-day {
  width: 24px; height: 24px; border-radius: 50%;
  border: 1px solid var(--border); cursor: pointer;
  font-size: 0.6rem; display: flex; align-items: center; justify-content: center;
  background: var(--surface); color: var(--text-secondary);
}
.calendar-day.green { background: var(--green); border-color: var(--green); color: white; }
.calendar-day.yellow { background: var(--yellow); border-color: var(--yellow); color: black; }
.calendar-day.red { background: var(--red); border-color: var(--red); color: white; }

/* Botones */
.btn-primary {
  display: inline-block; background: var(--accent); color: white; border: none;
  padding: 0.6rem 1rem; border-radius: var(--radius); font-weight: 600; cursor: pointer;
  font-size: 0.85rem;
}
.btn-secondary {
  background: transparent; border: 1px solid var(--border); color: var(--text);
  padding: 0.5rem 0.8rem; border-radius: var(--radius); cursor: pointer; font-size: 0.8rem;
}
.full-width { width: 100%; display: block; }
.btn-giant {
  display: block; width: 100%; padding: 2rem; font-size: 1.2rem;
  background: var(--red); color: white; border: none; border-radius: var(--radius);
  cursor: pointer; font-weight: 700; text-align: center;
}

/* Modal */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 500;
  display: flex; align-items: flex-end; justify-content: center;
}
.modal-container {
  background: var(--surface); border-radius: 14px 14px 0 0; width: 100%;
  max-width: 500px; max-height: 85vh; overflow-y: auto; padding: 1.2rem 1rem 1.8rem;
  animation: slideUp 0.2s ease;
}
@keyframes slideUp { from { transform: translateY(15%); } to { transform: translateY(0); } }
.modal-header { display: flex; justify-content: space-between; margin-bottom: 0.8rem; }
.modal-close { background: none; border: none; color: var(--text); font-size: 1.3rem; cursor: pointer; }
.modal-body { margin-bottom: 0.8rem; }
.modal-footer { display: flex; gap: 0.4rem; justify-content: flex-end; }

.form-group { margin-bottom: 0.8rem; }
.form-group label { display: block; margin-bottom: 0.2rem; font-weight: 500; font-size: 0.8rem; }
input, select, textarea {
  width: 100%; padding: 0.5rem; background: var(--bg); border: 1px solid var(--border);
  color: var(--text); border-radius: 6px; font-size: 0.85rem; font-family: inherit;
}
textarea { resize: vertical; min-height: 70px; }

/* Pestañas internas */
.tab-bar { display: flex; gap: 0; border-bottom: 1px solid var(--border); margin-bottom: 0.8rem; }
.tab-btn {
  flex: 1; background: none; border: none; color: var(--text-secondary);
  padding: 0.4rem; font-size: 0.75rem; cursor: pointer; border-bottom: 2px solid transparent;
}
.tab-btn.active { color: var(--accent); border-bottom-color: var(--accent); }

/* Temporizador */
.timer-display { font-size: 2rem; text-align: center; font-weight: 700; padding: 1rem; }
.timer-rest { background: var(--yellow-bg); }

/* Contadores acumulativos */
.accumulator { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem; }
.accumulator-card {
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 0.8rem; text-align: center; flex: 1; min-width: 100px;
}
.accumulator-value { font-size: 1.8rem; font-weight: 700; }
.accumulator-label { font-size: 0.7rem; color: var(--text-secondary); }

/* Chart */
.chart-container { background: var(--surface); border-radius: var(--radius); padding: 0.8rem; margin-bottom: 0.8rem; }

/* Checklist */
.checklist-item {
  display: flex; align-items: center; gap: 0.6rem; padding: 0.6rem;
  background: var(--surface); border-radius: var(--radius); margin-bottom: 0.4rem;
  border: 1px solid var(--border);
}
.checklist-item.completed { background: rgba(76,175,80,0.12); border-color: var(--green); }
.checklist-item input[type="checkbox"] { width: 18px; height: 18px; accent-color: var(--green); }

/* Toast */
.toast {
  position: fixed; bottom: 60px; left: 50%; transform: translateX(-50%);
  background: var(--surface); border: 1px solid var(--border); color: var(--text);
  padding: 0.6rem 1.2rem; border-radius: 20px; z-index: 600;
  animation: fadeInOut 2s ease forwards;
}
@keyframes fadeInOut {
  0% { opacity: 0; bottom: 40px; } 20% { opacity: 1; bottom: 60px; }
  80% { opacity: 1; bottom: 60px; } 100% { opacity: 0; bottom: 40px; }
}

/* Drag ghost */
.drag-ghost { position: fixed; opacity: 0.8; pointer-events: none; z-index: 999; }

/* Reproductor interno */
.video-iframe { width: 100%; height: 200px; border: none; border-radius: var(--radius); margin: 0.5rem 0; }
'''

# ==================== js/storage.js ====================
FILES["js/storage.js"] = '''const PREFIX = 'mentalo_';
export const Storage = {
  get(key) {
    try { return JSON.parse(localStorage.getItem(PREFIX + key)); } catch { return null; }
  },
  set(key, value) { localStorage.setItem(PREFIX + key, JSON.stringify(value)); },
  getLogs() { return this.get('logs') || {}; },
  addLog(date, data) {
    const logs = this.getLogs();
    logs[date] = data;
    this.set('logs', logs);
  },
  getConfig() {
    return this.get('config') || {
      pin: '2207',
      emergencyChecklist: ['Ducharse o lavarse la cara','Comer algo','Salir 5 minutos al aire libre','Mensaje a contacto de confianza','Leer 1 página de un libro favorito'],
      supportMessage: 'Tu cerebro está experimentando una baja química temporal. Esto va a pasar. Solo cumple estas 5 cosas y tu día habrá sido un éxito.'
    };
  },
  setConfig(c) { this.set('config', c); },
  getHabits() {
    let habits = this.get('habits');
    if (!habits || habits.length === 0) {
      habits = [
        { id: 'h1', name: 'Hidratación y Luz Solar', section: 'morning', duration: 5, order: 0 },
        { id: 'h2', name: 'Lectura técnica', section: 'morning', duration: 20, order: 1 },
        { id: 'h3', name: 'Ejercicio', section: 'afternoon', duration: 45, order: 0 },
        { id: 'h4', name: 'Movilidad', section: 'evening', duration: 10, order: 0 },
        { id: 'h5', name: 'Planificar día siguiente', section: 'evening', duration: 5, order: 1 }
      ];
      this.set('habits', habits);
    }
    return habits;
  },
  setHabits(h) { this.set('habits', h); },
  getAreas() { return this.get('areas') || []; },
  setAreas(a) { this.set('areas', a); },
  getRoutines() { return this.get('routines') || []; },
  setRoutines(r) { this.set('routines', r); },
  getExploitLog() { return this.get('exploit') || []; },
  addExploit(session) {
    const log = this.getExploitLog();
    log.push(session);
    this.set('exploit', log);
  },
  getCredits() { return this.get('credits') || 0; },
  setCredits(c) { this.set('credits', c); },
  exportAll() {
    return JSON.stringify({ logs: this.getLogs(), config: this.getConfig(), habits: this.getHabits(), areas: this.getAreas(), routines: this.getRoutines(), exploit: this.getExploitLog(), credits: this.getCredits() }, null, 2);
  }
};
'''

# ==================== js/state.js ====================
FILES["js/state.js"] = '''import { Storage } from './storage.js';
export function todayStr() { return new Date().toISOString().split('T')[0]; }
export function calculateBasal(dateStr = null) {
  const date = dateStr || todayStr();
  const logs = Storage.getLogs();
  const log = logs[date];
  if (!log || !log.core) return { score: null, mode: 'unknown' };
  const core = log.core;
  if (core.emotion !== undefined && core.emotion <= 2) return { score: 0, mode: 'red', reason: 'emotional' };
  if (core.sleep !== undefined && core.sleep < 5) return { score: 0, mode: 'red', reason: 'sleep' };
  const socialDays = [];
  for (let i=0; i<3; i++) {
    const d = new Date(); d.setDate(d.getDate()-i);
    socialDays.push(logs[d.toISOString().split('T')[0]]?.core?.social);
  }
  if (socialDays.filter(s => s === false).length >= 3) return { score: 0, mode: 'red', reason: 'social' };
  let score = 0, total = 0;
  const weights = { sleep: 30, emotion: 30, nutrition: 15, movement: 15, social: 10 };
  if (core.sleep !== undefined) { score += Math.min(core.sleep/8,1)*weights.sleep; total += weights.sleep; }
  if (core.emotion !== undefined) { score += (core.emotion/5)*weights.emotion; total += weights.emotion; }
  if (core.nutrition !== undefined) { score += (core.nutrition?1:0)*weights.nutrition; total += weights.nutrition; }
  if (core.movement !== undefined) { score += (core.movement?1:0)*weights.movement; total += weights.movement; }
  if (core.social !== undefined) { score += (core.social?1:0)*weights.social; total += weights.social; }
  if (total === 0) return { score: null, mode: 'unknown' };
  const final = Math.round((score/total)*100);
  if (final >= 70) return { score: final, mode: 'green' };
  if (final >= 40) return { score: final, mode: 'yellow' };
  return { score: final, mode: 'red' };
}
export function updateCreditsOnCheckin(allCoreOk) {
  let credits = Storage.getCredits();
  if (allCoreOk && credits < 3) { credits++; Storage.setCredits(credits); }
  return credits;
}
export function spendCredit() {
  let credits = Storage.getCredits();
  if (credits > 0) { credits--; Storage.setCredits(credits); return true; }
  return false;
}
'''

# ==================== js/ui.js ====================
FILES["js/ui.js"] = '''export function showModal(title, bodyHtml, footerHtml = '') {
  document.getElementById('modal-title').textContent = title;
  document.getElementById('modal-body').innerHTML = bodyHtml;
  document.getElementById('modal-footer').innerHTML = footerHtml;
  document.getElementById('modal-overlay').classList.remove('hidden');
  document.getElementById('modal-close').onclick = closeModal;
  document.getElementById('modal-overlay').onclick = (e) => { if (e.target === e.currentTarget) closeModal(); };
}
export function closeModal() { document.getElementById('modal-overlay').classList.add('hidden'); }
export function showToast(message, duration = 2000) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.remove('hidden');
  setTimeout(() => toast.classList.add('hidden'), duration);
}
export function switchView(view) {
  document.querySelectorAll('.top-nav-btn').forEach(b => b.classList.remove('active'));
  const btn = document.querySelector(`.top-nav-btn[data-view="${view}"]`);
  if (btn) btn.classList.add('active');
}
'''

# ==================== js/app.js ====================
FILES["js/app.js"] = '''import { Storage } from './storage.js';
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
'''

def create_files():
    dirs = ['css', 'js', 'js/components']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    for path, content in FILES.items():
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ {path}")
    print("\n✅ MentalOS generado en la carpeta actual.")

if __name__ == '__main__':
    create_files()