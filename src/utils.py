"""
Utility classes for score management, statistics, and settings.
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from src.config import (
    HIGHSCORE_FILE, SETTINGS_FILE, STATISTICS_FILE,
    STARTING_SCORE, COMBO_TIMEOUT, DEFAULT_VOLUME, MUSIC_VOLUME,
    STATS_GAME_PLAYED, STATS_TOTAL_SCORE, STATS_TOTAL_TIME,
    STATS_BEST_COMBO, STATS_OBJECTS_CAUGHT, STATS_OBJECTS_MISSED
)


class ScoreManager:
    """Manages score, high score, and combo system."""
    
    def __init__(self):
        """Initialize the score manager."""
        self.score = STARTING_SCORE
        self.high_score = self._load_high_score()
        self.combo = 0
        self.best_combo = 0
        self.combo_timer = 0
        self.is_combo_active = False
        
    def _load_high_score(self) -> int:
        """Load high score from file."""
        try:
            if HIGHSCORE_FILE.exists():
                with open(HIGHSCORE_FILE, 'r') as f:
                    return int(f.read().strip())
        except (ValueError, IOError):
            pass
        return 0
    
    def save_high_score(self) -> None:
        """Save high score to file."""
        try:
            with open(HIGHSCORE_FILE, 'w') as f:
                f.write(str(self.high_score))
        except IOError as e:
            print(f"Error saving high score: {e}")
    
    def add_points(self, points: int, multiplier: float = 1.0) -> int:
        """
        Add points to the score.
        
        Args:
            points: Base points to add
            multiplier: Score multiplier (from power-ups or combo)
            
        Returns:
            Actual points added
        """
        actual_points = int(points * multiplier)
        self.score += actual_points
        
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
            
        # Update combo
        self.combo += 1
        self.best_combo = max(self.best_combo, self.combo)
        self.combo_timer = COMBO_TIMEOUT
        self.is_combo_active = True
        
        return actual_points
    
    def subtract_points(self, points: int) -> None:
        """
        Subtract points from the score.
        
        Args:
            points: Points to subtract
        """
        self.score = max(0, self.score - points)
        self.reset_combo()
    
    def reset_combo(self) -> None:
        """Reset the combo counter."""
        self.combo = 0
        self.is_combo_active = False
    
    def update_combo_timer(self, dt: float) -> None:
        """
        Update combo timer.
        
        Args:
            dt: Delta time in seconds
        """
        if self.is_combo_active:
            self.combo_timer -= dt * 1000
            if self.combo_timer <= 0:
                self.reset_combo()
    
    def get_combo_multiplier(self) -> float:
        """
        Get score multiplier based on current combo.
        
        Returns:
            Combo multiplier
        """
        if self.combo < 3:
            return 1.0
        elif self.combo < 5:
            return 1.5
        elif self.combo < 10:
            return 2.0
        else:
            return 2.5
    
    def reset(self) -> None:
        """Reset score for new game."""
        self.score = STARTING_SCORE
        self.combo = 0
        self.best_combo = 0
        self.combo_timer = 0
        self.is_combo_active = False
    
    def is_game_over(self) -> bool:
        """Check if game is over (score reached 0)."""
        return self.score <= 0


class StatisticsManager:
    """Manages game statistics."""
    
    def __init__(self):
        """Initialize the statistics manager."""
        self.stats = self._load_statistics()
        self.session_start_time: Optional[float] = None
        
    def _load_statistics(self) -> Dict[str, Any]:
        """Load statistics from file."""
        default_stats = {
            STATS_GAME_PLAYED: 0,
            STATS_TOTAL_SCORE: 0,
            STATS_TOTAL_TIME: 0,
            STATS_BEST_COMBO: 0,
            STATS_OBJECTS_CAUGHT: 0,
            STATS_OBJECTS_MISSED: 0,
            "last_played": None
        }
        
        try:
            if STATISTICS_FILE.exists():
                with open(STATISTICS_FILE, 'r') as f:
                    loaded = json.load(f)
                    return {**default_stats, **loaded}
        except (json.JSONDecodeError, IOError):
            pass
        return default_stats
    
    def save_statistics(self) -> None:
        """Save statistics to file."""
        try:
            with open(STATISTICS_FILE, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except IOError as e:
            print(f"Error saving statistics: {e}")
    
    def start_session(self) -> None:
        """Start a game session."""
        import time
        self.session_start_time = time.time()
    
    def end_session(self, score: int, best_combo: int, objects_caught: int, objects_missed: int) -> None:
        """
        End a game session and update statistics.
        
        Args:
            score: Final score
            best_combo: Best combo achieved
            objects_caught: Number of objects caught
            objects_missed: Number of objects missed
        """
        import time
        
        if self.session_start_time:
            session_time = time.time() - self.session_start_time
            self.stats[STATS_TOTAL_TIME] += int(session_time)
        
        self.stats[STATS_GAME_PLAYED] += 1
        self.stats[STATS_TOTAL_SCORE] += score
        self.stats[STATS_BEST_COMBO] = max(self.stats[STATS_BEST_COMBO], best_combo)
        self.stats[STATS_OBJECTS_CAUGHT] += objects_caught
        self.stats[STATS_OBJECTS_MISSED] += objects_missed
        self.stats["last_played"] = datetime.now().isoformat()
        
        self.save_statistics()
        self.session_start_time = None
    
    def get_average_score(self) -> float:
        """Get average score per game."""
        games = self.stats[STATS_GAME_PLAYED]
        return self.stats[STATS_TOTAL_SCORE] / games if games > 0 else 0
    
    def get_catch_rate(self) -> float:
        """Get percentage of objects caught."""
        total = self.stats[STATS_OBJECTS_CAUGHT] + self.stats[STATS_OBJECTS_MISSED]
        return (self.stats[STATS_OBJECTS_CAUGHT] / total * 100) if total > 0 else 0


class SettingsManager:
    """Manages game settings."""
    
    def __init__(self):
        """Initialize the settings manager."""
        self.settings = self._load_settings()
        
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file."""
        default_settings = {
            "sound_volume": DEFAULT_VOLUME,
            "music_volume": MUSIC_VOLUME,
            "fullscreen": False,
            "show_fps": False,
            "difficulty": "normal",
            "particles_enabled": True
        }
        
        try:
            if SETTINGS_FILE.exists():
                with open(SETTINGS_FILE, 'r') as f:
                    loaded = json.load(f)
                    return {**default_settings, **loaded}
        except (json.JSONDecodeError, IOError):
            pass
        return default_settings
    
    def save_settings(self) -> None:
        """Save settings to file."""
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except IOError as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a setting value."""
        self.settings[key] = value
        self.save_settings()
    
    def toggle(self, key: str) -> bool:
        """Toggle a boolean setting."""
        current = self.settings.get(key, False)
        self.settings[key] = not current
        self.save_settings()
        return self.settings[key]
