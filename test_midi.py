#!/usr/bin/env python3
"""
Test script per verificare la funzionalità MIDI della Color Tree
"""

from chord_generator import ChordGenerator, MIDIScaleGenerator, Note

def test_midi_functionality():
    """Testa la generazione e riproduzione MIDI"""
    print("Test della funzionalità MIDI...")
    
    # Crea il generatore di accordi
    generator = ChordGenerator()
    
    # Crea il generatore MIDI
    midi_gen = MIDIScaleGenerator()
    
    if not midi_gen.initialized:
        print("❌ Pygame non disponibile. Installa pygame per testare l'audio.")
        print("   pip install pygame")
        return False
    
    print("✅ Pygame inizializzato correttamente")
    
    # Genera una Color Tree di test
    color_tree = generator.generate_color_tree(Note.C)
    
    # Testa alcune sound cells
    test_cells = [
        (1, 0),  # Livello 1, posizione 0 (solo root)
        (2, 0),  # Livello 2, posizione 0 (quinta sotto)
        (2, 1),  # Livello 2, posizione 1 (quinta sopra)
        (3, 1),  # Livello 3, posizione 1 (pentatonica)
    ]
    
    print("\nTest delle scale MIDI:")
    for level, position in test_cells:
        if level <= len(color_tree) and position < len(color_tree[level-1]):
            cell = color_tree[level-1][position]
            print(f"  Livello {level}, Posizione {position}: {cell}")
            
            # Genera le note MIDI
            midi_notes = midi_gen.generate_scale_notes(cell)
            print(f"    Note MIDI: {midi_notes}")
            
            # Riproduce la scala (solo per il primo test)
            if level == 1 and position == 0:
                print("    🎵 Riproduzione della scala...")
                midi_gen.play_scale(cell, duration=0.3)
    
    print("\n✅ Test completato!")
    return True

if __name__ == "__main__":
    test_midi_functionality()
