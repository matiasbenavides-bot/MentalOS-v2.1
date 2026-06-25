import { Storage } from '../storage.js';
import { showModal, closeModal, showToast } from '../ui.js';
export function openConfigModal() {
  const config = Storage.getConfig();
  const body = `
    <div class="form-group"><label>PIN</label><input type="password" id="cfg-pin" value="${config.pin}"></div>
    <div class="form-group"><label>Mensaje de apoyo</label><textarea id="cfg-support">${config.supportMessage}</textarea></div>
    <div class="form-group"><label>Checklist (uno por línea)</label><textarea id="cfg-checklist" rows="5">${config.emergencyChecklist.join('\n')}</textarea></div>`;
  const footer = `<button class="btn-primary" id="save-config-btn">Guardar</button><button class="btn-secondary" id="cancel-config-btn">Cancelar</button>`;
  showModal('⚙️ Configuración', body, footer);
  document.getElementById('save-config-btn').onclick = () => {
    config.pin = document.getElementById('cfg-pin').value || '2207';
    config.supportMessage = document.getElementById('cfg-support').value;
    config.emergencyChecklist = document.getElementById('cfg-checklist').value.split('\n').filter(l => l.trim());
    Storage.setConfig(config);
    closeModal();
    showToast('Configuración guardada');
  };
  document.getElementById('cancel-config-btn').onclick = closeModal;
}
