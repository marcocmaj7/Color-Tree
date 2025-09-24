#!/usr/bin/env python3
"""
Test migliorato per verificare la qualità audio con fade e envelope
"""

import pygame
import time
import numpy as np

def test_improved_audio():
    """Test di riproduzione audio migliorata"""
    print("Test audio migliorato...")
    
    try:
        # Inizializza pygame mixer
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        print("✅ Pygame mixer inizializzato")
        
        # Test 1: Tono con fade
        print("🎵 Test 1: Tono di 440Hz con fade...")
        frequency = 440.0
        duration = 2.0
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Genera onda sinusoidale
        t = np.linspace(0, duration, frames, False)
        wave = np.sin(2 * np.pi * frequency * t)
        
        # Aggiunge fade-in e fade-out
        fade_samples = int(0.01 * sample_rate)  # 10ms
        if frames > 2 * fade_samples:
            wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
            wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        # Applica envelope
        envelope = np.exp(-t * 1.5)
        wave *= envelope
        
        # Riduce volume per evitare clipping
        wave = (wave * 2048 * 0.3).astype(np.int16)
        
        # Crea stereo
        stereo_wave = np.column_stack((wave, wave))
        
        # Riproduce
        sound = pygame.sndarray.make_sound(stereo_wave)
        sound.play()
        time.sleep(duration + 0.5)
        
        # Test 2: Scala Do maggiore migliorata
        print("🎵 Test 2: Scala Do maggiore migliorata...")
        notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C, D, E, F, G, A, B, C
        
        for i, midi_note in enumerate(notes):
            frequency = 440.0 * (2 ** ((midi_note - 69) / 12.0))
            duration_note = 0.6
            
            frames = int(duration_note * sample_rate)
            t = np.linspace(0, duration_note, frames, False)
            wave = np.sin(2 * np.pi * frequency * t)
            
            # Fade-in e fade-out
            fade_samples = int(0.01 * sample_rate)
            if frames > 2 * fade_samples:
                wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
                wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            
            # Envelope
            envelope = np.exp(-t * 2)
            wave *= envelope
            
            # Volume bilanciato
            volume = 0.25 if i == 0 else 0.15
            wave = (wave * 2048 * volume).astype(np.int16)
            
            stereo_wave = np.column_stack((wave, wave))
            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.play()
            time.sleep(duration_note * 0.7)
        
        print("✅ Test audio migliorato completato!")
        return True
        
    except Exception as e:
        print(f"❌ Errore nel test audio: {e}")
        return False

if __name__ == "__main__":
    test_improved_audio()
