const PREFIX = 'mentalo_';
export const Storage = {
  get(key) {
    try { const raw = localStorage.getItem(PREFIX + key); return raw ? JSON.parse(raw) : null; }
    catch { return null; }
  },
  set(key, value) {
    localStorage.setItem(PREFIX + key, JSON.stringify(value));
  },
  getLogs() { return this.get('logs') || {}; },
  addLog(date, data) {
    const logs = this.getLogs();
    logs[date] = data;
    this.set('logs', logs);
  },
  getConfig() {
    return this.get('config') || {
      pin: '1234',
      emergencyChecklist: ['Ducharse o lavarse la cara','Comer algo','Salir 5 minutos al aire libre','Mensaje a contacto de confianza','Leer 1 página de un libro favorito'],
      supportMessage: 'Esto es pasajero. Ya saliste de episodios peores.',
      contactName: 'Contacto de confianza'
    };
  },
  setConfig(c) { this.set('config', c); },
  getHabits() { return this.get('habits') || []; },
  setHabits(h) { this.set('habits', h); },
  getAreas() { return this.get('areas') || []; },
  setAreas(a) { this.set('areas', a); },
  getExploitationLog() { return this.get('exploit') || []; },
  addExploit(session) {
    const log = this.getExploitationLog();
    log.push(session);
    this.set('exploit', log);
  },
  getCredits() { return this.get('credits') || 0; },
  setCredits(c) { this.set('credits', c); },
  exportAll() {
    return JSON.stringify({ logs: this.getLogs(), config: this.getConfig(), habits: this.getHabits(), areas: this.getAreas(), exploit: this.getExploitationLog(), credits: this.getCredits() }, null, 2);
  },
  importAll(data) {
    if (data.logs) this.set('logs', data.logs);
    if (data.config) this.set('config', data.config);
    if (data.habits) this.set('habits', data.habits);
    if (data.areas) this.set('areas', data.areas);
    if (data.exploit) this.set('exploit', data.exploit);
    if (data.credits !== undefined) this.set('credits', data.credits);
  }
};
