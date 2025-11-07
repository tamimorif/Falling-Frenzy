# 🚀 Quick Start Guide - Falling Frenzy

Get up and running with Falling Frenzy in under 2 minutes!

## ⚡ Super Quick Start (3 commands)

```bash
git clone https://github.com/tamimorif/Falling-Frenzy.git
cd Falling-Frenzy
pip3 install --break-system-packages pygame-ce  # or pygame
python3 main.py
```

That's it! You're playing! 🎮

---

## 📦 Detailed Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/tamimorif/Falling-Frenzy.git
cd Falling-Frenzy
```

### Step 2: Install Dependencies

**On macOS:**
```bash
pip3 install --break-system-packages pygame-ce
```

**On Windows:**
```bash
pip install pygame
```

**On Linux:**
```bash
pip3 install pygame
```

**Alternative (using virtual environment - recommended for development):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pygame
```

### Step 3: Run the Game

```bash
python3 main.py  # On Windows: python main.py
```

---

## 🎮 First-Time Playing?

### Controls
- **← / A**: Move basket left
- **→ / D**: Move basket right
- **ESC**: Pause game
- **Mouse**: Click buttons in menus

### Quick Tips
1. Start with the **Start Game** button from main menu
2. Catch colored objects to score points
3. Don't let objects fall - you lose points!
4. Build combos by catching consecutively (3+ for bonuses)
5. Grab power-ups (star shapes) for special abilities
6. Game ends when score reaches 0

### Scoring Guide
- 🔴 Red = 1 point
- 🟢 Green = 2 points
- 🟡 Yellow = 3 points
- 🟣 Purple (rare) = 5 points
- Missing object = -1 point

---

## ⚠️ Troubleshooting

### "No module named 'pygame'"
```bash
# Install pygame
pip3 install --break-system-packages pygame-ce  # macOS
pip install pygame  # Windows/Linux
```

### "command not found: python"
Try `python3` instead of `python`:
```bash
python3 main.py
```

### "SDL.h not found" error
Use pygame-ce instead which has precompiled wheels:
```bash
pip3 install --break-system-packages pygame-ce
```

### Game window doesn't open
- Make sure you have a display (won't work over SSH without X11)
- Check that pygame installed correctly: `python3 -c "import pygame; print(pygame.ver)"`
- Try updating pygame: `pip3 install --upgrade pygame-ce`

### Performance issues
- Check FPS in settings menu
- Close other applications
- Update graphics drivers
- Disable particles in settings (future feature)

---

## 🧪 Running Tests (Optional)

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src
```

---

## 🎯 What's Next?

- Check out the full [README.md](README.md) for detailed documentation
- Read [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute
- View [CHANGELOG.md](CHANGELOG.md) to see what's new
- Open an issue if you find bugs or have suggestions

---

## 🆘 Need Help?

- **Documentation**: Read the full [README.md](README.md)
- **Issues**: Check [existing issues](https://github.com/tamimorif/Falling-Frenzy/issues)
- **Questions**: Open a new issue with the `question` label

---

## 🎉 Enjoy the Game!

Have fun playing Falling Frenzy! If you enjoy it, please:
- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest features
- 🤝 Contribute improvements

Happy catching! 🎮✨
