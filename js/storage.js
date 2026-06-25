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
      emergencyChecklist: ['Ducharse o lavarse la cara','Comer algo','Salir 5 minutos al aire libre','Mensaje a contacto de confianza','Leer 1 pÃ¡gina de un libro favorito'],
      supportMessage: 'Tu cerebro estÃ¡ experimentando una baja quÃ­mica temporal. Esto va a pasar. Solo cumple estas 5 cosas y tu dÃ­a habrÃ¡ sido un Ã©xito.'
    };
  },
  setConfig(c) { this.set('config', c); },
  getHabits() {
    let habits = this.get('habits');
    if (!habits || habits.length === 0) {
      habits = [
        { id: 'h1', name: 'HidrataciÃ³n y Luz Solar', section: 'morning', duration: 5, order: 0 },
        { id: 'h2', name: 'Lectura tÃ©cnica', section: 'morning', duration: 20, order: 1 },
        { id: 'h3', name: 'Ejercicio', section: 'afternoon', duration: 45, order: 0 },
        { id: 'h4', name: 'Movilidad', section: 'evening', duration: 10, order: 0 },
        { id: 'h5', name: 'Planificar dÃ­a siguiente', section: 'evening', duration: 5, order: 1 }
      ];
      this.set('habits', habits);
    }
    return habits;
  },
  setHabits(h) { this.set('habits', h); },
  getAreas() { return this.get('areas') || []; },
  setAreas(a) { this.set('areas', a); },
  getRoutines() { return this.get('routines') || []; },
  setRoutines(r) { this.set('routines', r); },
  getExploitLog() { return this.get('exploit') || []; },
  addExploit(session) {
    const log = this.getExploitLog();
    log.push(session);
    this.set('exploit', log);
  },
  getCredits() { return this.get('credits') || 0; },
  setCredits(c) { this.set('credits', c); },
  exportAll() {
    return JSON.stringify({ logs: this.getLogs(), config: this.getConfig(), habits: this.getHabits(), areas: this.getAreas(), routines: this.getRoutines(), exploit: this.getExploitLog(), credits: this.getCredits() }, null, 2);
  }
};
