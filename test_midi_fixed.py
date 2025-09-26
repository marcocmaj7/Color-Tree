#!/usr/bin/env python3
"""
Test script per verificare la nuova implementazione MIDI senza threading
"""

from chord_generator import ChordGenerator, MIDIOutput, Note
import time

def test_midi_no_threading():
    """Testa la nuova implementazione MIDI senza threading"""
    print("Test della nuova implementazione MIDI (SENZA THREADING)...")
    
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
        from chord_generator import MIDIScaleGenerator
        midi_gen = MIDIScaleGenerator()
        
        print("\n🎵 Test 1: Accordi sequenziali (verifica stop_all_notes)")
        for i in range(3):
            test_cell = color_tree[1][i % len(color_tree[1])]
            midi_notes = midi_gen.generate_scale_notes(test_cell)
            print(f"  Accordo {i+1}: {len(midi_notes)} note - {test_cell}")
            midi_output.send_chord(midi_notes, duration=1.0, velocity=60)
            time.sleep(0.2)  # Pausa breve tra accordi
        
        print("\n🎵 Test 2: Accordi rapidi (verifica gestione race conditions)")
        print("  Invio 5 accordi molto rapidi...")
        for i in range(5):
            test_cell = color_tree[2][i % len(color_tree[2])]
            midi_notes = midi_gen.generate_scale_notes(test_cell)
            print(f"    Accordo rapido {i+1}: {len(midi_notes)} note")
            midi_output.send_chord(midi_notes, duration=0.5, velocity=70)
            time.sleep(0.05)  # Invio molto rapido
        
        print("\n🎵 Test 3: Test send_chord_immediate (nessun threading)")
        print("  Test accordi immediati...")
        for i in range(3):
            test_cell = color_tree[1][i % len(color_tree[1])]
            midi_notes = midi_gen.generate_scale_notes(test_cell)
            print(f"    Accordo immediato {i+1}: {len(midi_notes)} note")
            midi_output.send_chord_immediate(midi_notes, velocity=80)
            time.sleep(0.3)
        
        print("\n🎵 Test 4: Test stop_all_notes durante riproduzione")
        # Invia un accordo lungo
        test_cell = color_tree[1][0]
        midi_notes = midi_gen.generate_scale_notes(test_cell)
        print("  Invio accordo lungo (2 secondi)...")
        midi_output.send_chord(midi_notes, duration=2.0, velocity=50)
        
        # Aspetta un po' poi ferma tutto
        time.sleep(0.8)
        print("  Fermando tutte le note durante la riproduzione...")
        midi_output.stop_all_notes()
        time.sleep(0.5)
        
        print("\n🎵 Test 5: Test finale - accordi puliti")
        print("  Verifica che tutto funzioni correttamente...")
        for i in range(3):
            test_cell = color_tree[1][i % len(color_tree[1])]
            midi_notes = midi_gen.generate_scale_notes(test_cell)
            print(f"    Accordo finale {i+1}: {len(midi_notes)} note")
            midi_output.send_chord(midi_notes, duration=1.0, velocity=75)
            time.sleep(0.8)
        
        print("\n✅ Test completato! Controlla la tua DAW per verificare:")
        print("   ✅ Nessuna nota bloccata/tenuta")
        print("   ✅ Nessuna nota duplicata")
        print("   ✅ Velocity controllata")
        print("   ✅ Stop_all_notes funzionante")
        print("   ✅ Nessuna race condition")
        print("   ✅ Accordi puliti e precisi")
        
    else:
        print("❌ Impossibile connettersi alla porta MIDI")
        return False
    
    # Chiude la connessione
    midi_output.close()
    print("\nConnessione MIDI chiusa")
    
    return True

if __name__ == "__main__":
    test_midi_no_threading()
