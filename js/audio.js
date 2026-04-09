/**
 * Falling Frenzy — Procedural Web Audio
 * Generates all sound effects at runtime so no external files are needed.
 */

export class AudioManager {
  constructor() {
    this.ctx = null;       // created on first user gesture
    this.volume = 0.35;
    this.enabled = true;
  }

  /** Ensure AudioContext exists (must be called after a user gesture). */
  _ensure() {
    if (!this.ctx) {
      try {
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
      } catch {
        this.enabled = false;
      }
    }
    if (this.ctx?.state === 'suspended') this.ctx.resume();
  }

  /**
   * Play a sine-wave beep.
   * @param {number} freq   – frequency in Hz
   * @param {number} dur    – duration in seconds
   * @param {string} type   – oscillator type
   * @param {number} vol    – volume 0-1
   */
  _tone(freq, dur = 0.1, type = 'sine', vol = 1) {
    if (!this.enabled) return;
    this._ensure();
    if (!this.ctx) return;

    const osc  = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = type;
    osc.frequency.value = freq;
    gain.gain.setValueAtTime(this.volume * vol, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + dur);
    osc.connect(gain).connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + dur);
  }

  // ── Named sounds ───────────────────────────────────────

  catchRed()    { this._tone(523, 0.08, 'sine', 0.6); }
  catchGreen()  { this._tone(659, 0.08, 'sine', 0.7); }
  catchYellow() { this._tone(784, 0.08, 'sine', 0.8); }
  catchPurple() {
    this._tone(880, 0.12, 'sine', 0.9);
    setTimeout(() => this._tone(1100, 0.10, 'sine', 0.7), 60);
  }
  catchBomb() {
    this._tone(120, 0.25, 'sawtooth', 0.8);
    this._tone(80,  0.30, 'square',   0.5);
  }
  miss()     { this._tone(220, 0.15, 'triangle', 0.4); }
  combo()    {
    this._tone(700, 0.06, 'sine', 0.5);
    setTimeout(() => this._tone(900, 0.06, 'sine', 0.5), 70);
    setTimeout(() => this._tone(1100, 0.08, 'sine', 0.6), 140);
  }
  powerup()  {
    this._tone(600, 0.08, 'sine', 0.6);
    setTimeout(() => this._tone(800, 0.08, 'sine', 0.6), 80);
    setTimeout(() => this._tone(1000, 0.10, 'sine', 0.7), 160);
  }
  gameOver() {
    this._tone(400, 0.15, 'sine', 0.7);
    setTimeout(() => this._tone(300, 0.15, 'sine', 0.6), 150);
    setTimeout(() => this._tone(200, 0.30, 'sine', 0.5), 300);
  }
  click()    { this._tone(460, 0.04, 'sine', 0.3); }

  /** Map object type name → catch sound. */
  playCatch(typeName) {
    const map = {
      red: () => this.catchRed(),
      green: () => this.catchGreen(),
      yellow: () => this.catchYellow(),
      purple: () => this.catchPurple(),
      bomb: () => this.catchBomb(),
    };
    (map[typeName] || (() => {}))();
  }
}
