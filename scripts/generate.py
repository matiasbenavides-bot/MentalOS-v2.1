#!/usr/bin/env python3
"""
MentalOS v2.0 - Generador de proyecto completo
Herramienta de hábitos y regulación emocional a largo plazo.
Uso: python generate.py
"""

import os
import json

BASE_DIR = "mentalo"
DIRS = ["css", "js", "js/components", "scripts"]

FILES = {}

# ==================== index.html ====================
FILES["index.html"] = '''<!DOCTYPE html>
<html lang="es" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
  <title>MentalOS v2.0</title>
  <link rel="stylesheet" href="css/style.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body>
  <!-- PIN Overlay -->
  <div id="pin-overlay" class="pin-overlay">
    <div class="pin-container">
      <h2>MentalOS</h2>
      <input type="password" id="pin-input" maxlength="4" placeholder="PIN" autofocus>
      <button id="pin-submit">Entrar</button>
      <p id="pin-error"></p>
    </div>
  </div>

  <!-- App Container -->
  <div id="app" class="app hidden">
    <!-- Top Bar -->
    <header class="topbar">
      <div class="status-indicator" id="status-indicator">
        <div class="status-circle" id="status-circle"></div>
        <div class="status-text">
          <span id="status-score">--</span>
          <small id="status-mode"></small>
        </div>
      </div>
      <div class="credits" id="credits-display">
        <span>Créditos:</span>
        <span id="credits-dots"></span>
      </div>
      <div class="topbar-actions">
        <button id="force-mode-btn" class="icon-btn" title="Forzar modo">🔓</button>
        <button id="config-btn" class="icon-btn" title="Configuración">⚙️</button>
      </div>
    </header>

    <!-- Main Viewport -->
    <main id="viewport" class="viewport"></main>

    <!-- Bottom Navigation -->
    <nav class="bottom-nav">
      <button class="nav-btn active" data-view="home">🏠<span>Home</span></button>
      <button class="nav-btn" data-view="exploitation">⚡<span>Explotación</span></button>
      <button class="nav-btn" data-view="analysis">📊<span>Análisis</span></button>
      <button class="nav-btn" data-view="emergency" id="nav-emergency">🛡️<span>Emergencia</span></button>
    </nav>
  </div>

  <!-- Modals Container -->
  <div id="modal-overlay" class="modal-overlay hidden"></div>
  <div id="modal-content" class="modal-dialog hidden"></div>

  <script type="module" src="js/app.js"></script>
</body>
</html>'''

# ==================== css/style.css ====================
FILES["css/style.css"] = '''/* MentalOS v2.0 - Dark Minimalist with Tiimo-inspired habits */
:root {
  --bg: #0f0f0f;
  --surface: #1a1a1a;
  --surface-hover: #252525;
  --text: #e0e0e0;
  --text-secondary: #a0a0a0;
  --border: #2a2a2a;
  --accent: #5c8aff;
  --green: rgba(76, 175, 80, 0.8);
  --yellow: rgba(255, 193, 7, 0.8);
  --red: rgba(244, 67, 54, 0.8);
  --green-bg: rgba(76, 175, 80, 0.15);
  --yellow-bg: rgba(255, 193, 7, 0.15);
  --red-bg: rgba(244, 67, 54, 0.15);
  --radius: 12px;
}

* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}
.hidden { display: none !important; }

/* PIN */
.pin-overlay {
  position: fixed; inset: 0; background: var(--bg);
  display: flex; align-items: center; justify-content: center; z-index: 1000;
}
.pin-container { text-align: center; }
.pin-container h2 { margin-bottom: 1.5rem; font-size: 2rem; }
#pin-input {
  background: var(--surface); border: 1px solid var(--border); color: var(--text);
  padding: 0.75rem 1rem; border-radius: var(--radius); font-size: 1.5rem;
  text-align: center; width: 140px; letter-spacing: 0.5em;
}
#pin-submit {
  display: block; margin: 1rem auto 0; background: var(--accent); color: white;
  border: none; padding: 0.6rem 2rem; border-radius: var(--radius); cursor: pointer;
}
#pin-error { color: var(--red); margin-top: 0.5rem; font-size: 0.875rem; }

/* App Shell */
.app { display: flex; flex-direction: column; height: 100vh; }

/* Topbar */
.topbar {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.5rem 1rem; background: var(--surface); border-bottom: 1px solid var(--border);
}
.status-indicator { display: flex; align-items: center; gap: 0.5rem; flex: 1; }
.status-circle { width: 28px; height: 28px; border-radius: 50%; background: var(--border); }
.status-circle.green { background: var(--green); }
.status-circle.yellow { background: var(--yellow); }
.status-circle.red { background: var(--red); }
.status-text small { color: var(--text-secondary); font-size: 0.75rem; }
.credits { display: flex; align-items: center; gap: 0.25rem; font-size: 0.875rem; }
.credits-dot { display: inline-block; width: 12px; height: 12px; border-radius: 50%; background: var(--border); }
.credits-dot.filled { background: var(--accent); }
.icon-btn { background: none; border: none; color: var(--text); font-size: 1.25rem; padding: 0.25rem; cursor: pointer; }

/* Viewport */
.viewport { flex: 1; overflow-y: auto; padding: 1rem; }

/* Bottom Nav */
.bottom-nav {
  display: flex; justify-content: space-around;
  background: var(--surface); border-top: 1px solid var(--border); padding: 0.4rem 0;
}
.nav-btn {
  background: none; border: none; color: var(--text-secondary); display: flex;
  flex-direction: column; align-items: center; font-size: 0.7rem; gap: 2px; cursor: pointer;
}
.nav-btn.active { color: var(--accent); }
.nav-btn.atenuado { opacity: 0.4; }

/* Habit Grid */
.habit-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 0.75rem; }
.habit-card {
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 1rem; text-align: center; cursor: pointer; transition: all 0.2s; position: relative;
}
.habit-card:active { transform: scale(0.96); }
.habit-card.completed { border-color: var(--green); background: var(--green-bg); }
.habit-card.failed { border-color: var(--red); background: var(--red-bg); opacity: 0.7; }
.habit-card .habit-icon { font-size: 1.5rem; margin-bottom: 0.25rem; }
.habit-card .habit-name { font-weight: 600; font-size: 0.9rem; }
.habit-card .habit-status { font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.25rem; }
.habit-card .weekly-dots { display: flex; gap: 3px; justify-content: center; margin-top: 0.5rem; }
.weekly-dots span { width: 6px; height: 6px; border-radius: 50%; background: var(--border); }
.weekly-dots span.done { background: var(--green); }
.weekly-dots span.missed { background: var(--red); }
.habit-card.core { border-width: 2px; border-style: dashed; }

/* Sections */
.section-title { margin: 1rem 0 0.5rem; font-size: 1rem; font-weight: 600; color: var(--text-secondary); }

/* Exploitation Areas */
.area-card {
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 1rem; margin-bottom: 0.75rem; display: flex; justify-content: space-between; align-items: center;
}
.area-info h4 { margin-bottom: 0.25rem; }
.area-info p { font-size: 0.8rem; color: var(--text-secondary); }

/* Analysis */
.chart-container { width: 100%; margin: 1rem 0; background: var(--surface); border-radius: var(--radius); padding: 1rem; }
.chart-container canvas { max-height: 250px; }
.summary-text { background: var(--surface); border-radius: var(--radius); padding: 1rem; margin: 1rem 0; font-size: 0.9rem; }

/* Emergency Checklist */
.checklist-item {
  display: flex; align-items: center; gap: 1rem; padding: 0.75rem;
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); margin-bottom: 0.5rem;
}
.checklist-item.completed { background: var(--green-bg); border-color: var(--green); }
.checklist-item input[type="checkbox"] { width: 24px; height: 24px; accent-color: var(--green); }

/* Buttons */
.btn-primary {
  display: inline-block; background: var(--accent); color: white; border: none;
  padding: 0.6rem 1.2rem; border-radius: var(--radius); cursor: pointer; font-weight: 600;
}
.btn-secondary {
  background: transparent; color: var(--text); border: 1px solid var(--border);
  padding: 0.5rem 1rem; border-radius: var(--radius); cursor: pointer;
}
.btn-float {
  position: fixed; bottom: 80px; right: 20px; width: 56px; height: 56px;
  background: var(--accent); color: white; border: none; border-radius: 50%; font-size: 2rem;
  cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.5);
}

/* Modal */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.8); z-index: 500;
  display: flex; align-items: center; justify-content: center;
}
.modal-dialog {
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 1.5rem; width: 90%; max-width: 500px; max-height: 85vh; overflow-y: auto;
}

/* Forms */
input[type="text"], input[type="number"], textarea, select {
  width: 100%; background: var(--bg); border: 1px solid var(--border);
  color: var(--text); padding: 0.6rem; border-radius: 8px; font-family: inherit;
  margin-top: 0.25rem;
}
.form-group { margin-bottom: 1rem; }

/* Responsive */
@media (max-width: 480px) {
  .habit-grid { grid-template-columns: repeat(2, 1fr); }
}
'''

# ==================== js/storage.js ====================
FILES["js/storage.js"] = '''// Storage module for MentalOS v2.0
const PREFIX = 'mentalo_';

export const Storage = {
  get(key) {
    const raw = localStorage.getItem(PREFIX + key);
    return raw ? JSON.parse(raw) : null;
  },
  set(key, value) {
    localStorage.setItem(PREFIX + key, JSON.stringify(value));
  },
  getLogs() { return this.get('logs') || {}; },
  addLog(date, data) {
    const logs = this.getLogs();
    logs[date] = data;
    this.set('logs', logs);
  },
  getConfig() {
    return this.get('config') || {
      pin: '1234',
      emergencyChecklist: [
        'Ducharse o lavarse la cara',
        'Comer algo (lo que sea)',
        'Salir 5 minutos al aire libre',
        'Mensaje a contacto de confianza',
        'Leer 1 página de un libro favorito'
      ],
      supportMessage: 'Recordá que esto es pasajero. Ya saliste de episodios peores.',
      contactName: 'Contacto de confianza',
      thresholds: { sleepCritical: 5, emoCritical: 2, socialDays: 3 }
    };
  },
  setConfig(config) { this.set('config', config); },
  getHabits() { return this.get('habits') || []; },
  setHabits(habits) { this.set('habits', habits); },
  getAreas() { return this.get('areas') || []; },
  setAreas(areas) { this.set('areas', areas); },
  getExploitationLog() { return this.get('exploitation') || []; },
  addExploitationSession(session) {
    const log = this.getExploitationLog();
    log.push(session);
    this.set('exploitation', log);
  },
  exportAll() {
    return JSON.stringify({
      logs: this.getLogs(),
      config: this.getConfig(),
      habits: this.getHabits(),
      areas: this.getAreas(),
      exploitation: this.getExploitationLog(),
      exportDate: new Date().toISOString()
    }, null, 2);
  },
  importAll(data) {
    if (data.logs) this.set('logs', data.logs);
    if (data.config) this.set('config', data.config);
    if (data.habits) this.set('habits', data.habits);
    if (data.areas) this.set('areas', data.areas);
    if (data.exploitation) this.set('exploitation', data.exploitation);
  }
};
'''

# ==================== js/state.js ====================
FILES["js/state.js"] = '''// State calculation: basal status, credits, mode
import { Storage } from './storage.js';

export function getToday() {
  return new Date().toISOString().split('T')[0];
}

export function calculateBasalState(date = null) {
  const targetDate = date || getToday();
  const logs = Storage.getLogs();
  const todayLog = logs[targetDate];
  if (!todayLog || !todayLog.core) return { score: null, mode: 'unknown', isCritical: false };

  const core = todayLog.core;
  const config = Storage.getConfig();

  // Critical checks (override)
  if (core.emotional_baseline !== null && core.emotional_baseline <= config.thresholds.emoCritical) {
    return { score: 0, mode: 'red', isCritical: true, reason: 'emotional_critical' };
  }
  if (core.sleep !== null && core.sleep < config.thresholds.sleepCritical) {
    return { score: 0, mode: 'red', isCritical: true, reason: 'sleep_critical' };
  }
  // Social isolation: check last 3 days
  const socialDays = getLastNDays(3, logs);
  const socialMisses = socialDays.filter(d => d && d.core && d.core.social_microdose === false);
  if (socialMisses.length >= config.thresholds.socialDays) {
    return { score: 0, mode: 'red', isCritical: true, reason: 'social_isolation' };
  }

  // Weighted score
  let score = 0;
  let totalWeight = 0;
  const weights = { sleep: 30, emotional_baseline: 30, nutrition: 15, movement: 15, social_microdose: 10 };

  if (core.sleep !== null) { score += (core.sleep / 8) * weights.sleep; totalWeight += weights.sleep; }
  if (core.emotional_baseline !== null) { score += (core.emotional_baseline / 5) * weights.emotional_baseline; totalWeight += weights.emotional_baseline; }
  if (core.nutrition !== null) { score += (core.nutrition ? 1 : 0) * weights.nutrition; totalWeight += weights.nutrition; }
  if (core.movement !== null) { score += (core.movement ? 1 : 0) * weights.movement; totalWeight += weights.movement; }
  if (core.social_microdose !== null) { score += (core.social_microdose ? 1 : 0) * weights.social_microdose; totalWeight += weights.social_microdose; }

  const finalScore = totalWeight > 0 ? Math.round((score / totalWeight) * 100) : null;
  if (finalScore === null) return { score: null, mode: 'unknown', isCritical: false };

  if (finalScore >= 70) return { score: finalScore, mode: 'green', isCritical: false };
  if (finalScore >= 40) return { score: finalScore, mode: 'yellow', isCritical: false };
  return { score: finalScore, mode: 'red', isCritical: false, reason: 'low_score' };
}

export function getCredits() {
  return Storage.get('credits') || 0;
}

export function updateCreditsOnCheckin(date, allCoreCompleted) {
  let credits = getCredits();
  if (allCoreCompleted && credits < 3) {
    credits++;
    Storage.set('credits', credits);
  }
  return credits;
}

export function spendCredit() {
  let credits = getCredits();
  if (credits > 0) {
    credits--;
    Storage.set('credits', credits);
    return true;
  }
  return false;
}

function getLastNDays(n, logs) {
  const dates = [];
  for (let i = 0; i < n; i++) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    dates.push(d.toISOString().split('T')[0]);
  }
  return dates.map(d => logs[d] || null);
}
'''

# ==================== js/components/habits.js ====================
FILES["js/components/habits.js"] = '''// Home view: habits grid + check-in
import { Storage } from '../storage.js';
import { getToday, calculateBasalState, updateCreditsOnCheckin } from '../state.js';
import { showModal, closeModal } from '../app.js';

let currentHabits = [];

export function renderHome() {
  const viewport = document.getElementById('viewport');
  const today = getToday();
  const logs = Storage.getLogs();
  const todayLog = logs[today] || { core: {}, habits: {} };

  currentHabits = [
    { id: 'sleep', name: 'Sueño', icon: '😴', core: true, value: todayLog.core?.sleep },
    { id: 'nutrition', name: 'Nutrición', icon: '🍽️', core: true, value: todayLog.core?.nutrition },
    { id: 'movement', name: 'Movimiento', icon: '🚶', core: true, value: todayLog.core?.movement },
    { id: 'emotional', name: 'Emocional', icon: '🧠', core: true, value: todayLog.core?.emotional_baseline },
    { id: 'social', name: 'Social', icon: '💬', core: true, value: todayLog.core?.social_microdose },
    ...(Storage.getHabits().map(h => ({
      id: h.id, name: h.name, icon: h.icon || '✅', core: false,
      value: todayLog.habits?.[h.id] || false
    })))
  ];

  const completedCount = currentHabits.filter(h => h.value === true || (h.core && h.value !== null && h.value !== false)).length;
  const totalCore = 5;

  viewport.innerHTML = `
    <div class="habit-grid" id="habit-grid"></div>
    <div style="text-align:center; margin: 1rem 0;">
      <button class="btn-primary" id="end-day-btn">🌙 Cerrar día</button>
    </div>
    <button class="btn-float" id="add-habit-btn">+</button>
  `;

  renderHabitGrid();
  document.getElementById('end-day-btn').addEventListener('click', openEndDayCheckin);
  document.getElementById('add-habit-btn').addEventListener('click', openAddHabitModal);
}

function renderHabitGrid() {
  const grid = document.getElementById('habit-grid');
  grid.innerHTML = currentHabits.map(h => {
    const completed = h.value === true || (h.core && h.value !== null && h.value !== false);
    const classes = ['habit-card'];
    if (h.core) classes.push('core');
    if (completed) classes.push('completed');
    return `
      <div class="${classes.join(' ')}" data-habit="${h.id}" data-core="${h.core}">
        <div class="habit-icon">${h.icon}</div>
        <div class="habit-name">${h.name}</div>
        <div class="habit-status">${h.core ? formatCoreValue(h.id, h.value) : (completed ? '✓' : 'Pendiente')}</div>
        <div class="weekly-dots">${renderWeeklyDots(h.id)}</div>
      </div>
    `;
  }).join('');

  grid.querySelectorAll('.habit-card').forEach(card => {
    card.addEventListener('click', () => toggleHabit(card.dataset.habit, card.dataset.core === 'true'));
  });
}

function formatCoreValue(id, val) {
  if (val === null || val === undefined) return '--';
  if (id === 'sleep') return val + 'h';
  if (id === 'emotional') return val + '/5';
  if (val === true) return '✓';
  if (val === false) return '✗';
  return val;
}

function renderWeeklyDots(habitId) {
  const logs = Storage.getLogs();
  const dots = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date(); d.setDate(d.getDate() - i);
    const ds = d.toISOString().split('T')[0];
    const log = logs[ds];
    let done = false;
    if (log) {
      if (habitId === 'sleep') done = log.core?.sleep >= 6.5;
      else if (habitId === 'emotional') done = log.core?.emotional_baseline >= 3;
      else if (habitId === 'nutrition' || habitId === 'movement' || habitId === 'social') done = log.core?.[habitId] === true;
      else done = log.habits?.[habitId] === true;
    }
    dots.push(`<span class="${done ? 'done' : (log ? 'missed' : '')}"></span>`);
  }
  return dots.join('');
}

function toggleHabit(habitId, isCore) {
  const today = getToday();
  const logs = Storage.getLogs();
  const todayLog = logs[today] || { core: {}, habits: {} };
  if (isCore) {
    // Core habits need special input
    if (habitId === 'sleep') {
      const val = prompt('Horas de sueño:', todayLog.core?.sleep || '');
      if (val !== null) todayLog.core.sleep = parseFloat(val);
    } else if (habitId === 'emotional') {
      const val = prompt('Estado emocional (1-5):', todayLog.core?.emotional_baseline || '');
      if (val !== null) todayLog.core.emotional_baseline = parseInt(val);
    } else if (habitId === 'social') {
      todayLog.core.social_microdose = !todayLog.core.social_microdose;
    } else {
      todayLog.core[habitId] = !todayLog.core[habitId];
    }
  } else {
    todayLog.habits[habitId] = !todayLog.habits[habitId];
  }
  Storage.addLog(today, todayLog);
  renderHome();
}

function openEndDayCheckin() {
  const today = getToday();
  const logs = Storage.getLogs();
  const todayLog = logs[today] || { core: {}, habits: {} };
  // Check if emotional score is set; if not, prompt
  if (todayLog.core.emotional_baseline === undefined || todayLog.core.emotional_baseline === null) {
    const val = prompt('Estado emocional del día (1-5):', '');
    if (val) todayLog.core.emotional_baseline = parseInt(val);
  }
  const notes = prompt('Notas del día (opcional):', todayLog.notes || '');
  if (notes !== null) todayLog.notes = notes;
  Storage.addLog(today, todayLog);

  // Check if all core habits completed to grant credit
  const allCore = todayLog.core.sleep > 0 && todayLog.core.nutrition === true &&
                  todayLog.core.movement === true && todayLog.core.emotional_baseline >= 1 &&
                  todayLog.core.social_microdose === true;
  const credits = updateCreditsOnCheckin(today, allCore);
  alert(`Día cerrado. Créditos: ${'●'.repeat(credits)}${'○'.repeat(3-credits)}`);
  renderHome();
  updateTopBar();
}

function openAddHabitModal() {
  const modal = document.getElementById('modal-content');
  const overlay = document.getElementById('modal-overlay');
  modal.innerHTML = `
    <h3>Nuevo hábito</h3>
    <div class="form-group"><input type="text" id="new-habit-name" placeholder="Nombre"></div>
    <div class="form-group"><input type="text" id="new-habit-icon" placeholder="Icono (emoji)"></div>
    <button class="btn-primary" id="save-habit">Guardar</button>
    <button class="btn-secondary" id="cancel-habit">Cancelar</button>
  `;
  overlay.classList.remove('hidden');
  modal.classList.remove('hidden');
  document.getElementById('save-habit').onclick = () => {
    const name = document.getElementById('new-habit-name').value.trim();
    const icon = document.getElementById('new-habit-icon').value || '✅';
    if (name) {
      const habits = Storage.getHabits();
      habits.push({ id: Date.now().toString(), name, icon });
      Storage.setHabits(habits);
      closeModal();
      renderHome();
    }
  };
  document.getElementById('cancel-habit').onclick = closeModal;
}
'''

# ==================== js/components/exploitation.js ====================
FILES["js/components/exploitation.js"] = '''// Exploitation view: areas & sessions
import { Storage } from '../storage.js';
import { getToday, calculateBasalState, getCredits, spendCredit } from '../state.js';
import { showModal, closeModal } from '../app.js';

export function renderExploitation() {
  const viewport = document.getElementById('viewport');
  const basal = calculateBasalState();
  const credits = getCredits();
  const areas = Storage.getAreas();

  viewport.innerHTML = `
    <h3>⚡ Explotación</h3>
    <p style="color: var(--text-secondary); margin-bottom: 1rem;">Estado: ${basal.mode.toUpperCase()} | Créditos: ${'●'.repeat(credits)}${'○'.repeat(3-credits)}</p>
    ${basal.mode === 'red' ? '<div class="summary-text">Modo Protección activo. La explotación no está disponible. Tus créditos están seguros.</div>' : ''}
    <div id="areas-list"></div>
    <button class="btn-primary" id="new-area-btn" ${basal.mode === 'red' ? 'disabled' : ''}>+ Nueva Área</button>
  `;

  renderAreasList();
  document.getElementById('new-area-btn').addEventListener('click', openNewAreaModal);
}

function renderAreasList() {
  const container = document.getElementById('areas-list');
  const areas = Storage.getAreas();
  const log = Storage.getExploitationLog();
  container.innerHTML = areas.map(a => {
    const sessions = log.filter(l => l.areaId === a.id);
    const lastSession = sessions[sessions.length - 1];
    return `
      <div class="area-card">
        <div class="area-info">
          <h4 style="color: ${a.color || 'var(--accent)'}">${a.name} <small>(${a.type})</small></h4>
          <p>Última sesión: ${lastSession ? lastSession.date + ' - ' + lastSession.duration + 'min' : 'Nunca'}</p>
        </div>
        <button class="btn-secondary start-session" data-area-id="${a.id}">▶</button>
      </div>
    `;
  }).join('');

  container.querySelectorAll('.start-session').forEach(btn => {
    btn.addEventListener('click', () => startSession(btn.dataset.areaId));
  });
}

function startSession(areaId) {
  const basal = calculateBasalState();
  const credits = getCredits();
  if (basal.mode === 'red') {
    alert('No se puede iniciar sesión en Modo Protección.');
    return;
  }
  if (credits === 0) {
    alert('Necesitás al menos 1 crédito. Completá los hábitos del Core hoy para ganar uno mañana.');
    return;
  }
  if (!confirm(`¿Gastar 1 crédito para esta sesión? (${basal.mode === 'yellow' ? 'Limitado al 50%' : 'Modo completo'})`)) return;

  spendCredit();
  const startTime = Date.now();
  // Simple session: record manually after ending
  const endPrompt = () => {
    const elapsed = Math.round((Date.now() - startTime) / 60000);
    const intensity = prompt('Intensidad (1-10):', '7');
    const notes = prompt('Notas:', '');
    Storage.addExploitationSession({
      areaId,
      date: getToday(),
      duration: elapsed,
      intensity: parseInt(intensity) || 7,
      notes: notes || ''
    });
    alert('Sesión guardada. ¡Buen trabajo!');
    renderExploitation();
    updateTopBar();
  };
  // We'll just use a simple confirm to end
  if (confirm('Sesión iniciada. Presioná OK cuando termines.')) {
    endPrompt();
  }
}

function openNewAreaModal() {
  const modal = document.getElementById('modal-content');
  const overlay = document.getElementById('modal-overlay');
  modal.innerHTML = `
    <h3>Nueva Área</h3>
    <div class="form-group"><input type="text" id="area-name" placeholder="Nombre (ej: Fisiología)"></div>
    <div class="form-group">
      <select id="area-type"><option value="cognition">Estudio (Cognition)</option><option value="physique">Entrenamiento (Physique)</option></select>
    </div>
    <button class="btn-primary" id="save-area">Guardar</button>
    <button class="btn-secondary" id="cancel-area">Cancelar</button>
  `;
  overlay.classList.remove('hidden');
  modal.classList.remove('hidden');
  document.getElementById('save-area').onclick = () => {
    const name = document.getElementById('area-name').value.trim();
    const type = document.getElementById('area-type').value;
    if (name) {
      const areas = Storage.getAreas();
      areas.push({ id: Date.now().toString(), name, type, color: type === 'cognition' ? '#5c8aff' : '#ff9800' });
      Storage.setAreas(areas);
      closeModal();
      renderExploitation();
    }
  };
  document.getElementById('cancel-area').onclick = closeModal;
}
'''

# ==================== js/components/analysis.js ====================
FILES["js/components/analysis.js"] = '''// Analysis view: long-term progress charts
import { Storage } from '../storage.js';
import { calculateBasalState } from '../state.js';

let chartInstance = null;

export function renderAnalysis() {
  const viewport = document.getElementById('viewport');
  viewport.innerHTML = `
    <h3>📊 Análisis</h3>
    <div style="display:flex; gap:0.5rem; margin:0.5rem 0;">
      <button class="btn-secondary period-btn" data-months="3">3M</button>
      <button class="btn-secondary period-btn active" data-months="6">6M</button>
      <button class="btn-secondary period-btn" data-months="12">12M</button>
    </div>
    <div class="chart-container"><canvas id="basal-chart"></canvas></div>
    <div class="summary-text" id="stats-summary"></div>
    <div class="summary-text" id="auto-summary"></div>
    <button class="btn-secondary" id="export-btn">Exportar datos</button>
  `;

  document.querySelectorAll('.period-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderChart(parseInt(btn.dataset.months));
    });
  });
  renderChart(6); // default 6 months
  document.getElementById('export-btn').addEventListener('click', () => {
    const blob = new Blob([Storage.exportAll()], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'mentalo-backup.json';
    a.click();
  });
}

function renderChart(months) {
  const logs = Storage.getLogs();
  const dates = [];
  const endDate = new Date();
  const startDate = new Date();
  startDate.setMonth(startDate.getMonth() - months);
  for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
    dates.push(new Date(d).toISOString().split('T')[0]);
  }

  const scores = dates.map(d => {
    const state = calculateBasalState(d);
    return state.score;
  });

  const ctx = document.getElementById('basal-chart').getContext('2d');
  if (chartInstance) chartInstance.destroy();
  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dates.map(d => d.slice(5)),
      datasets: [{
        label: 'Estado Basal',
        data: scores,
        borderColor: '#5c8aff',
        backgroundColor: 'rgba(92,138,255,0.1)',
        fill: true,
        tension: 0.3,
        pointRadius: 0
      }]
    },
    options: {
      scales: {
        y: { min: 0, max: 100,
          ticks: { stepSize: 20 }
        }
      },
      plugins: {
        annotation: {
          annotations: {
            line70: { type: 'line', yMin: 70, yMax: 70, borderColor: 'rgba(76,175,80,0.5)', borderWidth: 1, borderDash: [5,5] },
            line40: { type: 'line', yMin: 40, yMax: 40, borderColor: 'rgba(255,193,7,0.5)', borderWidth: 1, borderDash: [5,5] }
          }
        }
      }
    }
  });

  // Summary stats
  const validScores = scores.filter(s => s !== null);
  const avg = validScores.length ? Math.round(validScores.reduce((a,b)=>a+b,0) / validScores.length) : '--';
  const redDays = validScores.filter(s => s < 40).length;
  const greenDays = validScores.filter(s => s >= 70).length;

  document.getElementById('stats-summary').innerHTML = `
    <strong>Resumen (${months} meses):</strong> Promedio: ${avg}/100 | Días en Verde: ${greenDays} | Días en Rojo: ${redDays}
  `;

  // Auto-generated text
  let comment = '';
  if (avg >= 70) comment = 'Tu estado basal promedio es alto. Mantené los hábitos.';
  else if (avg >= 40) comment = 'Estás en rango medio. Identificá qué días caen en rojo para prevenirlos.';
  else comment = 'Tu promedio es bajo. Priorizá el Core y usá el checklist de emergencia.';
  if (redDays > 5) comment += ' Tuviste varios días en rojo; considerá ajustar la carga.';
  document.getElementById('auto-summary').innerHTML = `<strong>Análisis automático:</strong> ${comment}`;
}
'''

# ==================== js/components/emergency.js ====================
FILES["js/components/emergency.js"] = '''// Emergency view: survival checklist
import { Storage } from '../storage.js';

export function renderEmergency() {
  const viewport = document.getElementById('viewport');
  const config = Storage.getConfig();
  const checklist = config.emergencyChecklist || [];

  viewport.innerHTML = `
    <h3>🛡️ Modo Protección</h3>
    <p style="color: var(--text-secondary); margin-bottom: 1rem;">Completá lo que puedas. No hay castigo.</p>
    <div id="checklist-container">
      ${checklist.map((item, idx) => `
        <div class="checklist-item" data-index="${idx}">
          <input type="checkbox" id="check-${idx}">
          <label for="check-${idx}">${item}</label>
        </div>
      `).join('')}
    </div>
    <div id="emergency-notes" style="margin: 1rem 0;">
      <p><em>${config.supportMessage || 'Esto es pasajero. Confiá en el proceso.'}</em></p>
    </div>
    <p id="progress-text" style="text-align:center; font-weight:bold;"></p>
  `;

  // Load today's checklist status
  const today = new Date().toISOString().split('T')[0];
  const logs = Storage.getLogs();
  const todayLog = logs[today] || {};
  const completed = todayLog.checklist || [];
  completed.forEach(idx => {
    const cb = document.getElementById('check-' + idx);
    if (cb) { cb.checked = true; cb.parentElement.classList.add('completed'); }
  });

  document.querySelectorAll('.checklist-item input').forEach(cb => {
    cb.addEventListener('change', (e) => {
      const idx = parseInt(e.target.parentElement.dataset.index);
      const checked = e.target.checked;
      if (checked) {
        e.target.parentElement.classList.add('completed');
      } else {
        e.target.parentElement.classList.remove('completed');
      }
      // Save state
      const logs = Storage.getLogs();
      const todayLog = logs[today] || {};
      const completedList = todayLog.checklist || [];
      if (checked && !completedList.includes(idx)) completedList.push(idx);
      else if (!checked) {
        const pos = completedList.indexOf(idx);
        if (pos > -1) completedList.splice(pos, 1);
      }
      todayLog.checklist = completedList;
      Storage.addLog(today, todayLog);
      updateProgress();
    });
  });

  updateProgress();
}

function updateProgress() {
  const total = document.querySelectorAll('.checklist-item').length;
  const checked = document.querySelectorAll('.checklist-item input:checked').length;
  document.getElementById('progress-text').textContent = `${checked} de ${total} completado`;
}
'''

# ==================== js/components/config.js ====================
FILES["js/components/config.js"] = '''// Configuration panel
import { Storage } from '../storage.js';
import { closeModal } from '../app.js';

export function openConfig() {
  const config = Storage.getConfig();
  const modal = document.getElementById('modal-content');
  const overlay = document.getElementById('modal-overlay');
  modal.innerHTML = `
    <h3>⚙️ Configuración</h3>
    <div class="form-group"><label>PIN</label><input type="password" id="cfg-pin" value="${config.pin}"></div>
    <h4>Checklist de Emergencia (5 items, uno por línea)</h4>
    <textarea id="cfg-checklist" rows="5">${config.emergencyChecklist.join('\\n')}</textarea>
    <div class="form-group"><label>Mensaje de apoyo</label><textarea id="cfg-support">${config.supportMessage}</textarea></div>
    <div class="form-group"><label>Nombre de contacto</label><input type="text" id="cfg-contact" value="${config.contactName}"></div>
    <button class="btn-primary" id="save-config">Guardar</button>
    <button class="btn-secondary" id="cancel-config">Cancelar</button>
  `;
  overlay.classList.remove('hidden');
  modal.classList.remove('hidden');

  document.getElementById('save-config').onclick = () => {
    config.pin = document.getElementById('cfg-pin').value || '1234';
    config.emergencyChecklist = document.getElementById('cfg-checklist').value.split('\\n').filter(l => l.trim());
    config.supportMessage = document.getElementById('cfg-support').value;
    config.contactName = document.getElementById('cfg-contact').value;
    Storage.setConfig(config);
    closeModal();
    alert('Configuración guardada');
  };
  document.getElementById('cancel-config').onclick = closeModal;
}
'''

# ==================== js/app.js ====================
FILES["js/app.js"] = '''// MentalOS v2.0 App Orchestrator
import { Storage } from './storage.js';
import { getToday, calculateBasalState, getCredits } from './state.js';
import { renderHome } from './components/habits.js';
import { renderExploitation } from './components/exploitation.js';
import { renderAnalysis } from './components/analysis.js';
import { renderEmergency } from './components/emergency.js';
import { openConfig } from './components/config.js';

let currentView = 'home';

document.addEventListener('DOMContentLoaded', () => {
  // PIN
  const config = Storage.getConfig();
  document.getElementById('pin-submit').addEventListener('click', () => {
    if (document.getElementById('pin-input').value === config.pin) {
      document.getElementById('pin-overlay').classList.add('hidden');
      document.getElementById('app').classList.remove('hidden');
      initApp();
    } else {
      document.getElementById('pin-error').textContent = 'PIN incorrecto';
    }
  });

  // Bottom nav
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentView = btn.dataset.view;
      navigateTo(currentView);
    });
  });

  // Force mode
  document.getElementById('force-mode-btn').addEventListener('click', forceMode);
  document.getElementById('config-btn').addEventListener('click', openConfig);
});

function initApp() {
  navigateTo('home');
  updateTopBar();
}

export function navigateTo(view) {
  switch(view) {
    case 'home': renderHome(); break;
    case 'exploitation': renderExploitation(); break;
    case 'analysis': renderAnalysis(); break;
    case 'emergency': renderEmergency(); break;
  }
  updateTopBar();
}

export function updateTopBar() {
  const basal = calculateBasalState();
  const credits = getCredits();
  const circle = document.getElementById('status-circle');
  circle.className = 'status-circle ' + basal.mode;
  document.getElementById('status-score').textContent = basal.score !== null ? basal.score : '--';
  document.getElementById('status-mode').textContent = basal.mode === 'green' ? 'Explotación disponible' :
    (basal.mode === 'yellow' ? 'Limitado' : 'Protección');
  document.getElementById('credits-dots').innerHTML = Array.from({length: 3}, (_,i) =>
    `<span class="credits-dot ${i < credits ? 'filled' : ''}"></span>`
  ).join('');
  // Emergency nav visibility
  const navEm = document.getElementById('nav-emergency');
  if (basal.mode === 'red') {
    navEm.classList.remove('atenuado');
  } else {
    navEm.classList.add('atenuado');
  }
}

function forceMode() {
  const basal = calculateBasalState();
  const options = { green: 'Explotación completo', yellow: 'Limitado', red: 'Protección' };
  const choices = Object.keys(options).filter(k => !(basal.mode === 'red' && k === 'red'));
  const choice = prompt(`Modo actual: ${basal.mode.toUpperCase()}. Forzar a (green/yellow/red):`, basal.mode);
  if (choice && options[choice]) {
    if (choice === 'red' && basal.mode !== 'red') {
      if (!confirm('¿Activar Modo Protección manualmente? Se registrará la razón.')) return;
    }
    if (choice !== basal.mode) {
      const reason = prompt('Justificación breve:');
      const logs = Storage.getLogs();
      const today = getToday();
      const log = logs[today] || {};
      log.forcedMode = { original: basal.mode, forced: choice, reason };
      Storage.addLog(today, log);
    }
    // For now, we don't physically change the mode; the user just acknowledges.
    alert('Preferencia registrada. La recomendación sigue siendo: ' + basal.mode);
    updateTopBar();
  }
}

export function showModal() {} // placeholder
export function closeModal() {
  document.getElementById('modal-overlay').classList.add('hidden');
  document.getElementById('modal-content').classList.add('hidden');
}
'''

# ==================== scripts/generate.py (self copy) ====================
# Will be copied later

def create_project():
    for d in DIRS:
        os.makedirs(os.path.join(BASE_DIR, d), exist_ok=True)
    for path, content in FILES.items():
        full = os.path.join(BASE_DIR, path)
        with open(full, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ {path}")
    # Copy self
    import shutil
    shutil.copy2(__file__, os.path.join(BASE_DIR, 'scripts', 'generate.py'))
    print("  ✓ scripts/generate.py (copied)")
    print(f"\n✅ MentalOS v2.0 generado en '{BASE_DIR}/'")
    print("Abrí index.html en tu navegador o desplegalo en Vercel.")

if __name__ == '__main__':
    create_project()