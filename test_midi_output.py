#!/usr/bin/env python3
"""
Test script per verificare la funzionalità MIDI output della Color Tree
"""

from chord_generator import ChordGenerator, MIDIOutput, Note

def test_midi_output():
    """Testa la funzionalità MIDI output"""
    print("Test della funzionalità MIDI output...")
    
    # Crea il generatore di accordi
    generator = ChordGenerator()
    
    # Crea il generatore MIDI output
    midi_output = MIDIOutput()
    
    if not midi_output.initialized:
        print("❌ MIDI non disponibile. Installa mido per testare l'output MIDI.")
        print("   pip install mido")
        return False
    
    print("✅ MIDI inizializzato correttamente")
    
    # Mostra le porte MIDI disponibili
    ports = midi_output.get_available_ports()
    print(f"Porte MIDI disponibili: {ports}")
    
    if not ports:
        print("⚠️  Nessuna porta MIDI disponibile. Crea una porta MIDI virtuale per testare.")
        print("   Su Windows: usa loopMIDI")
        print("   Su macOS: usa Configurazione Audio MIDI > Driver IAC")
        return False
    
    # Testa la connessione alla prima porta disponibile
    test_port = ports[0]
    print(f"Test connessione alla porta: {test_port}")
    
    success = midi_output.set_output_port(test_port)
    if success:
        print("✅ Connessione MIDI riuscita")
        
        # Genera una Color Tree di test
        color_tree = generator.generate_color_tree(Note.C)
        
        # Testa l'invio di un accordo MIDI
        test_cell = color_tree[1][0]  # Livello 2, posizione 0
        print(f"Test invio accordo: {test_cell}")
        
        # Genera le note MIDI
        from chord_generator import MIDIScaleGenerator
        midi_gen = MIDIScaleGenerator()
        midi_notes = midi_gen.generate_scale_notes(test_cell)
        print(f"Note MIDI: {midi_notes}")
        
        # Invia l'accordo MIDI
        print("🎵 Invio accordo MIDI...")
        midi_output.send_chord(midi_notes, duration=1.0)
        
        print("✅ Test completato! Controlla la tua DAW per verificare la ricezione MIDI.")
        
    else:
        print("❌ Impossibile connettersi alla porta MIDI")
        return False
    
    # Chiude la connessione
    midi_output.close()
    print("Connessione MIDI chiusa")
    
    return True

if __name__ == "__main__":
    test_midi_output()
