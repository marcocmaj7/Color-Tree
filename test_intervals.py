"""
Test per la nuova funzionalità degli intervalli
"""

from chord_generator import ChordGenerator, Note, Chord

def test_intervals():
    """Test della funzionalità degli intervalli"""
    
    print("=== Test Funzionalità Intervalli ===\n")
    
    # Crea il generatore
    generator = ChordGenerator()
    
    # Genera accordi per Do (C)
    levels = generator.generate_triangular_chords(Note.C)
    
    print("Accordi generati per Do (C):")
    print("=" * 50)
    
    for i, level in enumerate(levels[:4]):  # Mostra solo i primi 4 livelli
        print(f"\nLivello {i + 1}:")
        for j, chord in enumerate(level):
            print(f"  Posizione {j}:")
            print(f"    Note: {chord}")
            print(f"    Intervalli: {chord.to_intervals_string()}")
            print(f"    Intervalli dettagliati: {chord.get_intervals()}")
    
    print("\n" + "=" * 50)
    
    # Test con accordi specifici
    print("\nTest con accordi specifici:")
    print("-" * 30)
    
    # Accordo maggiore (C-E-G)
    major_chord = Chord([Note.C, Note.E, Note.G], Note.C)
    print(f"Accordo maggiore: {major_chord}")
    print(f"Intervalli: {major_chord.to_intervals_string()}")
    
    # Accordo minore (C-Eb-G)
    minor_chord = Chord([Note.C, Note.D_SHARP, Note.G], Note.C)
    print(f"Accordo minore: {minor_chord}")
    print(f"Intervalli: {minor_chord.to_intervals_string()}")
    
    # Accordo di settima (C-E-G-Bb)
    seventh_chord = Chord([Note.C, Note.E, Note.G, Note.A_SHARP], Note.C)
    print(f"Accordo di settima: {seventh_chord}")
    print(f"Intervalli: {seventh_chord.to_intervals_string()}")
    
    print("\n" + "=" * 50)
    
    # Test con note alterate
    print("\nTest con note alterate:")
    print("-" * 30)
    
    # Accordo con quinta diminuita (C-E-Gb)
    dim_chord = Chord([Note.C, Note.E, Note.F_SHARP], Note.C)
    print(f"Accordo con quinta diminuita: {dim_chord}")
    print(f"Intervalli: {dim_chord.to_intervals_string()}")
    
    # Accordo con sesta maggiore (C-E-G-A)
    sixth_chord = Chord([Note.C, Note.E, Note.G, Note.A], Note.C)
    print(f"Accordo con sesta maggiore: {sixth_chord}")
    print(f"Intervalli: {sixth_chord.to_intervals_string()}")

if __name__ == "__main__":
    test_intervals()
