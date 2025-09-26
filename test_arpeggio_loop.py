#!/usr/bin/env python3
"""
Test specifico per arpeggi in loop - verifica che le note non vengano bloccate
"""

from chord_generator import ChordGenerator, MIDIOutput, Note, MIDIScaleGenerator
from pattern_engine import PatternEngine, PatternType
import time

def test_arpeggio_loop():
    """Test specifico per arpeggi in loop"""
    print("Test specifico: ARPEGGI IN LOOP - VERIFICA NOTE NON BLOCCATE")
    print("=" * 70)
    
    # Crea i componenti
    generator = ChordGenerator()
    midi_output = MIDIOutput()
    midi_gen = MIDIScaleGenerator()
    
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
    
    # Crea il pattern engine
    pattern_engine = PatternEngine(midi_gen, midi_output)
    
    # Genera accordi di test
    color_tree = generator.generate_color_tree(Note.C)
    test_cell = color_tree[1][0]  # Primo accordo del secondo livello
    
    print(f"\n🎵 Test accordo: {test_cell}")
    print(f"   Note: {[note.name for note in test_cell.notes]}")
    
    print("\n🎵 Test 1: Arpeggio UP singolo (no loop)")
    print("  Avvio arpeggio UP singolo...")
    pattern_engine.play_pattern(
        test_cell,
        PatternType.UP,
        octave=4,
        base_duration=0.2,
        loop=False,
        reverse=False,
        duration_octaves=1,
        playback_speed=1.0,
        bpm=120,
        pause_duration=0.0
    )
    
    # Aspetta che finisca
    while pattern_engine.is_pattern_playing():
        time.sleep(0.1)
    
    print("  ✅ Arpeggio singolo completato")
    time.sleep(0.5)
    
    print("\n🎵 Test 2: Arpeggio UP in loop (3 secondi)")
    print("  Avvio arpeggio UP in loop...")
    pattern_engine.play_pattern(
        test_cell,
        PatternType.UP,
        octave=4,
        base_duration=0.15,
        loop=True,
        reverse=False,
        duration_octaves=1,
        playback_speed=1.0,
        bpm=120,
        pause_duration=0.0
    )
    
    # Lascia suonare per 3 secondi
    time.sleep(3.0)
    
    print("  Fermando arpeggio in loop...")
    pattern_engine.stop_pattern()
    print("  ✅ Arpeggio in loop fermato")
    time.sleep(0.5)
    
    print("\n🎵 Test 3: Arpeggio DOWN in loop (2 secondi)")
    print("  Avvio arpeggio DOWN in loop...")
    pattern_engine.play_pattern(
        test_cell,
        PatternType.DOWN,
        octave=4,
        base_duration=0.1,
        loop=True,
        reverse=False,
        duration_octaves=1,
        playback_speed=1.5,
        bpm=120,
        pause_duration=0.0
    )
    
    # Lascia suonare per 2 secondi
    time.sleep(2.0)
    
    print("  Fermando arpeggio DOWN...")
    pattern_engine.stop_pattern()
    print("  ✅ Arpeggio DOWN fermato")
    time.sleep(0.5)
    
    print("\n🎵 Test 4: Arpeggio UP-DOWN in loop (2 secondi)")
    print("  Avvio arpeggio UP-DOWN in loop...")
    pattern_engine.play_pattern(
        test_cell,
        PatternType.UP_DOWN,
        octave=4,
        base_duration=0.12,
        loop=True,
        reverse=False,
        duration_octaves=2,
        playback_speed=1.0,
        bpm=120,
        pause_duration=0.0
    )
    
    # Lascia suonare per 2 secondi
    time.sleep(2.0)
    
    print("  Fermando arpeggio UP-DOWN...")
    pattern_engine.stop_pattern()
    print("  ✅ Arpeggio UP-DOWN fermato")
    time.sleep(0.5)
    
    print("\n🎵 Test 5: Test finale - verifica che tutto sia pulito")
    # Ferma tutto prima del test finale
    midi_output.stop_all_notes()
    time.sleep(0.2)
    
    # Test finale con accordo semplice
    print("  Test finale: accordo semplice")
    midi_notes = midi_gen.generate_scale_notes(test_cell)
    midi_output.send_chord(midi_notes, duration=0.5, velocity=75)
    print("  ✅ Test finale completato")
    
    # Chiude la connessione
    midi_output.close()
    print("\n✅ Test arpeggi in loop completato!")
    print("   Controlla la tua DAW per verificare che:")
    print("   - Gli arpeggi in loop non lascino note bloccate")
    print("   - Lo stop funzioni immediatamente")
    print("   - Non ci siano note duplicate o sovrapposte")
    print("   - Il timing sia preciso e pulito")
    
    return True

if __name__ == "__main__":
    test_arpeggio_loop()
