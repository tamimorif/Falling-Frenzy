"""
Game entities - Basket, FallingObject, PowerUp, and Particle classes.
"""
import pygame
import random
import math
from typing import Tuple, List, Optional
from dataclasses import dataclass
from src.config import (
    BASKET_WIDTH, BASKET_HEIGHT, BASKET_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT,
    OBJECT_WIDTH, OBJECT_HEIGHT, ObjectType, PowerUpType, BASKET_Y_OFFSET,
    PARTICLE_LIFETIME, PARTICLE_SPEED_MIN, PARTICLE_SPEED_MAX,
    PARTICLE_SIZE_MIN, PARTICLE_SIZE_MAX, BLUE, WHITE
)


class Basket:
    """Player-controlled basket that catches falling objects."""
    
    def __init__(self, x: int, y: int):
        """
        Initialize the basket.
        
        Args:
            x: Initial x position
            y: Initial y position
        """
        self.x = x
        self.y = y
        self.width = BASKET_WIDTH
        self.height = BASKET_HEIGHT
        self.speed = BASKET_SPEED
        self.velocity_x = 0
        self.color = BLUE
        
    def update(self, keys: pygame.key.ScancodeWrapper, dt: float) -> None:
        """
        Update basket position based on input.
        
        Args:
            keys: Pygame key states
            dt: Delta time for frame-rate independence
        """
        self.velocity_x = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed
            
        self.x += self.velocity_x * dt * 60  # Normalize to 60 FPS
        
        # Keep basket within screen bounds
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the basket on the surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Draw basket with rounded corners
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.color, rect, border_radius=10)
        
        # Add highlight for 3D effect
        highlight_rect = pygame.Rect(self.x + 5, self.y + 2, self.width - 10, self.height // 3)
        pygame.draw.rect(surface, (min(255, self.color[0] + 50), 
                                   min(255, self.color[1] + 50), 
                                   min(255, self.color[2] + 50)), 
                        highlight_rect, border_radius=5)
    
    def get_rect(self) -> pygame.Rect:
        """Get the collision rectangle for the basket."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_center(self) -> Tuple[int, int]:
        """Get the center position of the basket."""
        return (int(self.x + self.width // 2), int(self.y + self.height // 2))


class FallingObject:
    """Objects that fall from the top of the screen."""
    
    def __init__(self, x: int, y: int, object_type: ObjectType, speed: float):
        """
        Initialize a falling object.
        
        Args:
            x: Initial x position
            y: Initial y position
            object_type: Type of object (determines color and points)
            speed: Falling speed
        """
        self.x = x
        self.y = y
        self.width = OBJECT_WIDTH
        self.height = OBJECT_HEIGHT
        self.type = object_type
        self.speed = speed
        self.base_speed = speed
        self.rotation = 0
        self.rotation_speed = random.uniform(-5, 5)
        self.scale = 1.0
        self.pulse_time = 0
        
    def update(self, dt: float, speed_multiplier: float = 1.0) -> None:
        """
        Update object position and animation.
        
        Args:
            dt: Delta time
            speed_multiplier: Speed modifier (for slow-motion effect)
        """
        self.y += self.speed * speed_multiplier * dt * 60
        self.rotation += self.rotation_speed
        
        # Pulse animation for special objects and bombs
        if self.type == ObjectType.PURPLE:
            self.pulse_time += dt * 10
            self.scale = 1.0 + math.sin(self.pulse_time) * 0.1
        elif self.type == ObjectType.BOMB:
            self.pulse_time += dt * 8
            self.scale = 1.0 + math.sin(self.pulse_time) * 0.15
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the object on the surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Calculate scaled dimensions
        scaled_width = int(self.width * self.scale)
        scaled_height = int(self.height * self.scale)
        center_x = int(self.x + self.width // 2)
        center_y = int(self.y + self.height // 2)
        
        # Special rendering for bombs
        if self.type == ObjectType.BOMB:
            # Draw bomb body (black circle)
            pygame.draw.circle(surface, (30, 30, 30), 
                             (center_x, center_y), 
                             scaled_width // 2)
            
            # Draw bomb outline
            pygame.draw.circle(surface, (255, 0, 0), 
                             (center_x, center_y), 
                             scaled_width // 2, 3)
            
            # Draw fuse
            fuse_start = (center_x, center_y - scaled_height // 2)
            fuse_end = (center_x, center_y - scaled_height // 2 - 10)
            pygame.draw.line(surface, (100, 100, 100), fuse_start, fuse_end, 3)
            
            # Draw spark at fuse tip (animated)
            spark_intensity = int(200 + 55 * math.sin(self.pulse_time * 3))
            spark_color = (255, spark_intensity, 0)
            pygame.draw.circle(surface, spark_color, fuse_end, 4)
            
            # Draw skull symbol
            font = pygame.font.Font(None, 24)
            skull_text = font.render("💣", True, (255, 255, 255))
            text_rect = skull_text.get_rect(center=(center_x, center_y))
            surface.blit(skull_text, text_rect)
        else:
            # Draw regular object as circle with gradient effect
            pygame.draw.circle(surface, self.type.color, 
                             (center_x, center_y), 
                             scaled_width // 2)
            
            # Add highlight
            highlight_color = tuple(min(255, c + 80) for c in self.type.color)
            pygame.draw.circle(surface, highlight_color, 
                             (center_x - scaled_width // 6, center_y - scaled_height // 6), 
                             scaled_width // 4)
            
            # Add points indicator
            font = pygame.font.Font(None, 20)
            points_text = font.render(f"+{self.type.points}", True, WHITE)
        text_rect = points_text.get_rect(center=(center_x, center_y))
        surface.blit(points_text, text_rect)
    
    def get_rect(self) -> pygame.Rect:
        """Get the collision rectangle for the object."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self) -> bool:
        """Check if object has fallen off screen."""
        return self.y > SCREEN_HEIGHT
    
    def get_center(self) -> Tuple[int, int]:
        """Get the center position of the object."""
        return (int(self.x + self.width // 2), int(self.y + self.height // 2))


class PowerUp:
    """Power-up items that provide temporary benefits."""
    
    def __init__(self, x: int, y: int, powerup_type: PowerUpType, speed: float):
        """
        Initialize a power-up.
        
        Args:
            x: Initial x position
            y: Initial y position
            powerup_type: Type of power-up
            speed: Falling speed
        """
        self.x = x
        self.y = y
        self.width = OBJECT_WIDTH
        self.height = OBJECT_HEIGHT
        self.type = powerup_type
        self.speed = speed
        self.rotation = 0
        self.glow_intensity = 0
        
    def update(self, dt: float) -> None:
        """Update power-up position and animation."""
        self.y += self.speed * dt * 60
        self.rotation += 2
        self.glow_intensity = (math.sin(pygame.time.get_ticks() / 200) + 1) / 2
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the power-up on the surface."""
        center_x = int(self.x + self.width // 2)
        center_y = int(self.y + self.height // 2)
        
        # Draw glow effect
        glow_radius = int(self.width // 2 + 10 * self.glow_intensity)
        glow_color = tuple(int(c * 0.5) for c in self.type.color)
        pygame.draw.circle(surface, glow_color, (center_x, center_y), glow_radius)
        
        # Draw star shape for power-up
        points = []
        for i in range(10):
            angle = math.radians(self.rotation + i * 36)
            radius = (self.width // 2) if i % 2 == 0 else (self.width // 4)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        
        pygame.draw.polygon(surface, self.type.color, points)
        pygame.draw.polygon(surface, WHITE, points, 2)
    
    def get_rect(self) -> pygame.Rect:
        """Get the collision rectangle for the power-up."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self) -> bool:
        """Check if power-up has fallen off screen."""
        return self.y > SCREEN_HEIGHT
    
    def get_center(self) -> Tuple[int, int]:
        """Get the center position of the power-up."""
        return (int(self.x + self.width // 2), int(self.y + self.height // 2))


@dataclass
class Particle:
    """Particle for visual effects."""
    x: float
    y: float
    vx: float
    vy: float
    color: Tuple[int, int, int]
    size: int
    lifetime: int
    age: int = 0
    
    def update(self, dt: float) -> bool:
        """
        Update particle position and age.
        
        Returns:
            True if particle is still alive, False otherwise
        """
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.vy += 0.3  # Gravity
        self.age += dt * 1000
        return self.age < self.lifetime
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the particle."""
        alpha = 1 - (self.age / self.lifetime)
        color = tuple(int(c * alpha) for c in self.color)
        size = max(1, int(self.size * alpha))
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), size)


class ParticleSystem:
    """Manages particle effects."""
    
    def __init__(self):
        """Initialize the particle system."""
        self.particles: List[Particle] = []
    
    def emit(self, x: int, y: int, color: Tuple[int, int, int], count: int = 10) -> None:
        """
        Emit particles at a position.
        
        Args:
            x: X position
            y: Y position
            color: Particle color
            count: Number of particles to emit
        """
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(PARTICLE_SPEED_MIN, PARTICLE_SPEED_MAX)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 2  # Upward bias
            size = random.randint(PARTICLE_SIZE_MIN, PARTICLE_SIZE_MAX)
            
            particle = Particle(
                x=float(x),
                y=float(y),
                vx=vx,
                vy=vy,
                color=color,
                size=size,
                lifetime=PARTICLE_LIFETIME
            )
            self.particles.append(particle)
    
    def update(self, dt: float) -> None:
        """Update all particles."""
        self.particles = [p for p in self.particles if p.update(dt)]
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw all particles."""
        for particle in self.particles:
            particle.draw(surface)
    
    def clear(self) -> None:
        """Clear all particles."""
        self.particles.clear()
