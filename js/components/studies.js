import { Storage } from '../storage.js';
import { todayStr, calculateBasal, spendCredit } from '../state.js';
import { showModal, closeModal, showToast } from '../ui.js';

let currentAreaId = null;
let timerInterval = null;

export function renderStudies(container) {
  const areas = Storage.getAreas().filter(a => a.type === 'study');
  container.innerHTML = `
    <h3>Ãreas de estudio</h3>
    <div id="areas-list">${areas.map(a => `<div class="card" style="margin:0.5rem 0; cursor:pointer" data-area-id="${a.id}"><strong>${a.name}</strong><div style="font-size:0.7rem; color:var(--text-secondary);">${a.documents?.length||0} docs Â· ${a.videos?.length||0} videos</div></div>`).join('')}</div>
    <button class="btn-secondary full-width" id="btn-add-area">+ Nueva Ã¡rea</button>
    <div id="area-detail" style="margin-top:1rem;"></div>
  `;

  document.querySelectorAll('#areas-list .card').forEach(card => {
    card.addEventListener('click', () => showAreaDetail(card.dataset.areaId));
  });
  document.getElementById('btn-add-area').addEventListener('click', () => {
    const name = prompt('Nombre del Ã¡rea de estudio:');
    if (name) {
      const areas = Storage.getAreas();
      areas.push({ id: Date.now().toString(), name, type: 'study', documents: [], videos: [], supportText: '' });
      Storage.setAreas(areas);
      renderStudies(container);
    }
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

  const tabs = detailDiv.querySelectorAll('.tab-btn');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
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
        <p>MÃ©todo de temporizaciÃ³n:</p>
        <select id="timer-method"><option value="pomodoro">Pomodoro (25/5)</option><option value="flow">Ultradiano (50-90)</option></select>
        <input type="text" id="focus-goal" placeholder="Entregable concreto de hoy" style="margin-top:0.5rem">
        <button class="btn-primary full-width" id="start-session-btn">Iniciar SesiÃ³n</button>
        <div id="timer-display" class="timer-display hidden"></div>
        <button class="btn-secondary full-width hidden" id="stop-timer-btn">Finalizar</button>
      `;
      document.getElementById('start-session-btn').addEventListener('click', () => startStudySession(area));
      break;
    case 'documents':
      contentDiv.innerHTML = `
        <div id="docs-list">${(area.documents||[]).map((d,i) => `<div class="card"><a href="${d.url}" target="_blank">${d.title}</a><button class="btn-secondary" data-del-doc="${i}" style="float:right">X</button></div>`).join('')}</div>
        <button class="btn-secondary full-width" id="add-doc-btn">+ Agregar documento</button>
      `;
      document.getElementById('add-doc-btn').addEventListener('click', () => {
        const title = prompt('TÃ­tulo del documento:');
        const url = prompt('URL:');
        if (title && url) {
          area.documents = area.documents || [];
          area.documents.push({ title, url });
          Storage.setAreas(Storage.getAreas().map(a => a.id === area.id ? area : a));
          loadTabContent('documents', area);
        }
      });
      break;
    case 'videos':
      contentDiv.innerHTML = `
        <div id="videos-list">${(area.videos||[]).map((v,i) => `<div class="card"><strong>${v.title}</strong><button class="btn-secondary view-video" data-url="${v.url}">Ver</button></div>`).join('')}</div>
        <button class="btn-secondary full-width" id="add-video-btn">+ Agregar video</button>
        <div id="video-player" class="hidden" style="margin-top:1rem;"></div>
      `;
      document.getElementById('add-video-btn').addEventListener('click', () => {
        const title = prompt('TÃ­tulo del video:');
        const url = prompt('URL de YouTube:');
        if (title && url) {
          area.videos = area.videos || [];
          area.videos.push({ title, url });
          Storage.setAreas(Storage.getAreas().map(a => a.id === area.id ? area : a));
          loadTabContent('videos', area);
        }
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
  if (basal.mode === 'red') { showToast('No disponible en ProtecciÃ³n'); return; }
  if (Storage.getCredits() === 0) { showToast('NecesitÃ¡s 1 crÃ©dito'); return; }
  if (!confirm('Gastar 1 crÃ©dito para iniciar sesiÃ³n?')) return;
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
      stopSession(area, minutes);
    }
  }, 1000);
  stopBtn.addEventListener('click', () => {
    clearInterval(timerInterval);
    stopSession(area, Math.round((minutes * 60 - remaining) / 60));
  });
}

function stopSession(area, duration) {
  const intensity = prompt('Intensidad (1-10):', '7');
  const notes = prompt('Notas:', '');
  Storage.addExploit({ areaId: area.id, date: todayStr(), duration, intensity: parseInt(intensity)||7, notes });
  showToast('SesiÃ³n guardada');
  renderStudies(document.getElementById('dev-content'));
}
