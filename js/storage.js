const PREFIX = 'mentalo_';
export const Storage = {
  get(key) {
    try { return JSON.parse(localStorage.getItem(PREFIX + key)); } catch { return null; }
  },
  set(key, value) { localStorage.setItem(PREFIX + key, JSON.stringify(value)); },
  getLogs() { return this.get('logs') || {}; },
  addLog(date, data) {
    const logs = this.getLogs();
    logs[date] = data;
    this.set('logs', logs);
  },
  getConfig() {
    return this.get('config') || {
      pin: '2207',
      emergencyChecklist: ['Ducharse o lavarse la cara','Comer algo','Salir 5 minutos al aire libre','Mensaje a contacto de confianza','Leer 1 página de un libro favorito'],
      supportMessage: 'Esto es pasajero. Ya saliste de episodios peores.',
      contactName: 'Contacto de confianza'
    };
  },
  setConfig(c) { this.set('config', c); },
  getHabits() {
    let habits = this.get('habits');
    if (!habits || habits.length === 0) {
      // Hábitos por defecto
      habits = [
        { id: '1', name: 'Estiramientos', icon: '🧘', section: 'morning', duration: 10 },
        { id: '2', name: 'Leer artículos', icon: '📄', section: 'morning', duration: 20 },
        { id: '3', name: 'Ejercicio', icon: '🏋️', section: 'afternoon', duration: 45 },
        { id: '4', name: 'Planificar el día', icon: '📅', section: 'morning', duration: 5 },
        { id: '5', name: 'Meditar', icon: '🧘‍♂️', section: 'evening', duration: 10 },
        { id: '6', name: 'Escribir diario', icon: '✍️', section: 'evening', duration: 15 }
      ];
      this.set('habits', habits);
    }
    return habits;
  },
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
