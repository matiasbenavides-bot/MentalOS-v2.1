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

  // Core rápido
  const coreItems = [
    { id: 'sleep', name: 'Sueño', icon: '😴', value: todayLog.core.sleep, format: v => v != null ? v + 'h' : '—' },
    { id: 'nutrition', name: 'Nutrición', icon: '🍽️', value: todayLog.core.nutrition, format: v => v ? '✓' : '✗' },
    { id: 'movement', name: 'Movimiento', icon: '🚶', value: todayLog.core.movement, format: v => v ? '✓' : '✗' },
    { id: 'emotional', name: 'Emocional', icon: '🧠', value: todayLog.core.emotional, format: v => v != null ? v + '/5' : '—' },
    { id: 'social', name: 'Social', icon: '💬', value: todayLog.core.social, format: v => v ? '✓' : '✗' }
  ];

  let html = `<div class="core-quick-panel">`;
  coreItems.forEach(item => {
    html += `<button class="core-chip" data-core-id="${item.id}">
      <span class="chip-icon">${item.icon}</span>
      <span class="chip-value">${item.format(item.value)}</span>
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
    html += `<div class="habit-section" data-section="${sec.key}">
      <h3 class="section-title">${sec.title}</h3>
      <div class="habit-list">
        ${habitsInSection.map(h => {
          const completed = todayLog.habits?.[h.id] === true;
          return `<div class="habit-item ${completed ? 'completed' : ''}" data-habit-id="${h.id}">
            <div class="habit-checkbox"></div>
            <div class="habit-info">
              <span class="habit-name">${h.icon ? h.icon + ' ' : ''}${h.name}</span>
              <span class="habit-duration">${h.duration ? h.duration + ' min' : ''}</span>
            </div>
            <div class="habit-actions">
              <button class="edit-habit-btn" data-id="${h.id}" title="Editar">✎</button>
              <button class="delete-habit-btn" data-id="${h.id}" title="Eliminar">🗑</button>
            </div>
          </div>`;
        }).join('')}
        <button class="btn-add-habit" data-section="${sec.key}">+ Agregar hábito</button>
      </div>
    </div>`;
  });

  html += `<button class="btn-primary full-width" id="open-checkin-btn" style="margin-top:0.5rem;">🌙 Cerrar día (Check-in)</button>`;
  vp.innerHTML = html;

  // Eventos Core
  document.querySelectorAll('.core-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const id = chip.dataset.coreId;
      if (id === 'sleep' || id === 'emotional') showCoreInputModal(id);
      else toggleCoreHabit(id);
    });
  });

  // Toggle hábito (check)
  document.querySelectorAll('.habit-item').forEach(item => {
    item.addEventListener('click', (e) => {
      // No activar si se clickeó en los botones de acción
      if (e.target.closest('.edit-habit-btn') || e.target.closest('.delete-habit-btn')) return;
      toggleCustomHabit(item.dataset.habitId);
    });
  });

  // Botones editar
  document.querySelectorAll('.edit-habit-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      openEditHabitModal(btn.dataset.id);
    });
  });

  // Botones eliminar
  document.querySelectorAll('.delete-habit-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      deleteHabit(btn.dataset.id);
    });
  });

  // Agregar hábito
  document.querySelectorAll('.btn-add-habit').forEach(btn => {
    btn.addEventListener('click', () => openAddHabitModal(btn.dataset.section));
  });

  document.getElementById('open-checkin-btn').onclick = openCheckinModal;
}

/* Funciones auxiliares */
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

/* --- CRUD Hábitos --- */
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

function openEditHabitModal(habitId) {
  const habits = Storage.getHabits();
  const habit = habits.find(h => h.id === habitId);
  if (!habit) return;
  const body = `
    <input type="text" id="edit-habit-name" value="${habit.name}">
    <input type="text" id="edit-habit-icon" value="${habit.icon || ''}" placeholder="Icono (emoji)" style="margin-top:0.5rem">
    <div class="form-group" style="margin-top:0.5rem"><label>Duración (minutos)</label><input type="number" id="edit-habit-duration" value="${habit.duration || 15}" min="1"></div>
    <div class="form-group"><label>Sección</label><select id="edit-habit-section">
      <option value="morning" ${habit.section === 'morning' ? 'selected' : ''}>Mañana</option>
      <option value="afternoon" ${habit.section === 'afternoon' ? 'selected' : ''}>Tarde</option>
      <option value="evening" ${habit.section === 'evening' ? 'selected' : ''}>Noche</option>
    </select></div>
  `;
  const footer = `<button class="btn-primary" id="save-edit-btn">Guardar cambios</button><button class="btn-secondary" id="cancel-edit-btn">Cancelar</button>`;
  showModal('✎ Editar hábito', body, footer);
  document.getElementById('save-edit-btn').onclick = () => {
    habit.name = document.getElementById('edit-habit-name').value.trim();
    habit.icon = document.getElementById('edit-habit-icon').value || '✅';
    habit.duration = parseInt(document.getElementById('edit-habit-duration').value) || 15;
    habit.section = document.getElementById('edit-habit-section').value;
    Storage.setHabits(habits);
    closeModal();
    renderHome();
  };
  document.getElementById('cancel-edit-btn').onclick = closeModal;
}

function deleteHabit(habitId) {
  if (!confirm('¿Eliminar este hábito?')) return;
  let habits = Storage.getHabits();
  habits = habits.filter(h => h.id !== habitId);
  Storage.setHabits(habits);
  renderHome();
}
