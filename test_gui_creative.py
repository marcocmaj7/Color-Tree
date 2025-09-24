#!/usr/bin/env python3
"""
Test script per verificare l'interfaccia grafica della finestra creativa
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Aggiunge la directory corrente al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chord_generator import ChordGenerator, Note, SoundCell, MIDIScaleGenerator
from creative_chord_window import CreativeChordWindow

def test_creative_window():
    """Testa l'apertura della finestra creativa"""
    print("Testing Creative Chord Window GUI...")
    
    try:
        # Crea una finestra di test
        root = tk.Tk()
        root.title("Test Creative Window")
        root.geometry("400x300")
        
        # Genera una sound cell di test
        generator = ChordGenerator()
        midi_gen = MIDIScaleGenerator()
        color_tree = generator.generate_color_tree(Note.C)
        test_sound_cell = color_tree[2][1]  # Livello 3, posizione 1
        
        print(f"Test Sound Cell: {test_sound_cell}")
        
        # Crea la finestra creativa
        creative_window = CreativeChordWindow(root, test_sound_cell, midi_gen)
        
        # Mostra la finestra
        creative_window.show()
        
        print("✓ Creative window opened successfully!")
        print("✓ All controls should be visible:")
        print("  - Play/Stop buttons")
        print("  - Loop checkbox")
        print("  - Octave slider (2-6)")
        print("  - Duration slider (0.1-1.0s)")
        print("  - Pattern selection radio buttons")
        print("  - Status log area")
        
        # Mostra un messaggio di conferma
        messagebox.showinfo("Test Success", 
                           "Creative window opened successfully!\n\n"
                           "You should see:\n"
                           "• Large PLAY/STOP buttons\n"
                           "• Octave and Duration sliders\n"
                           "• Pattern selection options\n"
                           "• Status log area\n\n"
                           "Close this window to continue the test.")
        
        # Avvia il loop principale per mostrare la finestra
        root.mainloop()
        
        print("✓ Test completed successfully!")
        
    except Exception as e:
        print(f"✗ Error testing creative window: {str(e)}")
        messagebox.showerror("Test Error", f"Error: {str(e)}")

if __name__ == "__main__":
    test_creative_window()
