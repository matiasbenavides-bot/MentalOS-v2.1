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
  const body = `<input type="text" id="routine-name" placeholder="Nombre de la rutina">`;
  const footer = '<button class="btn-primary" id="create-routine">Crear</button>';
  showModal('Nueva rutina', body, footer);
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
  const name = prompt('Nombre del ejercicio:');
  if (!name) return;
  const sets = parseInt(prompt('Series:')) || 3;
  const reps = parseInt(prompt('Repeticiones:')) || 10;
  const weight = parseInt(prompt('Peso (kg, opcional):')) || 0;
  routine.exercises.push({ name, sets, reps, weight });
  Storage.setRoutines(Storage.getRoutines().map(r => r.id === routine.id ? routine : r));
  showRoutineDetail(routine.id);
}

function startRoutine(routine) {
  const basal = calculateBasal();
  if (basal.mode === 'red') { showToast('No disponible en Protección'); return; }
  if (Storage.getCredits() === 0) { showToast('Necesitás 1 crédito'); return; }
  if (!confirm('Gastar 1 crédito para iniciar rutina?')) return;
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
    const notes = prompt('Notas de la sesión:');
    Storage.addExploit({ areaId: routine.id, date: todayStr(), duration: 0, intensity: parseInt(prompt('Intensidad (1-10):','7'))||7, notes });
    showToast('Rutina completada');
    renderTraining(document.getElementById('dev-content'));
  });
}
