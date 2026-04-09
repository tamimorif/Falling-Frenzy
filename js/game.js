/**
 * Falling Frenzy — Main Game Loop
 * Orchestrates all systems using requestAnimationFrame.
 */
import {
  CANVAS_WIDTH, CANVAS_HEIGHT,
  BASKET_WIDTH, BASKET_Y_OFFSET,
  OBJECT_RADIUS, OBJECT_BASE_SPEED, OBJECT_MAX_SPEED, OBJECT_SPEED_INC,
  OBJECT_SPAWN_DELAY, SPAWN_DELAY_MIN, SPAWN_DELAY_DEC, SPAWN_COLS,
  MISS_PENALTY, BOMB_DAMAGE,
  POWERUP_SPAWN_CHANCE, POWERUP_DURATION,
  PARTICLE_COUNT, DIFFICULTY_INTERVAL,
  ObjectType, PowerUpType, State, C,
} from './config.js';

import { Basket, FallingObject, PowerUp, ParticleSystem } from './entities.js';
import { ScoreManager, StatsManager } from './utils.js';
import { AudioManager } from './audio.js';
import {
  drawBackground, drawHUD, drawPowerUpBar,
  makeButton, drawButton, hitTestButtons,
  drawTitle, drawOverlay, drawCenteredText,
} from './ui.js';

// ── Canvas setup ──────────────────────────────────────────
const canvas = document.getElementById('gameCanvas');
const ctx    = canvas.getContext('2d');
canvas.width  = CANVAS_WIDTH;
canvas.height = CANVAS_HEIGHT;

// ── Managers ──────────────────────────────────────────────
const score   = new ScoreManager();
const stats   = new StatsManager();
const audio   = new AudioManager();
const particles = new ParticleSystem();

// ── Entities ──────────────────────────────────────────────
let basket  = new Basket(CANVAS_WIDTH / 2 - BASKET_WIDTH / 2, CANVAS_HEIGHT - BASKET_Y_OFFSET - 22);
let objects = [];
let powerups = [];

// ── Game state ────────────────────────────────────────────
let state       = State.MENU;
let lastTime    = 0;
let spawnTimer  = 0;
let spawnDelay  = OBJECT_SPAWN_DELAY;
let objSpeed    = OBJECT_BASE_SPEED;
let diffTimer   = 0;
let activePU    = null;      // active power-up type
let puTimer     = 0;         // ms remaining
let caughtCount = 0;
let missedCount = 0;

// ── Input state ───────────────────────────────────────────
const keys = { left: false, right: false };
let mouseX = CANVAS_WIDTH / 2;
let mouseY = CANVAS_HEIGHT / 2;
let mouseClicked = false;     // true for one frame

// ── Menus ─────────────────────────────────────────────────
const menuButtons = [
  makeButton('Start Game', -20, startGame),
  makeButton('Quit',        60, () => { /* no-op on web */ }),
];

const pauseButtons = [
  makeButton('Resume',     -20, () => { state = State.PLAYING; audio.click(); }),
  makeButton('Main Menu',   60, returnToMenu),
];

const gameOverButtons = [
  makeButton('Play Again',  30, startGame),
  makeButton('Main Menu',  110, returnToMenu),
];

// ── Action helpers ────────────────────────────────────────
function startGame() {
  audio.click();
  score.reset();
  objects = [];
  powerups = [];
  particles.clear();
  basket.x = CANVAS_WIDTH / 2 - BASKET_WIDTH / 2;
  spawnTimer = 0;
  spawnDelay = OBJECT_SPAWN_DELAY;
  objSpeed   = OBJECT_BASE_SPEED;
  diffTimer  = 0;
  activePU   = null;
  puTimer    = 0;
  caughtCount = 0;
  missedCount = 0;
  state = State.PLAYING;
  stats.startSession();
}

function returnToMenu() {
  audio.click();
  state = State.MENU;
}

function endGame() {
  state = State.GAME_OVER;
  audio.gameOver();
  stats.endSession(score.score, score.bestCombo, caughtCount, missedCount);
  score.saveHigh();
}

// ── Spawning ──────────────────────────────────────────────
function spawnObject() {
  const colW = CANVAS_WIDTH / SPAWN_COLS;
  const col  = Math.floor(Math.random() * SPAWN_COLS);
  let x = col * colW + Math.random() * (colW - OBJECT_RADIUS * 2) + OBJECT_RADIUS;
  x = Math.max(OBJECT_RADIUS, Math.min(x, CANVAS_WIDTH - OBJECT_RADIUS));

  const r = Math.random();
  let type;
  if (r < 0.15)       type = ObjectType.BOMB;
  else if (r < 0.20)  type = ObjectType.PURPLE;
  else {
    const regular = [ObjectType.RED, ObjectType.GREEN, ObjectType.YELLOW];
    type = regular[Math.floor(Math.random() * regular.length)];
  }
  objects.push(new FallingObject(x, -OBJECT_RADIUS, type, objSpeed));
}

function maybePowerup() {
  if (Math.random() < POWERUP_SPAWN_CHANCE) {
    const x = OBJECT_RADIUS + Math.random() * (CANVAS_WIDTH - OBJECT_RADIUS * 2);
    const types = [PowerUpType.SLOW_MOTION, PowerUpType.DOUBLE_POINTS, PowerUpType.SHIELD];
    const t = types[Math.floor(Math.random() * types.length)];
    powerups.push(new PowerUp(x, -OBJECT_RADIUS, t, objSpeed * 0.65));
  }
}

// ── Collision detection ───────────────────────────────────
function rectsCollide(a, b) {
  return a.x < b.x + b.w && a.x + a.w > b.x &&
         a.y < b.y + b.h && a.y + a.h > b.y;
}

function checkCollisions() {
  const br = basket.rect();

  // Objects
  for (let i = objects.length - 1; i >= 0; i--) {
    const obj = objects[i];
    if (!rectsCollide(br, obj.getRect())) continue;

    if (obj.type.isBomb) {
      score.subtractPoints(BOMB_DAMAGE);
      score.resetCombo();
      missedCount++;
      particles.emit(obj.x, obj.y, C.orange, PARTICLE_COUNT * 3);
      audio.playCatch('bomb');
    } else {
      let mult = score.getMultiplier();
      if (activePU === PowerUpType.DOUBLE_POINTS) mult *= 2;
      score.addPoints(obj.type.points, mult);
      caughtCount++;
      particles.emit(obj.x, obj.y, obj.type.color, PARTICLE_COUNT);
      audio.playCatch(obj.type.name);
      if (score.combo > 2) audio.combo();
    }
    objects.splice(i, 1);
  }

  // Power-ups
  for (let i = powerups.length - 1; i >= 0; i--) {
    const pu = powerups[i];
    if (!rectsCollide(br, pu.getRect())) continue;
    activePU = pu.type;
    puTimer  = POWERUP_DURATION;
    particles.emit(pu.x, pu.y, pu.type.color, PARTICLE_COUNT * 2);
    audio.powerup();
    powerups.splice(i, 1);
  }
}

// ── Update (playing) ──────────────────────────────────────
function updatePlaying(dt) {
  const dtMs = dt * 1000;

  basket.update(keys, dt);

  // Difficulty
  diffTimer += dt;
  if (diffTimer >= DIFFICULTY_INTERVAL) {
    if (objSpeed < OBJECT_MAX_SPEED) objSpeed += OBJECT_SPEED_INC;
    if (spawnDelay > SPAWN_DELAY_MIN) spawnDelay -= SPAWN_DELAY_DEC;
    diffTimer = 0;
  }

  // Spawning
  spawnTimer += dtMs;
  if (spawnTimer >= spawnDelay) {
    spawnObject();
    maybePowerup();
    spawnTimer = 0;
  }

  // Speed multiplier from power-up
  const speedMult = activePU === PowerUpType.SLOW_MOTION ? 0.5 : 1;

  // Update objects (iterate backwards for safe removal)
  for (let i = objects.length - 1; i >= 0; i--) {
    objects[i].update(dt, speedMult);
    if (objects[i].isOffScreen()) {
      if (activePU !== PowerUpType.SHIELD) {
        score.subtractPoints(MISS_PENALTY);
        audio.miss();
      }
      missedCount++;
      objects.splice(i, 1);
    }
  }

  for (let i = powerups.length - 1; i >= 0; i--) {
    powerups[i].update(dt);
    if (powerups[i].isOffScreen()) powerups.splice(i, 1);
  }

  // Power-up timer
  if (activePU) {
    puTimer -= dtMs;
    if (puTimer <= 0) activePU = null;
  }

  checkCollisions();
  score.updateComboTimer(dtMs);
  particles.update(dt);

  if (score.isGameOver()) endGame();
}

// ── Render ────────────────────────────────────────────────
function render() {
  drawBackground(ctx);

  if (state === State.MENU) {
    drawTitle(ctx, 'FALLING FRENZY');
    drawCenteredText(ctx, 'Catch the falling objects — avoid the bombs!', 145, '16px Inter, sans-serif', C.gray);
    menuButtons.forEach(b => drawButton(ctx, b, mouseX, mouseY));
  }

  else if (state === State.PLAYING) {
    // Entities
    basket.draw(ctx);
    objects.forEach(o => o.draw(ctx));
    powerups.forEach(p => p.draw(ctx));
    particles.draw(ctx);
    drawHUD(ctx, score.score, score.highScore, score.combo, score.getMultiplier());
    drawPowerUpBar(ctx, activePU, puTimer);
  }

  else if (state === State.PAUSED) {
    // Draw game dimmed
    basket.draw(ctx);
    objects.forEach(o => o.draw(ctx));
    drawOverlay(ctx, 0.55);
    drawTitle(ctx, 'PAUSED');
    pauseButtons.forEach(b => drawButton(ctx, b, mouseX, mouseY));
  }

  else if (state === State.GAME_OVER) {
    drawOverlay(ctx, 0.45);
    drawTitle(ctx, 'GAME OVER', 80);
    drawCenteredText(ctx, `Final Score: ${score.score}`, 150, 'bold 24px Inter, sans-serif', C.white);
    drawCenteredText(ctx, `High Score: ${score.highScore}`, 185, '18px Inter, sans-serif', C.gold);

    if (score.bestCombo > 2) {
      drawCenteredText(ctx, `Best Combo: ×${score.bestCombo}`, 215, '16px Inter, sans-serif', C.green);
    }

    gameOverButtons.forEach(b => drawButton(ctx, b, mouseX, mouseY));
  }
}

// ── Main loop ─────────────────────────────────────────────
function loop(ts) {
  const dt = Math.min((ts - lastTime) / 1000, 0.1);   // cap dt to avoid spirals
  lastTime = ts;

  if (state === State.PLAYING) updatePlaying(dt);

  render();
  mouseClicked = false;
  requestAnimationFrame(loop);
}

// ── Input listeners ───────────────────────────────────────

// Keyboard
window.addEventListener('keydown', e => {
  if (e.key === 'ArrowLeft'  || e.key === 'a') keys.left  = true;
  if (e.key === 'ArrowRight' || e.key === 'd') keys.right = true;
  if (e.key === 'Escape') {
    if (state === State.PLAYING) { state = State.PAUSED; audio.click(); }
    else if (state === State.PAUSED) { state = State.PLAYING; audio.click(); }
  }
});
window.addEventListener('keyup', e => {
  if (e.key === 'ArrowLeft'  || e.key === 'a') keys.left  = false;
  if (e.key === 'ArrowRight' || e.key === 'd') keys.right = false;
});

// Mouse — translate to canvas coordinates
function canvasCoords(e) {
  const r = canvas.getBoundingClientRect();
  const scaleX = CANVAS_WIDTH  / r.width;
  const scaleY = CANVAS_HEIGHT / r.height;
  return {
    x: (e.clientX - r.left) * scaleX,
    y: (e.clientY - r.top)  * scaleY,
  };
}

canvas.addEventListener('mousemove', e => {
  const c = canvasCoords(e);
  mouseX = c.x;
  mouseY = c.y;
  if (basket.dragging) basket.dragTo(c.x);
});

canvas.addEventListener('mousedown', e => {
  const c = canvasCoords(e);
  mouseX = c.x;
  mouseY = c.y;

  // Check buttons first
  let btns;
  if (state === State.MENU)      btns = menuButtons;
  else if (state === State.PAUSED)    btns = pauseButtons;
  else if (state === State.GAME_OVER) btns = gameOverButtons;

  if (btns) {
    const hit = hitTestButtons(btns, c.x, c.y);
    if (hit) { hit.action(); return; }
  }

  // Basket drag
  if (state === State.PLAYING) {
    const br = basket.rect();
    // Allow dragging from a generous area around the basket
    if (c.x >= br.x - 20 && c.x <= br.x + br.w + 20 &&
        c.y >= br.y - 40 && c.y <= br.y + br.h + 20) {
      basket.dragging = true;
    }
  }
});

canvas.addEventListener('mouseup', () => { basket.dragging = false; });

// Touch support
canvas.addEventListener('touchstart', e => {
  e.preventDefault();
  const t = e.touches[0];
  const c = canvasCoords(t);
  mouseX = c.x; mouseY = c.y;

  let btns;
  if (state === State.MENU)       btns = menuButtons;
  else if (state === State.PAUSED)     btns = pauseButtons;
  else if (state === State.GAME_OVER)  btns = gameOverButtons;

  if (btns) {
    const hit = hitTestButtons(btns, c.x, c.y);
    if (hit) { hit.action(); return; }
  }

  if (state === State.PLAYING) {
    basket.dragging = true;
    basket.dragTo(c.x);
  }
}, { passive: false });

canvas.addEventListener('touchmove', e => {
  e.preventDefault();
  const c = canvasCoords(e.touches[0]);
  mouseX = c.x; mouseY = c.y;
  if (basket.dragging) basket.dragTo(c.x);
}, { passive: false });

canvas.addEventListener('touchend', e => {
  e.preventDefault();
  basket.dragging = false;
}, { passive: false });

// ── Boot ──────────────────────────────────────────────────
lastTime = performance.now();
requestAnimationFrame(loop);
