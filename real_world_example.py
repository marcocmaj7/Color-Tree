#!/usr/bin/env python3
"""
Esempio di utilizzo reale della funzionalità degli intervalli
Simula un'applicazione per l'analisi armonica
"""

from chord_generator import ChordGenerator, Note, Chord
from typing import List, Dict, Tuple

class HarmonicAnalyzer:
    """Analizzatore armonico per accordi generati"""
    
    def __init__(self):
        self.generator = ChordGenerator()
    
    def find_chord_types(self, root: Note, levels: int = 5) -> Dict[str, List[Chord]]:
        """Trova diversi tipi di accordi nei livelli generati"""
        chord_levels = self.generator.generate_triangular_chords(root)
        chord_types = {
            'major': [],
            'minor': [],
            'seventh': [],
            'suspended': [],
            'diminished': [],
            'augmented': []
        }
        
        for level in chord_levels[:levels]:
            for chord in level:
                chord_type = self._classify_chord(chord)
                if chord_type in chord_types:
                    chord_types[chord_type].append(chord)
        
        return chord_types
    
    def _classify_chord(self, chord: Chord) -> str:
        """Classifica un accordo in base ai suoi intervalli"""
        intervals = chord.get_intervals()
        
        if '3' in intervals and '5' in intervals:
            if '7' in intervals or 'b7' in intervals:
                return 'seventh'
            else:
                return 'major'
        elif 'b3' in intervals and '5' in intervals:
            if '7' in intervals or 'b7' in intervals:
                return 'seventh'
            else:
                return 'minor'
        elif '4' in intervals and '5' in intervals:
            return 'suspended'
        elif 'b5' in intervals:
            return 'diminished'
        elif 'b5' in intervals and '3' in intervals:
            return 'augmented'
        else:
            return 'other'
    
    def analyze_harmonic_progression(self, root: Note, level: int) -> List[Dict]:
        """Analizza una progressione armonica"""
        levels = self.generator.generate_triangular_chords(root)
        if level >= len(levels):
            return []
        
        progression = []
        for i, chord in enumerate(levels[level]):
            analysis = {
                'position': i + 1,
                'chord': chord,
                'notes': str(chord),
                'intervals': chord.to_intervals_string(),
                'type': self._classify_chord(chord),
                'complexity': len(chord.notes),
                'harmonic_function': self._get_harmonic_function(chord, i, len(levels[level]))
            }
            progression.append(analysis)
        
        return progression
    
    def _get_harmonic_function(self, chord: Chord, position: int, total: int) -> str:
        """Determina la funzione armonica dell'accordo"""
        if position == 0:
            return 'Tonic'
        elif position == total - 1:
            return 'Dominant'
        else:
            return 'Subdominant'
    
    def generate_chord_voicings(self, root: Note, level: int) -> List[Dict]:
        """Genera diverse voicing per gli accordi"""
        levels = self.generator.generate_triangular_chords(root)
        if level >= len(levels):
            return []
        
        voicings = []
        for chord in levels[level]:
            voicing = {
                'chord': chord,
                'notes': str(chord),
                'intervals': chord.to_intervals_string(),
                'voicings': self._generate_voicings(chord)
            }
            voicings.append(voicing)
        
        return voicings
    
    def _generate_voicings(self, chord: Chord) -> List[str]:
        """Genera diverse voicing per un accordo"""
        # Implementazione semplificata - in realtà si dovrebbero generare
        # diverse disposizioni delle note
        voicings = []
        
        # Voicing originale
        voicings.append(str(chord))
        
        # Voicing con intervalli
        voicings.append(chord.to_intervals_string())
        
        # Voicing con analisi
        intervals = chord.get_intervals()
        analysis = []
        for interval in intervals:
            if interval == 'T':
                analysis.append('Root')
            elif interval == '3':
                analysis.append('Third')
            elif interval == 'b3':
                analysis.append('Minor Third')
            elif interval == '5':
                analysis.append('Fifth')
            elif interval == 'b7':
                analysis.append('Minor Seventh')
            elif interval == '7':
                analysis.append('Major Seventh')
            else:
                analysis.append(interval)
        
        voicings.append(' - '.join(analysis))
        
        return voicings

def main():
    """Esempio di utilizzo dell'analizzatore armonico"""
    
    print("=== Analizzatore Armonico - Esempio Reale ===\n")
    
    analyzer = HarmonicAnalyzer()
    
    # Analizza i tipi di accordi
    print("1. Analisi dei tipi di accordi per Do (C):")
    print("-" * 50)
    
    chord_types = analyzer.find_chord_types(Note.C, 4)
    
    for chord_type, chords in chord_types.items():
        if chords:
            print(f"\n{chord_type.upper()}:")
            for chord in chords[:3]:  # Mostra solo i primi 3
                print(f"  {chord} -> {chord.to_intervals_string()}")
    
    # Analizza una progressione armonica
    print(f"\n2. Progressione armonica per il livello 3:")
    print("-" * 50)
    
    progression = analyzer.analyze_harmonic_progression(Note.C, 2)
    
    for chord_analysis in progression:
        print(f"\nPosizione {chord_analysis['position']}:")
        print(f"  Accordo: {chord_analysis['notes']}")
        print(f"  Intervalli: {chord_analysis['intervals']}")
        print(f"  Tipo: {chord_analysis['type']}")
        print(f"  Funzione: {chord_analysis['harmonic_function']}")
        print(f"  Complessità: {chord_analysis['complexity']} note")
    
    # Genera voicing
    print(f"\n3. Voicing per il livello 2:")
    print("-" * 50)
    
    voicings = analyzer.generate_chord_voicings(Note.C, 1)
    
    for voicing in voicings:
        print(f"\nAccordo: {voicing['notes']}")
        print(f"Intervalli: {voicing['intervals']}")
        print("Voicing disponibili:")
        for v in voicing['voicings']:
            print(f"  - {v}")
    
    # Analisi comparativa
    print(f"\n4. Analisi comparativa per diverse note radice:")
    print("-" * 50)
    
    roots = [Note.C, Note.G, Note.F]
    root_names = ["Do (C)", "Sol (G)", "Fa (F)"]
    
    for root, name in zip(roots, root_names):
        print(f"\n{name}:")
        levels = analyzer.generator.generate_triangular_chords(root)
        level_2 = levels[1]  # Secondo livello
        
        for i, chord in enumerate(level_2):
            chord_type = analyzer._classify_chord(chord)
            print(f"  {i + 1}. {chord} -> {chord.to_intervals_string()} ({chord_type})")

if __name__ == "__main__":
    main()
