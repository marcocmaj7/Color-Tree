#!/usr/bin/env python3
"""
Esempio di utilizzo della configurazione per la funzionalità degli intervalli
"""

from chord_generator import ChordGenerator, Note, Chord
from config import INTERVAL_CONFIG, APP_CONFIG

def demo_configuration():
    """Demo dell'utilizzo della configurazione"""
    
    print("=== Demo Configurazione Intervalli ===\n")
    
    # Mostra la configurazione corrente
    print("Configurazione corrente:")
    print("-" * 30)
    print(f"Modalità predefinita: {APP_CONFIG['default_display_mode']}")
    print(f"Analisi intervalli abilitata: {APP_CONFIG['enable_interval_analysis']}")
    print(f"Separatore intervalli: '{INTERVAL_CONFIG['interval_separator']}'")
    print(f"Mostra nomi completi: {INTERVAL_CONFIG['show_interval_names']}")
    
    print("\nSimboli degli intervalli disponibili:")
    print("-" * 40)
    for symbol, name in INTERVAL_CONFIG['interval_symbols'].items():
        print(f"  {symbol}: {name}")
    
    print("\n" + "=" * 50)
    
    # Demo con configurazione personalizzata
    print("\nDemo con configurazione personalizzata:")
    print("-" * 40)
    
    # Crea il generatore
    generator = ChordGenerator()
    
    # Genera alcuni accordi
    levels = generator.generate_triangular_chords(Note.C)
    
    print("Accordi con visualizzazione standard:")
    for i, level in enumerate(levels[:2]):
        print(f"\nLivello {i + 1}:")
        for j, chord in enumerate(level):
            print(f"  {j + 1}. {chord} -> {chord.to_intervals_string()}")
    
    print("\n" + "=" * 50)
    
    # Demo con analisi degli intervalli
    print("\nDemo con analisi degli intervalli:")
    print("-" * 40)
    
    # Crea alcuni accordi di esempio
    chords = [
        Chord([Note.C, Note.E, Note.G], Note.C),  # Maggiore
        Chord([Note.C, Note.D_SHARP, Note.G], Note.C),  # Minore
        Chord([Note.C, Note.E, Note.G, Note.A_SHARP], Note.C),  # Settima
    ]
    
    chord_names = ["Maggiore", "Minore", "Settima"]
    
    for chord, name in zip(chords, chord_names):
        print(f"\n{name}:")
        print(f"  Note: {chord}")
        print(f"  Intervalli: {chord.to_intervals_string()}")
        
        # Analisi dettagliata
        intervals = chord.get_intervals()
        print(f"  Analisi:")
        for interval in intervals:
            if interval in INTERVAL_CONFIG['interval_symbols']:
                full_name = INTERVAL_CONFIG['interval_symbols'][interval]
                print(f"    {interval}: {full_name}")
            else:
                print(f"    {interval}: Intervallo sconosciuto")

if __name__ == "__main__":
    demo_configuration()
