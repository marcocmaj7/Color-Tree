"""
Chord Generator App - Generatore di accordi basato sul circolo delle quinte
Seguendo le best practices Python con struttura modulare e OOP
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
from dataclasses import dataclass
from enum import Enum


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


class ChordGenerator:
    """Genera accordi seguendo la struttura triangolare del circolo delle quinte"""
    
    def __init__(self):
        self.circle = CircleOfFifths()
    
    def generate_triangular_chords(self, root_note: Note = Note.C) -> List[List[Chord]]:
        """
        Genera la struttura triangolare degli accordi
        Livello 1: Do (C)
        Livello 2: C F - C G
        Livello 3: C F Bb - C F G - C D G
        E così via...
        """
        levels = []
        
        # Livello 1: Solo la nota radice
        levels.append([Chord([root_note], root_note)])
        
        # Livelli 2-12: Costruzione triangolare
        for level in range(1, 12):
            current_level = []
            
            # Calcola il numero di accordi per questo livello
            num_chords = level + 1
            
            for chord_index in range(num_chords):
                # Costruisce l'accordo basandosi sulla posizione
                # Invertiamo l'ordine: posizione 0 = solo quinte discendenti
                chord_notes = self._build_chord_notes(root_note, level, level - chord_index)
                chord = Chord(chord_notes, root_note)
                current_level.append(chord)
            
            levels.append(current_level)
        
        return levels
    
    def _build_chord_notes(self, root: Note, level: int, position: int) -> List[Note]:
        """
        Costruisce le note di un accordo specifico basandosi su:
        - root: nota radice
        - level: livello (0-11)
        - position: posizione nell'accordo (0-level)
        
        La logica è:
        - position 0: solo quinte discendenti (sinistra)
        - position level: solo quinte ascendenti (destra)
        - position intermedia: mix di quinte discendenti e ascendenti
        
        Le note vengono ordinate per mantenere la tonica (T) sempre per prima
        """
        notes = [root]  # La nota radice è sempre presente
        
        # Aggiunge le quinte discendenti (a sinistra)
        for i in range(position):
            if i == 0:
                # Prima quinta discendente
                notes.insert(0, self.circle.get_fifth_down(root))
            else:
                # Quinte discendenti successive
                prev_note = notes[0]
                notes.insert(0, self.circle.get_fifth_down(prev_note))
        
        # Aggiunge le quinte ascendenti (a destra)
        for i in range(level - position):
            if i == 0:
                # Prima quinta ascendente
                notes.append(self.circle.get_fifth_up(root))
            else:
                # Quinte ascendenti successive
                prev_note = notes[-1]
                notes.append(self.circle.get_fifth_up(prev_note))
        
        # Riordina le note per mantenere la tonica sempre per prima
        # e le altre note in ordine crescente di semitoni
        root_index = notes.index(root)
        if root_index != 0:
            # Rimuove la root dalla sua posizione attuale
            notes.pop(root_index)
            # La inserisce all'inizio
            notes.insert(0, root)
        
        # Ordina le note rimanenti (esclusa la root) per semitoni crescenti
        if len(notes) > 1:
            root_note = notes[0]
            other_notes = notes[1:]
            # Calcola la distanza in semitoni dalla root per ogni nota
            other_notes.sort(key=lambda note: (note.value - root_note.value) % 12)
            # Ricostruisce la lista con root per prima e le altre ordinate
            notes = [root_note] + other_notes
        
        return notes


class ChordDisplayApp:
    """Interfaccia grafica per visualizzare gli accordi"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Generatore di Accordi - Circolo delle Quinte")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        self.generator = ChordGenerator()
        self.chord_levels = []
        self.display_mode = tk.StringVar(value="notes")  # "notes" o "intervals"
        
        self.setup_ui()
        self.generate_chords()
    
    def setup_ui(self):
        """Configura l'interfaccia utente"""
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titolo
        title_label = ttk.Label(main_frame, text="Generatore di Accordi", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Frame per la selezione della nota radice
        root_frame = ttk.LabelFrame(main_frame, text="Nota Radice", padding="10")
        root_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.root_note_var = tk.StringVar(value="C")
        root_combo = ttk.Combobox(root_frame, textvariable=self.root_note_var,
                                 values=[note.name.replace('_', '#') for note in Note],
                                 state="readonly", width=10)
        root_combo.grid(row=0, column=0, padx=(0, 10))
        root_combo.bind('<<ComboboxSelected>>', self.on_root_note_change)
        
        ttk.Button(root_frame, text="Genera Accordi", 
                  command=self.generate_chords).grid(row=0, column=1)
        
        # Frame per la selezione del tipo di visualizzazione
        display_frame = ttk.LabelFrame(main_frame, text="Tipo di Visualizzazione", padding="10")
        display_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(display_frame, text="Note", variable=self.display_mode, 
                       value="notes", command=self.on_display_mode_change).grid(row=0, column=0, padx=(0, 20))
        ttk.Radiobutton(display_frame, text="Intervalli", variable=self.display_mode, 
                       value="intervals", command=self.on_display_mode_change).grid(row=0, column=1)
        
        # Frame per la visualizzazione degli accordi
        self.chord_frame = ttk.Frame(main_frame)
        self.chord_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        self.canvas = tk.Canvas(self.chord_frame, bg='white')
        self.scrollbar = ttk.Scrollbar(self.chord_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurazione del grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        self.chord_frame.columnconfigure(0, weight=1)
        self.chord_frame.rowconfigure(0, weight=1)
    
    def on_root_note_change(self, event=None):
        """Gestisce il cambio della nota radice"""
        self.generate_chords()
    
    def on_display_mode_change(self):
        """Gestisce il cambio della modalità di visualizzazione"""
        self.display_chords()
    
    def generate_chords(self):
        """Genera e visualizza gli accordi"""
        # Pulisce il frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Ottiene la nota radice selezionata
        root_note_name = self.root_note_var.get().replace('#', '_SHARP')
        try:
            root_note = Note[root_note_name]
        except KeyError:
            root_note = Note.C
        
        # Genera gli accordi
        self.chord_levels = self.generator.generate_triangular_chords(root_note)
        
        # Visualizza gli accordi
        self.display_chords()
    
    def display_chords(self):
        """Visualizza gli accordi in formato triangolare"""
        # Inverte l'ordine per mostrare il primo livello in basso
        for level, chords in enumerate(reversed(self.chord_levels)):
            actual_level = len(self.chord_levels) - level - 1
            # Frame per ogni livello
            level_frame = ttk.LabelFrame(self.scrollable_frame, 
                                       text=f"Livello {actual_level + 1}", 
                                       padding="10")
            level_frame.grid(row=level, column=0, sticky=(tk.W, tk.E), 
                           pady=5, padx=10)
            
            # Visualizza gli accordi del livello
            for i, chord in enumerate(chords):
                # Sceglie la rappresentazione in base alla modalità
                if self.display_mode.get() == "intervals":
                    chord_text = chord.to_intervals_string()
                else:
                    chord_text = str(chord)
                
                chord_label = ttk.Label(level_frame, text=chord_text, 
                                      font=('Arial', 10, 'bold'),
                                      background='#e8f4fd',
                                      relief='raised',
                                      padding="5")
                chord_label.grid(row=0, column=i, padx=5, pady=5)
    
    def run(self):
        """Avvia l'applicazione"""
        self.root.mainloop()


def main():
    """Funzione principale"""
    try:
        app = ChordDisplayApp()
        app.run()
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")


if __name__ == "__main__":
    main()
