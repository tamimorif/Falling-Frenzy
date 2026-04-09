/**
 * Falling Frenzy — Game Configuration
 * All constants, enums, and tuning values.
 */

// ── Canvas ────────────────────────────────────────────────
export const CANVAS_WIDTH  = 800;
export const CANVAS_HEIGHT = 600;
export const FPS = 60;
export const GAME_TITLE = 'Falling Frenzy';

// ── Basket ────────────────────────────────────────────────
export const BASKET_WIDTH    = 110;
export const BASKET_HEIGHT   = 22;
export const BASKET_SPEED    = 14;
export const BASKET_Y_OFFSET = 18;

// ── Falling objects ───────────────────────────────────────
export const OBJECT_RADIUS        = 18;
export const OBJECT_BASE_SPEED    = 3.2;
export const OBJECT_MAX_SPEED     = 11;
export const OBJECT_SPEED_INC     = 0.08;
export const OBJECT_SPAWN_DELAY   = 950;   // ms
export const SPAWN_DELAY_MIN      = 380;
export const SPAWN_DELAY_DEC      = 40;
export const SPAWN_COLS           = 5;

// ── Scoring ───────────────────────────────────────────────
export const STARTING_SCORE    = 10;
export const MISS_PENALTY      = 1;
export const BOMB_DAMAGE       = 3;
export const COMBO_TIMEOUT     = 2200;   // ms
export const DIFFICULTY_INTERVAL = 12;   // seconds

// ── Power-ups ─────────────────────────────────────────────
export const POWERUP_SPAWN_CHANCE = 0.06;
export const POWERUP_DURATION     = 5000; // ms

// ── Particles ─────────────────────────────────────────────
export const PARTICLE_COUNT     = 12;
export const PARTICLE_LIFETIME  = 520; // ms
export const PARTICLE_SPEED_MIN = 1.8;
export const PARTICLE_SPEED_MAX = 5.2;
export const PARTICLE_SIZE_MIN  = 2;
export const PARTICLE_SIZE_MAX  = 6;

// ── UI sizes ──────────────────────────────────────────────
export const BUTTON_W = 220;
export const BUTTON_H = 52;
export const BUTTON_R = 12;

// ── Colors ────────────────────────────────────────────────
export const C = Object.freeze({
  white:     '#ffffff',
  black:     '#000000',
  red:       '#ff4444',
  green:     '#44ff70',
  yellow:    '#ffdc44',
  blue:      '#3c78ff',
  purple:    '#b844ff',
  orange:    '#ff8c00',
  gray:      '#c8c8c8',
  darkGray:  '#323232',
  lightBlue: '#64b4ff',
  gold:      '#ffd740',
  bgTop:     '#141428',
  bgBot:     '#3c2850',
  panelBg:   'rgba(20,20,40,0.75)',
  panelBorder:'rgba(255,255,255,0.08)',
});

// ── Object types ──────────────────────────────────────────
export const ObjectType = Object.freeze({
  RED:    { name: 'red',    color: C.red,    points: 1, isBomb: false },
  GREEN:  { name: 'green',  color: C.green,  points: 2, isBomb: false },
  YELLOW: { name: 'yellow', color: C.yellow, points: 3, isBomb: false },
  PURPLE: { name: 'purple', color: C.purple, points: 5, isBomb: false },
  BOMB:   { name: 'bomb',   color: C.black,  points: -3, isBomb: true },
});

// ── Power-up types ────────────────────────────────────────
export const PowerUpType = Object.freeze({
  SLOW_MOTION:   { name: 'Slow-Mo',  color: C.lightBlue, value: 0.5 },
  DOUBLE_POINTS: { name: '2× Points', color: C.gold,      value: 2.0 },
  SHIELD:        { name: 'Shield',    color: C.purple,     value: 1.0 },
});

// ── Game states ───────────────────────────────────────────
export const State = Object.freeze({
  MENU:      'menu',
  PLAYING:   'playing',
  PAUSED:    'paused',
  GAME_OVER: 'game_over',
});
