# 🎮 Falling Frenzy

A fast-paced arcade game built with **HTML5 Canvas** and vanilla JavaScript — catch the falling objects, build combos, grab power-ups, and avoid the bombs!

## ▶️ Play Now

👉 **[Play Falling Frenzy](https://tamimorif.github.io/Falling-Frenzy/)** — runs directly in your browser, no install needed.

## 🕹️ Controls

| Input | Action |
|-------|--------|
| ← → Arrow Keys | Move basket |
| A / D | Move basket |
| Click & Drag | Move basket (mouse) |
| Touch & Drag | Move basket (mobile) |
| Escape | Pause / Resume |

## 🎯 How to Play

- **Catch** falling objects to earn points
- **Red** = +1 · **Green** = +2 · **Yellow** = +3 · **Purple** = +5 (rare!)
- **Avoid bombs** 💣 — they cost you 3 points and reset your combo
- Build **combos** by catching objects in quick succession for multiplied points
- Grab glowing **power-ups** ⚡ for temporary boosts:
  - 🔵 **Slow-Mo** — slows all falling objects
  - 🟡 **2× Points** — doubles your score gain
  - 🟣 **Shield** — missed objects don't cost points
- Game starts with **10 points** — if you hit **0**, it's game over!
- Difficulty increases over time — objects fall faster and spawn more frequently

## 🏗️ Tech Stack

- Pure **HTML5 Canvas** + **vanilla JavaScript** (ES modules)
- **CSS** with glassmorphism dark-mode design
- **Web Audio API** for procedural sound effects
- **localStorage** for persistent high scores
- Zero dependencies — no build step required

## 📂 Project Structure

```
├── index.html        Main page
├── styles.css        Global styles
├── js/
│   ├── config.js     Constants & enums
│   ├── entities.js   Basket, FallingObject, PowerUp, Particles
│   ├── game.js       Main game loop & state machine
│   ├── ui.js         Canvas rendering (HUD, menus, background)
│   ├── audio.js      Procedural Web Audio sounds
│   └── utils.js      Score & statistics managers
└── src/              Legacy Python source (reference only)
```

## 🚀 Run Locally

Just open `index.html` in a browser, or start a local server:

```bash
npx serve .
```

## 📜 License

MIT
