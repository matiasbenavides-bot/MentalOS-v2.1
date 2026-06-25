import { Storage } from '../storage.js';
import { calculateBasal } from '../state.js';
import { showToast } from '../ui.js';

let chart;

export function renderAnalysis() {
  const vp = document.getElementById('viewport');
  vp.innerHTML = `
    <h3>📊 Progreso a largo plazo</h3>
    <div style="display:flex; gap:0.5rem; margin:0.8rem 0 1.2rem;">
      <button class="btn-secondary period-btn active" data-months="3">3 meses</button>
      <button class="btn-secondary period-btn" data-months="6">6 meses</button>
      <button class="btn-secondary period-btn" data-months="12">12 meses</button>
    </div>
    <div class="chart-container"><canvas id="basal-chart"></canvas></div>
    <div id="stats-text" class="card" style="margin-top:1rem;"></div>
    <button class="btn-secondary full-width" id="export-btn" style="margin-top:1.2rem;">📥 Exportar datos</button>
  `;
  document.querySelectorAll('.period-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      loadChart(parseInt(btn.dataset.months));
    });
  });
  loadChart(3);
  document.getElementById('export-btn').onclick = () => {
    const blob = new Blob([Storage.exportAll()], {type:'application/json'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'mentalo-backup.json';
    a.click();
    showToast('Datos exportados');
  };
}

function loadChart(months) {
  const logs = Storage.getLogs();
  const dates = [];
  const end = new Date();
  const start = new Date();
  start.setMonth(start.getMonth() - months);
  for (let d = new Date(start); d <= end; d.setDate(d.getDate()+1)) {
    dates.push(new Date(d).toISOString().split('T')[0]);
  }
  const scores = dates.map(d => {
    const state = calculateBasal(d);
    return state.score;
  });
  const ctx = document.getElementById('basal-chart').getContext('2d');
  if (chart) chart.destroy();
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dates.map(d => d.slice(5)),
      datasets: [{
        label: 'Estado Basal',
        data: scores,
        borderColor: '#5c8aff',
        backgroundColor: 'rgba(92,138,255,0.1)',
        fill: true,
        tension: 0.3,
        pointRadius: 0
      }]
    },
    options: {
      scales: { y: { min:0, max:100, ticks:{stepSize:20} } },
      plugins: { tooltip: { mode: 'index' } }
    }
  });
  const valid = scores.filter(s => s!==null);
  const avg = valid.length ? Math.round(valid.reduce((a,b)=>a+b,0)/valid.length) : '—';
  const redDays = valid.filter(s => s<40).length;
  const greenDays = valid.filter(s => s>=70).length;
  document.getElementById('stats-text').innerHTML = `
    <strong>Resumen (${months} meses):</strong> Promedio: ${avg}/100 | Días en verde: ${greenDays} | Días en rojo: ${redDays}
    <p style="margin-top:0.5rem; font-style:italic;">${generateInsight(avg, redDays, greenDays)}</p>
  `;
}

function generateInsight(avg, red, green) {
  if (avg === '—') return 'Sin datos suficientes.';
  if (avg >= 70) return 'Excelente estado basal. Mantené la racha.';
  if (avg >= 40) return 'Estás en rango medio. Identificá los días rojos para prevenirlos.';
  return 'Tu promedio es bajo. Priorizá el Core y usá el checklist de emergencia.';
}
