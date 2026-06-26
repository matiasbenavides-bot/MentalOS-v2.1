#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MentalOS – Proyecto completo (HTML + CSS + JS) con codificación UTF-8 correcta."""

import os

BASE_DIR = "."  # genera los archivos en la carpeta actual
DIRS = ["css", "js", "js/components"]

FILES = {}

# ==================== index.html ====================
FILES["index.html"] = r"""<!DOCTYPE html>
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
</html>"""

# ==================== css/style.css ====================
FILES["css/style.css"] = r"""/* MentalOS – Neutralidad sensorial, móvil primero */
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
  --green-bg: rgba(76,175,80,0.12);
  --yellow-bg: rgba(255,193,7,0.12);
  --red-bg: rgba(244,67,54,0.12);
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
  position: relative; overflow: hidden;
}
.habit-item.dragging { opacity: 0.5; transform: scale(0.96); }
.habit-item.drag-over { border-color: var(--accent); background: rgba(92,138,255,0.12); }
.habit-item.completed { opacity: 0.6; }
.drag-handle { color: var(--text-secondary); cursor: grab; font-size: 1.2rem; margin-right: 0.2rem; }
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

/* Swipe actions */
.swipe-delete {
  position: absolute; right: 0; top: 0; bottom: 0; width: 80px;
  background: var(--red); color: white; display: flex; align-items: center; justify-content: center;
  font-weight: 600; font-size: 0.8rem; transform: translateX(100%); transition: transform 0.2s;
}
.swipe-edit {
  position: absolute; left: 0; top: 0; bottom: 0; width: 80px;
  background: var(--accent); color: white; display: flex; align-items: center; justify-content: center;
  font-weight: 600; font-size: 0.8rem; transform: translateX(-100%); transition: transform 0.2s;
}

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

/* Pestañas */
.tab-bar { display: flex; gap: 0; border-bottom: 1px solid var(--border); margin-bottom: 0.8rem; }
.tab-btn {
  flex: 1; background: none; border: none; color: var(--text-secondary);
  padding: 0.4rem; font-size: 0.75rem; cursor: pointer; border-bottom: 2px solid transparent;
}
.tab-btn.active { color: var(--accent); border-bottom-color: var(--accent); }

/* Temporizador */
.timer-display { font-size: 2rem; text-align: center; font-weight: 700; padding: 1rem; }

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

/* Reproductor interno */
.video-iframe { width: 100%; height: 200px; border: none; border-radius: var(--radius); margin: 0.5rem 0; }
"""

# ==================== js/storage.js ====================
FILES["js/storage.js"] = r"""const PREFIX = 'mentalo_';
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
"""

# ==================== js/state.js ====================
FILES["js/state.js"] = r"""import { Storage } from './storage.js';
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
"""

# ==================== js/ui.js ====================
FILES["js/ui.js"] = r"""export function showModal(title, bodyHtml, footerHtml = '') {
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
"""

# ==================== js/app.js ====================
FILES["js/app.js"] = r"""import { Storage } from './storage.js';
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

  const navDev = document.querySelector('.top-nav-btn[data-view="development"]');
  const navAnalysis = document.querySelector('.top-nav-btn[data-view="analysis"]');
  const navEmergency = document.getElementById('nav-emergency');

  if (basal.mode === 'red') {
    if (navDev) navDev.classList.add('hidden');
    if (navAnalysis) navAnalysis.classList.add('hidden');
    if (navEmergency) navEmergency.classList.remove('hidden');
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
"""

# ==================== js/components/home.js (con drag & drop mejorado) ====================
FILES["js/components/home.js"] = r"""import { Storage } from '../storage.js';
import { todayStr, calculateBasal, updateCreditsOnCheckin } from '../state.js';
import { showModal, closeModal, showToast } from '../ui.js';
import { updateTopBar } from '../app.js';

let draggedItem = null;
let draggedId = null;

export function renderHome() {
  const vp = document.getElementById('viewport');
  const today = todayStr();
  const logs = Storage.getLogs();
  const todayLog = logs[today] || { core: {}, habits: {} };
  const habits = Storage.getHabits().sort((a,b) => (a.order||0) - (b.order||0));

  // Core chips
  const coreItems = [
    { id: 'sleep', label: 'Sueño', value: todayLog.core.sleep, fmt: v => v !== null ? v+'h' : '--' },
    { id: 'nutrition', label: 'Nutrición', value: todayLog.core.nutrition, fmt: v => v ? 'Sí' : 'No' },
    { id: 'movement', label: 'Movimiento', value: todayLog.core.movement, fmt: v => v ? 'Sí' : 'No' },
    { id: 'emotion', label: 'Emocional', value: todayLog.core.emotion, fmt: v => v !== null ? v+'/5' : '--' },
    { id: 'social', label: 'Social', value: todayLog.core.social, fmt: v => v ? 'Sí' : 'No' }
  ];

  let html = '<div class="core-quick-panel">';
  coreItems.forEach(item => {
    html += `<button class="core-chip" data-core-id="${item.id}">
      <span class="chip-value">${item.label}: ${item.fmt(item.value)}</span>
    </button>`;
  });
  html += '</div>';

  const sections = [
    { key: 'morning', title: 'Mañana' },
    { key: 'afternoon', title: 'Tarde' },
    { key: 'evening', title: 'Noche' }
  ];

  sections.forEach(sec => {
    const sectionHabits = habits.filter(h => h.section === sec.key);
    html += `<div class="habit-section" data-section="${sec.key}">
      <h3 class="section-title">${sec.title}</h3>
      <div class="habit-list" id="habit-list-${sec.key}">
        ${sectionHabits.map(h => {
          const done = todayLog.habits?.[h.id] === true;
          return `<div class="habit-item ${done ? 'completed' : ''}" data-id="${h.id}" draggable="true">
            <div class="drag-handle">⋮⋮</div>
            <div class="habit-checkbox"></div>
            <div class="habit-info">
              <span class="habit-name">${h.name}</span>
              <span class="habit-duration">${h.duration} min</span>
            </div>
            <div class="swipe-edit">Editar</div>
            <div class="swipe-delete">Borrar</div>
          </div>`;
        }).join('')}
        <button class="btn-add-habit" data-section="${sec.key}">+ Agregar</button>
      </div>
    </div>`;
  });

  // Mini calendario semanal
  html += '<div class="mini-calendar">';
  for (let i = 6; i >= 0; i--) {
    const d = new Date(); d.setDate(d.getDate() - i);
    const ds = d.toISOString().split('T')[0];
    const state = calculateBasal(ds);
    html += `<div class="calendar-day ${state.mode}" data-date="${ds}">${d.getDate()}</div>`;
  }
  html += '</div>';

  html += '<button class="btn-primary full-width" id="open-checkin-btn">Cerrar día (Check-in)</button>';
  vp.innerHTML = html;

  // Eventos Core
  document.querySelectorAll('.core-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const id = chip.dataset.coreId;
      if (id === 'sleep' || id === 'emotion') showCoreInputModal(id);
      else toggleCoreHabit(id);
    });
  });

  // Eventos hábitos
  document.querySelectorAll('.habit-item').forEach(item => {
    const habitId = item.dataset.id;
    item.addEventListener('click', (e) => {
      if (e.target.closest('.swipe-delete') || e.target.closest('.swipe-edit') || e.target.closest('.drag-handle')) return;
      toggleCustomHabit(habitId);
    });
    addSwipeListeners(item, habitId);
  });

  document.querySelectorAll('.btn-add-habit').forEach(btn => {
    btn.addEventListener('click', () => openAddHabitModal(btn.dataset.section));
  });

  document.querySelectorAll('.calendar-day').forEach(day => {
    day.addEventListener('click', () => showDaySummary(day.dataset.date));
  });

  document.getElementById('open-checkin-btn').onclick = openCheckinModal;

  enableDragDrop();
}

function formatValue(val, id) {
  if (val === undefined || val === null) return '--';
  if (id === 'sleep') return val + 'h';
  if (id === 'emotion') return val + '/5';
  return val ? 'Sí' : 'No';
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
  const footer = '<button class="btn-primary" id="save-core">Guardar</button><button class="btn-secondary" id="cancel-core">Cancelar</button>';
  showModal(title, body, footer);
  document.getElementById('save-core').onclick = () => {
    const val = parseFloat(document.getElementById('core-input').value);
    if (!isNaN(val)) { log.core[id] = val; Storage.addLog(today, log); closeModal(); renderHome(); }
  };
  document.getElementById('cancel-core').onclick = closeModal;
}

function openCheckinModal() {
  const today = todayStr();
  const logs = Storage.getLogs();
  const log = logs[today] || { core: {}, habits: {} };
  const body = `
    <div class="form-group"><label>Horas de sueño</label><input type="number" id="ci-sleep" value="${log.core.sleep||''}" min="0" max="24" step="0.5"></div>
    <div class="form-group"><label>¿Comiste al menos 3 veces?</label><select id="ci-nutrition"><option value="">--</option><option value="1" ${log.core.nutrition?'selected':''}>Sí</option><option value="0" ${log.core.nutrition===false?'selected':''}>No</option></select></div>
    <div class="form-group"><label>¿Te moviste al menos 30 min?</label><select id="ci-movement"><option value="">--</option><option value="1" ${log.core.movement?'selected':''}>Sí</option><option value="0" ${log.core.movement===false?'selected':''}>No</option></select></div>
    <div class="form-group"><label>Estado emocional (1-5)</label><input type="number" id="ci-emotion" value="${log.core.emotion||''}" min="1" max="5"></div>
    <div class="form-group"><label>¿Interacción social hoy?</label><select id="ci-social"><option value="">--</option><option value="1" ${log.core.social?'selected':''}>Sí</option><option value="0" ${log.core.social===false?'selected':''}>No</option></select></div>
    <div class="form-group"><label>Notas del día</label><textarea id="ci-notes">${log.notes||''}</textarea></div>
  `;
  const footer = '<button class="btn-primary" id="save-checkin">Guardar</button><button class="btn-secondary" id="cancel-checkin">Cancelar</button>';
  showModal('Check-in diario', body, footer);
  document.getElementById('save-checkin').onclick = () => {
    const core = {
      sleep: parseFloat(document.getElementById('ci-sleep').value) || null,
      nutrition: document.getElementById('ci-nutrition').value === '1' ? true : (document.getElementById('ci-nutrition').value === '0' ? false : null),
      movement: document.getElementById('ci-movement').value === '1' ? true : (document.getElementById('ci-movement').value === '0' ? false : null),
      emotion: parseInt(document.getElementById('ci-emotion').value) || null,
      social: document.getElementById('ci-social').value === '1' ? true : (document.getElementById('ci-social').value === '0' ? false : null)
    };
    log.core = core;
    log.notes = document.getElementById('ci-notes').value;
    Storage.addLog(today, log);
    const allOk = core.sleep>0 && core.nutrition===true && core.movement===true && core.emotion>=1 && core.social===true;
    updateCreditsOnCheckin(allOk);
    closeModal();
    renderHome();
    updateTopBar();
    showToast('Check-in guardado');
  };
  document.getElementById('cancel-checkin').onclick = closeModal;
}

function openAddHabitModal(section) {
  const body = `<input type="text" id="new-habit-name" placeholder="Nombre"><input type="number" id="new-habit-duration" placeholder="Duración (min)" min="1" value="15" style="margin-top:0.5rem">`;
  const footer = '<button class="btn-primary" id="save-habit">Guardar</button><button class="btn-secondary" id="cancel-habit">Cancelar</button>';
  showModal('Nuevo hábito', body, footer);
  document.getElementById('save-habit').onclick = () => {
    const name = document.getElementById('new-habit-name').value.trim();
    const duration = parseInt(document.getElementById('new-habit-duration').value) || 15;
    if (name) {
      const habits = Storage.getHabits();
      habits.push({ id: Date.now().toString(), name, section, duration, order: habits.filter(h => h.section === section).length });
      Storage.setHabits(habits);
      closeModal();
      renderHome();
    }
  };
  document.getElementById('cancel-habit').onclick = closeModal;
}

function showDaySummary(dateStr) {
  const log = Storage.getLogs()[dateStr];
  if (!log) { showToast('Sin datos para ese día'); return; }
  const core = log.core || {};
  const habits = log.habits || {};
  const allHabits = Storage.getHabits();
  const body = `
    <p><strong>Sueño:</strong> ${core.sleep ? core.sleep+'h' : '--'}</p>
    <p><strong>Nutrición:</strong> ${core.nutrition ? 'Sí' : 'No'}</p>
    <p><strong>Movimiento:</strong> ${core.movement ? 'Sí' : 'No'}</p>
    <p><strong>Emocional:</strong> ${core.emotion ? core.emotion+'/5' : '--'}</p>
    <p><strong>Social:</strong> ${core.social ? 'Sí' : 'No'}</p>
    <p><strong>Notas:</strong> ${log.notes || '--'}</p>
    <h4>Hábitos</h4>
    <ul>${allHabits.filter(h => habits[h.id]).map(h => `<li>${h.name}</li>`).join('') || '<li>Ninguno completado</li>'}</ul>
  `;
  showModal(dateStr, body, '<button class="btn-secondary" id="close-summary">Cerrar</button>');
  document.getElementById('close-summary').onclick = closeModal;
}

/* Swipe */
function addSwipeListeners(item, habitId) {
  let startX = 0;
  item.addEventListener('touchstart', (e) => { startX = e.touches[0].clientX; }, {passive: true});
  item.addEventListener('touchend', (e) => {
    const diff = e.changedTouches[0].clientX - startX;
    if (Math.abs(diff) > 60) {
      if (diff > 0) {
        openEditHabitModal(habitId);
      } else {
        // Usar modal de confirmación en vez de confirm nativo
        showModal('Eliminar hábito', '<p>¿Estás seguro de que querés eliminar este hábito?</p>',
          `<button class="btn-primary" id="confirm-delete">Sí, eliminar</button><button class="btn-secondary" id="cancel-delete">Cancelar</button>`);
        document.getElementById('confirm-delete').onclick = () => {
          const habits = Storage.getHabits().filter(h => h.id !== habitId);
          Storage.setHabits(habits);
          closeModal();
          renderHome();
        };
        document.getElementById('cancel-delete').onclick = closeModal;
      }
    }
  });
}

function openEditHabitModal(habitId) {
  const habits = Storage.getHabits();
  const habit = habits.find(h => h.id === habitId);
  if (!habit) return;
  const body = `
    <input type="text" id="edit-habit-name" value="${habit.name}">
    <input type="number" id="edit-habit-duration" value="${habit.duration || 15}" min="1" style="margin-top:0.5rem">
    <select id="edit-habit-section" style="margin-top:0.5rem">
      <option value="morning" ${habit.section==='morning'?'selected':''}>Mañana</option>
      <option value="afternoon" ${habit.section==='afternoon'?'selected':''}>Tarde</option>
      <option value="evening" ${habit.section==='evening'?'selected':''}>Noche</option>
    </select>
  `;
  const footer = '<button class="btn-primary" id="save-edit">Guardar</button><button class="btn-secondary" id="cancel-edit">Cancelar</button>';
  showModal('Editar hábito', body, footer);
  document.getElementById('save-edit').onclick = () => {
    habit.name = document.getElementById('edit-habit-name').value.trim();
    habit.duration = parseInt(document.getElementById('edit-habit-duration').value) || 15;
    habit.section = document.getElementById('edit-habit-section').value;
    Storage.setHabits(habits);
    closeModal();
    renderHome();
  };
  document.getElementById('cancel-edit').onclick = closeModal;
}

/* Drag & drop mejorado */
function enableDragDrop() {
  const items = document.querySelectorAll('.habit-item');
  items.forEach(item => {
    item.addEventListener('dragstart', handleDragStart);
    item.addEventListener('dragend', handleDragEnd);
  });

  const lists = document.querySelectorAll('.habit-list');
  lists.forEach(list => {
    list.addEventListener('dragover', handleDragOver);
    list.addEventListener('dragleave', handleDragLeave);
    list.addEventListener('drop', handleDrop);
  });
}

function handleDragStart(e) {
  draggedItem = this;
  draggedId = this.dataset.id;
  this.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', draggedId);
}

function handleDragEnd(e) {
  this.classList.remove('dragging');
  document.querySelectorAll('.habit-item').forEach(el => el.classList.remove('drag-over'));
  draggedItem = null;
  draggedId = null;
}

function handleDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  const list = this;
  const afterElement = getDragAfterElement(list, e.clientY);
  list.querySelectorAll('.habit-item').forEach(el => el.classList.remove('drag-over'));
  if (afterElement) {
    afterElement.classList.add('drag-over');
  }
}

function handleDragLeave(e) {
  this.querySelectorAll('.habit-item').forEach(el => el.classList.remove('drag-over'));
}

function handleDrop(e) {
  e.preventDefault();
  const list = this;
  const newSection = list.closest('.habit-section').dataset.section;
  const habits = Storage.getHabits();
  const habit = habits.find(h => h.id === draggedId);
  if (!habit) return;

  const afterElement = getDragAfterElement(list, e.clientY);
  // Actualizar sección si cambió
  if (habit.section !== newSection) {
    habit.section = newSection;
  }
  // Reordenar
  const sectionHabits = habits.filter(h => h.section === newSection).sort((a,b) => a.order - b.order);
  const oldIdx = sectionHabits.findIndex(h => h.id === habit.id);
  if (oldIdx !== -1) sectionHabits.splice(oldIdx, 1);
  
  if (afterElement) {
    const afterId = afterElement.dataset.id;
    const insertIdx = sectionHabits.findIndex(h => h.id === afterId);
    sectionHabits.splice(insertIdx !== -1 ? insertIdx : 0, 0, habit);
  } else {
    sectionHabits.push(habit);
  }
  // Reasignar órdenes
  sectionHabits.forEach((h, i) => { h.order = i; });
  // Ajustar órdenes en la sección anterior si cambió
  if (habit.section !== newSection) {
    const oldSectionHabits = habits.filter(h => h.section === habit.section).sort((a,b) => a.order - b.order);
    oldSectionHabits.forEach((h, i) => { h.order = i; });
  }
  Storage.setHabits(habits);
  renderHome();
}

function getDragAfterElement(container, y) {
  const draggableElements = [...container.querySelectorAll('.habit-item:not(.dragging)')];
  return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect();
    const offset = y - box.top - box.height / 2;
    if (offset < 0 && offset > closest.offset) {
      return { offset: offset, element: child };
    } else {
      return closest;
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element;
}
"""

# ==================== js/components/development.js ====================
FILES["js/components/development.js"] = r"""import { renderStudies } from './studies.js';
import { renderTraining } from './training.js';

export function renderDevelopment() {
  const vp = document.getElementById('viewport');
  vp.innerHTML = `
    <div style="display:flex; gap:1rem; margin-top:2rem;">
      <button class="btn-primary full-width" id="btn-studies">Estudios</button>
      <button class="btn-primary full-width" id="btn-training">Entrenamientos</button>
    </div>
    <div id="dev-content"></div>
  `;
  document.getElementById('btn-studies').addEventListener('click', () => {
    renderStudies(document.getElementById('dev-content'));
  });
  document.getElementById('btn-training').addEventListener('click', () => {
    renderTraining(document.getElementById('dev-content'));
  });
  renderStudies(document.getElementById('dev-content'));
}
"""

# ==================== js/components/studies.js (sin prompts) ====================
FILES["js/components/studies.js"] = r"""import { Storage } from '../storage.js';
import { todayStr, calculateBasal, spendCredit } from '../state.js';
import { showModal, closeModal, showToast } from '../ui.js';

let currentAreaId = null;
let timerInterval = null;

export function renderStudies(container) {
  const areas = Storage.getAreas().filter(a => a.type === 'study');
  container.innerHTML = `
    <h3>Áreas de estudio</h3>
    <div id="areas-list">${areas.map(a => `<div class="card" style="margin:0.5rem 0; cursor:pointer" data-area-id="${a.id}"><strong>${a.name}</strong><div style="font-size:0.7rem; color:var(--text-secondary);">${a.documents?.length||0} docs · ${a.videos?.length||0} videos</div></div>`).join('')}</div>
    <button class="btn-secondary full-width" id="btn-add-area">+ Nueva área</button>
    <div id="area-detail" style="margin-top:1rem;"></div>
  `;

  document.querySelectorAll('#areas-list .card').forEach(card => {
    card.addEventListener('click', () => showAreaDetail(card.dataset.areaId));
  });
  document.getElementById('btn-add-area').addEventListener('click', () => {
    showModal('Nueva área de estudio', `<input type="text" id="new-area-name" placeholder="Nombre">`, 
      '<button class="btn-primary" id="create-area">Crear</button><button class="btn-secondary" id="cancel-area">Cancelar</button>');
    document.getElementById('create-area').onclick = () => {
      const name = document.getElementById('new-area-name').value.trim();
      if (name) {
        const areas = Storage.getAreas();
        areas.push({ id: Date.now().toString(), name, type: 'study', documents: [], videos: [], supportText: '' });
        Storage.setAreas(areas);
        closeModal();
        renderStudies(container);
      }
    };
    document.getElementById('cancel-area').onclick = closeModal;
  });
}

function showAreaDetail(areaId) {
  currentAreaId = areaId;
  const area = Storage.getAreas().find(a => a.id === areaId);
  if (!area) return;
  const detailDiv = document.getElementById('area-detail');
  detailDiv.innerHTML = `
    <h4>${area.name}</h4>
    <div class="tab-bar">
      <button class="tab-btn active" data-tab="focus">Enfoque</button>
      <button class="tab-btn" data-tab="documents">Documentos</button>
      <button class="tab-btn" data-tab="videos">Videos</button>
      <button class="tab-btn" data-tab="notes">Anotaciones</button>
    </div>
    <div id="tab-content"></div>
  `;

  detailDiv.querySelectorAll('.tab-btn').forEach(tab => {
    tab.addEventListener('click', () => {
      detailDiv.querySelectorAll('.tab-btn').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      loadTabContent(tab.dataset.tab, area);
    });
  });
  loadTabContent('focus', area);
}

function loadTabContent(tabName, area) {
  const contentDiv = document.getElementById('tab-content');
  switch(tabName) {
    case 'focus':
      contentDiv.innerHTML = `
        <p>Método de temporización:</p>
        <select id="timer-method"><option value="pomodoro">Pomodoro (25/5)</option><option value="flow">Ultradiano (50-90)</option></select>
        <input type="text" id="focus-goal" placeholder="Entregable concreto de hoy" style="margin-top:0.5rem">
        <button class="btn-primary full-width" id="start-session-btn">Iniciar Sesión</button>
        <div id="timer-display" class="timer-display hidden"></div>
        <button class="btn-secondary full-width hidden" id="stop-timer-btn">Finalizar</button>
      `;
      document.getElementById('start-session-btn').addEventListener('click', () => startStudySession(area));
      break;
    case 'documents':
      contentDiv.innerHTML = `
        <div id="docs-list">${(area.documents||[]).map((d,i) => `<div class="card"><a href="${d.url}" target="_blank">${d.title}</a><button class="btn-secondary remove-doc" data-index="${i}" style="float:right">X</button></div>`).join('')}</div>
        <button class="btn-secondary full-width" id="add-doc-btn">+ Agregar documento</button>
      `;
      document.getElementById('add-doc-btn').addEventListener('click', () => {
        showModal('Agregar documento', `<input type="text" id="doc-title" placeholder="Título"><input type="text" id="doc-url" placeholder="URL" style="margin-top:0.5rem">`,
          '<button class="btn-primary" id="save-doc">Guardar</button><button class="btn-secondary" id="cancel-doc">Cancelar</button>');
        document.getElementById('save-doc').onclick = () => {
          const title = document.getElementById('doc-title').value.trim();
          const url = document.getElementById('doc-url').value.trim();
          if (title && url) {
            area.documents = area.documents || [];
            area.documents.push({ title, url });
            Storage.setAreas(Storage.getAreas().map(a => a.id === area.id ? area : a));
            closeModal();
            loadTabContent('documents', area);
          }
        };
        document.getElementById('cancel-doc').onclick = closeModal;
      });
      document.querySelectorAll('.remove-doc').forEach(btn => {
        btn.addEventListener('click', () => {
          const idx = parseInt(btn.dataset.index);
          area.documents.splice(idx, 1);
          Storage.setAreas(Storage.getAreas().map(a => a.id === area.id ? area : a));
          loadTabContent('documents', area);
        });
      });
      break;
    case 'videos':
      contentDiv.innerHTML = `
        <div id="videos-list">${(area.videos||[]).map((v,i) => `<div class="card"><strong>${v.title}</strong><button class="btn-secondary view-video" data-url="${v.url}">Ver</button></div>`).join('')}</div>
        <button class="btn-secondary full-width" id="add-video-btn">+ Agregar video</button>
        <div id="video-player" class="hidden" style="margin-top:1rem;"></div>
      `;
      document.getElementById('add-video-btn').addEventListener('click', () => {
        showModal('Agregar video', `<input type="text" id="video-title" placeholder="Título"><input type="text" id="video-url" placeholder="URL de YouTube" style="margin-top:0.5rem">`,
          '<button class="btn-primary" id="save-video">Guardar</button><button class="btn-secondary" id="cancel-video">Cancelar</button>');
        document.getElementById('save-video').onclick = () => {
          const title = document.getElementById('video-title').value.trim();
          const url = document.getElementById('video-url').value.trim();
          if (title && url) {
            area.videos = area.videos || [];
            area.videos.push({ title, url });
            Storage.setAreas(Storage.getAreas().map(a => a.id === area.id ? area : a));
            closeModal();
            loadTabContent('videos', area);
          }
        };
        document.getElementById('cancel-video').onclick = closeModal;
      });
      document.querySelectorAll('.view-video').forEach(btn => {
        btn.addEventListener('click', () => {
          const url = btn.dataset.url;
          const player = document.getElementById('video-player');
          player.innerHTML = `<iframe src="${url.replace('watch?v=','embed/')}" frameborder="0" allowfullscreen style="width:100%; height:200px;"></iframe>`;
          player.classList.remove('hidden');
        });
      });
      break;
    case 'notes':
      contentDiv.innerHTML = `
        <textarea id="support-text" rows="6">${area.supportText || ''}</textarea>
        <button class="btn-primary full-width" id="save-support-text">Guardar anotaciones</button>
      `;
      document.getElementById('save-support-text').addEventListener('click', () => {
        area.supportText = document.getElementById('support-text').value;
        Storage.setAreas(Storage.getAreas().map(a => a.id === area.id ? area : a));
        showToast('Anotaciones guardadas');
      });
      break;
  }
}

function startStudySession(area) {
  const basal = calculateBasal();
  if (basal.mode === 'red') { showToast('No disponible en Protección'); return; }
  if (Storage.getCredits() === 0) { showToast('Necesitás 1 crédito'); return; }
  showModal('Iniciar sesión', '<p>¿Gastar 1 crédito para comenzar?</p>',
    '<button class="btn-primary" id="confirm-session">Sí</button><button class="btn-secondary" id="cancel-session">Cancelar</button>');
  document.getElementById('confirm-session').onclick = () => {
    closeModal();
    spendCredit();
    const method = document.getElementById('timer-method').value;
    const minutes = method === 'pomodoro' ? 25 : 50;
    let remaining = minutes * 60;
    const timerDiv = document.getElementById('timer-display');
    const stopBtn = document.getElementById('stop-timer-btn');
    const startBtn = document.getElementById('start-session-btn');
    timerDiv.classList.remove('hidden');
    stopBtn.classList.remove('hidden');
    startBtn.classList.add('hidden');
    timerInterval = setInterval(() => {
      const mins = Math.floor(remaining / 60);
      const secs = remaining % 60;
      timerDiv.textContent = `${mins}:${secs.toString().padStart(2,'0')}`;
      remaining--;
      if (remaining < 0) {
        clearInterval(timerInterval);
        finishSession(area, minutes);
      }
    }, 1000);
    stopBtn.addEventListener('click', () => {
      clearInterval(timerInterval);
      finishSession(area, Math.round((minutes * 60 - remaining) / 60));
    });
  };
  document.getElementById('cancel-session').onclick = closeModal;
}

function finishSession(area, duration) {
  showModal('Sesión finalizada', `<input type="number" id="session-intensity" placeholder="Intensidad (1-10)" min="1" max="10" value="7"><textarea id="session-notes" placeholder="Notas" style="margin-top:0.5rem;"></textarea>`,
    '<button class="btn-primary" id="save-session-data">Guardar</button>');
  document.getElementById('save-session-data').onclick = () => {
    const intensity = parseInt(document.getElementById('session-intensity').value) || 7;
    const notes = document.getElementById('session-notes').value;
    Storage.addExploit({ areaId: area.id, date: todayStr(), duration, intensity, notes });
    closeModal();
    showToast('Sesión guardada');
    renderStudies(document.getElementById('dev-content'));
  };
}
"""

# ==================== js/components/training.js (sin prompts) ====================
FILES["js/components/training.js"] = r"""import { Storage } from '../storage.js';
import { todayStr, calculateBasal, spendCredit } from '../state.js';
import { showModal, closeModal, showToast } from '../ui.js';

export function renderTraining(container) {
  const routines = Storage.getRoutines();
  container.innerHTML = `
    <h3>Rutinas</h3>
    <div id="routines-list">${routines.map(r => `<div class="card" data-routine-id="${r.id}" style="cursor:pointer; margin:0.5rem 0;">${r.name}</div>`).join('')}</div>
    <button class="btn-secondary full-width" id="btn-new-routine">+ Nueva rutina</button>
    <div id="routine-detail"></div>
  `;
  document.querySelectorAll('#routines-list .card').forEach(card => {
    card.addEventListener('click', () => showRoutineDetail(card.dataset.routineId));
  });
  document.getElementById('btn-new-routine').addEventListener('click', openNewRoutineModal);
}

function openNewRoutineModal() {
  showModal('Nueva rutina', '<input type="text" id="routine-name" placeholder="Nombre">',
    '<button class="btn-primary" id="create-routine">Crear</button><button class="btn-secondary" id="cancel-routine">Cancelar</button>');
  document.getElementById('create-routine').onclick = () => {
    const name = document.getElementById('routine-name').value.trim();
    if (name) {
      const routines = Storage.getRoutines();
      routines.push({ id: Date.now().toString(), name, exercises: [] });
      Storage.setRoutines(routines);
      closeModal();
      renderTraining(document.getElementById('dev-content'));
    }
  };
  document.getElementById('cancel-routine').onclick = closeModal;
}

function showRoutineDetail(routineId) {
  const routine = Storage.getRoutines().find(r => r.id === routineId);
  if (!routine) return;
  const detailDiv = document.getElementById('routine-detail');
  detailDiv.innerHTML = `
    <h4>${routine.name}</h4>
    <div id="exercises-list">${routine.exercises.map((e,i) => `<div class="card" style="margin:0.3rem 0;"><strong>${e.name}</strong> ${e.sets}x${e.reps} ${e.weight?e.weight+'kg':''}</div>`).join('')}</div>
    <button class="btn-secondary full-width" id="btn-add-exercise">+ Agregar ejercicio</button>
    <button class="btn-primary full-width" id="btn-start-routine">Iniciar rutina</button>
  `;
  document.getElementById('btn-add-exercise').addEventListener('click', () => addExercise(routine));
  document.getElementById('btn-start-routine').addEventListener('click', () => startRoutine(routine));
}

function addExercise(routine) {
  showModal('Nuevo ejercicio', `
    <input type="text" id="ex-name" placeholder="Nombre">
    <input type="number" id="ex-sets" placeholder="Series" value="3" min="1" style="margin-top:0.5rem">
    <input type="number" id="ex-reps" placeholder="Repeticiones" value="10" min="1" style="margin-top:0.5rem">
    <input type="number" id="ex-weight" placeholder="Peso (kg, opcional)" value="0" style="margin-top:0.5rem">
  `, '<button class="btn-primary" id="save-exercise">Agregar</button><button class="btn-secondary" id="cancel-exercise">Cancelar</button>');
  document.getElementById('save-exercise').onclick = () => {
    const name = document.getElementById('ex-name').value.trim();
    if (!name) return;
    const sets = parseInt(document.getElementById('ex-sets').value) || 3;
    const reps = parseInt(document.getElementById('ex-reps').value) || 10;
    const weight = parseInt(document.getElementById('ex-weight').value) || 0;
    routine.exercises.push({ name, sets, reps, weight });
    Storage.setRoutines(Storage.getRoutines().map(r => r.id === routine.id ? routine : r));
    closeModal();
    showRoutineDetail(routine.id);
  };
  document.getElementById('cancel-exercise').onclick = closeModal;
}

function startRoutine(routine) {
  const basal = calculateBasal();
  if (basal.mode === 'red') { showToast('No disponible en Protección'); return; }
  if (Storage.getCredits() === 0) { showToast('Necesitás 1 crédito'); return; }
  showModal('Iniciar rutina', '<p>¿Gastar 1 crédito para comenzar?</p>',
    '<button class="btn-primary" id="confirm-routine">Sí</button><button class="btn-secondary" id="cancel-routine-start">Cancelar</button>');
  document.getElementById('confirm-routine').onclick = () => {
    closeModal();
    spendCredit();
    const detailDiv = document.getElementById('routine-detail');
    let html = `<h4>${routine.name} - En progreso</h4>`;
    routine.exercises.forEach((ex, i) => {
      html += `<div class="card" id="ex-${i}" style="margin:0.5rem 0;">
        <div><strong>${ex.name}</strong> ${ex.sets}x${ex.reps} ${ex.weight?ex.weight+'kg':''}</div>
        <div id="ex-${i}-sets" class="sets"></div>
        <button class="btn-secondary" data-ex-id="${i}" onclick="completeSet(${i}, ${ex.sets})">+1 set</button>
      </div>`;
    });
    html += '<button class="btn-primary full-width" id="finish-routine">Finalizar rutina</button>';
    detailDiv.innerHTML = html;
    window.completeSet = function(exIdx, totalSets) {
      const setDiv = document.getElementById(`ex-${exIdx}-sets`);
      const current = setDiv.children.length;
      if (current < totalSets) {
        setDiv.innerHTML += '<span class="dot" style="background:var(--green)"></span> ';
        if (current === totalSets - 1) {
          document.querySelector(`[data-ex-id="${exIdx}"]`).disabled = true;
        }
      }
    };
    document.getElementById('finish-routine').addEventListener('click', () => {
      showModal('Rutina completada', '<input type="number" id="routine-intensity" placeholder="Intensidad (1-10)" min="1" max="10" value="7"><textarea id="routine-notes" placeholder="Notas" style="margin-top:0.5rem;"></textarea>',
        '<button class="btn-primary" id="save-routine-data">Guardar</button>');
      document.getElementById('save-routine-data').onclick = () => {
        const intensity = parseInt(document.getElementById('routine-intensity').value) || 7;
        const notes = document.getElementById('routine-notes').value;
        Storage.addExploit({ areaId: routine.id, date: todayStr(), duration: 0, intensity, notes });
        closeModal();
        showToast('Rutina completada');
        renderTraining(document.getElementById('dev-content'));
      };
    });
  };
  document.getElementById('cancel-routine-start').onclick = closeModal;
}
"""

# ==================== js/components/analysis.js ====================
FILES["js/components/analysis.js"] = r"""import { Storage } from '../storage.js';
import { calculateBasal } from '../state.js';
let chart;
export function renderAnalysis() {
  const logs = Storage.getLogs();
  const exploitLog = Storage.getExploitLog();
  const studyAreas = Storage.getAreas().filter(a => a.type === 'study');
  const trainingAreas = Storage.getAreas().filter(a => a.type === 'training');
  const totalStudyHours = Math.round(exploitLog.filter(e => studyAreas.some(a => a.id === e.areaId)).reduce((s,e) => s + e.duration, 0) / 60);
  const totalTrainingCount = exploitLog.filter(e => trainingAreas.some(a => a.id === e.areaId)).length;

  document.getElementById('viewport').innerHTML = `
    <div class="accumulator">
      <div class="accumulator-card"><div class="accumulator-value">${totalStudyHours}h</div><div class="accumulator-label">Horas de estudio</div></div>
      <div class="accumulator-card"><div class="accumulator-value">${totalTrainingCount}</div><div class="accumulator-label">Entrenamientos</div></div>
    </div>
    <div style="display:flex; gap:0.5rem; margin:0.8rem 0;">
      <button class="btn-secondary period-btn active" data-months="3">3M</button>
      <button class="btn-secondary period-btn" data-months="6">6M</button>
      <button class="btn-secondary period-btn" data-months="12">12M</button>
    </div>
    <div class="chart-container"><canvas id="basal-chart"></canvas></div>
    <div id="stats-text" class="card"></div>
    <button class="btn-secondary full-width" id="export-btn">Exportar datos</button>
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
  const labels = dates.map(d => d.slice(5));
  if (chart) chart.destroy();
  // Suavizado media móvil 7 días
  const smoothed = [];
  for (let i = 0; i < scores.length; i++) {
    let count = 0, sum = 0;
    for (let j = Math.max(0, i-3); j <= Math.min(scores.length-1, i+3); j++) {
      if (scores[j] !== null) { sum += scores[j]; count++; }
    }
    smoothed.push(count > 0 ? Math.round(sum/count) : null);
  }
  chart = new Chart(document.getElementById('basal-chart').getContext('2d'), {
    type: 'line',
    data: { labels, datasets: [{ label: 'Estado Basal (suavizado)', data: smoothed, borderColor: '#5c8aff', tension: 0.4, pointRadius: 0 }] },
    options: { scales: { y: { min:0, max:100 } } }
  });
  const valid = scores.filter(s => s !== null);
  const avg = valid.length ? Math.round(valid.reduce((a,b)=>a+b,0)/valid.length) : '--';
  document.getElementById('stats-text').innerHTML = `<strong>Promedio (${months}M):</strong> ${avg}/100`;
}
"""

# ==================== js/components/emergency.js ====================
FILES["js/components/emergency.js"] = r"""import { Storage } from '../storage.js';
import { todayStr } from '../state.js';
export function renderEmergency() {
  const config = Storage.getConfig();
  const checklist = config.emergencyChecklist;
  const today = todayStr();
  const log = Storage.getLogs()[today] || {};
  const completed = log.checklist || [];
  document.getElementById('viewport').innerHTML = `
    <h3>Protocolo de Emergencia</h3>
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
"""

# ==================== js/components/config.js ====================
FILES["js/components/config.js"] = r"""import { Storage } from '../storage.js';
import { showModal, closeModal, showToast } from '../ui.js';
export function openConfigModal() {
  const config = Storage.getConfig();
  const body = `
    <div class="form-group"><label>PIN</label><input type="password" id="cfg-pin" value="${config.pin}"></div>
    <div class="form-group"><label>Mensaje de apoyo</label><textarea id="cfg-support">${config.supportMessage}</textarea></div>
    <div class="form-group"><label>Checklist de emergencia (uno por línea)</label><textarea id="cfg-checklist" rows="5">${config.emergencyChecklist.join('\n')}</textarea></div>`;
  const footer = '<button class="btn-primary" id="save-config-btn">Guardar</button><button class="btn-secondary" id="cancel-config-btn">Cancelar</button>';
  showModal('Configuración', body, footer);
  document.getElementById('save-config-btn').onclick = () => {
    config.pin = document.getElementById('cfg-pin').value || '2207';
    config.supportMessage = document.getElementById('cfg-support').value;
    config.emergencyChecklist = document.getElementById('cfg-checklist').value.split('\n').filter(l => l.trim());
    Storage.setConfig(config);
    closeModal();
    showToast('Configuración guardada');
  };
  document.getElementById('cancel-config-btn').onclick = closeModal;
}
"""

# Crear carpetas y archivos
for d in DIRS:
    os.makedirs(d, exist_ok=True)

for path, content in FILES.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ {path}")

print("\n✅ Proyecto MentalOS regenerado completamente.")