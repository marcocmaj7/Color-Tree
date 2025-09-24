#!/usr/bin/env python3
"""
Demo della funzionalità degli intervalli
Mostra come usare la visualizzazione duale note/intervalli
"""

from chord_generator import ChordGenerator, Note, Chord

def demo_intervals():
    """Demo della funzionalità degli intervalli"""
    
    print("=== Demo Funzionalità Intervalli ===\n")
    
    # Crea il generatore
    generator = ChordGenerator()
    
    # Genera accordi per Do (C)
    levels = generator.generate_triangular_chords(Note.C)
    
    print("Accordi generati per Do (C):")
    print("=" * 60)
    
    for i, level in enumerate(levels[:4]):  # Mostra solo i primi 4 livelli
        print(f"\nLivello {i + 1}:")
        for j, chord in enumerate(level):
            print(f"  Posizione {j + 1}:")
            print(f"    Note:        {chord}")
            print(f"    Intervalli:  {chord.to_intervals_string()}")
            print(f"    Dettagli:    {chord.get_intervals()}")
    
    print("\n" + "=" * 60)
    
    # Demo con accordi specifici
    print("\nDemo con accordi specifici:")
    print("-" * 40)
    
    # Crea alcuni accordi di esempio
    chords = [
        Chord([Note.C, Note.E, Note.G], Note.C),  # Maggiore
        Chord([Note.C, Note.D_SHARP, Note.G], Note.C),  # Minore
        Chord([Note.C, Note.E, Note.G, Note.A_SHARP], Note.C),  # Settima
        Chord([Note.C, Note.E, Note.G, Note.A], Note.C),  # Sesta
        Chord([Note.C, Note.E, Note.F_SHARP], Note.C),  # Quinta diminuita
    ]
    
    chord_names = [
        "Maggiore (C-E-G)",
        "Minore (C-Eb-G)", 
        "Settima (C-E-G-Bb)",
        "Sesta (C-E-G-A)",
        "Quinta diminuita (C-E-Gb)"
    ]
    
    for chord, name in zip(chords, chord_names):
        print(f"\n{name}:")
        print(f"  Note:       {chord}")
        print(f"  Intervalli: {chord.to_intervals_string()}")
        print(f"  Dettagli:   {chord.get_intervals()}")
    
    print("\n" + "=" * 60)
    
    # Demo con diverse note radice
    print("\nDemo con diverse note radice:")
    print("-" * 40)
    
    roots = [Note.C, Note.G, Note.F]
    root_names = ["Do (C)", "Sol (G)", "Fa (F)"]
    
    for root, name in zip(roots, root_names):
        print(f"\n{name}:")
        levels = generator.generate_triangular_chords(root)
        level_2 = levels[1]  # Secondo livello
        
        for j, chord in enumerate(level_2):
            print(f"  {j + 1}. {chord} -> {chord.to_intervals_string()}")

if __name__ == "__main__":
    demo_intervals()
