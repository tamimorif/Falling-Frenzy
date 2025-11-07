"""
UI components - Buttons, Menus, and rendering utilities.
"""
import pygame
from typing import Tuple, Optional, Callable, List
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GRAY, DARK_GRAY,
    BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_RADIUS, BUTTON_PADDING,
    FONT_SMALL, FONT_MEDIUM, FONT_LARGE, FONT_TITLE, BLUE, GREEN, RED,
    BG_COLOR_TOP, BG_COLOR_BOTTOM
)


class Button:
    """Interactive button with hover effects."""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str, color: Tuple[int, int, int], 
                 hover_color: Tuple[int, int, int],
                 callback: Optional[Callable] = None):
        """
        Initialize a button.
        
        Args:
            x: X position
            y: Y position
            width: Button width
            height: Button height
            text: Button text
            color: Normal button color
            hover_color: Color when hovered
            callback: Function to call when clicked
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.callback = callback
        self.is_hovered = False
        self.is_pressed = False
        self.font = pygame.font.Font(None, FONT_MEDIUM)
        
    def update(self, mouse_pos: Tuple[int, int], mouse_pressed: bool) -> bool:
        """
        Update button state.
        
        Args:
            mouse_pos: Current mouse position
            mouse_pressed: Whether mouse is pressed
            
        Returns:
            True if button was clicked, False otherwise
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if self.is_hovered and mouse_pressed and not self.is_pressed:
            self.is_pressed = True
            if self.callback:
                self.callback()
            return True
        
        if not mouse_pressed:
            self.is_pressed = False
            
        return False
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the button."""
        color = self.hover_color if self.is_hovered else self.color
        
        # Draw button background
        pygame.draw.rect(surface, color, self.rect, border_radius=BUTTON_RADIUS)
        
        # Draw border
        border_color = WHITE if self.is_hovered else DARK_GRAY
        pygame.draw.rect(surface, border_color, self.rect, 3, border_radius=BUTTON_RADIUS)
        
        # Draw text
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class TextElement:
    """Static or animated text element."""
    
    def __init__(self, x: int, y: int, text: str, 
                 font_size: int, color: Tuple[int, int, int],
                 center: bool = False):
        """
        Initialize a text element.
        
        Args:
            x: X position
            y: Y position
            text: Text to display
            font_size: Font size
            color: Text color
            center: Whether to center the text at x, y
        """
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.center = center
        
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the text."""
        text_surface = self.font.render(self.text, True, self.color)
        if self.center:
            text_rect = text_surface.get_rect(center=(self.x, self.y))
            surface.blit(text_surface, text_rect)
        else:
            surface.blit(text_surface, (self.x, self.y))
    
    def update_text(self, new_text: str) -> None:
        """Update the text content."""
        self.text = new_text


class Menu:
    """Base menu class."""
    
    def __init__(self, title: str):
        """
        Initialize a menu.
        
        Args:
            title: Menu title
        """
        self.title = title
        self.buttons: List[Button] = []
        self.text_elements: List[TextElement] = []
        self.title_font = pygame.font.Font(None, FONT_TITLE)
        
    def add_button(self, text: str, y_offset: int, 
                   callback: Optional[Callable] = None,
                   color: Tuple[int, int, int] = BLUE) -> Button:
        """
        Add a button to the menu.
        
        Args:
            text: Button text
            y_offset: Vertical offset from center
            callback: Click callback
            color: Button color
            
        Returns:
            The created button
        """
        x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
        y = SCREEN_HEIGHT // 2 + y_offset
        hover_color = tuple(min(255, c + 50) for c in color)
        button = Button(x, y, BUTTON_WIDTH, BUTTON_HEIGHT, 
                       text, color, hover_color, callback)
        self.buttons.append(button)
        return button
    
    def add_text(self, text: str, y: int, font_size: int = FONT_MEDIUM,
                 color: Tuple[int, int, int] = WHITE, center: bool = True) -> TextElement:
        """
        Add a text element to the menu.
        
        Args:
            text: Text content
            y: Y position
            font_size: Font size
            color: Text color
            center: Whether to center
            
        Returns:
            The created text element
        """
        x = SCREEN_WIDTH // 2 if center else 10
        text_elem = TextElement(x, y, text, font_size, color, center)
        self.text_elements.append(text_elem)
        return text_elem
    
    def update(self, mouse_pos: Tuple[int, int], mouse_pressed: bool) -> None:
        """Update all buttons."""
        for button in self.buttons:
            button.update(mouse_pos, mouse_pressed)
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the menu."""
        # Draw title
        title_surface = self.title_font.render(self.title, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        surface.blit(title_surface, title_rect)
        
        # Draw all text elements
        for text_elem in self.text_elements:
            text_elem.draw(surface)
        
        # Draw all buttons
        for button in self.buttons:
            button.draw(surface)


class HUD:
    """Heads-up display for in-game information."""
    
    def __init__(self):
        """Initialize the HUD."""
        self.font_large = pygame.font.Font(None, FONT_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SMALL)
        self.combo_scale = 1.0
        self.combo_target_scale = 1.0
        
    def draw(self, surface: pygame.Surface, score: int, high_score: int,
             combo: int, combo_multiplier: float, fps: Optional[int] = None) -> None:
        """
        Draw the HUD.
        
        Args:
            surface: Surface to draw on
            score: Current score
            high_score: High score
            combo: Current combo count
            combo_multiplier: Combo multiplier
            fps: Frames per second (optional)
        """
        # Draw score
        score_text = self.font_large.render(f"Score: {score}", True, WHITE)
        surface.blit(score_text, (10, 10))
        
        # Draw high score
        high_score_text = self.font_small.render(f"High Score: {high_score}", True, GRAY)
        surface.blit(high_score_text, (10, 50))
        
        # Draw combo if active
        if combo > 0:
            combo_color = self._get_combo_color(combo)
            combo_text = self.font_large.render(f"COMBO x{combo}", True, combo_color)
            
            # Animate combo text
            if combo_multiplier > 1.0:
                self.combo_target_scale = 1.2
            else:
                self.combo_target_scale = 1.0
            
            self.combo_scale += (self.combo_target_scale - self.combo_scale) * 0.1
            
            # Scale the text
            scaled_width = int(combo_text.get_width() * self.combo_scale)
            scaled_height = int(combo_text.get_height() * self.combo_scale)
            scaled_text = pygame.transform.scale(combo_text, (scaled_width, scaled_height))
            
            text_rect = scaled_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
            surface.blit(scaled_text, text_rect)
            
            # Draw multiplier
            if combo_multiplier > 1.0:
                multiplier_text = self.font_small.render(
                    f"{combo_multiplier:.1f}x Points!", True, combo_color
                )
                mult_rect = multiplier_text.get_rect(center=(SCREEN_WIDTH // 2, 85))
                surface.blit(multiplier_text, mult_rect)
        
        # Draw FPS if provided
        if fps is not None:
            fps_text = self.font_small.render(f"FPS: {fps}", True, GRAY)
            surface.blit(fps_text, (SCREEN_WIDTH - 100, 10))
    
    def _get_combo_color(self, combo: int) -> Tuple[int, int, int]:
        """Get color based on combo level."""
        if combo < 3:
            return WHITE
        elif combo < 5:
            return GREEN
        elif combo < 10:
            return (255, 215, 0)  # Gold
        else:
            return (255, 0, 255)  # Magenta


class Background:
    """Animated background renderer."""
    
    def __init__(self):
        """Initialize the background."""
        self.offset = 0
        
    def update(self, dt: float) -> None:
        """Update background animation."""
        self.offset += dt * 20
        if self.offset > SCREEN_HEIGHT:
            self.offset = 0
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw gradient background with animated stars."""
        # Draw gradient
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            color = tuple(
                int(BG_COLOR_TOP[i] * (1 - ratio) + BG_COLOR_BOTTOM[i] * ratio)
                for i in range(3)
            )
            pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
        
        # Draw animated stars
        import random
        random.seed(42)  # Fixed seed for consistent star positions
        for i in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = (random.randint(0, SCREEN_HEIGHT) + self.offset) % SCREEN_HEIGHT
            size = random.randint(1, 3)
            alpha = 128 + int(127 * ((y + self.offset * 0.5) % 200) / 200)
            color = (alpha, alpha, alpha)
            pygame.draw.circle(surface, color, (x, int(y)), size)


def draw_gradient_rect(surface: pygame.Surface, rect: pygame.Rect,
                       color1: Tuple[int, int, int], 
                       color2: Tuple[int, int, int]) -> None:
    """
    Draw a rectangle with vertical gradient.
    
    Args:
        surface: Surface to draw on
        rect: Rectangle dimensions
        color1: Top color
        color2: Bottom color
    """
    for y in range(rect.height):
        ratio = y / rect.height
        color = tuple(
            int(color1[i] * (1 - ratio) + color2[i] * ratio)
            for i in range(3)
        )
        pygame.draw.line(surface, color, 
                        (rect.x, rect.y + y), 
                        (rect.x + rect.width, rect.y + y))
