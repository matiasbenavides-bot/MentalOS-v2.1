import { Storage } from '../storage.js';
import { todayStr, calculateBasal, updateCreditsOnCheckin } from '../state.js';
import { showModal, closeModal, showToast } from '../ui.js';
import { updateTopBar } from '../app.js';

export function renderHome() {
  const vp = document.getElementById('viewport');
  const today = todayStr();
  const logs = Storage.getLogs();
  const todayLog = logs[today] || { core: {}, habits: {} };
  const habits = Storage.getHabits().sort((a,b) => (a.order||0) - (b.order||0));

  // Core chips (sin emojis)
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

  // Secciones de hábitos
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
          return `<div class="habit-item ${done ? 'completed' : ''}" data-id="${h.id}" draggable="false">
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
      if (e.target.closest('.swipe-delete') || e.target.closest('.swipe-edit')) return;
      toggleCustomHabit(habitId);
    });
    // Swipe
    addSwipeListeners(item, habitId);
  });

  document.querySelectorAll('.btn-add-habit').forEach(btn => {
    btn.addEventListener('click', () => openAddHabitModal(btn.dataset.section));
  });

  document.querySelectorAll('.calendar-day').forEach(day => {
    day.addEventListener('click', () => showDaySummary(day.dataset.date));
  });

  document.getElementById('open-checkin-btn').onclick = openCheckinModal;

  // Drag and drop (long press)
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

/* Swipe handlers */
function addSwipeListeners(item, habitId) {
  let startX = 0;
  item.addEventListener('touchstart', (e) => { startX = e.touches[0].clientX; });
  item.addEventListener('touchend', (e) => {
    const diff = e.changedTouches[0].clientX - startX;
    if (Math.abs(diff) > 60) {
      if (diff > 0) { // Swipe right: edit
        openEditHabitModal(habitId);
      } else { // Swipe left: delete
        if (confirm('¿Eliminar hábito?')) {
          const habits = Storage.getHabits().filter(h => h.id !== habitId);
          Storage.setHabits(habits);
          renderHome();
        }
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

/* Drag and drop básico (long press) */
function enableDragDrop() {
  const lists = document.querySelectorAll('.habit-list');
  lists.forEach(list => {
    list.addEventListener('dragover', e => e.preventDefault());
    list.addEventListener('drop', e => {
      e.preventDefault();
      const draggedId = e.dataTransfer.getData('text/plain');
      const draggedEl = document.querySelector(`.habit-item[data-id="${draggedId}"]`);
      if (draggedEl && list !== draggedEl.parentNode) {
        const newSection = list.closest('.habit-section').dataset.section;
        const habits = Storage.getHabits();
        const habit = habits.find(h => h.id === draggedId);
        if (habit) {
          habit.section = newSection;
          habit.order = list.children.length;
          Storage.setHabits(habits);
          renderHome();
        }
      }
    });
    list.querySelectorAll('.habit-item').forEach(item => {
      item.addEventListener('dragstart', e => {
        e.dataTransfer.setData('text/plain', item.dataset.id);
        item.classList.add('dragging');
      });
      item.addEventListener('dragend', () => {
        item.classList.remove('dragging');
      });
      item.setAttribute('draggable', 'true');
    });
  });
}
