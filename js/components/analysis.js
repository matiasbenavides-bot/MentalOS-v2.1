import { Storage } from '../storage.js';
import { calculateBasal } from '../state.js';
let chart;
export function renderAnalysis() {
  const logs = Storage.getLogs();
  const exploitLog = Storage.getExploitLog();
  // Contadores acumulativos
  const studyAreas = Storage.getAreas().filter(a => a.type === 'study');
  const trainingAreas = Storage.getAreas().filter(a => a.type === 'training');
  const totalStudyHours = Math.round(exploitLog.filter(e => studyAreas.some(a => a.id === e.areaId)).reduce((s,e) => s + e.duration, 0) / 60);
  const totalTrainingCount = exploitLog.filter(e => trainingAreas.some(a => a.id === e.areaId)).length;

  document.getElementById('viewport').innerHTML = `
    <div class="accumulator">
      <div class="accumulator-card"><div class="accumulator-value">${totalStudyHours}h</div><div class="accumulator-label">Horas de estudio</div></div>
      <div class="accumulator-card"><div class="accumulator-value">${totalTrainingCount}</div><div class="accumulator-label">Entrenamientos</div></div>
    </div>
    <div style="display:flex; gap:0.5rem; margin:0.8rem 0;">
      <button class="btn-secondary period-btn active" data-months="3">3M</button>
      <button class="btn-secondary period-btn" data-months="6">6M</button>
      <button class="btn-secondary period-btn" data-months="12">12M</button>
    </div>
    <div class="chart-container"><canvas id="basal-chart"></canvas></div>
    <div id="stats-text" class="card"></div>
    <button class="btn-secondary full-width" id="export-btn">Exportar datos</button>
  `;
  document.querySelectorAll('.period-btn').forEach(b => b.addEventListener('click', function() {
    document.querySelectorAll('.period-btn').forEach(x => x.classList.remove('active'));
    this.classList.add('active');
    loadChart(parseInt(this.dataset.months));
  }));
  loadChart(3);
  document.getElementById('export-btn').onclick = () => {
    const blob = new Blob([Storage.exportAll()], {type:'application/json'});
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'mentalo-backup.json'; a.click();
  };
}

function loadChart(months) {
  const logs = Storage.getLogs();
  const dates = [], end = new Date(), start = new Date();
  start.setMonth(start.getMonth()-months);
  for (let d = new Date(start); d <= end; d.setDate(d.getDate()+1)) dates.push(new Date(d).toISOString().split('T')[0]);
  const scores = dates.map(d => calculateBasal(d).score);
  const labels = dates.map(d => d.slice(5));
  if (chart) chart.destroy();
  // Suavizado con media mÃ³vil de 7 dÃ­as
  const smoothed = [];
  for (let i = 0; i < scores.length; i++) {
    let count = 0, sum = 0;
    for (let j = Math.max(0, i-3); j <= Math.min(scores.length-1, i+3); j++) {
      if (scores[j] !== null) { sum += scores[j]; count++; }
    }
    smoothed.push(count > 0 ? Math.round(sum/count) : null);
  }
  chart = new Chart(document.getElementById('basal-chart').getContext('2d'), {
    type: 'line',
    data: { labels, datasets: [{ label: 'Estado Basal (suavizado)', data: smoothed, borderColor: '#5c8aff', tension: 0.4, pointRadius: 0 }] },
    options: { scales: { y: { min:0, max:100 } } }
  });
  const valid = scores.filter(s => s !== null);
  const avg = valid.length ? Math.round(valid.reduce((a,b)=>a+b,0)/valid.length) : '--';
  document.getElementById('stats-text').innerHTML = `<strong>Promedio (${months}M):</strong> ${avg}/100`;
}
