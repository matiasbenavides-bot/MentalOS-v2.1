import { renderStudies } from './studies.js';
import { renderTraining } from './training.js';

export function renderDevelopment() {
  const vp = document.getElementById('viewport');
  vp.innerHTML = `
    <div style="display:flex; gap:1rem; margin-top:2rem;">
      <button class="btn-primary full-width" id="btn-studies">Estudios</button>
      <button class="btn-primary full-width" id="btn-training">Entrenamientos</button>
    </div>
    <div id="dev-content"></div>
  `;
  document.getElementById('btn-studies').addEventListener('click', () => {
    renderStudies(document.getElementById('dev-content'));
  });
  document.getElementById('btn-training').addEventListener('click', () => {
    renderTraining(document.getElementById('dev-content'));
  });
  // Cargar estudios por defecto
  renderStudies(document.getElementById('dev-content'));
}
