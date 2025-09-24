#!/usr/bin/env python3
"""
Test script per verificare il funzionamento dei pattern creativi
"""

import sys
import os

# Aggiunge la directory corrente al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chord_generator import ChordGenerator, Note, SoundCell, MIDIScaleGenerator
from pattern_engine import PatternEngine, PatternType

def test_pattern_generation():
    """Testa la generazione di tutti i pattern"""
    print("Testing Creative Chord Patterns...")
    
    # Inizializza i componenti
    generator = ChordGenerator()
    midi_gen = MIDIScaleGenerator()
    pattern_engine = PatternEngine(midi_gen)
    
    # Genera una sound cell di test (livello 3 - pentatonica)
    color_tree = generator.generate_color_tree(Note.C)
    test_sound_cell = color_tree[2][1]  # Livello 3, posizione 1
    
    print(f"Test Sound Cell: {test_sound_cell}")
    print(f"Notes: {[note.name for note in test_sound_cell.notes]}")
    print()
    
    # Testa tutti i pattern
    patterns_to_test = [
        # Pattern Base
        (PatternType.UP, "Ascendente semplice"),
        (PatternType.DOWN, "Discendente semplice"),
        (PatternType.UP_DOWN, "Su poi giù"),
        (PatternType.DOWN_UP, "Giù poi su"),
        
        # Pattern Geometrici
        (PatternType.TRIANGLE, "Triangolo melodico"),
        (PatternType.DIAMOND, "Dentro-fuori-dentro"),
        (PatternType.ZIGZAG, "Alternanza estremi-centro"),
        (PatternType.SPIRAL, "Giri concentrici"),
        
        # Pattern Ritmici
        (PatternType.GALLOP, "Due note veloci + una lunga"),
        (PatternType.TRIPLET, "Gruppetti di tre note"),
        (PatternType.SYNCOPATED, "Enfasi sui tempi deboli"),
        (PatternType.STUTTER, "Ripetizione rapida"),
        
        # Pattern Avanzati
        (PatternType.SKIP, "Salta note casualmente"),
        (PatternType.GHOST, "Include note fantasma"),
        (PatternType.CASCADE, "Effetto cascata"),
        (PatternType.BOUNCE, "Rimbalza tra estremi"),
        
        # Pattern Espressivi
        (PatternType.CRESCENDO, "Volume crescente"),
        (PatternType.DIMINUENDO, "Volume decrescente"),
        (PatternType.ACCENT_FIRST, "Prima nota accentata"),
        (PatternType.SWING, "Timing swing")
    ]
    
    print("Testing pattern generation...")
    for pattern_type, description in patterns_to_test:
        try:
            # Genera le note del pattern
            pattern_notes = pattern_engine.generate_pattern_notes(
                test_sound_cell, pattern_type, octave=4, base_duration=0.2
            )
            
            print(f"✓ {pattern_type.value}: {description}")
            print(f"  Generated {len(pattern_notes)} note events")
            
            # Mostra le prime 3 note per verifica
            if pattern_notes:
                first_notes = pattern_notes[:3]
                note_names = [f"{note.note.name}{note.octave}" for note in first_notes]
                print(f"  First notes: {' → '.join(note_names)}")
            print()
            
        except Exception as e:
            print(f"✗ {pattern_type.value}: ERROR - {str(e)}")
            print()
    
    print("Pattern generation test completed!")

def test_audio_playback():
    """Testa la riproduzione audio (solo se pygame è disponibile)"""
    print("\nTesting audio playback...")
    
    try:
        import pygame
        print("✓ Pygame available - audio playback should work")
        
        # Test di riproduzione breve
        generator = ChordGenerator()
        midi_gen = MIDIScaleGenerator()
        pattern_engine = PatternEngine(midi_gen)
        
        color_tree = generator.generate_color_tree(Note.C)
        test_sound_cell = color_tree[1][0]  # Livello 2, posizione 0
        
        print("Playing a short test pattern...")
        pattern_engine.play_pattern(
            test_sound_cell, 
            PatternType.UP, 
            octave=4, 
            base_duration=0.1, 
            loop=False
        )
        
        # Aspetta un momento per la riproduzione
        import time
        time.sleep(2)
        
        print("✓ Audio playback test completed!")
        
    except ImportError:
        print("✗ Pygame not available - audio playback will not work")
        print("Install pygame with: pip install pygame")

if __name__ == "__main__":
    test_pattern_generation()
    test_audio_playback()
    print("\nAll tests completed!")
