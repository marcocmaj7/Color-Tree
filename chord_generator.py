"""
Chord Generator App - Generatore di accordi basato sul circolo delle quinte
Seguendo le best practices Python con struttura modulare e OOP
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
from dataclasses import dataclass
from enum import Enum
import math


class Note(Enum):
    """Enum per le 12 note cromatiche"""
    C = 0
    C_SHARP = 1  # Db
    D = 2
    D_SHARP = 3  # Eb
    E = 4
    F = 5
    F_SHARP = 6  # Gb
    G = 7
    G_SHARP = 8  # Ab
    A = 9
    A_SHARP = 10  # Bb
    B = 11


@dataclass
class Chord:
    """Rappresenta un accordo con le sue note"""
    notes: List[Note]
    root: Note
    
    def __str__(self) -> str:
        """Rappresentazione stringa dell'accordo"""
        note_names = {
            Note.C: "C", Note.C_SHARP: "C#", Note.D: "D", Note.D_SHARP: "D#",
            Note.E: "E", Note.F: "F", Note.F_SHARP: "F#", Note.G: "G",
            Note.G_SHARP: "G#", Note.A: "A", Note.A_SHARP: "A#", Note.B: "B"
        }
        return " - ".join(note_names[note] for note in self.notes)
    
    def get_intervals(self) -> List[str]:
        """Calcola gli intervalli dell'accordo rispetto alla nota radice"""
        intervals = []
        
        for note in self.notes:
            if note == self.root:
                intervals.append("T")  # Tonic (Tonica)
            else:
                # Calcola la distanza in semitoni dalla nota radice
                semitones = (note.value - self.root.value) % 12
                interval_name = self._semitones_to_interval(semitones)
                intervals.append(interval_name)
        
        return intervals
    
    def _semitones_to_interval(self, semitones: int) -> str:
        """Converte semitoni in nome dell'intervallo"""
        interval_map = {
            0: "T",      # Tonic
            1: "b2",     # Seconda minore
            2: "2",      # Seconda maggiore
            3: "b3",     # Terza minore
            4: "3",      # Terza maggiore
            5: "4",      # Quarta giusta
            6: "b5",     # Quinta diminuita
            7: "5",      # Quinta giusta
            8: "b6",     # Sesta minore
            9: "6",      # Sesta maggiore
            10: "b7",    # Settima minore
            11: "7"      # Settima maggiore
        }
        return interval_map.get(semitones, f"{semitones}")
    
    def to_intervals_string(self) -> str:
        """Rappresentazione stringa dell'accordo come intervalli"""
        intervals = self.get_intervals()
        return " - ".join(intervals)


class CircleOfFifths:
    """Gestisce il circolo delle quinte per calcolare le note"""
    
    def __init__(self):
        self.notes = list(Note)
    
    def get_fifth_up(self, note: Note) -> Note:
        """Calcola la quinta ascendente (7 semitoni)"""
        return Note((note.value + 7) % 12)
    
    def get_fifth_down(self, note: Note) -> Note:
        """Calcola la quinta discendente (7 semitoni indietro)"""
        return Note((note.value - 7) % 12)
    
    def get_interval(self, root: Note, semitones: int) -> Note:
        """Calcola un intervallo specifico dalla nota radice"""
        return Note((root.value + semitones) % 12)


@dataclass
class SoundCell:
    """Rappresenta una sound cell della Color Tree"""
    notes: List[Note]
    root: Note
    level: int
    position: int  # posizione nel livello (0 = più scuro, level = più brillante)
    fifths_below: int  # numero di quinte sotto la root
    fifths_above: int  # numero di quinte sopra la root
    brightness: float  # valore da 0 (scuro) a 1 (brillante)
    
    def __str__(self) -> str:
        """Rappresentazione stringa della sound cell"""
        note_names = {
            Note.C: "C", Note.C_SHARP: "C#", Note.D: "D", Note.D_SHARP: "D#",
            Note.E: "E", Note.F: "F", Note.F_SHARP: "F#", Note.G: "G",
            Note.G_SHARP: "G#", Note.A: "A", Note.A_SHARP: "A#", Note.B: "B"
        }
        return " - ".join(note_names[note] for note in self.notes)
    
    def get_intervals(self) -> List[str]:
        """Calcola gli intervalli della sound cell rispetto alla nota radice"""
        intervals = []
        
        for note in self.notes:
            if note == self.root:
                intervals.append("1")  # Root
            else:
                # Calcola la distanza in semitoni dalla nota radice
                semitones = (note.value - self.root.value) % 12
                interval_name = self._semitones_to_interval(semitones)
                intervals.append(interval_name)
        
        return intervals
    
    def _semitones_to_interval(self, semitones: int) -> str:
        """Converte semitoni in nome dell'intervallo"""
        interval_map = {
            0: "1",      # Root
            1: "b2",     # Seconda minore
            2: "2",      # Seconda maggiore
            3: "b3",     # Terza minore
            4: "3",      # Terza maggiore
            5: "4",      # Quarta giusta
            6: "b5",     # Quinta diminuita
            7: "5",      # Quinta giusta
            8: "b6",     # Sesta minore
            9: "6",      # Sesta maggiore
            10: "b7",    # Settima minore
            11: "7"      # Settima maggiore
        }
        return interval_map.get(semitones, f"{semitones}")
    
    def to_intervals_string(self) -> str:
        """Rappresentazione stringa della sound cell come intervalli"""
        intervals = self.get_intervals()
        return ".".join(intervals)
    
    def get_circle_representation(self) -> List[bool]:
        """Restituisce una rappresentazione del circolo delle quinte per la visualizzazione"""
        # 12 posizioni nel circolo delle quinte
        circle = [False] * 12
        circle[self.root.value] = True  # Root sempre presente
        
        # Aggiunge le quinte sopra
        current_note = self.root
        for _ in range(self.fifths_above):
            current_note = Note((current_note.value + 7) % 12)
            circle[current_note.value] = True
        
        # Aggiunge le quinte sotto
        current_note = self.root
        for _ in range(self.fifths_below):
            current_note = Note((current_note.value - 7) % 12)
            circle[current_note.value] = True
        
        return circle


class ChordGenerator:
    """Genera la Color Tree seguendo la struttura piramidale del circolo delle quinte"""
    
    def __init__(self):
        self.circle = CircleOfFifths()
    
    def generate_color_tree(self, root_note: Note = Note.C) -> List[List[SoundCell]]:
        """
        Genera la Color Tree con 12 livelli:
        - Livello 1: 1 sound cell (solo root)
        - Livello 2: 2 sound cells (quinte sotto e sopra)
        - ...
        - Livello 12: 12 sound cells (scala cromatica completa)
        """
        levels = []
        
        # Livello 1: Solo la nota radice
        levels.append([SoundCell(
            notes=[root_note], 
            root=root_note, 
            level=1, 
            position=0,
            fifths_below=0, 
            fifths_above=0, 
            brightness=0.5  # Neutro
        )])
        
        # Livelli 2-12: Costruzione piramidale
        for level in range(2, 13):
            current_level = []
            
            # Calcola il numero di sound cells per questo livello
            num_cells = level
            
            for position in range(num_cells):
                # Calcola quinte sotto e sopra basandosi sulla posizione
                fifths_below = position
                fifths_above = level - 1 - position
                
                # Costruisce le note della sound cell
                notes = self._build_sound_cell_notes(root_note, fifths_below, fifths_above)
                
                # Calcola la luminosità (0 = scuro, 1 = brillante)
                brightness = self._calculate_brightness(fifths_below, fifths_above, level)
                
                sound_cell = SoundCell(
                    notes=notes,
                    root=root_note,
                    level=level,
                    position=position,
                    fifths_below=fifths_below,
                    fifths_above=fifths_above,
                    brightness=brightness
                )
                
                current_level.append(sound_cell)
            
            levels.append(current_level)
        
        return levels
    
    def _build_sound_cell_notes(self, root: Note, fifths_below: int, fifths_above: int) -> List[Note]:
        """Costruisce le note di una sound cell basandosi sulle quinte sotto e sopra"""
        notes = [root]  # La root è sempre presente
        
        # Aggiunge le quinte sotto (a sinistra nel circolo)
        current_note = root
        for _ in range(fifths_below):
            current_note = self.circle.get_fifth_down(current_note)
            notes.insert(0, current_note)
        
        # Aggiunge le quinte sopra (a destra nel circolo)
        current_note = root
        for _ in range(fifths_above):
            current_note = self.circle.get_fifth_up(current_note)
            notes.append(current_note)
        
        # Ordina le note per mantenere la root per prima e le altre in ordine crescente
        root_index = notes.index(root)
        if root_index != 0:
            notes.pop(root_index)
            notes.insert(0, root)
        
        # Ordina le note rimanenti (esclusa la root) per semitoni crescenti
        if len(notes) > 1:
            root_note = notes[0]
            other_notes = notes[1:]
            other_notes.sort(key=lambda note: (note.value - root_note.value) % 12)
            notes = [root_note] + other_notes
        
        return notes
    
    def _calculate_brightness(self, fifths_below: int, fifths_above: int, level: int) -> float:
        """Calcola la luminosità di una sound cell (0 = scuro, 1 = brillante)"""
        if level == 1:
            return 0.5  # Neutro per il livello 1
        
        # La luminosità è proporzionale al rapporto tra quinte sopra e quinte sotto
        total_fifths = fifths_below + fifths_above
        if total_fifths == 0:
            return 0.5
        
        # Calcola il rapporto: più quinte sopra = più brillante
        brightness_ratio = fifths_above / total_fifths
        
        # Per livelli pari, non ci sono suoni neutri (solo scuri o brillanti)
        if level % 2 == 0:
            if brightness_ratio < 0.5:
                return 0.0  # Scuro
            else:
                return 1.0  # Brillante
        else:
            # Per livelli dispari, ci possono essere suoni neutri
            if brightness_ratio < 0.3:
                return 0.0  # Scuro
            elif brightness_ratio > 0.7:
                return 1.0  # Brillante
            else:
                return 0.5  # Neutro
    


class ColorTreeDisplayApp:
    """Interfaccia grafica per visualizzare la Color Tree"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Color Tree")
        self.root.geometry("1600x930")
        self.root.configure(bg='#f0f0f0')
        
        self.generator = ChordGenerator()
        self.color_tree_levels = []
        self.display_mode = tk.StringVar(value="notes")  # "notes", "intervals", "circle"
        
        self.setup_ui()
        self.generate_color_tree()
    
    def setup_ui(self):
        """Configura l'interfaccia utente"""
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Controlli compatti in alto
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Nota radice - compatta
        ttk.Label(controls_frame, text="Nota:", font=('Arial', 10)).grid(row=0, column=0, padx=(0, 5))
        self.root_note_var = tk.StringVar(value="C")
        root_combo = ttk.Combobox(controls_frame, textvariable=self.root_note_var,
                                 values=[note.name.replace('_', '#') for note in Note],
                                 state="readonly", width=8)
        root_combo.grid(row=0, column=1, padx=(0, 20))
        root_combo.bind('<<ComboboxSelected>>', self.on_root_note_change)
        
        # Tipo di visualizzazione - compatto
        ttk.Label(controls_frame, text="Visualizza:", font=('Arial', 10)).grid(row=0, column=2, padx=(0, 5))
        ttk.Radiobutton(controls_frame, text="Note", variable=self.display_mode, 
                       value="notes", command=self.on_display_mode_change).grid(row=0, column=3, padx=(0, 10))
        ttk.Radiobutton(controls_frame, text="Intervalli", variable=self.display_mode, 
                       value="intervals", command=self.on_display_mode_change).grid(row=0, column=4)
        
        # Frame per la visualizzazione della Color Tree - layout orizzontale
        self.tree_frame = ttk.Frame(main_frame)
        self.tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame principale per la Color Tree - centrato per triangolo equilatero
        self.main_tree_frame = ttk.Frame(self.tree_frame)
        self.main_tree_frame.pack(fill='both', expand=True)
        
        # Configurazione per centrare il contenuto
        self.main_tree_frame.columnconfigure(0, weight=1)
        
        # Configurazione del grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        self.tree_frame.columnconfigure(0, weight=1)
        self.tree_frame.rowconfigure(0, weight=1)
    
    def on_root_note_change(self, event=None):
        """Gestisce il cambio della nota radice"""
        del event  # Ignora il parametro event non utilizzato
        self.generate_color_tree()
    
    def on_display_mode_change(self):
        """Gestisce il cambio della modalità di visualizzazione"""
        self.display_color_tree()
    
    def generate_color_tree(self):
        """Genera e visualizza la Color Tree"""
        # Pulisce il frame
        for widget in self.main_tree_frame.winfo_children():
            widget.destroy()
        
        # Ottiene la nota radice selezionata
        root_note_name = self.root_note_var.get().replace('#', '_SHARP')
        try:
            root_note = Note[root_note_name]
        except KeyError:
            root_note = Note.C
        
        # Genera la Color Tree
        self.color_tree_levels = self.generator.generate_color_tree(root_note)
        
        # Visualizza la Color Tree
        self.display_color_tree()
    
    def display_color_tree(self):
        """Visualizza la Color Tree in formato piramidale - triangolo equilatero centrato"""
        # Inverte l'ordine per mostrare il primo livello in basso
        for level, sound_cells in enumerate(reversed(self.color_tree_levels)):
            actual_level = len(self.color_tree_levels) - level - 1
            
            # Frame per ogni livello - centrato per triangolo equilatero
            level_frame = ttk.Frame(self.main_tree_frame)
            level_frame.grid(row=level, column=0, sticky='', 
                           pady=0, padx=0)
            
            # Configura le colonne per centrare le sound cells con meno spazio
            num_cells = len(sound_cells)
            
            # Non configurare weight per evitare espansione orizzontale delle colonne
            
            # Centra le sound cells direttamente
            for i, sound_cell in enumerate(sound_cells):
                self._create_sound_cell_widget(level_frame, sound_cell, i)
    
    def _get_level_description(self, level: int) -> str:
        """Restituisce la descrizione del livello - versione compatta"""
        descriptions = {
            1: "One",
            2: "Power", 
            3: "Penta",
            4: "Major",
            5: "Minor",
            6: "Dim",
            7: "Aug",
            8: "Alt",
            9: "Sym",
            10: "Complex",
            11: "Ext",
            12: "Chromatic"
        }
        return descriptions.get(level, f"L{level}")
    
    def _create_sound_cell_widget(self, parent, sound_cell: SoundCell, position: int):
        """Crea un widget per visualizzare una sound cell"""
        # Tutte le sound cells hanno sfondo bianco
        bg_color = 'white'
        
        # Frame principale della sound cell - dimensioni bilanciate e centrate
        main_cell = tk.Frame(parent, bg=bg_color, relief='raised', bd=1, width=90, height=70)
        main_cell.grid(row=0, column=position, padx=0, pady=1, sticky='')
        main_cell.pack_propagate(False)  # Mantiene le dimensioni fisse
        
        # Numeri delle quinte (in alto) - leggibili
        fifths_frame = tk.Frame(main_cell, bg=bg_color, height=12)
        fifths_frame.pack(fill='x', padx=2, pady=1)
        
        tk.Label(fifths_frame, text=f"-{sound_cell.fifths_below}", 
                bg=bg_color, font=('Arial', 6, 'bold')).pack(side='left')
        tk.Label(fifths_frame, text=f"+{sound_cell.fifths_above}", 
                bg=bg_color, font=('Arial', 6, 'bold')).pack(side='right')
        
        # Rappresentazione del circolo delle quinte (centro) - bilanciata
        circle_frame = tk.Frame(main_cell, bg=bg_color, height=25)
        circle_frame.pack(fill='both', expand=True, padx=2, pady=1)
        
        # Mostra le note principali o intervalli essenziali - bilanciati
        if self.display_mode.get() == "intervals":
            # Mostra i primi 4 intervalli per leggibilità
            intervals = sound_cell.get_intervals()[:4]
            text = ".".join(intervals)
        else:
            # Mostra le prime 4 note per leggibilità
            notes = sound_cell.notes[:4]
            note_names = {
                Note.C: "C", Note.C_SHARP: "C#", Note.D: "D", Note.D_SHARP: "D#",
                Note.E: "E", Note.F: "F", Note.F_SHARP: "F#", Note.G: "G",
                Note.G_SHARP: "G#", Note.A: "A", Note.A_SHARP: "A#", Note.B: "B"
            }
            text = " ".join(note_names[note] for note in notes)
        
        tk.Label(circle_frame, text=text, bg=bg_color, 
                font=('Arial', 7, 'bold')).pack(expand=True)
        
        # Intervalli (in basso) - leggibili
        intervals_frame = tk.Frame(main_cell, bg=bg_color, height=12)
        intervals_frame.pack(fill='x', padx=2, pady=1)
        
        # Mostra i primi 3 intervalli per leggibilità
        intervals = sound_cell.get_intervals()[:3]
        intervals_text = ".".join(intervals)
        tk.Label(intervals_frame, text=intervals_text, bg=bg_color, 
                font=('Arial', 5)).pack()
    
    def _get_brightness_color(self, brightness: float) -> str:
        """Converte la luminosità in un colore"""
        if brightness == 0.0:
            return '#404040'  # Scuro
        elif brightness == 1.0:
            return '#E0E0E0'  # Brillante
        else:
            return '#808080'  # Neutro
    
    
    def run(self):
        """Avvia l'applicazione"""
        self.root.mainloop()


def main():
    """Funzione principale"""
    try:
        app = ColorTreeDisplayApp()
        app.run()
    except (tk.TclError, ImportError, OSError) as e:
        messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")
    except Exception as e:
        messagebox.showerror("Errore", f"Errore imprevisto: {str(e)}")


if __name__ == "__main__":
    main()
