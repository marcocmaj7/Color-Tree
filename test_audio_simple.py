#!/usr/bin/env python3
"""
Test semplice per verificare la riproduzione audio con pygame
"""

import pygame
import time
import numpy as np

def test_simple_audio():
    """Test di riproduzione audio semplice"""
    print("Test audio semplice...")
    
    try:
        # Inizializza pygame mixer
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        print("✅ Pygame mixer inizializzato")
        
        # Test 1: Tono semplice
        print("🎵 Test 1: Tono di 440Hz (La)...")
        frequency = 440.0
        duration = 1.0
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Genera onda sinusoidale
        t = np.linspace(0, duration, frames, False)
        wave = np.sin(2 * np.pi * frequency * t)
        wave = (wave * 4096 * 0.3).astype(np.int16)
        
        # Crea stereo
        stereo_wave = np.column_stack((wave, wave))
        
        # Riproduce
        sound = pygame.sndarray.make_sound(stereo_wave)
        sound.play()
        time.sleep(duration + 0.5)
        
        # Test 2: Scala Do maggiore
        print("🎵 Test 2: Scala Do maggiore...")
        notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C, D, E, F, G, A, B, C
        
        for i, midi_note in enumerate(notes):
            frequency = 440.0 * (2 ** ((midi_note - 69) / 12.0))
            duration_note = 0.5
            
            frames = int(duration_note * sample_rate)
            t = np.linspace(0, duration_note, frames, False)
            wave = np.sin(2 * np.pi * frequency * t)
            wave = (wave * 4096 * 0.2).astype(np.int16)
            
            stereo_wave = np.column_stack((wave, wave))
            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.play()
            time.sleep(duration_note * 0.8)
        
        print("✅ Test audio completato!")
        return True
        
    except Exception as e:
        print(f"❌ Errore nel test audio: {e}")
        return False

if __name__ == "__main__":
    test_simple_audio()
