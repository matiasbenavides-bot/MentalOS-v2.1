#!/usr/bin/env python3
"""
MentalOS v2.2 - Interfaz sólida, clara y responsive.
Sin prompts ni alerts nativos. Todo con modales propios.
"""

import os
import json

BASE_DIR = "mentalo"
DIRS = ["css", "js", "js/components"]

FILES = {}

# ==================== index.html ====================
FILES["index.html"] = '''<!DOCTYPE html>
<html lang="es" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>MentalOS v2.2</title>
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="css/style.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body>
  <!-- PIN Lock Screen -->
  <div id="pin-screen" class="fullscreen-center">
    <div class="card pin-card">
      <h1>MentalOS</h1>
      <input type="password" id="pin-input" maxlength="4" placeholder="••••" inputmode="numeric" pattern="[0-9]*">
      <button id="pin-btn" class="btn-primary full-width">Entrar</button>
      <p id="pin-error" class="text-error hidden"></p>
    </div>
  </div>

  <!-- Main App -->
  <div id="app" class="app-container hidden">
    <!-- Top Bar -->
    <header class="topbar">
      <div class="status-badge" id="status-badge">
        <div class="status-dot" id="status-dot"></div>
        <div class="status-info">
          <span id="status-score" class="status-score">--</span>
          <small id="status-label">Cargando...</small>
        </div>
      </div>
      <div class="credits-badge" id="credits-badge">
        <span>⚡</span><span id="credits-count">0</span>
      </div>
      <button class="icon-btn" id="config-btn" title="Configuración">⚙️</button>
    </header>

    <!-- Viewport -->
    <main id="viewport" class="viewport"></main>

    <!-- Bottom Navigation -->
    <nav class="bottom-nav">
      <button class="nav-btn active" data-view="home">
        <span class="nav-icon">🏠</span><span class="nav-label">Hoy</span>
      </button>
      <button class="nav-btn" data-view="exploit">
        <span class="nav-icon">⚡</span><span class="nav-label">Explotar</span>
      </button>
      <button class="nav-btn" data-view="analysis">
        <span class="nav-icon">📊</span><span class="nav-label">Análisis</span>
      </button>
      <button class="nav-btn" data-view="emergency" id="nav-emergency">
        <span class="nav-icon">🛡️</span><span class="nav-label">Emergencia</span>
      </button>
    </nav>
  </div>

  <!-- Generic Modal -->
  <div id="modal-overlay" class="modal-overlay hidden">
    <div class="modal-container" id="modal-container">
      <div class="modal-header">
        <h2 id="modal-title"></h2>
        <button class="modal-close" id="modal-close">✕</button>
      </div>
      <div class="modal-body" id="modal-body"></div>
      <div class="modal-footer" id="modal-footer"></div>
    </div>
  </div>

  <!-- Toast notifications -->
  <div id="toast" class="toast hidden"></div>

  <script type="module" src="js/app.js"></script>
</body>
</html>'''

# ==================== css/style.css ====================
FILES["css/style.css"] = '''/* MentalOS v2.2 - Clean, responsive, mobile-first */
:root {
  --bg: #0f0f0f;
  --surface: #1c1c1c;
  --surface-hover: #2a2a2a;
  --text: #eee;
  --text-secondary: #aaa;
  --border: #333;
  --accent: #5c8aff;
  --green: #4caf50;
  --yellow: #ffc107;
  --red: #f44336;
  --green-bg: rgba(76,175,80,0.15);
  --yellow-bg: rgba(255,193,7,0.15);
  --red-bg: rgba(244,67,54,0.15);
  --radius: 12px;
  --transition: 0.2s ease;
}

* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  height: 100vh;
  overflow: hidden;
  -webkit-tap-highlight-color: transparent;
}

.fullscreen-center {
  display: flex; align-items: center; justify-content: center;
  height: 100vh; background: var(--bg);
}
.hidden { display: none !important; }

/* PIN */
.pin-card {
  text-align: center; padding: 2rem; width: 280px;
}
.pin-card h1 { margin-bottom: 1.5rem; font-size: 2.5rem; }
#pin-input {
  width: 100%; padding: 0.8rem; font-size: 1.5rem; text-align: center;
  background: var(--surface); border: 1px solid var(--border); color: var(--text);
  border-radius: var(--radius); letter-spacing: 0.5em;
}
.text-error { color: var(--red); margin-top: 0.5rem; font-size: 0.85rem; }

/* App Shell */
.app-container {
  display: flex; flex-direction: column; height: 100vh; overflow: hidden;
}

/* Topbar */
.topbar {
  display: flex; align-items: center; padding: 0.8rem 1.2rem;
  background: var(--surface); border-bottom: 1px solid var(--border);
  gap: 1rem; flex-shrink: 0;
}
.status-badge {
  display: flex; align-items: center; gap: 0.6rem; flex: 1;
}
.status-dot {
  width: 18px; height: 18px; border-radius: 50%; background: var(--border);
}
.status-dot.green { background: var(--green); }
.status-dot.yellow { background: var(--yellow); }
.status-dot.red { background: var(--red); }
.status-score { font-weight: 700; font-size: 1.2rem; }
.status-info small { color: var(--text-secondary); font-size: 0.7rem; display: block; }
.credits-badge {
  display: flex; align-items: center; gap: 0.3rem; font-weight: 600; font-size: 1rem;
  background: var(--bg); padding: 0.3rem 0.6rem; border-radius: 20px;
}
.icon-btn {
  background: none; border: none; color: var(--text); font-size: 1.4rem;
  padding: 0.3rem; cursor: pointer; border-radius: 8px;
}
.icon-btn:active { background: var(--surface-hover); }

/* Viewport */
.viewport {
  flex: 1; overflow-y: auto; padding: 1rem;
  -webkit-overflow-scrolling: touch;
}

/* Bottom Nav */
.bottom-nav {
  display: flex; justify-content: space-around; background: var(--surface);
  border-top: 1px solid var(--border); padding: 0.5rem 0 0.6rem;
  flex-shrink: 0;
}
.nav-btn {
  display: flex; flex-direction: column; align-items: center; background: none;
  border: none; color: var(--text-secondary); font-size: 0.65rem; cursor: pointer;
  padding: 0.3rem 0.5rem; gap: 2px; transition: var(--transition);
}
.nav-btn.active { color: var(--accent); }
.nav-btn .nav-icon { font-size: 1.4rem; }
.nav-btn.atenuado { opacity: 0.3; pointer-events: none; }

/* Cards & grid */
.card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 1rem;
}
.habit-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 0.8rem;
  margin-bottom: 1.2rem;
}
.habit-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 1rem 0.6rem; text-align: center;
  cursor: pointer; transition: all 0.15s; position: relative;
}
.habit-card:active { transform: scale(0.96); }
.habit-card.completed { border-color: var(--green); background: var(--green-bg); }
.habit-card.failed { border-color: var(--red); background: var(--red-bg); opacity: 0.6; }
.habit-card.core { border-style: dashed; border-width: 2px; }
.habit-icon { font-size: 1.8rem; margin-bottom: 0.4rem; }
.habit-name { font-weight: 600; font-size: 0.9rem; margin-bottom: 0.2rem; }
.habit-value { font-size: 0.75rem; color: var(--text-secondary); }
.weekly-dots { display: flex; gap: 3px; justify-content: center; margin-top: 0.5rem; }
.dot { width: 6px; height: 6px; border-radius: 50%; background: var(--border); }
.dot.done { background: var(--green); }
.dot.missed { background: var(--red); }

/* Buttons */
.btn-primary {
  display: inline-block; background: var(--accent); color: white; border: none;
  padding: 0.7rem 1.2rem; border-radius: var(--radius); font-weight: 600;
  cursor: pointer; text-align: center; transition: opacity 0.2s; font-size: 0.9rem;
}
.btn-primary:active { opacity: 0.8; }
.btn-secondary {
  background: transparent; border: 1px solid var(--border); color: var(--text);
  padding: 0.6rem 1rem; border-radius: var(--radius); cursor: pointer; font-size: 0.9rem;
}
.btn-secondary:active { background: var(--surface-hover); }
.full-width { width: 100%; display: block; }

/* Modal */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 500;
  display: flex; align-items: flex-end; justify-content: center;
}
.modal-container {
  background: var(--surface); border-radius: 16px 16px 0 0; width: 100%;
  max-width: 500px; max-height: 85vh; overflow-y: auto; padding: 1.5rem 1.2rem 2rem;
  animation: slideUp 0.25s ease;
}
@keyframes slideUp { from { transform: translateY(15%); opacity: 0.5; } to { transform: translateY(0); opacity: 1; } }
.modal-header {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;
}
.modal-header h2 { font-size: 1.3rem; }
.modal-close {
  background: none; border: none; color: var(--text); font-size: 1.5rem;
  cursor: pointer; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center;
}
.modal-body { margin-bottom: 1rem; }
.modal-footer { display: flex; gap: 0.5rem; justify-content: flex-end; }

/* Forms */
.form-group { margin-bottom: 1.2rem; }
.form-group label { display: block; margin-bottom: 0.3rem; font-weight: 500; font-size: 0.9rem; }
input, select, textarea {
  width: 100%; padding: 0.7rem; background: var(--bg); border: 1px solid var(--border);
  color: var(--text); border-radius: 8px; font-size: 0.95rem; font-family: inherit;
}
textarea { resize: vertical; min-height: 80px; }
input[type="number"] { -moz-appearance: textfield; }
input[type="number"]::-webkit-inner-spin-button { -webkit-appearance: none; }

/* Charts */
.chart-container {
  background: var(--surface); border-radius: var(--radius); padding: 1rem; margin-bottom: 1rem;
}

/* Emergency checklist */
.checklist-item {
  display: flex; align-items: center; gap: 0.8rem; padding: 0.8rem;
  background: var(--surface); border-radius: var(--radius); margin-bottom: 0.5rem;
  border: 1px solid var(--border);
}
.checklist-item.completed { background: var(--green-bg); border-color: var(--green); }
.checklist-item input[type="checkbox"] {
  width: 22px; height: 22px; accent-color: var(--green);
}

/* Toast */
.toast {
  position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%);
  background: var(--surface); border: 1px solid var(--border); color: var(--text);
  padding: 0.8rem 1.5rem; border-radius: 30px; z-index: 600; font-size: 0.9rem;
  animation: fadeInOut 2s ease forwards; white-space: nowrap;
}
@keyframes fadeInOut {
  0% { opacity: 0; bottom: 60px; } 20% { opacity: 1; bottom: 80px; }
  80% { opacity: 1; bottom: 80px; } 100% { opacity: 0; bottom: 60px; }
}

/* ============ RESPONSIVE TWEAKS ============ */
/* Mobile first, so these are for larger screens */
@media (min-width: 600px) {
  .habit-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
  }
  .viewport {
    max-width: 650px;
    margin: 0 auto;
    padding: 1.5rem 1rem;
  }
  .topbar {
    justify-content: center;
  }
  .topbar .status-badge {
    max-width: 400px;
  }
  .modal-container {
    border-radius: 16px;
    margin: auto;
    max-width: 480px;
  }
}

@media (min-width: 900px) {
  .viewport {
    max-width: 750px;
  }
  .habit-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
'''

# ==================== js/storage.js ====================
FILES["js/storage.js"] = '''const PREFIX = 'mentalo_';
export const Storage = {
  get(key) {
    try { const raw = localStorage.getItem(PREFIX + key); return raw ? JSON.parse(raw) : null; }
    catch { return null; }
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
      emergencyChecklist: ['Ducharse o lavarse la cara','Comer algo','Salir 5 minutos al aire libre','Mensaje a contacto de confianza','Leer 1 página de un libro favorito'],
      supportMessage: 'Esto es pasajero. Ya saliste de episodios peores.',
      contactName: 'Contacto de confianza'
    };
  },
  setConfig(c) { this.set('config', c); },
  getHabits() { return this.get('habits') || []; },
  setHabits(h) { this.set('habits', h); },
  getAreas() { return this.get('areas') || []; },
  setAreas(a) { this.set('areas', a); },
  getExploitationLog() { return this.get('exploit') || []; },
  addExploit(session) {
    const log = this.getExploitationLog();
    log.push(session);
    this.set('exploit', log);
  },
  getCredits() { return this.get('credits') || 0; },
  setCredits(c) { this.set('credits', c); },
  exportAll() {
    return JSON.stringify({ logs: this.getLogs(), config: this.getConfig(), habits: this.getHabits(), areas: this.getAreas(), exploit: this.getExploitationLog(), credits: this.getCredits() }, null, 2);
  },
  importAll(data) {
    if (data.logs) this.set('logs', data.logs);
    if (data.config) this.set('config', data.config);
    if (data.habits) this.set('habits', data.habits);
    if (data.areas) this.set('areas', data.areas);
    if (data.exploit) this.set('exploit', data.exploit);
    if (data.credits !== undefined) this.set('credits', data.credits);
  }
};
'''

# ==================== js/state.js ====================
FILES["js/state.js"] = '''import { Storage } from './storage.js';

export function todayStr() {
  return new Date().toISOString().split('T')[0];
}

export function getCredits() {
  return Storage.getCredits();
}

export function calculateBasal(dateStr = null) {
  const date = dateStr || todayStr();
  const logs = Storage.getLogs();
  const log = logs[date];
  if (!log || !log.core) return { score: null, mode: 'unknown' };

  const core = log.core;
  // Critical overrides
  if (core.emotional !== undefined && core.emotional <= 2) return { score: 0, mode: 'red', reason: 'emotional' };
  if (core.sleep !== undefined && core.sleep < 5) return { score: 0, mode: 'red', reason: 'sleep' };
  // Social isolation check (last 3 days)
  const socialDays = [];
  for (let i=0; i<3; i++) {
    const d = new Date(); d.setDate(d.getDate()-i);
    const ds = d.toISOString().split('T')[0];
    socialDays.push(logs[ds]?.core?.social);
  }
  if (socialDays.filter(s => s === false).length >= 3) return { score: 0, mode: 'red', reason: 'social' };

  // Weighted score
  let score = 0, total = 0;
  const weights = { sleep: 30, emotional: 30, nutrition: 15, movement: 15, social: 10 };
  if (core.sleep !== undefined) { score += Math.min(core.sleep/8, 1) * weights.sleep; total += weights.sleep; }
  if (core.emotional !== undefined) { score += (core.emotional/5) * weights.emotional; total += weights.emotional; }
  if (core.nutrition !== undefined) { score += (core.nutrition ? 1 : 0) * weights.nutrition; total += weights.nutrition; }
  if (core.movement !== undefined) { score += (core.movement ? 1 : 0) * weights.movement; total += weights.movement; }
  if (core.social !== undefined) { score += (core.social ? 1 : 0) * weights.social; total += weights.social; }
  if (total === 0) return { score: null, mode: 'unknown' };
  const final = Math.round((score/total)*100);
  if (final >= 70) return { score: final, mode: 'green' };
  if (final >= 40) return { score: final, mode: 'yellow' };
  return { score: final, mode: 'red' };
}

export function updateCreditsOnCheckin(date, allCoreOk) {
  let credits = Storage.getCredits();
  if (allCoreOk && credits < 3) {
    credits++;
    Storage.setCredits(credits);
  }
  return credits;
}

export function spendCredit() {
  let credits = Storage.getCredits();
  if (credits > 0) {
    credits--;
    Storage.setCredits(credits);
    return true;
  }
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

export function closeModal() {
  document.getElementById('modal-overlay').classList.add('hidden');
}

export function showToast(message, duration = 2000) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.remove('hidden');
  setTimeout(() => toast.classList.add('hidden'), duration);
}

export function switchView(view) {
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  const btn = document.querySelector(`[data-view="${view}"]`);
  if (btn) btn.classList.add('active');
}
'''

# ==================== js/components/home.js ====================
FILES["js/components/home.js"] = '''import { Storage } from '../storage.js';
import { todayStr, calculateBasal, updateCreditsOnCheckin } from '../state.js';
import { showModal, closeModal, showToast } from '../ui.js';
import { updateTopBar } from '../app.js';

export function renderHome() {
  const vp = document.getElementById('viewport');
  const today = todayStr();
  const logs = Storage.getLogs();
  const todayLog = logs[today] || { core: {}, habits: {} };
  const customHabits = Storage.getHabits();
  const allHabits = [
    { id: 'sleep', name: 'Sueño', icon: '😴', core: true, val: todayLog.core.sleep },
    { id: 'nutrition', name: 'Nutrición', icon: '🍽️', core: true, val: todayLog.core.nutrition },
    { id: 'movement', name: 'Movimiento', icon: '🚶', core: true, val: todayLog.core.movement },
    { id: 'emotional', name: 'Emocional', icon: '🧠', core: true, val: todayLog.core.emotional },
    { id: 'social', name: 'Social', icon: '💬', core: true, val: todayLog.core.social },
    ...customHabits.map(h => ({ id: h.id, name: h.name, icon: h.icon||'✅', core: false, val: todayLog.habits?.[h.id] }))
  ];

  vp.innerHTML = `
    <div class="habit-grid" id="habit-grid"></div>
    <button class="btn-primary full-width" id="open-checkin-btn">🌙 Cerrar día (Check-in)</button>
    <button class="btn-secondary full-width" style="margin-top:0.5rem" id="add-habit-btn">+ Agregar hábito</button>
  `;
  renderHabitCards(allHabits, logs);
  document.getElementById('open-checkin-btn').onclick = openCheckinModal;
  document.getElementById('add-habit-btn').onclick = openAddHabitModal;
}

function renderHabitCards(habits, logs) {
  const grid = document.getElementById('habit-grid');
  grid.innerHTML = habits.map(h => {
    const completed = h.core ? (h.val !== undefined && h.val !== false && h.val !== null) : (h.val === true);
    const cls = ['habit-card'];
    if (h.core) cls.push('core');
    if (completed) cls.push('completed');
    return `
      <div class="${cls.join(' ')}" data-id="${h.id}" data-core="${h.core}">
        <div class="habit-icon">${h.icon}</div>
        <div class="habit-name">${h.name}</div>
        <div class="habit-value">${formatValue(h.id, h.val)}</div>
        <div class="weekly-dots">${renderDots(h.id, logs)}</div>
      </div>
    `;
  }).join('');

  grid.querySelectorAll('.habit-card').forEach(card => {
    card.addEventListener('click', () => {
      const id = card.dataset.id;
      const core = card.dataset.core === 'true';
      if (core) {
        if (id === 'sleep' || id === 'emotional') {
          showCoreInputModal(id, card.dataset.core === 'true');
        } else {
          toggleCoreHabit(id);
        }
      } else {
        toggleCustomHabit(id);
      }
    });
  });
}

function formatValue(id, val) {
  if (val === undefined || val === null) return '—';
  if (id === 'sleep') return val + 'h';
  if (id === 'emotional') return val + '/5';
  return val ? '✓' : '✗';
}

function renderDots(habitId, logs) {
  let html = '';
  for (let i = 6; i >= 0; i--) {
    const d = new Date(); d.setDate(d.getDate() - i);
    const ds = d.toISOString().split('T')[0];
    const log = logs[ds];
    let done = false;
    if (log) {
      if (habitId === 'sleep') done = log.core.sleep >= 6.5;
      else if (habitId === 'emotional') done = log.core.emotional >= 3;
      else if (['nutrition','movement','social'].includes(habitId)) done = log.core[habitId] === true;
      else done = log.habits?.[habitId] === true;
    }
    html += `<span class="dot ${done ? 'done' : (log ? 'missed' : '')}"></span>`;
  }
  return html;
}

function toggleCoreHabit(id) {
  const today = todayStr();
  const logs = Storage.getLogs();
  const log = logs[today] || { core: {}, habits: {} };
  log.core[id] = !log.core[id];
  Storage.addLog(today, log);
  renderHome();
}

function toggleCustomHabit(id) {
  const today = todayStr();
  const logs = Storage.getLogs();
  const log = logs[today] || { core: {}, habits: {} };
  if (!log.habits) log.habits = {};
  log.habits[id] = !log.habits[id];
  Storage.addLog(today, log);
  renderHome();
}

function showCoreInputModal(id, core) {
  const today = todayStr();
  const logs = Storage.getLogs();
  const log = logs[today] || { core: {}, habits: {} };
  const current = log.core[id] || '';
  const title = id === 'sleep' ? 'Horas de sueño' : 'Estado emocional (1-5)';
  const body = `<input type="number" id="core-input" value="${current}" min="${id==='sleep'?0:1}" max="${id==='sleep'?24:5}" step="0.5">`;
  const footer = `<button class="btn-primary" id="save-core-btn">Guardar</button><button class="btn-secondary" id="cancel-core-btn">Cancelar</button>`;
  showModal(title, body, footer);
  document.getElementById('save-core-btn').onclick = () => {
    const val = parseFloat(document.getElementById('core-input').value);
    if (!isNaN(val)) {
      log.core[id] = val;
      Storage.addLog(today, log);
      closeModal();
      renderHome();
    }
  };
  document.getElementById('cancel-core-btn').onclick = closeModal;
}

function openCheckinModal() {
  const today = todayStr();
  const logs = Storage.getLogs();
  const log = logs[today] || { core: {}, habits: {} };
  let body = `
    <div class="form-group"><label>😴 Horas de sueño</label><input type="number" id="ci-sleep" value="${log.core.sleep||''}" min="0" max="24" step="0.5"></div>
    <div class="form-group"><label>🍽️ ¿Comiste al menos 3 veces?</label>
      <select id="ci-nutrition"><option value="">—</option><option value="1" ${log.core.nutrition?'selected':''}>Sí</option><option value="0" ${log.core.nutrition===false?'selected':''}>No</option></select></div>
    <div class="form-group"><label>🚶 ¿Te moviste al menos 30 min?</label>
      <select id="ci-movement"><option value="">—</option><option value="1" ${log.core.movement?'selected':''}>Sí</option><option value="0" ${log.core.movement===false?'selected':''}>No</option></select></div>
    <div class="form-group"><label>🧠 Estado emocional (1-5)</label><input type="number" id="ci-emotional" value="${log.core.emotional||''}" min="1" max="5"></div>
    <div class="form-group"><label>💬 ¿Interacción social hoy?</label>
      <select id="ci-social"><option value="">—</option><option value="1" ${log.core.social?'selected':''}>Sí</option><option value="0" ${log.core.social===false?'selected':''}>No</option></select></div>
    <div class="form-group"><label>📝 Notas del día</label><textarea id="ci-notes">${log.notes||''}</textarea></div>
  `;
  const footer = `<button class="btn-primary" id="save-checkin">Guardar</button><button class="btn-secondary" id="cancel-checkin">Cancelar</button>`;
  showModal('🌙 Check-in diario', body, footer);
  document.getElementById('save-checkin').onclick = () => {
    const core = {
      sleep: parseFloat(document.getElementById('ci-sleep').value) || null,
      nutrition: document.getElementById('ci-nutrition').value === '1' ? true : (document.getElementById('ci-nutrition').value === '0' ? false : null),
      movement: document.getElementById('ci-movement').value === '1' ? true : (document.getElementById('ci-movement').value === '0' ? false : null),
      emotional: parseInt(document.getElementById('ci-emotional').value) || null,
      social: document.getElementById('ci-social').value === '1' ? true : (document.getElementById('ci-social').value === '0' ? false : null)
    };
    const notes = document.getElementById('ci-notes').value;
    log.core = core;
    log.notes = notes;
    Storage.addLog(today, log);
    const allOk = core.sleep>0 && core.nutrition===true && core.movement===true && core.emotional>=1 && core.social===true;
    updateCreditsOnCheckin(today, allOk);
    closeModal();
    renderHome();
    updateTopBar();
    showToast('Check-in guardado ✅');
  };
  document.getElementById('cancel-checkin').onclick = closeModal;
}

function openAddHabitModal() {
  const body = `<input type="text" id="new-habit-name" placeholder="Nombre del hábito"><input type="text" id="new-habit-icon" placeholder="Icono (emoji)" style="margin-top:0.5rem">`;
  const footer = `<button class="btn-primary" id="save-habit-btn">Guardar</button><button class="btn-secondary" id="cancel-habit-btn">Cancelar</button>`;
  showModal('➕ Nuevo hábito', body, footer);
  document.getElementById('save-habit-btn').onclick = () => {
    const name = document.getElementById('new-habit-name').value.trim();
    const icon = document.getElementById('new-habit-icon').value || '✅';
    if (name) {
      const habits = Storage.getHabits();
      habits.push({ id: Date.now().toString(), name, icon });
      Storage.setHabits(habits);
      closeModal();
      renderHome();
      showToast('Hábito agregado');
    }
  };
  document.getElementById('cancel-habit-btn').onclick = closeModal;
}
'''

# ==================== js/components/exploit.js ====================
FILES["js/components/exploit.js"] = '''import { Storage } from '../storage.js';
import { todayStr, calculateBasal, spendCredit, getCredits } from '../state.js';
import { showModal, closeModal, showToast } from '../ui.js';

export function renderExploit() {
  const vp = document.getElementById('viewport');
  const areas = Storage.getAreas();
  const credits = getCredits();
  const basal = calculateBasal();
  vp.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
      <h3>⚡ Áreas de Explotación</h3>
      <span style="font-weight:600;">Créditos: ${'●'.repeat(credits)}${'○'.repeat(3-credits)}</span>
    </div>
    ${basal.mode === 'red' ? '<p style="color:var(--red); margin-bottom:1rem;">Modo Protección activo. No podés iniciar sesiones.</p>' : ''}
    <div id="areas-list" style="margin-top:0.5rem;"></div>
    <button class="btn-primary full-width" id="new-area-btn" style="margin-top:1.2rem;">➕ Nueva área</button>
  `;
  renderAreaCards(areas);
  document.getElementById('new-area-btn').addEventListener('click', openNewAreaModal);
}

function renderAreaCards(areas) {
  const container = document.getElementById('areas-list');
  const log = Storage.getExploitationLog();
  container.innerHTML = areas.map(a => {
    const sessions = log.filter(s => s.areaId === a.id);
    const last = sessions[sessions.length-1];
    return `
      <div class="card" style="margin-bottom:0.8rem; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <strong>${a.name}</strong>
          <div style="font-size:0.8rem; color:var(--text-secondary);">Última: ${last ? last.date + ' - ' + last.duration + 'min' : 'nunca'}</div>
        </div>
        <button class="btn-secondary start-session-btn" data-id="${a.id}">▶ Iniciar</button>
      </div>
    `;
  }).join('');
  document.querySelectorAll('.start-session-btn').forEach(btn => {
    btn.addEventListener('click', () => startSessionModal(btn.dataset.id));
  });
}

function startSessionModal(areaId) {
  const basal = calculateBasal();
  const credits = getCredits();
  if (basal.mode === 'red') { showToast('No disponible en Modo Protección'); return; }
  if (credits === 0) { showToast('Necesitás al menos 1 crédito'); return; }
  const body = `
    <p>Vas a gastar 1 crédito para esta sesión.</p>
    <div class="form-group"><label>Duración (minutos)</label><input type="number" id="session-duration" min="1" value="30"></div>
    <div class="form-group"><label>Intensidad (1-10)</label><input type="number" id="session-intensity" min="1" max="10" value="7"></div>
    <div class="form-group"><label>Notas</label><textarea id="session-notes" rows="2"></textarea></div>
  `;
  const footer = `<button class="btn-primary" id="save-session-btn">Guardar sesión</button><button class="btn-secondary" id="cancel-session-btn">Cancelar</button>`;
  showModal('▶ Iniciar sesión', body, footer);
  document.getElementById('save-session-btn').onclick = () => {
    const duration = parseInt(document.getElementById('session-duration').value);
    const intensity = parseInt(document.getElementById('session-intensity').value);
    const notes = document.getElementById('session-notes').value;
    if (duration > 0) {
      const success = spendCredit();
      if (success) {
        Storage.addExploit({ areaId, date: todayStr(), duration, intensity, notes });
        closeModal();
        renderExploit();
        showToast('Sesión guardada ⚡');
      } else {
        showToast('Error al gastar crédito');
      }
    }
  };
  document.getElementById('cancel-session-btn').onclick = closeModal;
}

function openNewAreaModal() {
  const body = `
    <div class="form-group"><label>Nombre</label><input type="text" id="area-name" placeholder="Ej: Fisiología"></div>
    <div class="form-group"><label>Tipo</label><select id="area-type"><option value="cognition">Estudio</option><option value="physique">Entrenamiento</option></select></div>
  `;
  const footer = `<button class="btn-primary" id="save-area-btn">Crear</button><button class="btn-secondary" id="cancel-area-btn">Cancelar</button>`;
  showModal('➕ Nueva área', body, footer);
  document.getElementById('save-area-btn').onclick = () => {
    const name = document.getElementById('area-name').value.trim();
    const type = document.getElementById('area-type').value;
    if (name) {
      const areas = Storage.getAreas();
      areas.push({ id: Date.now().toString(), name, type });
      Storage.setAreas(areas);
      closeModal();
      renderExploit();
      showToast('Área creada');
    }
  };
  document.getElementById('cancel-area-btn').onclick = closeModal;
}
'''

# ==================== js/components/analysis.js ====================
FILES["js/components/analysis.js"] = '''import { Storage } from '../storage.js';
import { calculateBasal } from '../state.js';
import { showToast } from '../ui.js';

let chart;

export function renderAnalysis() {
  const vp = document.getElementById('viewport');
  vp.innerHTML = `
    <h3>📊 Progreso a largo plazo</h3>
    <div style="display:flex; gap:0.5rem; margin:0.8rem 0 1.2rem;">
      <button class="btn-secondary period-btn active" data-months="3">3 meses</button>
      <button class="btn-secondary period-btn" data-months="6">6 meses</button>
      <button class="btn-secondary period-btn" data-months="12">12 meses</button>
    </div>
    <div class="chart-container"><canvas id="basal-chart"></canvas></div>
    <div id="stats-text" class="card" style="margin-top:1rem;"></div>
    <button class="btn-secondary full-width" id="export-btn" style="margin-top:1.2rem;">📥 Exportar datos</button>
  `;
  document.querySelectorAll('.period-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      loadChart(parseInt(btn.dataset.months));
    });
  });
  loadChart(3);
  document.getElementById('export-btn').onclick = () => {
    const blob = new Blob([Storage.exportAll()], {type:'application/json'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'mentalo-backup.json';
    a.click();
    showToast('Datos exportados');
  };
}

function loadChart(months) {
  const logs = Storage.getLogs();
  const dates = [];
  const end = new Date();
  const start = new Date();
  start.setMonth(start.getMonth() - months);
  for (let d = new Date(start); d <= end; d.setDate(d.getDate()+1)) {
    dates.push(new Date(d).toISOString().split('T')[0]);
  }
  const scores = dates.map(d => {
    const state = calculateBasal(d);
    return state.score;
  });
  const ctx = document.getElementById('basal-chart').getContext('2d');
  if (chart) chart.destroy();
  chart = new Chart(ctx, {
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
      scales: { y: { min:0, max:100, ticks:{stepSize:20} } },
      plugins: { tooltip: { mode: 'index' } }
    }
  });
  const valid = scores.filter(s => s!==null);
  const avg = valid.length ? Math.round(valid.reduce((a,b)=>a+b,0)/valid.length) : '—';
  const redDays = valid.filter(s => s<40).length;
  const greenDays = valid.filter(s => s>=70).length;
  document.getElementById('stats-text').innerHTML = `
    <strong>Resumen (${months} meses):</strong> Promedio: ${avg}/100 | Días en verde: ${greenDays} | Días en rojo: ${redDays}
    <p style="margin-top:0.5rem; font-style:italic;">${generateInsight(avg, redDays, greenDays)}</p>
  `;
}

function generateInsight(avg, red, green) {
  if (avg === '—') return 'Sin datos suficientes.';
  if (avg >= 70) return 'Excelente estado basal. Mantené la racha.';
  if (avg >= 40) return 'Estás en rango medio. Identificá los días rojos para prevenirlos.';
  return 'Tu promedio es bajo. Priorizá el Core y usá el checklist de emergencia.';
}
'''

# ==================== js/components/emergency.js ====================
FILES["js/components/emergency.js"] = '''import { Storage } from '../storage.js';
import { todayStr } from '../state.js';

export function renderEmergency() {
  const vp = document.getElementById('viewport');
  const config = Storage.getConfig();
  const checklist = config.emergencyChecklist || [];
  const today = todayStr();
  const log = Storage.getLogs()[today] || {};
  const completed = log.checklist || [];

  vp.innerHTML = `
    <h3>🛡️ Checklist de Emergencia</h3>
    <p style="color: var(--text-secondary); margin-bottom:1rem;">Completá lo que puedas. Sin presión.</p>
    <div id="checklist-container">
      ${checklist.map((item, idx) => `
        <div class="checklist-item ${completed.includes(idx) ? 'completed' : ''}" data-index="${idx}">
          <input type="checkbox" id="ec-${idx}" ${completed.includes(idx) ? 'checked' : ''}>
          <label for="ec-${idx}" style="flex:1;">${item}</label>
        </div>
      `).join('')}
    </div>
    <div class="card" style="margin-top:1rem; font-style:italic;">${config.supportMessage || ''}</div>
    <p id="progress-text" style="text-align:center; margin-top:1rem; font-weight:bold;"></p>
  `;

  document.querySelectorAll('.checklist-item input').forEach(cb => {
    cb.addEventListener('change', (e) => {
      const idx = parseInt(e.target.closest('.checklist-item').dataset.index);
      const logs = Storage.getLogs();
      const log = logs[today] || {};
      if (!log.checklist) log.checklist = [];
      if (e.target.checked) {
        if (!log.checklist.includes(idx)) log.checklist.push(idx);
        e.target.closest('.checklist-item').classList.add('completed');
      } else {
        log.checklist = log.checklist.filter(i => i !== idx);
        e.target.closest('.checklist-item').classList.remove('completed');
      }
      Storage.addLog(today, log);
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
FILES["js/components/config.js"] = '''import { Storage } from '../storage.js';
import { showModal, closeModal, showToast } from '../ui.js';

export function openConfigModal() {
  const config = Storage.getConfig();
  const body = `
    <div class="form-group"><label>PIN de acceso</label><input type="password" id="cfg-pin" value="${config.pin}"></div>
    <div class="form-group"><label>Mensaje de apoyo (Emergencia)</label><textarea id="cfg-support">${config.supportMessage}</textarea></div>
    <div class="form-group"><label>Checklist de emergencia (uno por línea)</label>
      <textarea id="cfg-checklist" rows="5">${config.emergencyChecklist.join('\\n')}</textarea></div>
  `;
  const footer = `<button class="btn-primary" id="save-config-btn">Guardar</button><button class="btn-secondary" id="cancel-config-btn">Cancelar</button>`;
  showModal('⚙️ Configuración', body, footer);
  document.getElementById('save-config-btn').onclick = () => {
    config.pin = document.getElementById('cfg-pin').value || '1234';
    config.supportMessage = document.getElementById('cfg-support').value;
    config.emergencyChecklist = document.getElementById('cfg-checklist').value.split('\\n').filter(l => l.trim());
    Storage.setConfig(config);
    closeModal();
    showToast('Configuración guardada');
  };
  document.getElementById('cancel-config-btn').onclick = closeModal;
}
'''

# ==================== js/app.js ====================
FILES["js/app.js"] = '''import { Storage } from './storage.js';
import { todayStr, calculateBasal, getCredits } from './state.js';
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
  const credits = getCredits();
  const dot = document.getElementById('status-dot');
  dot.className = 'status-dot ' + basal.mode;
  document.getElementById('status-score').textContent = basal.score !== null ? basal.score : '--';
  const label = basal.mode === 'green' ? 'Explotación disponible' : (basal.mode === 'yellow' ? 'Limitado' : 'Protección');
  document.getElementById('status-label').textContent = label;
  document.getElementById('credits-count').textContent = credits;
  const navEm = document.getElementById('nav-emergency');
  if (basal.mode === 'red') navEm.classList.remove('atenuado');
  else navEm.classList.add('atenuado');
}
'''

def create_project():
    for d in DIRS:
        os.makedirs(os.path.join(BASE_DIR, d), exist_ok=True)
    for path, content in FILES.items():
        full = os.path.join(BASE_DIR, path)
        with open(full, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ {path}")
    import shutil
    shutil.copy2(__file__, os.path.join(BASE_DIR, 'scripts', 'generate_v3.py'))
    print(f"\n✅ MentalOS v2.2 generado en '{BASE_DIR}/'")
    print("Abrí index.html en tu navegador o desplegalo en Vercel.")

if __name__ == '__main__':
    create_project()