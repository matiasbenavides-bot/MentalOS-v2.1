import { Storage } from '../storage.js';
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
