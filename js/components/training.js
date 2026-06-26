import { Storage } from '../storage.js';
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
