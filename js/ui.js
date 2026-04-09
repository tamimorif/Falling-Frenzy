/**
 * Falling Frenzy — UI Renderer
 * Background, HUD, menus rendered onto the Canvas.
 */
import {
  CANVAS_WIDTH, CANVAS_HEIGHT,
  BUTTON_W, BUTTON_H, BUTTON_R,
  C,
} from './config.js';

// ── Background (cached gradient + starfield) ──────────────
let bgCache = null;

function buildBgCache() {
  const off = document.createElement('canvas');
  off.width = CANVAS_WIDTH;
  off.height = CANVAS_HEIGHT;
  const oc = off.getContext('2d');
  const grad = oc.createLinearGradient(0, 0, 0, CANVAS_HEIGHT);
  grad.addColorStop(0, C.bgTop);
  grad.addColorStop(1, C.bgBot);
  oc.fillStyle = grad;
  oc.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

  // Fixed stars
  const rng = mulberry32(42);
  for (let i = 0; i < 60; i++) {
    const sx = rng() * CANVAS_WIDTH;
    const sy = rng() * CANVAS_HEIGHT;
    const sr = 0.5 + rng() * 2;
    oc.beginPath();
    oc.arc(sx, sy, sr, 0, Math.PI * 2);
    oc.fillStyle = `rgba(255,255,255,${0.15 + rng() * 0.35})`;
    oc.fill();
  }
  bgCache = off;
}

/** Deterministic PRNG so stars don't flicker. */
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = seed + 0x6D2B79F5 | 0;
    let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

export function drawBackground(ctx) {
  if (!bgCache) buildBgCache();
  ctx.drawImage(bgCache, 0, 0);
}

// ── HUD ───────────────────────────────────────────────────
export function drawHUD(ctx, score, highScore, combo, multiplier) {
  // Score
  ctx.font = 'bold 22px Inter, sans-serif';
  ctx.textAlign = 'left';
  ctx.textBaseline = 'top';
  ctx.fillStyle = C.white;
  ctx.fillText(`Score: ${score}`, 14, 14);

  // High score
  ctx.font = '15px Inter, sans-serif';
  ctx.fillStyle = C.gray;
  ctx.fillText(`High Score: ${highScore}`, 14, 44);

  // Combo
  if (combo > 0) {
    let comboColor = C.white;
    if (combo >= 10) comboColor = '#ff44ff';
    else if (combo >= 5) comboColor = C.gold;
    else if (combo >= 3) comboColor = C.green;

    ctx.font = `bold ${18 + Math.min(combo, 10)}px Inter, sans-serif`;
    ctx.textAlign = 'center';
    ctx.fillStyle = comboColor;
    ctx.fillText(`COMBO ×${combo}`, CANVAS_WIDTH / 2, 18);

    if (multiplier > 1) {
      ctx.font = '14px Inter, sans-serif';
      ctx.fillText(`${multiplier.toFixed(1)}× Points!`, CANVAS_WIDTH / 2, 46);
    }
    ctx.textAlign = 'left';
  }
}

// ── Power-up bar ──────────────────────────────────────────
export function drawPowerUpBar(ctx, activePowerUp, timerMs) {
  if (!activePowerUp) return;
  const sec = (timerMs / 1000).toFixed(1);
  ctx.font = 'bold 14px Inter, sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'bottom';
  ctx.fillStyle = activePowerUp.color;
  ctx.fillText(`⚡ ${activePowerUp.name.toUpperCase()} (${sec}s)`, CANVAS_WIDTH / 2, CANVAS_HEIGHT - 12);
  ctx.textAlign = 'left';
  ctx.textBaseline = 'top';
}

// ── Button helpers ────────────────────────────────────────
/**
 * @typedef {{ label:string, x:number, y:number, w:number, h:number, action:function }} Btn
 */

export function makeButton(label, yOffset, action) {
  return {
    label,
    x: CANVAS_WIDTH / 2 - BUTTON_W / 2,
    y: CANVAS_HEIGHT / 2 + yOffset,
    w: BUTTON_W,
    h: BUTTON_H,
    action,
  };
}

export function drawButton(ctx, btn, mx, my) {
  const hover = mx >= btn.x && mx <= btn.x + btn.w &&
                my >= btn.y && my <= btn.y + btn.h;

  // Background
  ctx.fillStyle = hover ? '#4a90e2' : C.blue;
  ctx.beginPath();
  ctx.roundRect(btn.x, btn.y, btn.w, btn.h, BUTTON_R);
  ctx.fill();

  // Border
  ctx.strokeStyle = hover ? C.white : 'rgba(255,255,255,0.15)';
  ctx.lineWidth = 2;
  ctx.stroke();

  // Label
  ctx.font = 'bold 18px Inter, sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle = C.white;
  ctx.fillText(btn.label, btn.x + btn.w / 2, btn.y + btn.h / 2);
  ctx.textAlign = 'left';
  ctx.textBaseline = 'top';

  return hover;
}

/** Returns the button that was hit, or null. */
export function hitTestButtons(buttons, mx, my) {
  for (const b of buttons) {
    if (mx >= b.x && mx <= b.x + b.w && my >= b.y && my <= b.y + b.h) return b;
  }
  return null;
}

// ── Title ─────────────────────────────────────────────────
export function drawTitle(ctx, text, y = 90) {
  ctx.font = 'bold 52px Outfit, Inter, sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  // Glow
  ctx.shadowColor = C.blue;
  ctx.shadowBlur = 24;
  ctx.fillStyle = C.white;
  ctx.fillText(text, CANVAS_WIDTH / 2, y);
  ctx.shadowBlur = 0;
  ctx.textAlign = 'left';
  ctx.textBaseline = 'top';
}

// ── Overlay ───────────────────────────────────────────────
export function drawOverlay(ctx, alpha = 0.55) {
  ctx.fillStyle = `rgba(0,0,0,${alpha})`;
  ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
}

// ── Centered text line helper ─────────────────────────────
export function drawCenteredText(ctx, text, y, font = '18px Inter, sans-serif', color = C.white) {
  ctx.font = font;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle = color;
  ctx.fillText(text, CANVAS_WIDTH / 2, y);
  ctx.textAlign = 'left';
  ctx.textBaseline = 'top';
}
