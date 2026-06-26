import { Storage } from '../storage.js';
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
