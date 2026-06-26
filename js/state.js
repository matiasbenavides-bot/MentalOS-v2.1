import { Storage } from './storage.js';
export function todayStr() { return new Date().toISOString().split('T')[0]; }
export function calculateBasal(dateStr = null) {
  const date = dateStr || todayStr();
  const logs = Storage.getLogs();
  const log = logs[date];
  if (!log || !log.core) return { score: null, mode: 'unknown' };
  const core = log.core;
  if (core.emotion !== undefined && core.emotion <= 2) return { score: 0, mode: 'red', reason: 'emotional' };
  if (core.sleep !== undefined && core.sleep < 5) return { score: 0, mode: 'red', reason: 'sleep' };
  const socialDays = [];
  for (let i=0; i<3; i++) {
    const d = new Date(); d.setDate(d.getDate()-i);
    socialDays.push(logs[d.toISOString().split('T')[0]]?.core?.social);
  }
  if (socialDays.filter(s => s === false).length >= 3) return { score: 0, mode: 'red', reason: 'social' };
  let score = 0, total = 0;
  const weights = { sleep: 30, emotion: 30, nutrition: 15, movement: 15, social: 10 };
  if (core.sleep !== undefined) { score += Math.min(core.sleep/8,1)*weights.sleep; total += weights.sleep; }
  if (core.emotion !== undefined) { score += (core.emotion/5)*weights.emotion; total += weights.emotion; }
  if (core.nutrition !== undefined) { score += (core.nutrition?1:0)*weights.nutrition; total += weights.nutrition; }
  if (core.movement !== undefined) { score += (core.movement?1:0)*weights.movement; total += weights.movement; }
  if (core.social !== undefined) { score += (core.social?1:0)*weights.social; total += weights.social; }
  if (total === 0) return { score: null, mode: 'unknown' };
  const final = Math.round((score/total)*100);
  if (final >= 70) return { score: final, mode: 'green' };
  if (final >= 40) return { score: final, mode: 'yellow' };
  return { score: final, mode: 'red' };
}
export function updateCreditsOnCheckin(allCoreOk) {
  let credits = Storage.getCredits();
  if (allCoreOk && credits < 3) { credits++; Storage.setCredits(credits); }
  return credits;
}
export function spendCredit() {
  let credits = Storage.getCredits();
  if (credits > 0) { credits--; Storage.setCredits(credits); return true; }
  return false;
}
