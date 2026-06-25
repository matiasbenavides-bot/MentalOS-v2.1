// Home view: habits grid + check-in
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
