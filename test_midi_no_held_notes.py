#!/usr/bin/env python3
"""
Test specifico per verificare che le note non vengano tenute/bloccate
"""

from chord_generator import ChordGenerator, MIDIOutput, Note
import time

def test_no_held_notes():
    """Test specifico per verificare che le note non vengano tenute"""
    print("Test specifico: VERIFICA CHE LE NOTE NON VENGANO TENUTE")
    print("=" * 60)
    
    # Crea il generatore di accordi
    generator = ChordGenerator()
    midi_output = MIDIOutput()
    
    if not midi_output.initialized:
        print("❌ MIDI non disponibile. Installa mido per testare l'output MIDI.")
        return False
    
    # Mostra le porte MIDI disponibili
    ports = midi_output.get_available_ports()
    if not ports:
        print("⚠️  Nessuna porta MIDI disponibile.")
        return False
    
    # Connessione
    test_port = ports[0]
    success = midi_output.set_output_port(test_port)
    if not success:
        print("❌ Impossibile connettersi alla porta MIDI")
        return False
    
    print("✅ Connessione MIDI riuscita")
    
    # Genera accordi di test
    color_tree = generator.generate_color_tree(Note.C)
    from chord_generator import MIDIScaleGenerator
    midi_gen = MIDIScaleGenerator()
    
    print("\n🎵 Test 1: Accordi sequenziali (verifica che ogni accordo fermi il precedente)")
    for i in range(5):
        test_cell = color_tree[1][i % len(color_tree[1])]
        midi_notes = midi_gen.generate_scale_notes(test_cell)
        print(f"  Accordo {i+1}: {len(midi_notes)} note - {test_cell}")
        
        # Usa il metodo sincrono che dovrebbe fermare tutto
        midi_output.send_chord(midi_notes, duration=0.5, velocity=60)
        print(f"    ✅ Accordo {i+1} inviato e fermato")
        time.sleep(0.2)
    
    print("\n🎵 Test 2: Test stop_all_notes manuale")
    # Invia un accordo
    test_cell = color_tree[1][0]
    midi_notes = midi_gen.generate_scale_notes(test_cell)
    print("  Invio accordo...")
    midi_output.send_chord_non_blocking(midi_notes, duration=0.1, velocity=70)
    time.sleep(0.05)
    print("  Chiamando stop_all_notes()...")
    midi_output.stop_all_notes()
    print("  ✅ stop_all_notes() chiamato")
    time.sleep(0.5)
    
    print("\n🎵 Test 3: Test accordi rapidi (verifica che non si sovrappongano)")
    for i in range(3):
        test_cell = color_tree[2][i % len(color_tree[2])]
        midi_notes = midi_gen.generate_scale_notes(test_cell)
        print(f"  Accordo rapido {i+1}: {len(midi_notes)} note")
        midi_output.send_chord_non_blocking(midi_notes, duration=0.1, velocity=80)
        time.sleep(0.05)  # Molto rapido
    
    print("\n🎵 Test 4: Test finale - verifica che tutto sia pulito")
    # Ferma tutto prima del test finale
    midi_output.stop_all_notes()
    time.sleep(0.2)
    
    # Test finale
    test_cell = color_tree[1][0]
    midi_notes = midi_gen.generate_scale_notes(test_cell)
    print("  Test finale: accordo pulito")
    midi_output.send_chord(midi_notes, duration=0.3, velocity=75)
    print("  ✅ Test finale completato")
    
    # Chiude la connessione
    midi_output.close()
    print("\n✅ Test completato! Se non senti note tenute, il problema è risolto.")
    print("   Controlla la tua DAW per verificare che:")
    print("   - Ogni accordo si fermi completamente")
    print("   - Non ci siano note bloccate")
    print("   - Gli accordi siano puliti e precisi")
    
    return True

if __name__ == "__main__":
    test_no_held_notes()
