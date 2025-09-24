"""
Esempio di utilizzo del generatore di accordi
Mostra come usare le classi principali senza interfaccia grafica
"""

from chord_generator import ChordGenerator, Note

def main():
    """Esempio di utilizzo del generatore di accordi"""
    
    # Crea il generatore
    generator = ChordGenerator()
    
    print("=== Generatore di Accordi - Circolo delle Quinte ===\n")
    
    # Genera accordi per Do (C)
    print("Accordi generati per Do (C):")
    print("=" * 40)
    
    levels = generator.generate_triangular_chords(Note.C)
    
    for i, level in enumerate(levels[:6]):  # Mostra solo i primi 6 livelli
        print(f"\nLivello {i + 1}:")
        for j, chord in enumerate(level):
            print(f"  Posizione {j}: {chord}")
    
    print("\n" + "=" * 40)
    
    # Genera accordi per Sol (G)
    print("\nAccordi generati per Sol (G):")
    print("=" * 40)
    
    levels_g = generator.generate_triangular_chords(Note.G)
    
    for i, level in enumerate(levels_g[:4]):  # Mostra solo i primi 4 livelli
        print(f"\nLivello {i + 1}:")
        for j, chord in enumerate(level):
            print(f"  Posizione {j}: {chord}")
    
    print("\n" + "=" * 40)
    
    # Mostra informazioni sui livelli
    print(f"\nInformazioni:")
    print(f"- Numero totale di livelli: {len(levels)}")
    print(f"- Numero totale di accordi: {sum(len(level) for level in levels)}")
    
    # Mostra la struttura triangolare
    print(f"\nStruttura triangolare:")
    for i, level in enumerate(levels):
        print(f"  Livello {i + 1}: {len(level)} accordi")

if __name__ == "__main__":
    main()
