"""
Esempio di integrazione del Chord Generator in altri progetti
Mostra come usare le classi principali per creare funzionalità personalizzate
"""

from chord_generator import ChordGenerator, Note, Chord
from typing import List, Dict

class CustomChordAnalyzer:
    """Analizzatore personalizzato per accordi generati"""
    
    def __init__(self):
        self.generator = ChordGenerator()
    
    def analyze_chord_complexity(self, chord: Chord) -> Dict[str, int]:
        """Analizza la complessità di un accordo"""
        return {
            'note_count': len(chord.notes),
            'unique_intervals': len(set(chord.notes)),
            'complexity_score': len(chord.notes) * 2,
            'interval_count': len(chord.get_intervals())
        }
    
    def find_chord_by_notes(self, target_notes: List[Note], root: Note = Note.C) -> List[Chord]:
        """Trova accordi che contengono le note specificate"""
        levels = self.generator.generate_triangular_chords(root)
        matching_chords = []
        
        for level in levels:
            for chord in level:
                if all(note in chord.notes for note in target_notes):
                    matching_chords.append(chord)
        
        return matching_chords
    
    def generate_chord_progression(self, root: Note, level: int) -> List[Chord]:
        """Genera una progressione di accordi per un livello specifico"""
        levels = self.generator.generate_triangular_chords(root)
        if level < len(levels):
            return levels[level]
        return []
    
    def analyze_chord_intervals(self, chord: Chord) -> Dict[str, any]:
        """Analizza gli intervalli di un accordo"""
        intervals = chord.get_intervals()
        return {
            'intervals': intervals,
            'interval_string': chord.to_intervals_string(),
            'has_third': '3' in intervals or 'b3' in intervals,
            'has_fifth': '5' in intervals or 'b5' in intervals,
            'has_seventh': '7' in intervals or 'b7' in intervals,
            'is_major': '3' in intervals,
            'is_minor': 'b3' in intervals
        }
    
    def export_chords_to_text(self, root: Note, filename: str) -> None:
        """Esporta gli accordi in un file di testo"""
        levels = self.generator.generate_triangular_chords(root)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Accordi generati per {root.name}\n")
            f.write("=" * 50 + "\n\n")
            
            for i, level in enumerate(levels):
                f.write(f"Livello {i + 1}:\n")
                for j, chord in enumerate(level):
                    f.write(f"  {j + 1}. {chord} ({chord.to_intervals_string()})\n")
                f.write("\n")

def main():
    """Esempio di utilizzo dell'analizzatore personalizzato"""
    
    analyzer = CustomChordAnalyzer()
    
    print("=== Analizzatore di Accordi Personalizzato ===\n")
    
    # Analizza la complessità degli accordi
    print("Analisi della complessità degli accordi:")
    print("-" * 40)
    
    levels = analyzer.generator.generate_triangular_chords(Note.C)
    for i, level in enumerate(levels[:3]):
        print(f"\nLivello {i + 1}:")
        for j, chord in enumerate(level):
            complexity = analyzer.analyze_chord_complexity(chord)
            print(f"  {chord}: {complexity}")
    
    # Analizza gli intervalli degli accordi
    print(f"\nAnalisi degli intervalli degli accordi:")
    print("-" * 40)
    
    for i, level in enumerate(levels[:3]):
        print(f"\nLivello {i + 1}:")
        for j, chord in enumerate(level):
            interval_analysis = analyzer.analyze_chord_intervals(chord)
            print(f"  {chord}: {interval_analysis}")
    
    # Trova accordi che contengono note specifiche
    print(f"\nAccordi che contengono Do e Sol:")
    print("-" * 40)
    
    target_notes = [Note.C, Note.G]
    matching_chords = analyzer.find_chord_by_notes(target_notes, Note.C)
    
    for chord in matching_chords[:5]:  # Mostra solo i primi 5
        print(f"  {chord}")
    
    # Genera una progressione per il livello 3
    print(f"\nProgressione per il livello 3:")
    print("-" * 40)
    
    progression = analyzer.generate_chord_progression(Note.C, 2)
    for i, chord in enumerate(progression):
        print(f"  {i + 1}. {chord}")
    
    # Esporta gli accordi
    print(f"\nEsportazione degli accordi...")
    analyzer.export_chords_to_text(Note.C, "chords_export.txt")
    print("Accordi esportati in 'chords_export.txt'")

if __name__ == "__main__":
    main()
