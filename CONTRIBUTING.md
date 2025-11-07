# Contributing to Falling Frenzy 🎮

First off, thank you for considering contributing to Falling Frenzy! It's people like you that make this project better.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

---

## Code of Conduct

This project and everyone participating in it is governed by basic principles of respect and professionalism. Please:

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

---

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When submitting a bug report, include:**
- Clear and descriptive title
- Steps to reproduce the behavior
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Your environment (OS, Python version, Pygame version)
- Error messages or logs

**Example:**
```markdown
**Title:** Game crashes when catching purple object

**Description:**
The game crashes with a KeyError when catching a purple falling object.

**Steps to Reproduce:**
1. Start the game
2. Wait for a purple object to appear
3. Catch it with the basket
4. Game crashes

**Error Message:**
```
KeyError: 'purple' in audio.py, line 42
```

**Environment:**
- OS: macOS 14.0
- Python: 3.11.5
- Pygame: 2.5.2
```

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**When suggesting an enhancement, include:**
- Clear and descriptive title
- Detailed description of the proposed feature
- Why this enhancement would be useful
- Possible implementation approach (optional)

### 🎨 Contributing Assets

We welcome contributions of graphics and sound assets!

**For Graphics:**
- PNG format with transparency
- Appropriate resolution (32x32 to 64x64 for objects)
- Consistent art style
- Place in `assets/images/`

**For Sounds:**
- WAV or OGG format
- Clear, high quality audio
- Appropriate volume levels
- Place in `assets/sounds/`

### 💻 Contributing Code

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- pip

### Setup Steps

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/Falling-Frenzy.git
cd Falling-Frenzy

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run tests to verify setup
pytest tests/ -v

# 5. Run the game
python main.py
```

---

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with these specific guidelines:

**1. Type Hints**
Always use type hints for function parameters and return values:

```python
def spawn_object(x: int, y: int, speed: float) -> FallingObject:
    """Spawn a new falling object."""
    return FallingObject(x, y, ObjectType.RED, speed)
```

**2. Docstrings**
Use Google-style docstrings for all classes and methods:

```python
def calculate_score(base_points: int, multiplier: float) -> int:
    """
    Calculate the final score with multiplier.
    
    Args:
        base_points: Base point value
        multiplier: Score multiplier
        
    Returns:
        Final calculated score
    """
    return int(base_points * multiplier)
```

**3. Naming Conventions**
- `snake_case` for functions and variables
- `PascalCase` for classes
- `UPPER_CASE` for constants
- Descriptive names (avoid single letters except in loops)

**4. Code Organization**
- Keep functions small and focused (< 50 lines)
- One class per file when appropriate
- Group related functionality
- Minimize nesting depth

**5. Comments**
- Write self-documenting code
- Add comments for complex logic
- Avoid obvious comments
- Keep comments up-to-date

### Project Structure

When adding new features:
- Put game logic in `src/game.py`
- Put entity classes in `src/entities.py`
- Put UI components in `src/ui.py`
- Put configuration in `src/config.py`
- Put utility functions in `src/utils.py`
- Put tests in `tests/`

---

## Commit Guidelines

### Commit Message Format

Use conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes (formatting, missing semi-colons, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvement
- `test`: Adding or updating tests
- `chore`: Changes to build process or auxiliary tools

**Examples:**

```bash
# Good commits
feat(powerups): add shield power-up that prevents score loss
fix(collision): correct basket boundary detection
docs(readme): update installation instructions
refactor(entities): extract particle system to separate class
test(score): add tests for combo multiplier calculation

# Bad commits
fix stuff
updated code
changes
```

### Branch Naming

Use descriptive branch names:
- `feature/add-new-powerup`
- `fix/collision-detection-bug`
- `refactor/entity-system`
- `docs/update-contributing-guide`

---

## Pull Request Process

### Before Submitting

**Checklist:**
- [ ] Code follows the style guidelines
- [ ] All tests pass (`pytest tests/`)
- [ ] New tests added for new features
- [ ] Documentation updated if needed
- [ ] No merge conflicts with main branch
- [ ] Commit messages follow guidelines

### Submitting a Pull Request

1. **Update your fork:**
```bash
git fetch upstream
git checkout main
git merge upstream/main
```

2. **Create a feature branch:**
```bash
git checkout -b feature/amazing-feature
```

3. **Make your changes and commit:**
```bash
git add .
git commit -m "feat: add amazing feature"
```

4. **Push to your fork:**
```bash
git push origin feature/amazing-feature
```

5. **Open a Pull Request on GitHub**

### Pull Request Description

Include in your PR description:
- What does this PR do?
- Why is this change needed?
- How has this been tested?
- Screenshots (if applicable)
- Related issues

**Template:**

```markdown
## Description
Brief description of what this PR does.

## Motivation
Why is this change necessary?

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
How was this tested?

## Screenshots
(if applicable)

## Related Issues
Fixes #123
```

### Code Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, a maintainer will merge your PR
- Your contribution will be acknowledged in the changelog!

---

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_game.py

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Writing Tests

When adding new features, include tests:

```python
def test_new_feature():
    """Test description."""
    # Arrange
    game = Game()
    
    # Act
    result = game.new_feature()
    
    # Assert
    assert result == expected_value
```

---

## Getting Help

If you need help:
- Check existing documentation
- Look through closed issues
- Open a new issue with the `question` label
- Reach out to maintainers

---

## Recognition

Contributors will be:
- Listed in the changelog
- Mentioned in release notes
- Forever appreciated! 🎉

---

Thank you for contributing to Falling Frenzy! 🚀
