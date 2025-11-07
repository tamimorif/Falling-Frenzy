"""
Main game class that orchestrates all game systems.
"""
import pygame
import random
import sys
from typing import List, Optional
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE, GameState, ObjectType,
    PowerUpType, OBJECT_SPAWN_DELAY, OBJECT_BASE_SPEED, BASKET_Y_OFFSET,
    BASKET_WIDTH, OBJECT_MAX_SPEED, OBJECT_SPEED_INCREMENT, MISS_PENALTY,
    POWERUP_SPAWN_CHANCE, POWERUP_DURATION, SPAWN_DELAY_MIN, 
    SPAWN_DELAY_DECREASE, DIFFICULTY_INCREASE_INTERVAL, WHITE, BLACK,
    PARTICLE_COUNT, BOMB_DAMAGE, SPAWN_POSITION_VARIANCE
)
from src.entities import Basket, FallingObject, PowerUp, ParticleSystem
from src.utils import ScoreManager, StatisticsManager, SettingsManager
from src.ui import Menu, HUD, Background, Button
from src.audio import AudioManager


class Game:
    """Main game class managing all game systems."""
    
    def __init__(self):
        """Initialize the game."""
        # Initialize Pygame
        pygame.init()
        
        # Create screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        
        # Clock for FPS control
        self.clock = pygame.time.Clock()
        self.dt = 0
        
        # Game state
        self.state = GameState.MAIN_MENU
        self.running = True
        
        # Managers
        self.score_manager = ScoreManager()
        self.stats_manager = StatisticsManager()
        self.settings_manager = SettingsManager()
        self.audio_manager = AudioManager()
        
        # Load audio
        self.audio_manager.load_all_sounds()
        
        # Game entities
        self.basket = Basket(
            SCREEN_WIDTH // 2 - BASKET_WIDTH // 2,
            SCREEN_HEIGHT - 30 - BASKET_Y_OFFSET
        )
        self.falling_objects: List[FallingObject] = []
        self.powerups: List[PowerUp] = []
        
        # Visual effects
        self.particle_system = ParticleSystem()
        self.background = Background()
        self.hud = HUD()
        
        # UI
        self._create_menus()
        
        # Game variables
        self.last_spawn_time = 0
        self.spawn_delay = OBJECT_SPAWN_DELAY
        self.object_speed = OBJECT_BASE_SPEED
        self.game_time = 0
        self.difficulty_timer = 0
        
        # Power-up tracking
        self.active_powerup: Optional[PowerUpType] = None
        self.powerup_timer = 0
        
        # Statistics tracking
        self.objects_caught = 0
        self.objects_missed = 0
        
        # Mouse state
        self.mouse_pressed_last_frame = False
    
    def _create_menus(self) -> None:
        """Create all game menus."""
        # Main menu
        self.main_menu = Menu("FALLING FRENZY")
        self.main_menu.add_button("Start Game", -20, self._start_game)
        self.main_menu.add_button("Statistics", 60, self._show_statistics)
        self.main_menu.add_button("Settings", 140, self._show_settings)
        self.main_menu.add_button("Quit", 220, self._quit_game)
        
        # Pause menu
        self.pause_menu = Menu("PAUSED")
        self.pause_menu.add_button("Resume", -20, self._resume_game)
        self.pause_menu.add_button("Main Menu", 60, self._return_to_menu)
        
        # Game over menu
        self.game_over_menu = Menu("GAME OVER")
        self.game_over_text = self.game_over_menu.add_text("", SCREEN_HEIGHT // 2 - 100)
        self.game_over_menu.add_button("Play Again", 20, self._start_game)
        self.game_over_menu.add_button("Main Menu", 100, self._return_to_menu)
        
        # Statistics menu
        self.stats_menu = Menu("STATISTICS")
        self.stats_texts = {
            "games": self.stats_menu.add_text("", 200, center=True),
            "avg_score": self.stats_menu.add_text("", 240, center=True),
            "best_combo": self.stats_menu.add_text("", 280, center=True),
            "catch_rate": self.stats_menu.add_text("", 320, center=True),
            "total_time": self.stats_menu.add_text("", 360, center=True),
        }
        self.stats_menu.add_button("Back", 180, self._return_to_menu)
        
        # Settings menu
        self.settings_menu = Menu("SETTINGS")
        self.settings_menu.add_text("Sound Volume", 200, center=True)
        self.settings_menu.add_text("Music Volume", 280, center=True)
        self.settings_menu.add_button("Back", 180, self._return_to_menu)
    
    def _start_game(self) -> None:
        """Start a new game."""
        self.audio_manager.play_sound("button_click")
        self.state = GameState.PLAYING
        self._reset_game()
        self.stats_manager.start_session()
    
    def _show_statistics(self) -> None:
        """Show statistics menu."""
        self.audio_manager.play_sound("button_click")
        self._update_statistics_display()
        self.state = GameState.STATISTICS
    
    def _show_settings(self) -> None:
        """Show settings menu."""
        self.audio_manager.play_sound("button_click")
        self.state = GameState.SETTINGS
    
    def _quit_game(self) -> None:
        """Quit the game."""
        self.audio_manager.play_sound("button_click")
        self.running = False
    
    def _resume_game(self) -> None:
        """Resume from pause."""
        self.audio_manager.play_sound("button_click")
        self.state = GameState.PLAYING
    
    def _return_to_menu(self) -> None:
        """Return to main menu."""
        self.audio_manager.play_sound("button_click")
        self.state = GameState.MAIN_MENU
    
    def _reset_game(self) -> None:
        """Reset game state for a new game."""
        self.score_manager.reset()
        self.falling_objects.clear()
        self.powerups.clear()
        self.particle_system.clear()
        self.basket.x = SCREEN_WIDTH // 2 - BASKET_WIDTH // 2
        self.last_spawn_time = 0
        self.spawn_delay = OBJECT_SPAWN_DELAY
        self.object_speed = OBJECT_BASE_SPEED
        self.game_time = 0
        self.difficulty_timer = 0
        self.active_powerup = None
        self.powerup_timer = 0
        self.objects_caught = 0
        self.objects_missed = 0
    
    def _update_statistics_display(self) -> None:
        """Update statistics menu text."""
        stats = self.stats_manager.stats
        self.stats_texts["games"].update_text(
            f"Games Played: {stats['games_played']}"
        )
        self.stats_texts["avg_score"].update_text(
            f"Average Score: {self.stats_manager.get_average_score():.1f}"
        )
        self.stats_texts["best_combo"].update_text(
            f"Best Combo: {stats['best_combo']}"
        )
        self.stats_texts["catch_rate"].update_text(
            f"Catch Rate: {self.stats_manager.get_catch_rate():.1f}%"
        )
        minutes = stats['total_time_seconds'] // 60
        seconds = stats['total_time_seconds'] % 60
        self.stats_texts["total_time"].update_text(
            f"Total Play Time: {minutes}m {seconds}s"
        )
    
    def _spawn_object(self) -> None:
        """Spawn a new falling object in varied positions."""
        # Create spawn columns across the screen
        column_width = SCREEN_WIDTH // SPAWN_POSITION_VARIANCE
        column = random.randint(0, SPAWN_POSITION_VARIANCE - 1)
        
        # Random position within the column
        x = column * column_width + random.randint(0, column_width - 40)
        
        # Ensure x is within bounds
        x = max(0, min(x, SCREEN_WIDTH - 40))
        
        # Determine object type with varied probabilities
        rand = random.random()
        if rand < 0.15:  # 15% chance for bomb
            obj_type = ObjectType.BOMB
        elif rand < 0.20:  # 5% chance for purple (rare good object)
            obj_type = ObjectType.PURPLE
        else:  # 80% chance for regular objects
            obj_type = random.choice([ObjectType.RED, ObjectType.GREEN, ObjectType.YELLOW])
        
        obj = FallingObject(x, -40, obj_type, self.object_speed)
        self.falling_objects.append(obj)
    
    def _spawn_powerup(self) -> None:
        """Spawn a power-up."""
        if random.random() < POWERUP_SPAWN_CHANCE:
            x = random.randint(0, SCREEN_WIDTH - 40)
            powerup_type = random.choice(list(PowerUpType))
            powerup = PowerUp(x, -40, powerup_type, self.object_speed * 0.7)
            self.powerups.append(powerup)
    
    def _check_collisions(self) -> None:
        """Check for collisions between basket and objects."""
        basket_rect = self.basket.get_rect()
        
        # Check object collisions
        for obj in self.falling_objects[:]:
            if basket_rect.colliderect(obj.get_rect()):
                # Check if it's a bomb
                if obj.type.is_bomb:
                    # Bomb caught! Lose points and reset combo
                    self.score_manager.subtract_points(BOMB_DAMAGE)
                    self.score_manager.reset_combo()
                    self.objects_missed += 1
                    
                    # Explosive visual and audio feedback
                    self.particle_system.emit(*obj.get_center(), (255, 100, 0), PARTICLE_COUNT * 3)
                    self.audio_manager.play_sound("catch_bomb")
                    
                    self.falling_objects.remove(obj)
                else:
                    # Caught a good object
                    multiplier = self.score_manager.get_combo_multiplier()
                    if self.active_powerup == PowerUpType.DOUBLE_POINTS:
                        multiplier *= 2.0
                    
                    points_earned = self.score_manager.add_points(obj.type.points, multiplier)
                    self.objects_caught += 1
                    
                    # Visual and audio feedback
                    self.particle_system.emit(*obj.get_center(), obj.type.color, PARTICLE_COUNT)
                    self.audio_manager.play_sound(f"catch_{obj.type.object_name}")
                    
                    if self.score_manager.combo > 2:
                        self.audio_manager.play_sound("combo")
                    
                    self.falling_objects.remove(obj)
        
        # Check power-up collisions
        for powerup in self.powerups[:]:
            if basket_rect.colliderect(powerup.get_rect()):
                self._activate_powerup(powerup.type)
                self.particle_system.emit(*powerup.get_center(), powerup.type.color, PARTICLE_COUNT * 2)
                self.audio_manager.play_sound("powerup")
                self.powerups.remove(powerup)
    
    def _activate_powerup(self, powerup_type: PowerUpType) -> None:
        """Activate a power-up."""
        self.active_powerup = powerup_type
        self.powerup_timer = POWERUP_DURATION
    
    def _increase_difficulty(self) -> None:
        """Gradually increase game difficulty."""
        if self.object_speed < OBJECT_MAX_SPEED:
            self.object_speed += OBJECT_SPEED_INCREMENT
        
        if self.spawn_delay > SPAWN_DELAY_MIN:
            self.spawn_delay -= SPAWN_DELAY_DECREASE
    
    def _handle_input(self) -> None:
        """Handle input events."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pressed = mouse_buttons[0] and not self.mouse_pressed_last_frame
        self.mouse_pressed_last_frame = mouse_buttons[0]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                    elif self.state in [GameState.STATISTICS, GameState.SETTINGS]:
                        self.state = GameState.MAIN_MENU
        
        # Update current menu based on state
        if self.state == GameState.MAIN_MENU:
            self.main_menu.update(mouse_pos, mouse_pressed)
        elif self.state == GameState.PAUSED:
            self.pause_menu.update(mouse_pos, mouse_pressed)
        elif self.state == GameState.GAME_OVER:
            self.game_over_menu.update(mouse_pos, mouse_pressed)
        elif self.state == GameState.STATISTICS:
            self.stats_menu.update(mouse_pos, mouse_pressed)
        elif self.state == GameState.SETTINGS:
            self.settings_menu.update(mouse_pos, mouse_pressed)
    
    def _update_playing(self) -> None:
        """Update game logic during playing state."""
        keys = pygame.key.get_pressed()
        
        # Update basket
        self.basket.update(keys, self.dt)
        
        # Update game time and difficulty
        self.game_time += self.dt
        self.difficulty_timer += self.dt
        
        if self.difficulty_timer >= DIFFICULTY_INCREASE_INTERVAL:
            self._increase_difficulty()
            self.difficulty_timer = 0
        
        # Spawn objects
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_delay:
            self._spawn_object()
            self._spawn_powerup()
            self.last_spawn_time = current_time
        
        # Get speed multiplier from power-up
        speed_multiplier = 1.0
        if self.active_powerup == PowerUpType.SLOW_MOTION:
            speed_multiplier = 0.5
        
        # Update objects
        for obj in self.falling_objects[:]:
            obj.update(self.dt, speed_multiplier)
            if obj.is_off_screen():
                # Missed an object
                if self.active_powerup != PowerUpType.SHIELD:
                    self.score_manager.subtract_points(MISS_PENALTY)
                    self.audio_manager.play_sound("miss")
                self.objects_missed += 1
                self.falling_objects.remove(obj)
        
        # Update power-ups
        for powerup in self.powerups[:]:
            powerup.update(self.dt)
            if powerup.is_off_screen():
                self.powerups.remove(powerup)
        
        # Update power-up timer
        if self.active_powerup:
            self.powerup_timer -= self.dt * 1000
            if self.powerup_timer <= 0:
                self.active_powerup = None
        
        # Check collisions
        self._check_collisions()
        
        # Update combo timer
        self.score_manager.update_combo_timer(self.dt)
        
        # Update particle system
        self.particle_system.update(self.dt)
        
        # Update background
        self.background.update(self.dt)
        
        # Check game over
        if self.score_manager.is_game_over():
            self._end_game()
    
    def _end_game(self) -> None:
        """End the current game."""
        self.state = GameState.GAME_OVER
        self.audio_manager.play_sound("game_over")
        
        # Update statistics
        self.stats_manager.end_session(
            self.score_manager.score,
            self.score_manager.best_combo,
            self.objects_caught,
            self.objects_missed
        )
        
        # Save high score
        self.score_manager.save_high_score()
        
        # Update game over text
        self.game_over_text.update_text(
            f"Final Score: {self.score_manager.score} | High Score: {self.score_manager.high_score}"
        )
    
    def _render(self) -> None:
        """Render the current game state."""
        # Draw background
        self.background.draw(self.screen)
        
        if self.state == GameState.MAIN_MENU:
            self.main_menu.draw(self.screen)
        
        elif self.state == GameState.PLAYING:
            # Draw game entities
            self.basket.draw(self.screen)
            for obj in self.falling_objects:
                obj.draw(self.screen)
            for powerup in self.powerups:
                powerup.draw(self.screen)
            
            # Draw particles
            self.particle_system.draw(self.screen)
            
            # Draw HUD
            fps = int(self.clock.get_fps()) if self.settings_manager.get("show_fps") else None
            self.hud.draw(
                self.screen,
                self.score_manager.score,
                self.score_manager.high_score,
                self.score_manager.combo,
                self.score_manager.get_combo_multiplier(),
                fps
            )
            
            # Draw active power-up indicator
            if self.active_powerup:
                font = pygame.font.Font(None, 24)
                remaining = self.powerup_timer / 1000
                text = font.render(
                    f"Power-up: {self.active_powerup.powerup_name.upper()} ({remaining:.1f}s)",
                    True, self.active_powerup.color
                )
                self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT - 40))
        
        elif self.state == GameState.PAUSED:
            # Draw game state (dimmed)
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))
            
            self.pause_menu.draw(self.screen)
        
        elif self.state == GameState.GAME_OVER:
            self.game_over_menu.draw(self.screen)
        
        elif self.state == GameState.STATISTICS:
            self.stats_menu.draw(self.screen)
        
        elif self.state == GameState.SETTINGS:
            self.settings_menu.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self) -> None:
        """Main game loop."""
        while self.running:
            # Calculate delta time
            self.dt = self.clock.tick(FPS) / 1000.0
            
            # Handle input
            self._handle_input()
            
            # Update game logic
            if self.state == GameState.PLAYING:
                self._update_playing()
            
            # Render
            self._render()
        
        # Cleanup
        pygame.quit()
        sys.exit()
