#!/usr/bin/env python3
"""
Esempio di utilizzo della funzionalità Creative Chord Patterns
"""

import sys
import os

# Aggiunge la directory corrente al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chord_generator import main

if __name__ == "__main__":
    print("=== Creative Chord Patterns Usage Example ===")
    print()
    print("1. Run the main application:")
    print("   python chord_generator.py")
    print()
    print("2. In the main window:")
    print("   - Click on any chord in the Color Tree to select it")
    print("   - Click the '🎵 Creative' button in the bottom left")
    print()
    print("3. In the Creative Chord window:")
    print("   - Select a pattern from the categories:")
    print("     * Base Patterns: Up, Down, Up-Down, Down-Up")
    print("     * Geometric Patterns: Triangle, Diamond, Zigzag, Spiral")
    print("     * Rhythmic Patterns: Gallop, Triplet, Syncopated, Stutter")
    print("     * Advanced Patterns: Skip, Ghost, Cascade, Bounce")
    print("     * Expressive Patterns: Crescendo, Diminuendo, Accent First, Swing")
    print("   - Adjust octave (2-6) and duration (0.1-1.0s)")
    print("   - Enable loop if desired")
    print("   - Click '▶ Play' to start playback")
    print("   - Click '⏹ Stop' to stop playback")
    print()
    print("4. Features:")
    print("   - Real-time audio playback using pygame")
    print("   - MIDI output support (if configured)")
    print("   - Visual feedback and status messages")
    print("   - Multiple pattern types for creative exploration")
    print()
    print("Starting the application...")
    print()
    
    # Avvia l'applicazione principale
    main()
