import { Storage } from '../storage.js';
import { todayStr, updateCreditsOnCheckin } from '../state.js';
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
      if (core && (id === 'sleep' || id === 'emotional')) showCoreInputModal(id);
      else if (core) toggleCoreHabit(id);
      else toggleCustomHabit(id);
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

function openAddHabitModal() {
  const body = `<input type="text" id="new-habit-name" placeholder="Nombre del hábito"><input type="text" id="new-habit-icon" placeholder="Icono (emoji)" style="margin-top:0.5rem">`;
  const footer = `<button class="btn-primary" id="save-habit-btn">Guardar</button><button class="btn-secondary" id="cancel-habit-btn">Cancelar</button>`;
  showModal('➕ Nuevo hábito', body, footer);
  document.getElementById('save-habit-btn').onclick = () => {
    const name = document.getElementById('new-habit-name').value.trim();
    const icon = document.getElementById('new-habit-icon').value || '✅';
    if (name) { const habits = Storage.getHabits(); habits.push({ id: Date.now().toString(), name, icon }); Storage.setHabits(habits); closeModal(); renderHome(); }
  };
  document.getElementById('cancel-habit-btn').onclick = closeModal;
}
