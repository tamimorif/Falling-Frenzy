# Changelog

All notable changes to Falling Frenzy will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-11-07

### Added - Complete Rewrite! 🎉
- **Professional Architecture**: Complete OOP refactor with proper separation of concerns
- **Project Structure**: Organized into `src/`, `assets/`, `tests/`, and `data/` directories
- **Configuration System**: All constants centralized in `config.py` with enums
- **Entity System**: Proper classes for Basket, FallingObject, PowerUp, and Particle
- **Manager Classes**: ScoreManager, StatisticsManager, SettingsManager, AudioManager
- **UI System**: Professional menus, buttons, HUD, and background renderer
- **Particle Effects**: Dynamic particle system for visual feedback on catches
- **Power-up System**: 4 power-ups (Slow Motion, Double Points, Shield, Magnet)
- **Combo System**: Chain catches for score multipliers up to 2.5x
- **Adaptive Difficulty**: Progressively increases speed and spawn rate
- **Statistics Tracking**: Comprehensive stats (games played, average score, catch rate, play time)
- **Settings System**: Persistent settings with JSON storage
- **Audio System**: Complete audio manager with placeholder sound generation
- **Multiple Menus**: Main menu, pause menu, game over, statistics, and settings screens
- **Gradient Background**: Animated starfield with parallax scrolling
- **Testing Suite**: Comprehensive unit tests with pytest
- **Type Hints**: Full type annotations throughout the codebase
- **Documentation**: Docstrings for all classes and methods
- **Purple Objects**: Rare high-value objects (5 points)
- **Delta Time**: Frame-rate independent physics
- **Professional README**: Comprehensive documentation with badges and formatting

### Changed
- Moved from single-file to modular architecture
- Increased base FPS from 30 to 60
- Improved collision detection accuracy
- Enhanced visual feedback with particles and animations
- Better UI with hover effects and smooth transitions
- Starting score increased from 10 to 10 (kept same but now with better balance)

### Technical Improvements
- Object-Oriented Design with proper encapsulation
- Separation of rendering, logic, and input handling
- Manager pattern for subsystems
- Enum-based state management
- Dataclasses for simple data structures
- Comprehensive error handling
- Memory-efficient particle system
- Optimized rendering pipeline

### Developer Experience
- Added `.gitignore` for Python projects
- Added `requirements.txt` for dependency management
- Added comprehensive test suite
- Added type hints for better IDE support
- Added documentation for all major components
- Added professional project structure

## [1.0.0] - 2025-11-06

### Initial Release
- Basic catching game mechanics
- Simple basket and falling objects
- Score and high score tracking
- Basic menu system
- Three object types (red, green, yellow)
- Simple collision detection
- High score persistence to file

---

## Upcoming Features

### [2.1.0] - Planned
- [ ] Custom sprite graphics for all objects
- [ ] Real sound effects and background music
- [ ] Achievement system
- [ ] Multiple difficulty modes
- [ ] Controller support
- [ ] Fullscreen toggle
- [ ] Screen shake effects

### [3.0.0] - Future
- [ ] Online leaderboards
- [ ] Multiple game modes (timed, survival, endless)
- [ ] Level system with themes
- [ ] Character/basket customization
- [ ] Special events and challenges
- [ ] Mobile port
- [ ] Replay system
