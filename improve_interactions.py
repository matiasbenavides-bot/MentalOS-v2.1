#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MentalOS - Mejora de interactividad: drag & drop intra-sección, sin prompts nativos."""

import os

# Asegurar carpetas
os.makedirs("js/components", exist_ok=True)

files = {}

# ==================== js/components/home.js (mejorado) ====================
files["js/components/home.js"] = r"""import { Storage } from '../storage.js';
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
  // Remove previous drag-over
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
  // Mover a nueva sección si es distinta
  if (habit.section !== newSection) {
    habit.section = newSection;
  }
  // Reordenar dentro de la lista
  if (afterElement) {
    const afterId = afterElement.dataset.id;
    const afterHabit = habits.find(h => h.id === afterId);
    const targetOrder = afterHabit.order || 0;
    // Reasignar órdenes en la sección destino
    const sectionHabits = habits.filter(h => h.section === newSection).sort((a,b) => a.order - b.order);
    // Remover habit actual
    const idx = sectionHabits.findIndex(h => h.id === habit.id);
    if (idx !== -1) sectionHabits.splice(idx, 1);
    // Insertar después del elemento de referencia
    const insertIdx = sectionHabits.findIndex(h => h.id === afterId);
    sectionHabits.splice(insertIdx !== -1 ? insertIdx : 0, 0, habit);
    // Reasignar órdenes
    sectionHabits.forEach((h, i) => { h.order = i; });
    // Actualizar otros si vienen de otra sección
    if (habit.section !== newSection) {
      // Limpiar orden en sección anterior
      const oldSectionHabits = habits.filter(h => h.section === habit.section && h.id !== habit.id).sort((a,b) => a.order - b.order);
      oldSectionHabits.forEach((h, i) => { h.order = i; });
    }
  } else {
    // Soltar al final de la lista
    const sectionHabits = habits.filter(h => h.section === newSection).sort((a,b) => a.order - b.order);
    const idx = sectionHabits.findIndex(h => h.id === habit.id);
    if (idx !== -1) sectionHabits.splice(idx, 1);
    sectionHabits.push(habit);
    sectionHabits.forEach((h, i) => { h.order = i; });
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

# ==================== js/components/studies.js (sin prompts) ====================
files["js/components/studies.js"] = r"""import { Storage } from '../storage.js';
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
      // Remove doc buttons
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
      // View video buttons
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
files["js/components/training.js"] = r"""import { Storage } from '../storage.js';
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

# Escribir archivos
for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ {path}")

print("\n✅ Interactividad mejorada: drag & drop intra-sección, sin prompts nativos.")