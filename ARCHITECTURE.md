# 🏗️ Architecture Documentation

## Table of Contents
- [Overview](#overview)
- [Design Principles](#design-principles)
- [Project Structure](#project-structure)
- [Core Systems](#core-systems)
- [Data Flow](#data-flow)
- [Class Diagram](#class-diagram)
- [State Management](#state-management)
- [Extension Points](#extension-points)

---

## Overview

Falling Frenzy is built using **Object-Oriented Programming** principles with a focus on:
- **Separation of Concerns**: Each module has a single, well-defined purpose
- **Composition**: Systems are built from composable components
- **Encapsulation**: Internal state is hidden, exposed through clean APIs
- **Type Safety**: Full type hints for better IDE support and fewer bugs

### Architecture Pattern

The game follows a **Component-Based Architecture** with clear separation between:
- **Entities** (game objects)
- **Systems** (managers and controllers)
- **UI** (rendering and interaction)
- **Configuration** (constants and settings)

---

## Design Principles

### 1. Single Responsibility Principle
Each class has one reason to change:
- `Basket`: Player-controlled entity
- `ScoreManager`: Score and combo logic
- `AudioManager`: Sound effects and music
- `Game`: Game loop orchestration

### 2. Dependency Injection
Dependencies are passed explicitly:
```python
def __init__(self, score_manager: ScoreManager, audio_manager: AudioManager):
    self.score_manager = score_manager
    self.audio_manager = audio_manager
```

### 3. Configuration Over Hard-Coding
All constants are in `config.py`:
```python
from src.config import SCREEN_WIDTH, BASKET_SPEED, ObjectType
```

### 4. Type Safety
Full type hints throughout:
```python
def spawn_object(x: int, y: int, speed: float) -> FallingObject:
    return FallingObject(x, y, ObjectType.RED, speed)
```

---

## Project Structure

```
src/
├── __init__.py       # Package metadata
├── config.py         # ALL constants, enums, and configuration
├── entities.py       # Game entities (Basket, Objects, Particles)
├── utils.py          # Manager classes (Score, Stats, Settings)
├── ui.py             # UI components (Menu, Button, HUD)
├── audio.py          # Audio system
└── game.py           # Main game loop and orchestration
```

### Module Responsibilities

| Module | Responsibility | Dependencies |
|--------|---------------|--------------|
| `config.py` | Constants and configuration | None |
| `entities.py` | Game objects and behavior | `config.py`, `pygame` |
| `utils.py` | Cross-cutting concerns | `config.py`, `json` |
| `ui.py` | User interface | `config.py`, `pygame` |
| `audio.py` | Sound management | `config.py`, `pygame.mixer` |
| `game.py` | Game loop orchestration | All of the above |

---

## Core Systems

### 1. Entity System (`entities.py`)

**Basket**
- Player-controlled entity
- Handles input and physics
- Bounded movement within screen

**FallingObject**
- Objects that fall from top
- Different types with point values
- Animation (rotation, scaling)

**PowerUp**
- Special collectibles
- Temporary effects
- Animated appearance (glow, rotation)

**ParticleSystem**
- Visual effects manager
- Spawns and updates particles
- Particle lifecycle management

### 2. Manager System (`utils.py`)

**ScoreManager**
```python
class ScoreManager:
    - score: int
    - high_score: int
    - combo: int
    + add_points(points: int, multiplier: float) -> int
    + subtract_points(points: int) -> None
    + get_combo_multiplier() -> float
```

**StatisticsManager**
- Tracks long-term stats
- Session management
- JSON persistence

**SettingsManager**
- User preferences
- Volume controls
- Display settings

### 3. UI System (`ui.py`)

**Component Hierarchy**
```
Menu
├── TextElement (multiple)
└── Button (multiple)
    └── callback: Callable

HUD
├── Score display
├── Combo indicator
└── FPS counter

Background
├── Gradient renderer
└── Star field animation
```

### 4. Audio System (`audio.py`)

**AudioManager**
- Sound effect management
- Music playback
- Volume controls
- Graceful degradation (placeholder sounds)

---

## Data Flow

### Game Loop Flow

```
┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Initialize     │
│  - Pygame       │
│  - Managers     │
│  - Entities     │
└────────┬────────┘
         │
         ▼
    ┌────────────┐
    │ Game Loop  │◄─────┐
    └─────┬──────┘      │
          │             │
          ▼             │
    ┌──────────────┐    │
    │ Handle Input │    │
    └─────┬────────┘    │
          │             │
          ▼             │
    ┌──────────────┐    │
    │ Update Logic │    │
    │ - Entities   │    │
    │ - Physics    │    │
    │ - Collisions │    │
    └─────┬────────┘    │
          │             │
          ▼             │
    ┌──────────────┐    │
    │    Render    │    │
    │ - Background │    │
    │ - Entities   │    │
    │ - UI         │    │
    └─────┬────────┘    │
          │             │
          ▼             │
    ┌──────────────┐    │
    │  60 FPS Cap  │────┘
    └──────────────┘
```

### Event Flow

```
User Input
    │
    ▼
Event Queue (Pygame)
    │
    ├─── Key Press ────► Basket Movement
    │
    ├─── Mouse Click ──► Button Callback
    │
    └─── Quit ─────────► Exit Game
```

### Score Flow

```
Catch Object
    │
    ▼
ScoreManager.add_points()
    │
    ├─► Calculate Multiplier (Combo)
    │
    ├─► Apply Power-up Bonus
    │
    ├─► Update Score
    │
    ├─► Update Combo
    │
    └─► Check High Score
        │
        └─► Save if New High Score
```

---

## Class Diagram

```
┌─────────────────┐
│      Game       │
├─────────────────┤
│ - state         │
│ - basket        │
│ - objects[]     │
│ - powerups[]    │
├─────────────────┤
│ + run()         │
│ + _update()     │
│ + _render()     │
└────────┬────────┘
         │
         │ uses
         │
    ┌────┴────────────────────┬─────────────────┬────────────────┐
    │                         │                 │                │
    ▼                         ▼                 ▼                ▼
┌────────────┐      ┌──────────────┐   ┌─────────────┐  ┌──────────────┐
│   Basket   │      │FallingObject │   │  PowerUp    │  │ScoreManager  │
├────────────┤      ├──────────────┤   ├─────────────┤  ├──────────────┤
│ - x, y     │      │ - x, y       │   │ - x, y      │  │ - score      │
│ - speed    │      │ - type       │   │ - type      │  │ - combo      │
├────────────┤      │ - speed      │   │ - effect    │  ├──────────────┤
│ + update() │      ├──────────────┤   ├─────────────┤  │ + add_pts()  │
│ + draw()   │      │ + update()   │   │ + update()  │  │ + subtract() │
└────────────┘      │ + draw()     │   │ + draw()    │  └──────────────┘
                    └──────────────┘   └─────────────┘
```

---

## State Management

### Game States (Enum)

```python
class GameState(Enum):
    MAIN_MENU = "main_menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    STATISTICS = "statistics"
    SETTINGS = "settings"
```

### State Transitions

```
MAIN_MENU
    │
    ├─── Start ──────► PLAYING
    ├─── Stats ──────► STATISTICS ───► Back ───► MAIN_MENU
    ├─── Settings ───► SETTINGS ─────► Back ───► MAIN_MENU
    └─── Quit ───────► EXIT

PLAYING
    │
    ├─── ESC ────────► PAUSED ────► Resume ───► PLAYING
    │                      │
    │                      └────► Menu ────────► MAIN_MENU
    │
    └─── Score = 0 ──► GAME_OVER
                           │
                           ├─── Play Again ──► PLAYING
                           └─── Menu ────────► MAIN_MENU
```

### State Handling

```python
def _handle_state(self):
    if self.state == GameState.PLAYING:
        self._update_playing()
    elif self.state == GameState.MAIN_MENU:
        self.main_menu.update()
    elif self.state == GameState.PAUSED:
        self.pause_menu.update()
    # ... etc
```

---

## Extension Points

### Adding New Object Types

1. Add to `ObjectType` enum in `config.py`:
```python
class ObjectType(Enum):
    NEW_TYPE = ("new_type", COLOR, POINTS)
```

2. Object automatically supported by existing code!

### Adding New Power-ups

1. Add to `PowerUpType` enum in `config.py`:
```python
class PowerUpType(Enum):
    NEW_POWERUP = ("name", COLOR, EFFECT_VALUE)
```

2. Add handling in `game.py`:
```python
if self.active_powerup == PowerUpType.NEW_POWERUP:
    # Apply effect
```

### Adding New Game Modes

1. Add state to `GameState` enum
2. Create menu in `_create_menus()`
3. Add handler in `_handle_input()`
4. Add update logic in `_update_<mode>()`
5. Add rendering in `_render()`

### Custom Graphics

1. Load images in entity `__init__`:
```python
self.image = pygame.image.load(IMAGES_DIR / "basket.png")
```

2. Replace draw logic:
```python
def draw(self, surface):
    surface.blit(self.image, (self.x, self.y))
```

### Custom Sounds

1. Add sound file to `assets/sounds/`
2. Load in `AudioManager.load_all_sounds()`
3. Play with `audio_manager.play_sound("name")`

---

## Performance Considerations

### Optimization Techniques Used

1. **Object Pooling**: Particles reused instead of recreated
2. **Delta Time**: Frame-rate independent physics
3. **Dirty Rectangles**: Only update changed regions (TODO)
4. **Efficient Collision**: Simple rect collision, not per-pixel
5. **Limited Spawns**: Cap max objects on screen

### Profiling

To profile the game:
```python
import cProfile
cProfile.run('game.run()', 'profile_output')

# Analyze
import pstats
p = pstats.Stats('profile_output')
p.sort_stats('cumulative').print_stats(20)
```

---

## Testing Strategy

### Unit Tests
- Entity behavior
- Manager logic
- Score calculations
- Collision detection

### Integration Tests
- Game loop flow
- State transitions
- Save/Load functionality

### Manual Tests
- Visual appearance
- User experience
- Performance on target hardware

---

## Future Architecture Improvements

### Planned Refactors

1. **Entity Component System (ECS)**
   - Separate data from behavior
   - Better performance for many entities

2. **Event System**
   - Decouple components
   - Observer pattern for game events

3. **Scene System**
   - Manage different game screens
   - Easier state transitions

4. **Resource Manager**
   - Centralized asset loading
   - Memory management

5. **Save System**
   - Serialize game state
   - Save/load functionality

---

## Contributing to Architecture

When adding features:

1. **Follow existing patterns**: Use similar structure to current code
2. **Maintain separation**: Don't mix concerns
3. **Add documentation**: Update this file with major changes
4. **Write tests**: Cover new functionality
5. **Type hints**: Maintain type safety

Questions? Open an issue with the `architecture` label!
