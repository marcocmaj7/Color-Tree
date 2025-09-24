"""
Test per il generatore di accordi
Verifica che la logica del circolo delle quinte funzioni correttamente
"""

import unittest
from chord_generator import Note, CircleOfFifths, ChordGenerator, Chord


class TestCircleOfFifths(unittest.TestCase):
    """Test per la classe CircleOfFifths"""
    
    def setUp(self):
        self.circle = CircleOfFifths()
    
    def test_fifth_up(self):
        """Test quinta ascendente"""
        self.assertEqual(self.circle.get_fifth_up(Note.C), Note.G)
        self.assertEqual(self.circle.get_fifth_up(Note.G), Note.D)
        self.assertEqual(self.circle.get_fifth_up(Note.F), Note.C)
    
    def test_fifth_down(self):
        """Test quinta discendente"""
        self.assertEqual(self.circle.get_fifth_down(Note.C), Note.F)
        self.assertEqual(self.circle.get_fifth_down(Note.G), Note.C)
        self.assertEqual(self.circle.get_fifth_down(Note.F), Note.A_SHARP)
    
    def test_interval(self):
        """Test intervalli generici"""
        self.assertEqual(self.circle.get_interval(Note.C, 7), Note.G)  # Quinta
        self.assertEqual(self.circle.get_interval(Note.C, 4), Note.E)  # Terza maggiore
        self.assertEqual(self.circle.get_interval(Note.C, 0), Note.C)  # Unisono


class TestChordGenerator(unittest.TestCase):
    """Test per la classe ChordGenerator"""
    
    def setUp(self):
        self.generator = ChordGenerator()
    
    def test_triangular_structure(self):
        """Test che la struttura sia triangolare"""
        levels = self.generator.generate_triangular_chords(Note.C)
        
        # Verifica che ci siano 12 livelli
        self.assertEqual(len(levels), 12)
        
        # Verifica che ogni livello abbia il numero corretto di accordi
        for i, level in enumerate(levels):
            self.assertEqual(len(level), i + 1)
    
    def test_first_level(self):
        """Test primo livello (solo nota radice)"""
        levels = self.generator.generate_triangular_chords(Note.C)
        first_level = levels[0]
        
        self.assertEqual(len(first_level), 1)
        self.assertEqual(first_level[0].notes, [Note.C])
        self.assertEqual(first_level[0].root, Note.C)
    
    def test_second_level(self):
        """Test secondo livello (C F - C G)"""
        levels = self.generator.generate_triangular_chords(Note.C)
        second_level = levels[1]
        
        self.assertEqual(len(second_level), 2)
        
        # Primo accordo: C F (quinta discendente)
        self.assertEqual(second_level[0].notes, [Note.F, Note.C])
        
        # Secondo accordo: C G (quinta ascendente)
        self.assertEqual(second_level[1].notes, [Note.C, Note.G])
    
    def test_third_level(self):
        """Test terzo livello (C F Bb - C F G - C D G)"""
        levels = self.generator.generate_triangular_chords(Note.C)
        third_level = levels[2]
        
        self.assertEqual(len(third_level), 3)
        
        # Primo accordo: C F Bb (due quinte discendenti)
        expected_first = [Note.A_SHARP, Note.F, Note.C]
        self.assertEqual(third_level[0].notes, expected_first)
        
        # Secondo accordo: C F G (una quinta discendente, una ascendente)
        expected_second = [Note.F, Note.C, Note.G]
        self.assertEqual(third_level[1].notes, expected_second)
        
        # Terzo accordo: C G D (una quinta ascendente, una terza maggiore)
        expected_third = [Note.C, Note.G, Note.D]
        self.assertEqual(third_level[2].notes, expected_third)


class TestChord(unittest.TestCase):
    """Test per la classe Chord"""
    
    def test_chord_creation(self):
        """Test creazione accordo"""
        chord = Chord([Note.C, Note.E, Note.G], Note.C)
        self.assertEqual(chord.notes, [Note.C, Note.E, Note.G])
        self.assertEqual(chord.root, Note.C)
    
    def test_chord_string_representation(self):
        """Test rappresentazione stringa"""
        chord = Chord([Note.C, Note.E, Note.G], Note.C)
        expected = "C - E - G"
        self.assertEqual(str(chord), expected)
    
    def test_chord_intervals(self):
        """Test calcolo degli intervalli"""
        chord = Chord([Note.C, Note.E, Note.G], Note.C)
        expected_intervals = ["T", "3", "5"]
        self.assertEqual(chord.get_intervals(), expected_intervals)
    
    def test_chord_intervals_string(self):
        """Test rappresentazione stringa degli intervalli"""
        chord = Chord([Note.C, Note.E, Note.G], Note.C)
        expected = "T - 3 - 5"
        self.assertEqual(chord.to_intervals_string(), expected)
    
    def test_chord_intervals_with_sharps(self):
        """Test intervalli con note alterate"""
        chord = Chord([Note.C, Note.F, Note.A_SHARP], Note.C)
        expected_intervals = ["T", "4", "b7"]
        self.assertEqual(chord.get_intervals(), expected_intervals)


def run_tests():
    """Esegue tutti i test"""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()
