#!/usr/bin/env python3
"""
Test per verificare i diversi livelli di volume
"""

import pygame
import time
import numpy as np

def test_volume_levels():
    """Test di diversi livelli di volume"""
    print("Test livelli di volume...")
    
    try:
        # Inizializza pygame mixer
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        print("✅ Pygame mixer inizializzato")
        
        frequency = 440.0
        duration = 1.0
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Test diversi livelli di volume
        volume_levels = [0.2, 0.4, 0.6, 0.8, 1.0]
        
        for i, vol in enumerate(volume_levels):
            print(f"🎵 Test volume {vol} ({i+1}/5)...")
            
            # Genera onda sinusoidale
            t = np.linspace(0, duration, frames, False)
            wave = np.sin(2 * np.pi * frequency * t)
            
            # Fade-in e fade-out
            fade_samples = int(0.01 * sample_rate)
            if frames > 2 * fade_samples:
                wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
                wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            
            # Envelope
            envelope = np.exp(-t * 1.5)
            wave *= envelope
            
            # Applica volume
            wave = (wave * 4096 * vol).astype(np.int16)
            
            # Crea stereo
            stereo_wave = np.column_stack((wave, wave))
            
            # Riproduce
            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.play()
            time.sleep(duration + 0.3)
        
        print("✅ Test livelli di volume completato!")
        return True
        
    except Exception as e:
        print(f"❌ Errore nel test volume: {e}")
        return False

if __name__ == "__main__":
    test_volume_levels()
