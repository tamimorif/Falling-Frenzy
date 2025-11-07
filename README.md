# 🎮 **Falling Frenzy** 

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/Version-2.0.0-orange.svg)

A professional, feature-rich arcade-style catching game built with Python and Pygame. Experience smooth animations, particle effects, power-ups, combo systems, and adaptive difficulty!

[Features](#-features) • [Installation](#-installation) • [Gameplay](#-gameplay) • [Architecture](#-architecture) • [Development](#-development)

</div>

---

## ✨ **Features**

### 🎯 **Core Gameplay**
- **Dynamic Difficulty**: Speed and spawn rates increase progressively
- **Combo System**: Chain catches for score multipliers up to 2.5x
- **Multiple Object Types**: 4 types with different point values (1-5 points)
- **Smooth Physics**: Frame-rate independent movement with delta time
- **Smart Collision Detection**: Pixel-perfect collision handling

### ⚡ **Power-ups**
- **Slow Motion**: Slows down falling objects (50% speed)
- **Double Points**: 2x score multiplier
- **Shield**: Prevents score loss on misses
- **Magnet**: Attracts nearby objects

### 🎨 **Visual Polish**
- **Particle Effects**: Dynamic particle system for visual feedback
- **Gradient Background**: Animated starfield with parallax effect
- **Smooth Animations**: Object rotation and pulsing effects
- **Professional UI**: Custom buttons with hover states
- **HUD System**: Real-time score, combo, and stats display

### 📊 **Progression & Stats**
- **High Score Tracking**: Persistent storage across sessions
- **Comprehensive Statistics**: Games played, average score, catch rate, play time
- **Best Combo Tracking**: Record your longest combo streak
- **Session Management**: Automatic stat updates after each game

### 🎵 **Audio System** (Ready for assets)
- **Sound Effects**: Catch, miss, power-up, combo, game over sounds
- **Background Music**: Looping music with volume control
- **Dynamic Audio**: Placeholder sound generation when assets missing
- **Volume Controls**: Separate music and sound effect volume

### 🎮 **Game Modes**
- **Main Menu**: Professional menu system with multiple options
- **Play Mode**: Fast-paced action gameplay
- **Pause System**: Pause/resume with ESC key
- **Statistics View**: Detailed performance metrics
- **Settings Menu**: Customizable game options

---

## 🛠 **Tech Stack**

- **Language**: Python 3.8+
- **Game Engine**: Pygame 2.5.2
- **Architecture**: Object-Oriented Design with MVC pattern
- **Testing**: Pytest for comprehensive unit tests
- **Type Safety**: Full type hints throughout codebase
- **Documentation**: Docstrings for all classes and methods

---

## 📥 **Installation**

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tamimorif/Falling-Frenzy.git
   cd Falling-Frenzy
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   ```bash
   python main.py
   ```

### Development Setup

For development with testing capabilities:

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

---

## 🎮 **Gameplay**

### Objective
Catch falling objects with your basket to score points. Avoid missing objects, as each miss costs you points. Reach 0 points and it's game over!

### Controls
- **Arrow Keys** / **A & D**: Move basket left and right
- **ESC**: Pause/Resume game
- **Mouse**: Navigate menus and click buttons

### Scoring System

| Object | Color | Points | Rarity |
|--------|-------|--------|--------|
| � Red | Red | +1 | Common |
| � Green | Green | +2 | Common |
| 🟡 Yellow | Yellow | +3 | Common |
| 🟣 Purple | Purple | +5 | Rare (5%) |

**Miss Penalty**: -1 point (unless Shield power-up is active)

### Combo System
- Catch consecutive objects without missing to build combos
- **3-4 combo**: 1.5x multiplier
- **5-9 combo**: 2.0x multiplier
- **10+ combo**: 2.5x multiplier
- Combo resets after 2 seconds of inactivity or missing an object

### Power-ups
Power-ups spawn randomly (5% chance) and last for 5 seconds:
- ⚡ **Slow Motion** (Light Blue): Objects fall at half speed
- � **Double Points** (Gold): 2x score multiplier
- 🛡️ **Shield** (Purple): No penalty for missed objects
- 🧲 **Magnet** (Orange): Objects attracted to basket

---

## 🏗 **Architecture**

### Project Structure
```
Falling-Frenzy/
├── src/
│   ├── __init__.py           # Package initialization
│   ├── config.py             # All game constants and enums
│   ├── entities.py           # Game entities (Basket, Objects, Particles)
│   ├── utils.py              # Managers (Score, Statistics, Settings)
│   ├── ui.py                 # UI components (Menus, Buttons, HUD)
│   ├── audio.py              # Audio system
│   └── game.py               # Main game orchestration
├── assets/
│   ├── images/               # Sprites and graphics (ready for assets)
│   ├── sounds/               # Sound effects and music (ready for assets)
│   └── fonts/                # Custom fonts (ready for assets)
├── data/
│   ├── highscore.txt         # Persistent high score
│   ├── settings.json         # User settings
│   └── statistics.json       # Game statistics
├── tests/
│   ├── __init__.py
│   └── test_game.py          # Comprehensive unit tests
├── main.py                   # Entry point
├── catch_game.py             # Legacy version (deprecated)
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

### Key Design Patterns

**Separation of Concerns**:
- `config.py`: All constants, enums, and configuration
- `entities.py`: Game objects with their own logic
- `utils.py`: Reusable managers for cross-cutting concerns
- `ui.py`: User interface components
- `game.py`: Game loop and state management

**Object-Oriented Design**:
- Classes for all major components (Basket, FallingObject, PowerUp, etc.)
- Manager classes for subsystems (ScoreManager, AudioManager, etc.)
- Composition over inheritance

**Type Safety**:
- Full type hints throughout the codebase
- Enums for game states and object types
- Dataclasses for simple data structures

---

## 🧪 **Testing**

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_game.py -v
```

Test coverage includes:
- ✅ Entity behavior (Basket, FallingObject, Particle)
- ✅ Score management and combo system
- ✅ Statistics tracking
- ✅ Settings management
- ✅ Collision detection
- ✅ Game state transitions

---

## 🚀 **Development**

### Code Quality Standards

This project follows professional Python development practices:

1. **Type Hints**: All functions include type annotations
2. **Docstrings**: Comprehensive documentation for all classes and methods
3. **Clean Code**: Meaningful variable names, small functions, DRY principle
4. **Testing**: Unit tests for critical game logic
5. **Version Control**: Clear commit messages and git workflow

### Adding New Features

1. **Fork and clone** the repository
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** following the existing code style
4. **Add tests** for new functionality
5. **Update documentation** if needed
6. **Commit**: `git commit -m "Add: amazing feature description"`
7. **Push**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Adding Assets

To add custom graphics or sounds:

1. Place image files in `assets/images/`
2. Place sound files in `assets/sounds/`
3. Update `audio.py` to load your sound files
4. Modify `entities.py` to load and render custom graphics

---

## 📈 **Performance**

- **60 FPS** gameplay with consistent frame timing
- **Delta time** implementation for frame-rate independence
- **Efficient rendering** with dirty rectangle optimization
- **Memory management** with object pooling for particles
- **Optimized collision** detection

---

## 🎯 **Future Enhancements**

Potential improvements for the next version:

- [ ] Custom sprite graphics for all game objects
- [ ] Sound effects and background music
- [ ] Multiple levels with themes
- [ ] Online leaderboards
- [ ] Achievement system
- [ ] Controller support
- [ ] Fullscreen mode
- [ ] Mobile port (Pygame for Android)
- [ ] Special game events/challenges
- [ ] Character customization

---

## 🤝 **Contributing**

Contributions are welcome! Whether it's:

- 🐛 Bug reports
- 💡 Feature suggestions
- 📝 Documentation improvements
- 🎨 Graphics and sound assets
- 💻 Code contributions

Please feel free to open an issue or submit a pull request!

---

## 📜 **License**

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## �‍💻 **Author**

**Tamir Orif**

- GitHub: [@tamimorif](https://github.com/tamimorif)
- Repository: [Falling-Frenzy](https://github.com/tamimorif/Falling-Frenzy)

---

## 🙏 **Acknowledgments**

- Built with [Pygame](https://www.pygame.org/)
- Inspired by classic arcade catching games
- Thanks to the Python and Pygame communities

---

<div align="center">

**Made with ❤️ and Python**

If you enjoyed this game, please ⭐ star the repository!

</div>
