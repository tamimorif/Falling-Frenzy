/**
 * Falling Frenzy — Utility / Manager classes
 * ScoreManager and persistent storage helpers.
 */
import {
  STARTING_SCORE, COMBO_TIMEOUT,
} from './config.js';

// ── Local Storage helpers ─────────────────────────────────
const LS_HIGH  = 'ff_highscore';
const LS_STATS = 'ff_stats';

function lsGet(key, fallback) {
  try { const v = localStorage.getItem(key); return v !== null ? JSON.parse(v) : fallback; }
  catch { return fallback; }
}
function lsSet(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* quota */ }
}

// ── Score Manager ─────────────────────────────────────────
export class ScoreManager {
  constructor() {
    this.score     = STARTING_SCORE;
    this.highScore = lsGet(LS_HIGH, 0);
    this.combo     = 0;
    this.bestCombo = 0;
    this.comboTimer = 0;
    this.comboActive = false;
  }

  addPoints(pts, multiplier = 1) {
    const actual = Math.round(pts * multiplier);
    this.score += actual;
    if (this.score > this.highScore) this.highScore = this.score;
    this.combo++;
    this.bestCombo = Math.max(this.bestCombo, this.combo);
    this.comboTimer = COMBO_TIMEOUT;
    this.comboActive = true;
    return actual;
  }

  subtractPoints(pts) {
    this.score = Math.max(0, this.score - pts);
    this.resetCombo();
  }

  resetCombo() {
    this.combo = 0;
    this.comboActive = false;
  }

  updateComboTimer(dtMs) {
    if (this.comboActive) {
      this.comboTimer -= dtMs;
      if (this.comboTimer <= 0) this.resetCombo();
    }
  }

  getMultiplier() {
    if (this.combo < 3) return 1.0;
    if (this.combo < 5) return 1.5;
    if (this.combo < 10) return 2.0;
    return 2.5;
  }

  isGameOver() { return this.score <= 0; }

  saveHigh() { lsSet(LS_HIGH, this.highScore); }

  reset() {
    this.score = STARTING_SCORE;
    this.combo = 0;
    this.bestCombo = 0;
    this.comboTimer = 0;
    this.comboActive = false;
  }
}

// ── Statistics Manager ────────────────────────────────────
const defaultStats = () => ({
  gamesPlayed: 0, totalScore: 0, totalTimeSec: 0,
  bestCombo: 0, caught: 0, missed: 0,
});

export class StatsManager {
  constructor() {
    this.stats = { ...defaultStats(), ...lsGet(LS_STATS, {}) };
    this._sessionStart = null;
  }

  startSession() { this._sessionStart = performance.now(); }

  endSession(score, bestCombo, caught, missed) {
    if (this._sessionStart !== null) {
      this.stats.totalTimeSec += Math.round((performance.now() - this._sessionStart) / 1000);
    }
    this.stats.gamesPlayed++;
    this.stats.totalScore += score;
    this.stats.bestCombo = Math.max(this.stats.bestCombo, bestCombo);
    this.stats.caught += caught;
    this.stats.missed += missed;
    lsSet(LS_STATS, this.stats);
    this._sessionStart = null;
  }

  avgScore() {
    return this.stats.gamesPlayed > 0
      ? (this.stats.totalScore / this.stats.gamesPlayed).toFixed(1) : '0.0';
  }
  catchRate() {
    const total = this.stats.caught + this.stats.missed;
    return total > 0 ? ((this.stats.caught / total) * 100).toFixed(1) : '0.0';
  }
}
