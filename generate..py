#!/usr/bin/env python3
"""
MentalOS vFINAL – Home 100% responsive + hábitos por momento del día + Core rápido
"""
import os

BASE_DIR = "mentalo"
DIRS = ["css", "js", "js/components"]
FILES = {}

# ==================== index.html ====================
FILES["index.html"] = '''<!DOCTYPE html>
<html lang="es" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>MentalOS</title>
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="css/style.css?v=final">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body>
  <div id="pin-screen" class="fullscreen-center">
    <div class="card pin-card">
      <h1>MentalOS</h1>
      <input type="password" id="pin-input" maxlength="4" placeholder="••••" inputmode="numeric" pattern="[0-9]*">
      <button id="pin-btn" class="btn-primary full-width">Entrar</button>
      <p id="pin-error" class="text-error hidden"></p>
    </div>
  </div>

  <div id="app" class="app-container hidden">
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

    <main id="viewport" class="viewport"></main>

    <nav class="bottom-nav">
      <button class="nav-btn active" data-view="home"><span class="nav-icon">🏠</span><span class="nav-label">Hoy</span></button>
      <button class="nav-btn" data-view="exploit"><span class="nav-icon">⚡</span><span class="nav-label">Explotar</span></button>
      <button class="nav-btn" data-view="analysis"><span class="nav-icon">📊</span><span class="nav-label">Análisis</span></button>
      <button class="nav-btn" data-view="emergency" id="nav-emergency"><span class="nav-icon">🛡️</span><span class="nav-label">Emergencia</span></button>
    </nav>
  </div>

  <div id="modal-overlay" class="modal-overlay hidden">
    <div class="modal-container" id="modal-container">
      <div class="modal-header"><h2 id="modal-title"></h2><button class="modal-close" id="modal-close">✕</button></div>
      <div class="modal-body" id="modal-body"></div>
      <div class="modal-footer" id="modal-footer"></div>
    </div>
  </div>
  <div id="toast" class="toast hidden"></div>

  <script type="module" src="js/app.js?v=final"></script>
</body>
</html>'''

# ==================== css/style.css ====================
FILES["css/style.css"] = '''/* MentalOS – Responsive, Core rápido + Hábitos por sección */
:root {
  --bg: #0f0f0f;
  --surface: #1c1c1c;
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
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Inter', system-ui, sans-serif;
  background: var(--bg); color: var(--text);
  height: 100vh; overflow: hidden;
}
.fullscreen-center { display: flex; align-items: center; justify-content: center; height: 100vh; background: var(--bg); }
.hidden { display: none !important; }
.pin-card { text-align: center; padding: 2rem; width: 280px; }
.pin-card h1 { margin-bottom: 1.5rem; font-size: 2.5rem; }
#pin-input {
  width: 100%; padding: 0.8rem; font-size: 1.5rem; text-align: center;
  background: var(--surface); border: 1px solid var(--border); color: var(--text);
  border-radius: var(--radius); letter-spacing: 0.5em;
}
.text-error { color: var(--red); margin-top: 0.5rem; font-size: 0.85rem; }
.app-container { display: flex; flex-direction: column; height: 100vh; overflow: hidden; }

/* Topbar */
.topbar {
  display: flex; align-items: center; padding: 0.7rem 1rem;
  background: var(--surface); border-bottom: 1px solid var(--border); gap: 0.8rem;
}
.status-badge { display: flex; align-items: center; gap: 0.5rem; flex: 1; }
.status-dot { width: 16px; height: 16px; border-radius: 50%; background: var(--border); }
.status-dot.green { background: var(--green); }
.status-dot.yellow { background: var(--yellow); }
.status-dot.red { background: var(--red); }
.status-score { font-weight: 700; font-size: 1.1rem; }
.status-info small { color: var(--text-secondary); font-size: 0.65rem; display: block; }
.credits-badge { display: flex; align-items: center; gap: 0.25rem; font-weight: 600; background: var(--bg); padding: 0.25rem 0.5rem; border-radius: 20px; font-size: 0.9rem; }
.icon-btn { background: none; border: none; color: var(--text); font-size: 1.3rem; padding: 0.25rem; cursor: pointer; }

/* Viewport */
.viewport { flex: 1; overflow-y: auto; padding: 0.8rem; max-width: 600px; margin: 0 auto; width: 100%; }

/* Bottom nav */
.bottom-nav { display: flex; justify-content: space-around; background: var(--surface); border-top: 1px solid var(--border); padding: 0.4rem 0; }
.nav-btn { display: flex; flex-direction: column; align-items: center; background: none; border: none; color: var(--text-secondary); font-size: 0.6rem; cursor: pointer; }
.nav-btn.active { color: var(--accent); }
.nav-btn .nav-icon { font-size: 1.3rem; }
.nav-btn.atenuado { opacity: 0.3; pointer-events: none; }

/* Core rápido (chips) */
.core-quick-panel {
  display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 1rem;
}
.core-chip {
  display: flex; align-items: center; gap: 0.25rem;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 20px; padding: 0.35rem 0.7rem; cursor: pointer;
  font-size: 0.8rem; transition: background 0.2s;
}
.core-chip:active { background: var(--surface-hover); }
.chip-icon { font-size: 1rem; }
.chip-value { font-weight: 500; }

/* Secciones de hábitos */
.habit-section { margin-bottom: 1rem; }
.section-title { font-size: 0.95rem; margin-bottom: 0.4rem; font-weight: 600; }
.habit-list { display: flex; flex-direction: column; gap: 0.4rem; }

.habit-item {
  display: flex; align-items: center; gap: 0.6rem;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 0.6rem 0.8rem; cursor: pointer;
}
.habit-item:active { background: var(--surface-hover); }
.habit-checkbox {
  width: 20px; height: 20px; border-radius: 50%;
  border: 2px solid var(--border); background: transparent;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.7rem; color: white; flex-shrink: 0;
}
.habit-item.completed .habit-checkbox {
  background: var(--green); border-color: var(--green);
}
.habit-item.completed .habit-checkbox::after { content: '✓'; }
.habit-info { flex: 1; display: flex; justify-content: space-between; align-items: center; }
.habit-name { font-size: 0.85rem; }
.habit-duration { font-size: 0.75rem; color: var(--text-secondary); margin-left: 0.5rem; }

.btn-add-habit {
  background: none; border: 1px dashed var(--border); color: var(--text-secondary);
  padding: 0.5rem; border-radius: var(--radius); cursor: pointer;
  text-align: center; font-size: 0.8rem; margin-top: 0.2rem;
}

/* Botones */
.btn-primary {
  display: inline-block; background: var(--accent); color: white; border: none;
  padding: 0.7rem 1.2rem; border-radius: var(--radius); font-weight: 600; cursor: pointer;
}
.btn-secondary { background: transparent; border: 1px solid var(--border); color: var(--text); padding: 0.6rem 1rem; border-radius: var(--radius); cursor: pointer; }
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
@keyframes slideUp { from { transform: translateY(15%); } to { transform: translateY(0); } }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.modal-close { background: none; border: none; color: var(--text); font-size: 1.5rem; cursor: pointer; }
.modal-body { margin-bottom: 1rem; }
.modal-footer { display: flex; gap: 0.5rem; justify-content: flex-end; }

.form-group { margin-bottom: 1rem; }
.form-group label { display: block; margin-bottom: 0.25rem; font-weight: 500; }
input, select, textarea {
  width: 100%; padding: 0.65rem; background: var(--bg); border: 1px solid var(--border);
  color: var(--text); border-radius: 8px; font-size: 0.9rem; font-family: inherit;
}
textarea { resize: vertical; min-height: 80px; }

/* Otras secciones (sin cambios) */
.chart-container { background: var(--surface); border-radius: var(--radius); padding: 1rem; margin-bottom: 1rem; }
.checklist-item {
  display: flex; align-items: center; gap: 0.8rem; padding: 0.8rem;
  background: var(--surface); border-radius: var(--radius); margin-bottom: 0.5rem; border: 1px solid var(--border);
}
.checklist-item.completed { background: var(--green-bg); border-color: var(--green); }
.checklist-item input[type="checkbox"] { width: 22px; height: 22px; accent-color: var(--green); }
.toast {
  position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%);
  background: var(--surface); border: 1px solid var(--border); color: var(--text);
  padding: 0.8rem 1.5rem; border-radius: 30px; z-index: 600;
  animation: fadeInOut 2s ease forwards;
}
@keyframes fadeInOut {
  0% { opacity: 0; bottom: 60px; } 20% { opacity: 1; bottom: 80px; }
  80% { opacity: 1; bottom: 80px; } 100% { opacity: 0; bottom: 60px; }
}
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
      supportMessage: 'Esto es pasajero. Ya saliste de episodios peores.',
      contactName: 'Contacto de confianza'
    };
  },
  setConfig(c) { this.set('config', c); },
  getHabits() {
    let habits = this.get('habits');
    if (!habits || habits.length === 0) {
      // Hábitos por defecto
      habits = [
        { id: '1', name: 'Estiramientos', icon: '🧘', section: 'morning', duration: 10 },
        { id: '2', name: 'Leer artículos', icon: '📄', section: 'morning', duration: 20 },
        { id: '3', name: 'Ejercicio', icon: '🏋️', section: 'afternoon', duration: 45 },
        { id: '4', name: 'Planificar el día', icon: '📅', section: 'morning', duration: 5 },
        { id: '5', name: 'Meditar', icon: '🧘‍♂️', section: 'evening', duration: 10 },
        { id: '6', name: 'Escribir diario', icon: '✍️', section: 'evening', duration: 15 }
      ];
      this.set('habits', habits);
    }
    return habits;
  },
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
export function todayStr() { return new Date().toISOString().split('T')[0]; }
export function calculateBasal(dateStr = null) {
  const date = dateStr || todayStr();
  const logs = Storage.getLogs();
  const log = logs[date];
  if (!log || !log.core) return { score: null, mode: 'unknown' };
  const core = log.core;
  if (core.emotional !== undefined && core.emotional <= 2) return { score: 0, mode: 'red', reason: 'emotional' };
  if (core.sleep !== undefined && core.sleep < 5) return { score: 0, mode: 'red', reason: 'sleep' };
  const socialDays = [];
  for (let i=0; i<3; i++) {
    const d = new Date(); d.setDate(d.getDate()-i);
    socialDays.push(logs[d.toISOString().split('T')[0]]?.core?.social);
  }
  if (socialDays.filter(s => s === false).length >= 3) return { score: 0, mode: 'red', reason: 'social' };
  let score = 0, total = 0;
  const weights = { sleep: 30, emotional: 30, nutrition: 15, movement: 15, social: 10 };
  if (core.sleep !== undefined) { score += Math.min(core.sleep/8,1)*weights.sleep; total += weights.sleep; }
  if (core.emotional !== undefined) { score += (core.emotional/5)*weights.emotional; total += weights.emotional; }
  if (core.nutrition !== undefined) { score += (core.nutrition?1:0)*weights.nutrition; total += weights.nutrition; }
  if (core.movement !== undefined) { score += (core.movement?1:0)*weights.movement; total += weights.movement; }
  if (core.social !== undefined) { score += (core.social?1:0)*weights.social; total += weights.social; }
  if (total === 0) return { score: null, mode: 'unknown' };
  const final = Math.round((score/total)*100);
  if (final >= 70) return { score: final, mode: 'green' };
  if (final >= 40) return { score: final, mode: 'yellow' };
  return { score: final, mode: 'red' };
}
export function updateCreditsOnCheckin(date, allCoreOk) {
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
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  const btn = document.querySelector(`[data-view="${view}"]`);
  if (btn) btn.classList.add('active');
}
'''

# ==================== js/components/home.js ====================
FILES["js/components/home.js"] = '''import { Storage } from '../storage.js';
import { todayStr, updateCreditsOnCheckin } from '../state.js';
import { showModal, closeModal, showToast } from '../ui.js';
import { updateTopBar } from '../app.js';

export function renderHome() {
  const vp = document.getElementById('viewport');
  const today = todayStr();
  const logs = Storage.getLogs();
  const todayLog = logs[today] || { core: {}, habits: {} };
  const customHabits = Storage.getHabits();

  // Core rápido (chips)
  const coreItems = [
    { id: 'sleep', name: 'Sueño', icon: '😴', value: todayLog.core.sleep, unit: 'h', format: v => v+'h' },
    { id: 'nutrition', name: 'Nutrición', icon: '🍽️', value: todayLog.core.nutrition, unit: '', format: v => v?'✓':'✗' },
    { id: 'movement', name: 'Movimiento', icon: '🚶', value: todayLog.core.movement, unit: '', format: v => v?'✓':'✗' },
    { id: 'emotional', name: 'Emocional', icon: '🧠', value: todayLog.core.emotional, unit: '/5', format: v => v+'/5' },
    { id: 'social', name: 'Social', icon: '💬', value: todayLog.core.social, unit: '', format: v => v?'✓':'✗' }
  ];

  let html = `<div class="core-quick-panel">`;
  coreItems.forEach(item => {
    html += `<button class="core-chip" data-core-id="${item.id}">
      <span class="chip-icon">${item.icon}</span>
      <span class="chip-value">${item.value !== undefined && item.value !== null ? item.format(item.value) : '—'}</span>
    </button>`;
  });
  html += `</div>`;

  // Secciones de hábitos
  const sections = [
    { key: 'morning', title: '🌅 Mañana' },
    { key: 'afternoon', title: '☀️ Tarde' },
    { key: 'evening', title: '🌙 Noche' }
  ];

  sections.forEach(sec => {
    const habitsInSection = customHabits.filter(h => h.section === sec.key);
    html += `<div class="habit-section">
      <h3 class="section-title">${sec.title}</h3>
      <div class="habit-list" data-section="${sec.key}">
        ${habitsInSection.map(h => {
          const completed = todayLog.habits?.[h.id] === true;
          return `<div class="habit-item ${completed ? 'completed' : ''}" data-habit-id="${h.id}">
            <div class="habit-checkbox"></div>
            <div class="habit-info">
              <span class="habit-name">${h.icon ? h.icon + ' ' : ''}${h.name}</span>
              <span class="habit-duration">${h.duration ? h.duration + ' min' : ''}</span>
            </div>
          </div>`;
        }).join('')}
        <button class="btn-add-habit" data-section="${sec.key}">+ Agregar hábito</button>
      </div>
    </div>`;
  });

  html += `<button class="btn-primary full-width" id="open-checkin-btn" style="margin-top:0.5rem;">🌙 Cerrar día (Check-in)</button>`;
  vp.innerHTML = html;

  // Eventos Core chips
  document.querySelectorAll('.core-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const id = chip.dataset.coreId;
      if (id === 'sleep' || id === 'emotional') showCoreInputModal(id);
      else toggleCoreHabit(id);
    });
  });

  // Eventos hábitos
  document.querySelectorAll('.habit-item').forEach(item => {
    item.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleCustomHabit(item.dataset.habitId);
    });
  });

  // Agregar hábito a sección
  document.querySelectorAll('.btn-add-habit').forEach(btn => {
    btn.addEventListener('click', () => openAddHabitModal(btn.dataset.section));
  });

  document.getElementById('open-checkin-btn').onclick = openCheckinModal;
}

function formatValue(id, val) {
  if (val === undefined || val === null) return '—';
  if (id === 'sleep') return val + 'h';
  if (id === 'emotional') return val + '/5';
  return val ? '✓' : '✗';
}

function toggleCoreHabit(id) {
  const today = todayStr();
  const logs = Storage.getLogs();
  const log = logs[today] || { core: {}, habits: {} };
  log.core[id] = !log.core[id];
  Storage.addLog(today, log);
  renderHome();
}

function toggleCustomHabit(habitId) {
  const today = todayStr();
  const logs = Storage.getLogs();
  const log = logs[today] || { core: {}, habits: {} };
  if (!log.habits) log.habits = {};
  log.habits[habitId] = !log.habits[habitId];
  Storage.addLog(today, log);
  renderHome();
}

function showCoreInputModal(id) {
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
    if (!isNaN(val)) { log.core[id] = val; Storage.addLog(today, log); closeModal(); renderHome(); }
  };
  document.getElementById('cancel-core-btn').onclick = closeModal;
}

function openCheckinModal() {
  const today = todayStr();
  const logs = Storage.getLogs();
  const log = logs[today] || { core: {}, habits: {} };
  const body = `
    <div class="form-group"><label>😴 Horas de sueño</label><input type="number" id="ci-sleep" value="${log.core.sleep||''}" min="0" max="24" step="0.5"></div>
    <div class="form-group"><label>🍽️ ¿Comiste al menos 3 veces?</label><select id="ci-nutrition"><option value="">—</option><option value="1" ${log.core.nutrition?'selected':''}>Sí</option><option value="0" ${log.core.nutrition===false?'selected':''}>No</option></select></div>
    <div class="form-group"><label>🚶 ¿Te moviste al menos 30 min?</label><select id="ci-movement"><option value="">—</option><option value="1" ${log.core.movement?'selected':''}>Sí</option><option value="0" ${log.core.movement===false?'selected':''}>No</option></select></div>
    <div class="form-group"><label>🧠 Estado emocional (1-5)</label><input type="number" id="ci-emotional" value="${log.core.emotional||''}" min="1" max="5"></div>
    <div class="form-group"><label>💬 ¿Interacción social hoy?</label><select id="ci-social"><option value="">—</option><option value="1" ${log.core.social?'selected':''}>Sí</option><option value="0" ${log.core.social===false?'selected':''}>No</option></select></div>
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
    log.core = core;
    log.notes = document.getElementById('ci-notes').value;
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

function openAddHabitModal(section) {
  const body = `
    <input type="text" id="new-habit-name" placeholder="Nombre del hábito">
    <input type="text" id="new-habit-icon" placeholder="Icono (emoji)" style="margin-top:0.5rem">
    <div class="form-group" style="margin-top:0.5rem"><label>Duración (minutos)</label><input type="number" id="new-habit-duration" min="1" value="15"></div>
  `;
  const footer = `<button class="btn-primary" id="save-habit-btn">Guardar</button><button class="btn-secondary" id="cancel-habit-btn">Cancelar</button>`;
  showModal('➕ Nuevo hábito', body, footer);
  document.getElementById('save-habit-btn').onclick = () => {
    const name = document.getElementById('new-habit-name').value.trim();
    const icon = document.getElementById('new-habit-icon').value || '✅';
    const duration = parseInt(document.getElementById('new-habit-duration').value) || 15;
    if (name) {
      const habits = Storage.getHabits();
      habits.push({ id: Date.now().toString(), name, icon, section, duration });
      Storage.setHabits(habits);
      closeModal();
      renderHome();
    }
  };
  document.getElementById('cancel-habit-btn').onclick = closeModal;
}
'''

# ==================== js/components/exploit.js ====================
FILES["js/components/exploit.js"] = '''import { Storage } from '../storage.js';
import { todayStr, calculateBasal, spendCredit } from '../state.js';
import { showModal, closeModal, showToast } from '../ui.js';

export function renderExploit() {
  const vp = document.getElementById('viewport');
  const areas = Storage.getAreas();
  const credits = Storage.getCredits();
  const basal = calculateBasal();
  vp.innerHTML = `
    <div style="display:flex; justify-content:space-between; margin-bottom:1rem;">
      <h3>⚡ Explotar</h3><span>Créditos: ${'●'.repeat(credits)}${'○'.repeat(3-credits)}</span>
    </div>
    ${basal.mode==='red'?'<p style="color:var(--red);">Modo Protección. Sin sesiones.</p>':''}
    <div id="areas-list"></div>
    <button class="btn-primary full-width" id="new-area-btn" style="margin-top:1rem;">+ Nueva área</button>
  `;
  renderAreaCards(areas);
  document.getElementById('new-area-btn').onclick = openNewAreaModal;
}

function renderAreaCards(areas) {
  const log = Storage.getExploitationLog();
  document.getElementById('areas-list').innerHTML = areas.map(a => {
    const sessions = log.filter(s => s.areaId === a.id);
    const last = sessions[sessions.length-1];
    return `
      <div class="card" style="margin-bottom:0.8rem; display:flex; justify-content:space-between;">
        <div><strong>${a.name}</strong><div style="font-size:0.8rem; color:var(--text-secondary);">Última: ${last?last.date+ ' - '+last.duration+'min':'nunca'}</div></div>
        <button class="btn-secondary start-session-btn" data-id="${a.id}">▶</button>
      </div>`;
  }).join('');
  document.querySelectorAll('.start-session-btn').forEach(btn => btn.addEventListener('click', () => startSessionModal(btn.dataset.id)));
}

function startSessionModal(areaId) {
  if (calculateBasal().mode === 'red') { showToast('No disponible en Protección'); return; }
  if (Storage.getCredits() === 0) { showToast('Necesitás 1 crédito'); return; }
  const body = `<p>Gastar 1 crédito.</p><div class="form-group"><label>Duración (min)</label><input type="number" id="session-duration" min="1" value="30"></div>
    <div class="form-group"><label>Intensidad (1-10)</label><input type="number" id="session-intensity" min="1" max="10" value="7"></div>
    <div class="form-group"><label>Notas</label><textarea id="session-notes"></textarea></div>`;
  const footer = `<button class="btn-primary" id="save-session-btn">Guardar</button><button class="btn-secondary" id="cancel-session-btn">Cancelar</button>`;
  showModal('▶ Sesión', body, footer);
  document.getElementById('save-session-btn').onclick = () => {
    const duration = parseInt(document.getElementById('session-duration').value);
    if (duration > 0 && spendCredit()) {
      Storage.addExploit({ areaId, date: todayStr(), duration, intensity: parseInt(document.getElementById('session-intensity').value), notes: document.getElementById('session-notes').value });
      closeModal(); renderExploit(); showToast('Sesión guardada');
    }
  };
  document.getElementById('cancel-session-btn').onclick = closeModal;
}

function openNewAreaModal() {
  const body = `<div class="form-group"><label>Nombre</label><input type="text" id="area-name"></div><div class="form-group"><label>Tipo</label><select id="area-type"><option value="cognition">Estudio</option><option value="physique">Entrenamiento</option></select></div>`;
  const footer = `<button class="btn-primary" id="save-area-btn">Crear</button><button class="btn-secondary" id="cancel-area-btn">Cancelar</button>`;
  showModal('➕ Nueva área', body, footer);
  document.getElementById('save-area-btn').onclick = () => {
    const name = document.getElementById('area-name').value.trim();
    if (name) { const areas = Storage.getAreas(); areas.push({ id: Date.now().toString(), name, type: document.getElementById('area-type').value }); Storage.setAreas(areas); closeModal(); renderExploit(); }
  };
  document.getElementById('cancel-area-btn').onclick = closeModal;
}
'''

# ==================== js/components/analysis.js ====================
FILES["js/components/analysis.js"] = '''import { Storage } from '../storage.js';
import { calculateBasal } from '../state.js';
let chart;
export function renderAnalysis() {
  document.getElementById('viewport').innerHTML = `
    <h3>📊 Progreso</h3>
    <div style="display:flex; gap:0.5rem; margin:0.8rem 0;">
      <button class="btn-secondary period-btn active" data-months="3">3M</button>
      <button class="btn-secondary period-btn" data-months="6">6M</button>
      <button class="btn-secondary period-btn" data-months="12">12M</button>
    </div>
    <div class="chart-container"><canvas id="basal-chart"></canvas></div>
    <div id="stats-text" class="card"></div>
    <button class="btn-secondary full-width" id="export-btn" style="margin-top:1rem;">📥 Exportar</button>
  `;
  document.querySelectorAll('.period-btn').forEach(b => b.addEventListener('click', function() {
    document.querySelectorAll('.period-btn').forEach(x => x.classList.remove('active'));
    this.classList.add('active');
    loadChart(parseInt(this.dataset.months));
  }));
  loadChart(3);
  document.getElementById('export-btn').onclick = () => {
    const blob = new Blob([Storage.exportAll()], {type:'application/json'});
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'mentalo-backup.json'; a.click();
  };
}
function loadChart(months) {
  const logs = Storage.getLogs();
  const dates = [], end = new Date(), start = new Date();
  start.setMonth(start.getMonth()-months);
  for (let d = new Date(start); d <= end; d.setDate(d.getDate()+1)) dates.push(new Date(d).toISOString().split('T')[0]);
  const scores = dates.map(d => calculateBasal(d).score);
  if (chart) chart.destroy();
  chart = new Chart(document.getElementById('basal-chart').getContext('2d'), {
    type: 'line', data: { labels: dates.map(d => d.slice(5)), datasets: [{ label: 'Estado Basal', data: scores, borderColor: '#5c8aff', backgroundColor: 'rgba(92,138,255,0.1)', fill: true, tension: 0.3, pointRadius: 0 }] },
    options: { scales: { y: { min:0, max:100 } } }
  });
  const valid = scores.filter(s => s!==null);
  const avg = valid.length ? Math.round(valid.reduce((a,b)=>a+b,0)/valid.length) : '—';
  document.getElementById('stats-text').innerHTML = `<strong>Resumen (${months}M):</strong> Promedio: ${avg}/100`;
}
'''

# ==================== js/components/emergency.js ====================
FILES["js/components/emergency.js"] = '''import { Storage } from '../storage.js';
import { todayStr } from '../state.js';
export function renderEmergency() {
  const config = Storage.getConfig();
  const checklist = config.emergencyChecklist;
  const today = todayStr();
  const log = Storage.getLogs()[today] || {};
  const completed = log.checklist || [];
  document.getElementById('viewport').innerHTML = `
    <h3>🛡️ Emergencia</h3>
    <p style="color:var(--text-secondary);">Completá lo que puedas.</p>
    <div id="checklist-container">${checklist.map((item, idx) => `
      <div class="checklist-item ${completed.includes(idx)?'completed':''}" data-index="${idx}">
        <input type="checkbox" id="ec-${idx}" ${completed.includes(idx)?'checked':''}>
        <label for="ec-${idx}">${item}</label>
      </div>`).join('')}</div>
    <div class="card" style="margin-top:1rem; font-style:italic;">${config.supportMessage}</div>
    <p id="progress-text" style="text-align:center; margin-top:1rem; font-weight:bold;"></p>
  `;
  document.querySelectorAll('.checklist-item input').forEach(cb => {
    cb.addEventListener('change', (e) => {
      const idx = parseInt(e.target.closest('.checklist-item').dataset.index);
      const logs = Storage.getLogs();
      const log = logs[today] || {};
      if (!log.checklist) log.checklist = [];
      if (e.target.checked) { if (!log.checklist.includes(idx)) log.checklist.push(idx); e.target.closest('.checklist-item').classList.add('completed'); }
      else { log.checklist = log.checklist.filter(i => i !== idx); e.target.closest('.checklist-item').classList.remove('completed'); }
      Storage.addLog(today, log);
      updateProgress();
    });
  });
  updateProgress();
  function updateProgress() {
    const total = document.querySelectorAll('.checklist-item').length;
    const checked = document.querySelectorAll('.checklist-item input:checked').length;
    document.getElementById('progress-text').textContent = `${checked} de ${total} completado`;
  }
}
'''

# ==================== js/components/config.js ====================
FILES["js/components/config.js"] = '''import { Storage } from '../storage.js';
import { showModal, closeModal, showToast } from '../ui.js';
export function openConfigModal() {
  const config = Storage.getConfig();
  const body = `
    <div class="form-group"><label>PIN</label><input type="password" id="cfg-pin" value="${config.pin}"></div>
    <div class="form-group"><label>Mensaje de apoyo</label><textarea id="cfg-support">${config.supportMessage}</textarea></div>
    <div class="form-group"><label>Checklist (uno por línea)</label><textarea id="cfg-checklist" rows="5">${config.emergencyChecklist.join('\\n')}</textarea></div>`;
  const footer = `<button class="btn-primary" id="save-config-btn">Guardar</button><button class="btn-secondary" id="cancel-config-btn">Cancelar</button>`;
  showModal('⚙️ Configuración', body, footer);
  document.getElementById('save-config-btn').onclick = () => {
    config.pin = document.getElementById('cfg-pin').value || '2207';
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
  const credits = Storage.getCredits();
  document.getElementById('status-dot').className = 'status-dot ' + basal.mode;
  document.getElementById('status-score').textContent = basal.score ?? '--';
  document.getElementById('status-label').textContent = basal.mode === 'green' ? 'Explotación' : (basal.mode === 'yellow' ? 'Limitado' : 'Protección');
  document.getElementById('credits-count').textContent = credits;
  document.getElementById('nav-emergency').classList.toggle('atenuado', basal.mode !== 'red');
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
    print(f"\n✅ MentalOS con Home responsiva y hábitos por momento generado.")
    print("PIN por defecto: 2207")

if __name__ == '__main__':
    create_project()