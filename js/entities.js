/**
 * Falling Frenzy — Game Entities
 * Basket, FallingObject, PowerUp, ParticleSystem
 */
import {
  CANVAS_WIDTH, CANVAS_HEIGHT,
  BASKET_WIDTH, BASKET_HEIGHT, BASKET_SPEED,
  OBJECT_RADIUS,
  ObjectType, PowerUpType,
  PARTICLE_LIFETIME, PARTICLE_SPEED_MIN, PARTICLE_SPEED_MAX,
  PARTICLE_SIZE_MIN, PARTICLE_SIZE_MAX,
  C,
} from './config.js';

// ── Basket ────────────────────────────────────────────────
export class Basket {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.w = BASKET_WIDTH;
    this.h = BASKET_HEIGHT;
    this.speed = BASKET_SPEED;
    this.vx = 0;
    // Mouse / touch drag support
    this.dragging = false;
    this.dragOffsetX = 0;
  }

  update(keys, dt) {
    if (this.dragging) return;              // drag overrides keyboard
    this.vx = 0;
    if (keys.left)  this.vx = -this.speed;
    if (keys.right) this.vx =  this.speed;
    this.x += this.vx * dt * 60;
    this.x = Math.max(0, Math.min(this.x, CANVAS_WIDTH - this.w));
  }

  /** Move basket center to x during drag. */
  dragTo(x) {
    this.x = Math.max(0, Math.min(x - this.w / 2, CANVAS_WIDTH - this.w));
  }

  draw(ctx) {
    const r = 10;
    // Main body
    ctx.fillStyle = C.blue;
    ctx.beginPath();
    ctx.roundRect(this.x, this.y, this.w, this.h, r);
    ctx.fill();
    // Highlight strip
    ctx.fillStyle = 'rgba(255,255,255,0.25)';
    ctx.beginPath();
    ctx.roundRect(this.x + 6, this.y + 2, this.w - 12, this.h * 0.35, 4);
    ctx.fill();
  }

  rect() {
    return { x: this.x, y: this.y, w: this.w, h: this.h };
  }

  center() {
    return { x: this.x + this.w / 2, y: this.y + this.h / 2 };
  }
}

// ── Falling Object ────────────────────────────────────────
export class FallingObject {
  constructor(x, y, type, speed) {
    this.x = x;
    this.y = y;
    this.r = OBJECT_RADIUS;
    this.type = type;
    this.speed = speed;
    this.rotation = 0;
    this.rotSpeed = (Math.random() - 0.5) * 10;
    this.scale = 1;
    this.pulse = 0;
  }

  update(dt, speedMult = 1) {
    this.y += this.speed * speedMult * dt * 60;
    this.rotation += this.rotSpeed * dt;
    if (this.type === ObjectType.PURPLE) {
      this.pulse += dt * 10;
      this.scale = 1 + Math.sin(this.pulse) * 0.1;
    } else if (this.type === ObjectType.BOMB) {
      this.pulse += dt * 8;
      this.scale = 1 + Math.sin(this.pulse) * 0.15;
    }
  }

  draw(ctx) {
    const cx = this.x;
    const cy = this.y;
    const sr = this.r * this.scale;

    if (this.type.isBomb) {
      // Black body
      ctx.beginPath();
      ctx.arc(cx, cy, sr, 0, Math.PI * 2);
      ctx.fillStyle = '#1e1e1e';
      ctx.fill();
      // Red outline
      ctx.strokeStyle = C.red;
      ctx.lineWidth = 2.5;
      ctx.stroke();
      // Fuse
      ctx.beginPath();
      ctx.moveTo(cx, cy - sr);
      ctx.lineTo(cx, cy - sr - 10);
      ctx.strokeStyle = '#888';
      ctx.lineWidth = 2.5;
      ctx.stroke();
      // Spark
      const sparkBright = 200 + 55 * Math.sin(this.pulse * 3);
      ctx.beginPath();
      ctx.arc(cx, cy - sr - 10, 3.5, 0, Math.PI * 2);
      ctx.fillStyle = `rgb(255,${Math.round(sparkBright)},0)`;
      ctx.fill();
      // Skull emoji
      ctx.font = '16px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('💣', cx, cy);
    } else {
      // Circle body
      ctx.beginPath();
      ctx.arc(cx, cy, sr, 0, Math.PI * 2);
      ctx.fillStyle = this.type.color;
      ctx.fill();
      // Highlight
      ctx.beginPath();
      ctx.arc(cx - sr * 0.25, cy - sr * 0.25, sr * 0.38, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255,255,255,0.35)';
      ctx.fill();
      // Points label
      ctx.font = 'bold 13px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = '#fff';
      ctx.fillText(`+${this.type.points}`, cx, cy);
    }
  }

  getRect() {
    return { x: this.x - this.r, y: this.y - this.r, w: this.r * 2, h: this.r * 2 };
  }

  isOffScreen() { return this.y - this.r > CANVAS_HEIGHT; }

  center() { return { x: this.x, y: this.y }; }
}

// ── Power-Up ──────────────────────────────────────────────
export class PowerUp {
  constructor(x, y, type, speed) {
    this.x = x;
    this.y = y;
    this.r = OBJECT_RADIUS;
    this.type = type;
    this.speed = speed;
    this.rot = 0;
    this.glow = 0;
  }

  update(dt) {
    this.y += this.speed * dt * 60;
    this.rot += 2 * dt * 60;
    this.glow = (Math.sin(performance.now() / 200) + 1) / 2;
  }

  draw(ctx) {
    const cx = this.x;
    const cy = this.y;
    // Glow
    const gr = this.r + 10 * this.glow;
    ctx.beginPath();
    ctx.arc(cx, cy, gr, 0, Math.PI * 2);
    ctx.fillStyle = this.type.color + '44';
    ctx.fill();
    // Star
    ctx.beginPath();
    for (let i = 0; i < 10; i++) {
      const a = (this.rot * Math.PI / 180) + i * (Math.PI / 5);
      const rad = i % 2 === 0 ? this.r : this.r * 0.5;
      const sx = cx + rad * Math.cos(a);
      const sy = cy + rad * Math.sin(a);
      i === 0 ? ctx.moveTo(sx, sy) : ctx.lineTo(sx, sy);
    }
    ctx.closePath();
    ctx.fillStyle = this.type.color;
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 1.5;
    ctx.stroke();
    // Label
    ctx.font = 'bold 9px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#fff';
    ctx.fillText(this.type.name, cx, cy);
  }

  getRect() {
    return { x: this.x - this.r, y: this.y - this.r, w: this.r * 2, h: this.r * 2 };
  }

  isOffScreen() { return this.y - this.r > CANVAS_HEIGHT; }

  center() { return { x: this.x, y: this.y }; }
}

// ── Particle System ───────────────────────────────────────
class Particle {
  constructor(x, y, vx, vy, color, size) {
    this.x = x; this.y = y;
    this.vx = vx; this.vy = vy;
    this.color = color;
    this.size = size;
    this.life = PARTICLE_LIFETIME;
    this.age = 0;
  }

  update(dt) {
    const dt60 = dt * 60;
    this.x += this.vx * dt60;
    this.y += this.vy * dt60;
    this.vy += 0.3;
    this.age += dt * 1000;
    return this.age < this.life;
  }

  draw(ctx) {
    const alpha = 1 - this.age / this.life;
    const s = Math.max(1, this.size * alpha);
    ctx.globalAlpha = alpha;
    ctx.beginPath();
    ctx.arc(this.x, this.y, s, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.fill();
    ctx.globalAlpha = 1;
  }
}

export class ParticleSystem {
  constructor() { this.particles = []; }

  emit(x, y, color, count = 10) {
    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = PARTICLE_SPEED_MIN + Math.random() * (PARTICLE_SPEED_MAX - PARTICLE_SPEED_MIN);
      const vx = Math.cos(angle) * speed;
      const vy = Math.sin(angle) * speed - 2;
      const size = PARTICLE_SIZE_MIN + Math.random() * (PARTICLE_SIZE_MAX - PARTICLE_SIZE_MIN);
      this.particles.push(new Particle(x, y, vx, vy, color, size));
    }
  }

  update(dt) {
    this.particles = this.particles.filter(p => p.update(dt));
  }

  draw(ctx) {
    for (const p of this.particles) p.draw(ctx);
  }

  clear() { this.particles = []; }
}
