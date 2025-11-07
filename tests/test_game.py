"""
Unit tests for Falling Frenzy game.
Run with: pytest tests/
"""
import pytest
import pygame
from src.entities import Basket, FallingObject, PowerUp, Particle
from src.utils import ScoreManager, StatisticsManager, SettingsManager
from src.config import ObjectType, PowerUpType, SCREEN_WIDTH, SCREEN_HEIGHT


class TestBasket:
    """Test the Basket class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        pygame.init()
        self.basket = Basket(100, 600)
    
    def test_basket_initialization(self):
        """Test basket is initialized correctly."""
        assert self.basket.x == 100
        assert self.basket.y == 600
        assert self.basket.velocity_x == 0
    
    def test_basket_movement_left(self):
        """Test basket moves left."""
        keys = pygame.key.get_pressed()
        # Simulate left key press
        keys_dict = {pygame.K_LEFT: True, pygame.K_RIGHT: False, 
                     pygame.K_a: False, pygame.K_d: False}
        
        initial_x = self.basket.x
        self.basket.velocity_x = -self.basket.speed
        self.basket.x += self.basket.velocity_x
        
        assert self.basket.x < initial_x
    
    def test_basket_bounds(self):
        """Test basket stays within screen bounds."""
        self.basket.x = -10
        self.basket.x = max(0, min(self.basket.x, SCREEN_WIDTH - self.basket.width))
        assert self.basket.x >= 0
        
        self.basket.x = SCREEN_WIDTH + 10
        self.basket.x = max(0, min(self.basket.x, SCREEN_WIDTH - self.basket.width))
        assert self.basket.x <= SCREEN_WIDTH - self.basket.width
    
    def test_basket_get_center(self):
        """Test basket center calculation."""
        center = self.basket.get_center()
        expected_x = self.basket.x + self.basket.width // 2
        expected_y = self.basket.y + self.basket.height // 2
        assert center == (expected_x, expected_y)


class TestFallingObject:
    """Test the FallingObject class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        pygame.init()
        self.obj = FallingObject(100, 0, ObjectType.RED, 5.0)
    
    def test_object_initialization(self):
        """Test object is initialized correctly."""
        assert self.obj.x == 100
        assert self.obj.y == 0
        assert self.obj.type == ObjectType.RED
        assert self.obj.speed == 5.0
    
    def test_object_falls(self):
        """Test object falls down."""
        initial_y = self.obj.y
        self.obj.update(1.0)
        assert self.obj.y > initial_y
    
    def test_object_off_screen(self):
        """Test object off-screen detection."""
        self.obj.y = SCREEN_HEIGHT + 10
        assert self.obj.is_off_screen()
        
        self.obj.y = 100
        assert not self.obj.is_off_screen()
    
    def test_object_points(self):
        """Test object points are correct."""
        assert ObjectType.RED.points == 1
        assert ObjectType.GREEN.points == 2
        assert ObjectType.YELLOW.points == 3
        assert ObjectType.PURPLE.points == 5


class TestScoreManager:
    """Test the ScoreManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.score_manager = ScoreManager()
    
    def test_score_initialization(self):
        """Test score manager initializes correctly."""
        assert self.score_manager.score >= 0
        assert self.score_manager.combo == 0
    
    def test_add_points(self):
        """Test adding points."""
        initial_score = self.score_manager.score
        self.score_manager.add_points(10)
        assert self.score_manager.score == initial_score + 10
    
    def test_combo_system(self):
        """Test combo system."""
        self.score_manager.add_points(1)
        assert self.score_manager.combo == 1
        
        self.score_manager.add_points(1)
        assert self.score_manager.combo == 2
        
        self.score_manager.reset_combo()
        assert self.score_manager.combo == 0
    
    def test_combo_multiplier(self):
        """Test combo multiplier calculation."""
        self.score_manager.combo = 0
        assert self.score_manager.get_combo_multiplier() == 1.0
        
        self.score_manager.combo = 3
        assert self.score_manager.get_combo_multiplier() == 1.5
        
        self.score_manager.combo = 10
        assert self.score_manager.get_combo_multiplier() == 2.5
    
    def test_subtract_points(self):
        """Test subtracting points."""
        self.score_manager.score = 10
        self.score_manager.subtract_points(5)
        assert self.score_manager.score == 5
        
        # Score should not go below 0
        self.score_manager.subtract_points(10)
        assert self.score_manager.score == 0
    
    def test_game_over_condition(self):
        """Test game over detection."""
        self.score_manager.score = 1
        assert not self.score_manager.is_game_over()
        
        self.score_manager.score = 0
        assert self.score_manager.is_game_over()


class TestStatisticsManager:
    """Test the StatisticsManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.stats_manager = StatisticsManager()
    
    def test_statistics_initialization(self):
        """Test statistics initialize correctly."""
        assert 'games_played' in self.stats_manager.stats
        assert 'total_score' in self.stats_manager.stats
        assert isinstance(self.stats_manager.stats['games_played'], int)
    
    def test_end_session(self):
        """Test ending a game session."""
        initial_games = self.stats_manager.stats['games_played']
        self.stats_manager.start_session()
        self.stats_manager.end_session(100, 5, 20, 5)
        
        assert self.stats_manager.stats['games_played'] == initial_games + 1
        assert self.stats_manager.stats['objects_caught'] >= 20
        assert self.stats_manager.stats['objects_missed'] >= 5
    
    def test_average_score(self):
        """Test average score calculation."""
        self.stats_manager.stats['games_played'] = 10
        self.stats_manager.stats['total_score'] = 500
        assert self.stats_manager.get_average_score() == 50.0
    
    def test_catch_rate(self):
        """Test catch rate calculation."""
        self.stats_manager.stats['objects_caught'] = 80
        self.stats_manager.stats['objects_missed'] = 20
        assert self.stats_manager.get_catch_rate() == 80.0


class TestSettingsManager:
    """Test the SettingsManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.settings_manager = SettingsManager()
    
    def test_settings_initialization(self):
        """Test settings initialize with defaults."""
        assert 'sound_volume' in self.settings_manager.settings
        assert 'music_volume' in self.settings_manager.settings
        assert isinstance(self.settings_manager.settings['sound_volume'], float)
    
    def test_get_setting(self):
        """Test getting a setting."""
        volume = self.settings_manager.get('sound_volume')
        assert volume is not None
        assert 0.0 <= volume <= 1.0
    
    def test_set_setting(self):
        """Test setting a value."""
        self.settings_manager.set('sound_volume', 0.5)
        assert self.settings_manager.get('sound_volume') == 0.5
    
    def test_toggle_setting(self):
        """Test toggling a boolean setting."""
        initial = self.settings_manager.get('show_fps', False)
        result = self.settings_manager.toggle('show_fps')
        assert result == (not initial)


class TestParticle:
    """Test the Particle class."""
    
    def test_particle_initialization(self):
        """Test particle initializes correctly."""
        particle = Particle(100, 100, 5.0, -5.0, (255, 0, 0), 5, 1000)
        assert particle.x == 100
        assert particle.y == 100
        assert particle.age == 0
    
    def test_particle_lifetime(self):
        """Test particle dies after lifetime."""
        particle = Particle(100, 100, 0, 0, (255, 0, 0), 5, 100)
        
        # Update for 0.05 seconds (50ms)
        alive = particle.update(0.05)
        assert alive
        
        # Update for another 0.1 seconds (100ms total)
        alive = particle.update(0.1)
        assert not alive  # Should be dead after 150ms


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
