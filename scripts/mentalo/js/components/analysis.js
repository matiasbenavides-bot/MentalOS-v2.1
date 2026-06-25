import { Storage } from '../storage.js';
import { calculateBasal } from '../state.js';
let chart;
export function renderAnalysis() {
  document.getElementById('viewport').innerHTML = `
    <h3>📊 Progreso</h3>
    <div style="display:flex; gap:0.5rem; margin:0.8rem 0;">
      <button class="btn-secondary period-btn active" data-months="3">3M</button>
      <button class="btn-secondary period-btn" data-months="6">6M</button>
      <button class="btn-secondary period-btn" data-months="12">12M</button>
    </div>
    <div class="chart-container"><canvas id="basal-chart"></canvas></div>
    <div id="stats-text" class="card"></div>
    <button class="btn-secondary full-width" id="export-btn" style="margin-top:1rem;">📥 Exportar</button>
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
  if (chart) chart.destroy();
  chart = new Chart(document.getElementById('basal-chart').getContext('2d'), {
    type: 'line', data: { labels: dates.map(d => d.slice(5)), datasets: [{ label: 'Estado Basal', data: scores, borderColor: '#5c8aff', backgroundColor: 'rgba(92,138,255,0.1)', fill: true, tension: 0.3, pointRadius: 0 }] },
    options: { scales: { y: { min:0, max:100 } } }
  });
  const valid = scores.filter(s => s!==null);
  const avg = valid.length ? Math.round(valid.reduce((a,b)=>a+b,0)/valid.length) : '—';
  document.getElementById('stats-text').innerHTML = `<strong>Resumen (${months}M):</strong> Promedio: ${avg}/100`;
}
