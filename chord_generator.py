"""
Chord Generator App - Generatore di accordi basato sul circolo delle quinte
Seguendo le best practices Python con struttura modulare e OOP
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
from dataclasses import dataclass
from enum import Enum
import threading
import time

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


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
                intervals.append("T")  # Root
            else:
                # Calcola la distanza in semitoni dalla nota radice
                semitones = (note.value - self.root.value) % 12
                interval_name = self._semitones_to_interval(semitones)
                intervals.append(interval_name)
        
        return intervals
    
    def _semitones_to_interval(self, semitones: int) -> str:
        """Converte semitoni in nome dell'intervallo"""
        interval_map = {
            0: "T",      # Root
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
        - Livello 11: 11 sound cells
        - Livello 12: 1 sound cell (scala cromatica completa)
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
        
        # Livelli 2-11: Costruzione piramidale
        for level in range(2, 12):
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
        
        # Livello 12: Una singola sound cell con la scala cromatica completa
        chromatic_scale = list(Note)  # Tutte le 12 note cromatiche
        levels.append([SoundCell(
            notes=chromatic_scale,
            root=root_note,
            level=12,
            position=0,
            fifths_below=0,  # Non applicabile per la scala cromatica
            fifths_above=0,  # Non applicabile per la scala cromatica
            brightness=0.5   # Neutro per la scala cromatica completa
        )])
        
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


class MIDIScaleGenerator:
    """Genera e riproduce scale MIDI per le sound cells"""
    
    def __init__(self):
        self.initialized = False
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                self.initialized = True
            except (OSError, RuntimeError):
                self.initialized = False
    
    def note_to_midi_number(self, note: Note, octave: int = 4) -> int:
        """Converte una nota in numero MIDI"""
        # MIDI note 60 = C4 (Do centrale)
        return note.value + (octave * 12) + 12
    
    def generate_scale_notes(self, sound_cell: 'SoundCell', octave: int = 4) -> List[int]:
        """Genera le note MIDI per una sound cell"""
        midi_notes = []
        for note in sound_cell.notes:
            midi_notes.append(self.note_to_midi_number(note, octave))
        return midi_notes
    
    def play_scale(self, sound_cell: 'SoundCell', octave: int = 4, duration: float = 0.5):
        """Riproduce la scala di una sound cell"""
        if not self.initialized:
            messagebox.showwarning("MIDI", "Pygame non disponibile. Installa pygame per la riproduzione audio.")
            return
        
        def play_notes():
            try:
                midi_notes = self.generate_scale_notes(sound_cell, octave)
                
                for i, midi_note in enumerate(midi_notes):
                    # Calcola la frequenza dalla nota MIDI
                    frequency = 440.0 * (2 ** ((midi_note - 69) / 12.0))
                    
                    # Crea un tono sinusoidale
                    sample_rate = 22050
                    frames = int(duration * sample_rate)
                    arr = []
                    
                    # Root note più forte - volume aumentato
                    volume = 0.8 if i == 0 else 0.6
                    
                    # Genera onda sinusoidale usando numpy se disponibile
                    try:
                        import numpy as np
                        t = np.linspace(0, duration, frames, False)
                        wave = np.sin(2 * np.pi * frequency * t)
                        
                        # Aggiunge fade-in e fade-out per evitare click
                        fade_samples = int(0.01 * sample_rate)  # 10ms di fade
                        if frames > 2 * fade_samples:
                            # Fade-in
                            wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
                            # Fade-out
                            wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)
                        
                        # Applica envelope per suono più naturale
                        envelope = np.exp(-t * 2)  # Decadimento esponenziale leggero
                        wave *= envelope
                        
                        # Volume bilanciato per evitare clipping
                        wave = (wave * 4096 * volume).astype(np.int16)
                        
                        # Crea array stereo
                        stereo_wave = np.column_stack((wave, wave))
                        arr = stereo_wave
                    except ImportError:
                        # Fallback senza numpy
                        arr = []
                        for j in range(frames):
                            time_val = j / sample_rate
                            # Genera onda sinusoidale semplice
                            wave_val = np.sin(2 * np.pi * frequency * time_val)
                            
                            # Aggiunge fade-in e fade-out
                            fade_samples = int(0.01 * sample_rate)
                            if j < fade_samples:
                                wave_val *= j / fade_samples
                            elif j >= frames - fade_samples:
                                wave_val *= (frames - j) / fade_samples
                            
                            # Applica envelope
                            envelope = np.exp(-time_val * 2)
                            wave_val *= envelope
                            
                            wave_val = int(4096 * volume * wave_val)
                            arr.append([wave_val, wave_val])
                    
                    # Riproduce il suono
                    sound = pygame.sndarray.make_sound(arr)
                    sound.play()
                    time.sleep(duration * 0.8)  # Piccola pausa tra le note
                    
            except (OSError, RuntimeError) as e:
                print(f"Errore nella riproduzione: {e}")
        
        # Esegue la riproduzione in un thread separato
        thread = threading.Thread(target=play_notes)
        thread.daemon = True
        thread.start()


class ColorTreeDisplayApp:
    """Interfaccia grafica per visualizzare la Color Tree"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Color Tree")
        self.root.geometry("1800x930")
        self.root.configure(bg='#f0f0f0')
        
        self.generator = ChordGenerator()
        self.midi_generator = MIDIScaleGenerator()
        self.color_tree_levels = []
        self.display_mode = "intervals"  # "intervals" or "notes"
        
        # Inizializza i bottoni
        self.intervals_btn = None
        self.notes_btn = None
        
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
        
        # Switch per modalità visualizzazione
        self.create_display_mode_switch(controls_frame, 0, 2)
        
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
    
    def create_display_mode_switch(self, parent, row, column):
        """Crea due bottoni eleganti per alternare tra intervalli e note"""
        # Frame contenitore per i bottoni
        switch_frame = tk.Frame(parent, bg='#f0f0f0')
        switch_frame.grid(row=row, column=column, padx=(0, 5))
        
        # Bottone per intervalli
        self.intervals_btn = tk.Button(switch_frame, text="123", 
                                     font=('Arial', 8, 'bold'), 
                                     width=3, height=1,
                                     relief='raised', bd=1,
                                     command=self.set_intervals_mode)
        self.intervals_btn.pack(side='left', padx=(0, 2))
        
        # Bottone per note
        self.notes_btn = tk.Button(switch_frame, text="♪", 
                                  font=('Arial', 10, 'bold'), 
                                  width=3, height=1,
                                  relief='raised', bd=1,
                                  command=self.set_notes_mode)
        self.notes_btn.pack(side='left')
        
        # Inizializza lo stato dei bottoni
        self.update_button_states()
    
    def set_intervals_mode(self):
        """Imposta la modalità intervalli"""
        self.display_mode = "intervals"
        self.update_button_states()
        self.generate_color_tree()
    
    def set_notes_mode(self):
        """Imposta la modalità note"""
        self.display_mode = "notes"
        self.update_button_states()
        self.generate_color_tree()
    
    def update_button_states(self):
        """Aggiorna lo stato visivo dei bottoni"""
        if self.display_mode == "intervals":
            # Bottone intervalli attivo
            self.intervals_btn.config(relief='sunken', bg='#4CAF50', fg='white')
            self.notes_btn.config(relief='raised', bg='#F5F5F5', fg='#666666')
        else:
            # Bottone note attivo
            self.notes_btn.config(relief='sunken', bg='#2196F3', fg='white')
            self.intervals_btn.config(relief='raised', bg='#F5F5F5', fg='#666666')
    
    def on_root_note_change(self, event=None):
        """Gestisce il cambio della nota radice"""
        del event  # Ignora il parametro event non utilizzato
        self.generate_color_tree()
    
    def on_sound_cell_click(self, sound_cell: SoundCell):
        """Gestisce il click su una sound cell per riprodurre la scala MIDI"""
        self.midi_generator.play_scale(sound_cell)
    
    
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
            # Frame per ogni livello - centrato per triangolo equilatero
            level_frame = ttk.Frame(self.main_tree_frame)
            level_frame.grid(row=level, column=0, sticky='', 
                           pady=0, padx=0)
            
            # Inverte l'ordine delle sound cells per effetto specchio
            reversed_sound_cells = list(reversed(sound_cells))
            
            # Centra le sound cells direttamente
            for i, sound_cell in enumerate(reversed_sound_cells):
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
            12: "Chromatic Scale"
        }
        return descriptions.get(level, f"L{level}")
    
    def _create_sound_cell_widget(self, parent, sound_cell: SoundCell, position: int):
        """Crea un widget per visualizzare una sound cell"""
        # Tutte le sound cells hanno sfondo bianco
        bg_color = 'white'
        
        # Calcola la larghezza in base al livello
        if sound_cell.level == 12:
            # Per il livello 12, mantiene la larghezza originale
            cell_width = 130 * 12  # 12 caselle da 130px ciascuna (dimensione originale)
        else:
            cell_width = 160  # Larghezza aumentata di 20px (140 + 20 = 160) per tutti gli altri livelli
        
        # Frame principale della sound cell - dimensioni bilanciate e centrate
        main_cell = tk.Frame(parent, bg=bg_color, relief='raised', bd=1, width=cell_width, height=70)
        main_cell.grid(row=0, column=position, padx=0, pady=1, sticky='')
        main_cell.pack_propagate(False)  # Mantiene le dimensioni fisse
        
        # Aggiunge il click handler per la riproduzione MIDI
        main_cell.bind("<Button-1>", lambda e: self.on_sound_cell_click(sound_cell))
        main_cell.bind("<Enter>", lambda e: main_cell.config(relief='solid', bd=2))
        main_cell.bind("<Leave>", lambda e: main_cell.config(relief='raised', bd=1))
        
        # Numeri delle quinte (in alto) - leggibili
        fifths_frame = tk.Frame(main_cell, bg=bg_color, height=12)
        fifths_frame.pack(fill='x', padx=2, pady=1)
        
        if sound_cell.level == 12:
            # Per il livello 12, mostra "Chromatic Scale" al centro
            tk.Label(fifths_frame, text="Chromatic Scale", 
                    bg=bg_color, font=('Arial', 9, 'bold')).pack(expand=True)
        else:
            tk.Label(fifths_frame, text=f"-{sound_cell.fifths_below}", 
                    bg=bg_color, font=('Arial', 7, 'bold')).pack(side='left')
            tk.Label(fifths_frame, text=f"+{sound_cell.fifths_above}", 
                    bg=bg_color, font=('Arial', 7, 'bold')).pack(side='right')
        
        # Rappresentazione degli intervalli (centro) - bilanciata
        circle_frame = tk.Frame(main_cell, bg=bg_color, height=55)
        circle_frame.pack(fill='both', expand=True, padx=2, pady=1)
        
        # Mostra intervalli o note in base alla modalità selezionata
        if self.display_mode == "intervals":
            intervals = sound_cell.get_intervals()
            text = "-".join(intervals)
            font_size = 9  # Font size per gli intervalli
        else:
            # Mostra le note musicali
            note_names = {
                Note.C: "C", Note.C_SHARP: "C#", Note.D: "D", Note.D_SHARP: "D#",
                Note.E: "E", Note.F: "F", Note.F_SHARP: "F#", Note.G: "G",
                Note.G_SHARP: "G#", Note.A: "A", Note.A_SHARP: "A#", Note.B: "B"
            }
            notes = [note_names[note] for note in sound_cell.notes]
            text = "-".join(notes)
            font_size = 8  # Font size per le note (diminuito di 1)
        
        main_label = tk.Label(circle_frame, text=text, bg=bg_color, 
                font=('Arial', font_size, 'bold'))
        main_label.pack(expand=True)
        
        # Aggiunge click handler anche al label principale
        main_label.bind("<Button-1>", lambda e: self.on_sound_cell_click(sound_cell))
        main_label.bind("<Enter>", lambda e: main_cell.config(relief='solid', bd=2))
        main_label.bind("<Leave>", lambda e: main_cell.config(relief='raised', bd=1))
        
        # Frame vuoto per mantenere la struttura
        intervals_frame = tk.Frame(main_cell, bg=bg_color, height=12)
        intervals_frame.pack(fill='x', padx=2, pady=1)
        
        # Aggiunge click handler anche al frame vuoto
        intervals_frame.bind("<Button-1>", lambda e: self.on_sound_cell_click(sound_cell))
        intervals_frame.bind("<Enter>", lambda e: main_cell.config(relief='solid', bd=2))
        intervals_frame.bind("<Leave>", lambda e: main_cell.config(relief='raised', bd=1))
    
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
    except (tk.TclError, ImportError, RuntimeError) as e:
        messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")


if __name__ == "__main__":
    main()
