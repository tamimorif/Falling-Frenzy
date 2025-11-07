"""
Audio management system for sound effects and music.
"""
import pygame
from typing import Dict, Optional
from pathlib import Path
from src.config import SOUNDS_DIR, DEFAULT_VOLUME, MUSIC_VOLUME


class AudioManager:
    """Manages all game audio - music and sound effects."""
    
    def __init__(self):
        """Initialize the audio manager."""
        self.sound_effects: Dict[str, pygame.mixer.Sound] = {}
        self.music_loaded = False
        self.sound_volume = DEFAULT_VOLUME
        self.music_volume = MUSIC_VOLUME
        self.enabled = True
        
        # Initialize mixer with better quality
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        except pygame.error as e:
            print(f"Could not initialize audio: {e}")
            self.enabled = False
    
    def load_sound(self, name: str, filename: str) -> None:
        """
        Load a sound effect.
        
        Args:
            name: Internal name for the sound
            filename: Name of the sound file
        """
        if not self.enabled:
            return
            
        try:
            sound_path = SOUNDS_DIR / filename
            if sound_path.exists():
                sound = pygame.mixer.Sound(str(sound_path))
                sound.set_volume(self.sound_volume)
                self.sound_effects[name] = sound
            else:
                # Create a simple beep if file doesn't exist
                self._create_placeholder_sound(name)
        except pygame.error as e:
            print(f"Could not load sound {filename}: {e}")
            self._create_placeholder_sound(name)
    
    def _create_placeholder_sound(self, name: str) -> None:
        """Create a simple placeholder sound."""
        try:
            # Create a simple tone
            sample_rate = 22050
            duration = 0.1
            frequency = 440
            
            import numpy as np
            samples = int(sample_rate * duration)
            wave = np.sin(2.0 * np.pi * frequency * np.linspace(0, duration, samples))
            wave = (wave * 32767).astype(np.int16)
            stereo_wave = np.repeat(wave.reshape(samples, 1), 2, axis=1)
            
            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.set_volume(self.sound_volume)
            self.sound_effects[name] = sound
        except:
            # If even that fails, just skip
            pass
    
    def play_sound(self, name: str) -> None:
        """
        Play a sound effect.
        
        Args:
            name: Name of the sound to play
        """
        if not self.enabled or name not in self.sound_effects:
            return
            
        try:
            self.sound_effects[name].play()
        except pygame.error:
            pass
    
    def load_music(self, filename: str) -> None:
        """
        Load background music.
        
        Args:
            filename: Name of the music file
        """
        if not self.enabled:
            return
            
        try:
            music_path = SOUNDS_DIR / filename
            if music_path.exists():
                pygame.mixer.music.load(str(music_path))
                pygame.mixer.music.set_volume(self.music_volume)
                self.music_loaded = True
        except pygame.error as e:
            print(f"Could not load music {filename}: {e}")
    
    def play_music(self, loops: int = -1) -> None:
        """
        Play background music.
        
        Args:
            loops: Number of times to loop (-1 for infinite)
        """
        if not self.enabled or not self.music_loaded:
            return
            
        try:
            pygame.mixer.music.play(loops)
        except pygame.error:
            pass
    
    def stop_music(self) -> None:
        """Stop background music."""
        if not self.enabled:
            return
            
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass
    
    def pause_music(self) -> None:
        """Pause background music."""
        if not self.enabled:
            return
            
        try:
            pygame.mixer.music.pause()
        except pygame.error:
            pass
    
    def unpause_music(self) -> None:
        """Unpause background music."""
        if not self.enabled:
            return
            
        try:
            pygame.mixer.music.unpause()
        except pygame.error:
            pass
    
    def set_sound_volume(self, volume: float) -> None:
        """
        Set volume for sound effects.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sound_effects.values():
            sound.set_volume(self.sound_volume)
    
    def set_music_volume(self, volume: float) -> None:
        """
        Set volume for background music.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        if not self.enabled:
            return
            
        self.music_volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.music_volume)
        except pygame.error:
            pass
    
    def load_all_sounds(self) -> None:
        """Load all game sound effects."""
        # Define all sound effects
        sounds = {
            "catch_red": "catch_red.wav",
            "catch_green": "catch_green.wav",
            "catch_yellow": "catch_yellow.wav",
            "catch_purple": "catch_purple.wav",
            "catch_bomb": "explosion.wav",
            "miss": "miss.wav",
            "powerup": "powerup.wav",
            "combo": "combo.wav",
            "game_over": "game_over.wav",
            "button_click": "button_click.wav"
        }
        
        for name, filename in sounds.items():
            self.load_sound(name, filename)
