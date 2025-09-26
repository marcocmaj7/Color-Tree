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

try:
    import mido
    MIDI_AVAILABLE = True
except ImportError:
    MIDI_AVAILABLE = False

# Import per la finestra creativa
try:
    from creative_chord_window import CreativeChordWindow
    CREATIVE_WINDOW_AVAILABLE = True
except ImportError:
    CREATIVE_WINDOW_AVAILABLE = False


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
        self.current_sounds = []  # Lista per tenere traccia dei suoni attualmente in riproduzione
        self.stop_playing = False  # Flag per fermare la riproduzione
        self.current_thread = None  # Thread attualmente in esecuzione
        self.playback_id = 0  # ID univoco per ogni riproduzione
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                self.initialized = True
            except (OSError, RuntimeError):
                self.initialized = False
    
    def stop_all_sounds(self):
        """Ferma tutti i suoni attualmente in riproduzione"""
        if not self.initialized:
            return
        
        try:
            # Imposta il flag per fermare la riproduzione
            self.stop_playing = True
            # Ferma tutti i canali di pygame mixer
            pygame.mixer.stop()
            # Ferma tutti i suoni nella lista
            for sound in self.current_sounds:
                try:
                    sound.stop()
                except (OSError, RuntimeError):
                    pass
            # Pulisce la lista dei suoni attuali
            self.current_sounds.clear()
            # Aspetta che il thread corrente finisca (con timeout)
            if self.current_thread and self.current_thread.is_alive():
                self.current_thread.join(timeout=0.1)
        except (OSError, RuntimeError) as e:
            print(f"Errore nel fermare i suoni: {e}")
    
    def note_to_midi_number(self, note: Note, octave: int = 4) -> int:
        """Converte una nota in numero MIDI"""
        # MIDI note 60 = C4 (Do centrale)
        # C4 = 60, quindi C = 0, C# = 1, ..., B = 11
        # Per ottava 4: base = 4 * 12 = 48, quindi C4 = 48 + 0 = 48
        # Ma MIDI C4 = 60, quindi dobbiamo aggiungere 12
        return note.value + (octave * 12) + 12
    
    def generate_scale_notes(self, sound_cell: 'SoundCell', octave: int = 4) -> List[int]:
        """Genera le note MIDI per una sound cell con ottave corrette"""
        midi_notes = []
        
        if not sound_cell.notes:
            return midi_notes
        
        # La prima nota (root) è sempre nell'ottava specificata
        root_note = sound_cell.notes[0]
        root_midi = self.note_to_midi_number(root_note, octave)
        midi_notes.append(root_midi)
        
        # Per le altre note, calcola l'ottava corretta basandosi sulla distanza dalla root
        for note in sound_cell.notes[1:]:
            # Calcola la distanza in semitoni dalla root (senza modulo per vedere la direzione)
            semitones_from_root = note.value - root_note.value
            
            # Se la distanza è negativa (nota più bassa), usa un'ottava più alta
            if semitones_from_root < 0:
                target_octave = octave + 1
            else:
                target_octave = octave
            
            # Calcola il numero MIDI
            note_midi = self.note_to_midi_number(note, target_octave)
            midi_notes.append(note_midi)
        
        return midi_notes
    
    def play_scale(self, sound_cell: 'SoundCell', octave: int = 4, duration: float = 0.5):
        """Riproduce la scala di una sound cell"""
        if not self.initialized:
            messagebox.showwarning("MIDI", "Pygame non disponibile. Installa pygame per la riproduzione audio.")
            return
        
        # Ferma tutti i suoni precedenti prima di iniziare la riproduzione
        self.stop_all_sounds()
        
        # Incrementa l'ID di riproduzione per invalidare le riproduzioni precedenti
        self.playback_id += 1
        
        # Reset del flag di stop per permettere la nuova riproduzione
        self.stop_playing = False
        
        # Aspetta un momento per assicurarsi che il thread precedente sia fermato
        time.sleep(0.01)
        
        def play_notes():
            try:
                midi_notes = self.generate_scale_notes(sound_cell, octave)
                
                for i, midi_note in enumerate(midi_notes):
                    # Controlla se questa riproduzione è ancora valida (solo per fermare, non per interrompere il loop)
                    if self.stop_playing:
                        break
                        
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
                        import math
                        arr = []
                        for j in range(frames):
                            time_val = j / sample_rate
                            # Genera onda sinusoidale semplice
                            wave_val = math.sin(2 * math.pi * frequency * time_val)
                            
                            # Aggiunge fade-in e fade-out
                            fade_samples = int(0.01 * sample_rate)
                            if j < fade_samples:
                                wave_val *= j / fade_samples
                            elif j >= frames - fade_samples:
                                wave_val *= (frames - j) / fade_samples
                            
                            # Applica envelope
                            envelope = math.exp(-time_val * 2)
                            wave_val *= envelope
                            
                            wave_val = int(4096 * volume * wave_val)
                            arr.append([wave_val, wave_val])
                    
                    # Controlla di nuovo se questa riproduzione è ancora valida
                    if self.stop_playing:
                        break
                        
                    # Riproduce il suono
                    sound = pygame.sndarray.make_sound(arr)
                    sound.play()
                    # Aggiunge il suono alla lista per il tracking
                    self.current_sounds.append(sound)
                    
                    # Controlla se questa riproduzione è ancora valida durante la pausa
                    if not self.stop_playing:
                        time.sleep(duration * 0.8)  # Piccola pausa tra le note
                    
            except (OSError, RuntimeError) as e:
                print(f"Errore nella riproduzione: {e}")
            except (ValueError, TypeError) as e:
                print(f"Errore nei dati audio: {e}")
        
        # Esegue la riproduzione in un thread separato
        self.current_thread = threading.Thread(target=play_notes)
        self.current_thread.daemon = True
        self.current_thread.start()


class MIDIOutput:
    """Gestisce l'output MIDI verso dispositivi esterni come DAW"""
    
    def __init__(self):
        self.initialized = False
        self.output_port = None
        self.available_ports = []
        self.selected_port = None
        
        if MIDI_AVAILABLE:
            try:
                self._refresh_ports()
                self.initialized = True
            except (OSError, RuntimeError, AttributeError) as e:
                print(f"Errore nell'inizializzazione MIDI: {e}")
                self.initialized = False
    
    def _refresh_ports(self):
        """Aggiorna la lista delle porte MIDI disponibili"""
        if not MIDI_AVAILABLE:
            return
        
        try:
            self.available_ports = mido.get_output_names()
        except (OSError, RuntimeError, AttributeError) as e:
            print(f"Errore nel refresh delle porte MIDI: {e}")
            self.available_ports = []
    
    def get_available_ports(self):
        """Restituisce la lista delle porte MIDI disponibili"""
        self._refresh_ports()
        return self.available_ports
    
    def set_output_port(self, port_name):
        """Imposta la porta di output MIDI"""
        if not MIDI_AVAILABLE:
            return False
        
        try:
            if self.output_port:
                self.output_port.close()
            
            if port_name and port_name in self.available_ports:
                self.output_port = mido.open_output(port_name)
                self.selected_port = port_name
                return True
            else:
                self.output_port = None
                self.selected_port = None
                return False
        except (OSError, RuntimeError, AttributeError) as e:
            print(f"Errore nell'apertura della porta MIDI {port_name}: {e}")
            return False
    
    def send_note_on(self, note, velocity=64, channel=0):
        """Invia un messaggio Note On"""
        if not self.initialized or not self.output_port:
            return False
        
        try:
            msg = mido.Message('note_on', channel=channel, note=note, velocity=velocity)
            self.output_port.send(msg)
            return True
        except (OSError, RuntimeError, AttributeError) as e:
            print(f"Errore nell'invio Note On: {e}")
            return False
    
    def send_note_off(self, note, channel=0):
        """Invia un messaggio Note Off"""
        if not self.initialized or not self.output_port:
            return False
        
        try:
            msg = mido.Message('note_off', channel=channel, note=note, velocity=0)
            self.output_port.send(msg)
            return True
        except (OSError, RuntimeError, AttributeError) as e:
            print(f"Errore nell'invio Note Off: {e}")
            return False
    
    def send_chord(self, midi_notes, duration=0.5, channel=0):
        """Invia un accordo MIDI"""
        if not self.initialized or not self.output_port:
            return False
        
        try:
            # Invia tutte le note dell'accordo
            for note in midi_notes:
                self.send_note_on(note, channel=channel)
            
            # Programma lo spegnimento delle note dopo la durata specificata
            def stop_notes():
                time.sleep(duration)
                for note in midi_notes:
                    self.send_note_off(note, channel=channel)
            
            # Esegue in un thread separato per non bloccare l'UI
            thread = threading.Thread(target=stop_notes)
            thread.daemon = True
            thread.start()
            
            return True
        except (OSError, RuntimeError, AttributeError) as e:
            print(f"Errore nell'invio dell'accordo MIDI: {e}")
            return False
    
    def close(self):
        """Chiude la connessione MIDI"""
        if self.output_port:
            try:
                self.output_port.close()
            except (OSError, RuntimeError, AttributeError):
                pass
            self.output_port = None


class ColorTreeDisplayApp:
    """Interfaccia grafica per visualizzare la Color Tree"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Color Tree")
        self.root.geometry("1800x930")
        self.root.configure(bg='#f0f0f0')
        
        self.generator = ChordGenerator()
        self.midi_generator = MIDIScaleGenerator()
        self.midi_output = MIDIOutput()
        self.color_tree_levels = []
        self.display_mode = "intervals"  # "intervals" or "notes"
        self.blue_tone = "classic"  # "classic", "navy", "royal", "sky"
        
        # Inizializza i bottoni
        self.intervals_btn = None
        self.notes_btn = None
        
        # Inizializza le variabili per i controlli
        self.blue_tone_var = None
        self.midi_port_var = None
        self.midi_combo = None
        
        # Variabile per la sound cell selezionata per la finestra creativa
        self.selected_sound_cell = None
        
        # Riferimento alla finestra creative per il cambio dinamico di accordo
        self.creative_window = None
        
        # Inizializza il bottone creativo per evitare errori di linting
        self.creative_btn = None
        
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
        
        # Selettore tonalità blu
        self.create_blue_tone_selector(controls_frame, 0, 3)
        
        # Frame per la visualizzazione della Color Tree - layout orizzontale
        self.tree_frame = ttk.Frame(main_frame)
        self.tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame per i controlli MIDI in basso a destra
        self.midi_frame = ttk.Frame(main_frame)
        self.midi_frame.grid(row=2, column=0, sticky=(tk.E, tk.S), pady=(5, 0))
        self.create_midi_controls()
        
        # Frame per il bottone creativo in basso a sinistra
        self.creative_frame = ttk.Frame(main_frame)
        self.creative_frame.grid(row=2, column=0, sticky=(tk.W, tk.S), pady=(5, 0))
        self.create_creative_controls()
        
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
    
    def create_blue_tone_selector(self, parent, row, column):
        """Crea il selettore per le tonalità di blu"""
        # Frame contenitore
        tone_frame = tk.Frame(parent, bg='#f0f0f0')
        tone_frame.grid(row=row, column=column, padx=(10, 0))
        
        # Label
        ttk.Label(tone_frame, text="Tonalità:", font=('Arial', 10)).pack(side='left', padx=(0, 5))
        
        # Combobox per le tonalità
        self.blue_tone_var = tk.StringVar(value="Classic")
        tone_combo = ttk.Combobox(tone_frame, textvariable=self.blue_tone_var,
                                 values=["Classic", "Navy", "Royal", "Sky"],
                                 state="readonly", width=10)
        tone_combo.pack(side='left')
        tone_combo.bind('<<ComboboxSelected>>', self.on_blue_tone_change)
    
    def create_midi_controls(self):
        """Crea i controlli MIDI in basso a destra"""
        # Frame contenitore per i controlli MIDI
        midi_container = tk.Frame(self.midi_frame, bg='#f0f0f0')
        midi_container.pack(side='right', padx=(0, 10), pady=(0, 5))
        
        # Label MIDI
        midi_label = tk.Label(midi_container, text="MIDI:", 
                             font=('Arial', 10, 'bold'), bg='#f0f0f0')
        midi_label.pack(side='left', padx=(0, 5))
        
        # Combobox per la selezione della porta MIDI
        self.midi_port_var = tk.StringVar(value="Nessuna porta")
        self.midi_combo = ttk.Combobox(midi_container, textvariable=self.midi_port_var,
                                      state="readonly", width=20)
        self.midi_combo.pack(side='left', padx=(0, 5))
        self.midi_combo.bind('<<ComboboxSelected>>', self.on_midi_port_change)
        
        # Bottone per aggiornare le porte MIDI
        refresh_btn = tk.Button(midi_container, text="🔄", 
                               font=('Arial', 8), width=2, height=1,
                               command=self.refresh_midi_ports)
        refresh_btn.pack(side='left', padx=(2, 0))
        
        # Inizializza le porte MIDI
        self.refresh_midi_ports()
    
    def create_creative_controls(self):
        """Crea i controlli per la finestra creativa in basso a sinistra"""
        # Frame contenitore per i controlli creativi
        creative_container = tk.Frame(self.creative_frame, bg='#f0f0f0')
        creative_container.pack(side='left', padx=(10, 0), pady=(0, 5))
        
        # Bottone per aprire la finestra creativa
        self.creative_btn = tk.Button(creative_container, text="🎵 Creative", 
                                     font=('Arial', 10, 'bold'), 
                                     bg='#FF9800', fg='white',
                                     command=self.open_creative_window,
                                     width=12, height=2)
        self.creative_btn.pack(side='left')
        
        # Label di istruzioni
        instruction_label = tk.Label(creative_container, 
                                   text="Click a chord, then click Creative", 
                                   font=('Arial', 8), 
                                   fg='#666666', bg='#f0f0f0')
        instruction_label.pack(side='left', padx=(10, 0))
    
    def refresh_midi_ports(self):
        """Aggiorna la lista delle porte MIDI disponibili"""
        if not MIDI_AVAILABLE:
            self.midi_combo['values'] = ["MIDI non disponibile"]
            self.midi_combo.set("MIDI non disponibile")
            return
        
        ports = self.midi_output.get_available_ports()
        if not ports:
            self.midi_combo['values'] = ["Nessuna porta MIDI"]
            self.midi_combo.set("Nessuna porta MIDI")
        else:
            port_list = ["Nessuna porta"] + ports
            self.midi_combo['values'] = port_list
            self.midi_combo.set("Nessuna porta")
    
    def on_midi_port_change(self, event=None):
        """Gestisce il cambio della porta MIDI"""
        del event  # Ignora il parametro event non utilizzato
        selected_port = self.midi_port_var.get()
        
        if selected_port == "Nessuna porta" or selected_port == "Nessuna porta MIDI" or selected_port == "MIDI non disponibile":
            self.midi_output.set_output_port(None)
        else:
            success = self.midi_output.set_output_port(selected_port)
            if not success:
                messagebox.showerror("Errore MIDI", f"Impossibile connettersi alla porta: {selected_port}")
    
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
    
    def on_blue_tone_change(self, event=None):
        """Gestisce il cambio della tonalità blu"""
        del event  # Ignora il parametro event non utilizzato
        tone_map = {
            "Classic": "classic",
            "Navy": "navy", 
            "Royal": "royal",
            "Sky": "sky"
        }
        self.blue_tone = tone_map.get(self.blue_tone_var.get(), "classic")
        self.generate_color_tree()
    
    def on_sound_cell_click(self, sound_cell: SoundCell):
        """Gestisce il click su una sound cell per riprodurre la scala MIDI"""
        # Memorizza la sound cell selezionata per la finestra creativa
        self.selected_sound_cell = sound_cell
        
        # Se la finestra creative è aperta, cambia l'accordo in tempo reale
        if self.creative_window and self.creative_window.is_window_open():
            self.creative_window.change_chord(sound_cell)
            # Non riprodurre preview audio quando la finestra creative è aperta
            return
        
        # Riproduzione audio tramite pygame (solo quando finestra creative è chiusa)
        self.midi_generator.play_scale(sound_cell)
        
        # Output MIDI verso DAW se configurato
        if self.midi_output.initialized and self.midi_output.output_port:
            try:
                # Genera le note MIDI per l'accordo
                midi_notes = self.midi_generator.generate_scale_notes(sound_cell)
                # Invia l'accordo MIDI
                self.midi_output.send_chord(midi_notes, duration=2.0)
            except (OSError, RuntimeError, AttributeError) as e:
                print(f"Errore nell'invio MIDI: {e}")
    
    
    def open_creative_window(self):
        """Apre la finestra per la riproduzione creativa degli accordi"""
        if not CREATIVE_WINDOW_AVAILABLE:
            messagebox.showerror("Error", "Creative window module not available. Please check the installation.")
            return
        
        if self.selected_sound_cell is None:
            messagebox.showwarning("No Selection", "Please click on a chord first to select it for creative playback.")
            return
        
        try:
            # Se la finestra è già aperta, aggiorna l'accordo
            if self.creative_window and self.creative_window.is_window_open():
                self.creative_window.change_chord(self.selected_sound_cell)
                self.creative_window.show()
            else:
                # Crea e mostra la finestra creativa
                self.creative_window = CreativeChordWindow(
                    self.root, 
                    self.selected_sound_cell, 
                    self.midi_generator
                )
                self.creative_window.show()
        except (ImportError, RuntimeError, OSError) as e:
            messagebox.showerror("Error", f"Failed to open creative window: {str(e)}")
    
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
        # Calcola il colore basato sulla posizione (da scuro a sinistra a chiaro a destra)
        # Per il livello 12, usa 12 come numero totale, altrimenti usa il livello
        total_cells = 12 if sound_cell.level == 12 else sound_cell.level
        bg_color = self._get_position_color(sound_cell.level, position, total_cells)
        
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
        # Aggiunge click handler al frame delle quinte
        fifths_frame.bind("<Button-1>", lambda e: self.on_sound_cell_click(sound_cell))
        fifths_frame.bind("<Enter>", lambda e: main_cell.config(relief='solid', bd=2))
        fifths_frame.bind("<Leave>", lambda e: main_cell.config(relief='raised', bd=1))
        
        if sound_cell.level == 12:
            # Per il livello 12, mostra "Chromatic Scale" al centro
            chromatic_label = tk.Label(fifths_frame, text="Chromatic Scale", 
                    bg=bg_color, font=('Arial', 9, 'bold'))
            chromatic_label.pack(expand=True)
            # Aggiunge click handler al label
            chromatic_label.bind("<Button-1>", lambda e: self.on_sound_cell_click(sound_cell))
            chromatic_label.bind("<Enter>", lambda e: main_cell.config(relief='solid', bd=2))
            chromatic_label.bind("<Leave>", lambda e: main_cell.config(relief='raised', bd=1))
        else:
            left_label = tk.Label(fifths_frame, text=f"-{sound_cell.fifths_below}", 
                    bg=bg_color, font=('Arial', 7, 'bold'))
            left_label.pack(side='left')
            # Aggiunge click handler al label sinistro
            left_label.bind("<Button-1>", lambda e: self.on_sound_cell_click(sound_cell))
            left_label.bind("<Enter>", lambda e: main_cell.config(relief='solid', bd=2))
            left_label.bind("<Leave>", lambda e: main_cell.config(relief='raised', bd=1))
            
            right_label = tk.Label(fifths_frame, text=f"+{sound_cell.fifths_above}", 
                    bg=bg_color, font=('Arial', 7, 'bold'))
            right_label.pack(side='right')
            # Aggiunge click handler al label destro
            right_label.bind("<Button-1>", lambda e: self.on_sound_cell_click(sound_cell))
            right_label.bind("<Enter>", lambda e: main_cell.config(relief='solid', bd=2))
            right_label.bind("<Leave>", lambda e: main_cell.config(relief='raised', bd=1))
        
        # Rappresentazione degli intervalli (centro) - bilanciata
        circle_frame = tk.Frame(main_cell, bg=bg_color, height=55)
        circle_frame.pack(fill='both', expand=True, padx=2, pady=1)
        # Aggiunge click handler al frame centrale
        circle_frame.bind("<Button-1>", lambda e: self.on_sound_cell_click(sound_cell))
        circle_frame.bind("<Enter>", lambda e: main_cell.config(relief='solid', bd=2))
        circle_frame.bind("<Leave>", lambda e: main_cell.config(relief='raised', bd=1))
        
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
    
    def _get_position_color(self, level: int, position: int, total_cells: int) -> str:
        """Calcola il colore basato sulla posizione e sulla tonalità blu selezionata"""
        del level  # Non utilizzato ma mantenuto per compatibilità
        if total_cells <= 1:
            return self._get_single_cell_color()
        
        # Calcola il rapporto di posizione (0.0 = sinistra, 1.0 = destra)
        position_ratio = position / (total_cells - 1) if total_cells > 1 else 0.5
        
        # Ottiene i parametri HSV basati sulla tonalità selezionata
        hue_start, hue_end, sat_start, sat_end, val_start, val_end = self._get_blue_tone_params()
        
        # Calcola i valori HSV per questa posizione
        hue = hue_start - (position_ratio * (hue_start - hue_end))
        saturation = sat_start - (position_ratio * (sat_start - sat_end))
        value = val_start + (position_ratio * (val_end - val_start))
        
        # Converte HSV a RGB
        return self._hsv_to_hex(hue, saturation, value)
    
    def _get_single_cell_color(self) -> str:
        """Restituisce il colore per celle singole basato sulla tonalità"""
        tone_colors = {
            "classic": "#0059E8",  # Blu specifico richiesto
            "navy": "#0059E8",     # Blu specifico richiesto
            "royal": "#0059E8",    # Blu specifico richiesto
            "sky": "#0059E8"       # Blu specifico richiesto
        }
        return tone_colors.get(self.blue_tone, "#0059E8")
    
    def _get_blue_tone_params(self):
        """Restituisce i parametri HSV per la tonalità blu selezionata"""
        # #0059E8 convertito in HSV: H=217, S=100, V=91
        base_hue = 217  # Tonalità del blu #0059E8
        base_sat = 100  # Saturazione del blu #0059E8
        base_val = 91   # Luminosità del blu #0059E8
        
        tone_params = {
            "classic": (base_hue, 200, base_sat, 30, base_val, 90),  # #0059E8 -> Celestino
            "navy": (base_hue, 200, base_sat, 25, base_val, 80),     # #0059E8 -> Azzurro chiaro
            "royal": (base_hue, 200, base_sat, 35, base_val, 85),    # #0059E8 -> Azzurro reale
            "sky": (base_hue, 200, base_sat, 20, base_val, 95)       # #0059E8 -> Azzurro cielo
        }
        return tone_params.get(self.blue_tone, tone_params["classic"])
    
    def _hsv_to_hex(self, h: float, s: float, v: float) -> str:
        """Converte HSV a colore hex"""
        h = h / 360.0
        s = s / 100.0
        v = v / 100.0
        
        if s == 0:
            # Grigio
            rgb = [int(v * 255)] * 3
        else:
            i = int(h * 6)
            f = h * 6 - i
            p = v * (1 - s)
            q = v * (1 - s * f)
            t = v * (1 - s * (1 - f))
            
            if i == 0:
                rgb = [v, t, p]
            elif i == 1:
                rgb = [q, v, p]
            elif i == 2:
                rgb = [p, v, t]
            elif i == 3:
                rgb = [p, q, v]
            elif i == 4:
                rgb = [t, p, v]
            else:
                rgb = [v, p, q]
        
        # Converte a hex
        r, g, b = [int(x * 255) for x in rgb]
        return f"#{r:02x}{g:02x}{b:02x}"
    
    
    def run(self):
        """Avvia l'applicazione"""
        # Configura la chiusura pulita dell'applicazione
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Gestisce la chiusura dell'applicazione"""
        # Chiude la connessione MIDI
        if hasattr(self, 'midi_output'):
            self.midi_output.close()
        # Chiude l'applicazione
        self.root.destroy()


def main():
    """Funzione principale"""
    try:
        app = ColorTreeDisplayApp()
        app.run()
    except (tk.TclError, ImportError, RuntimeError) as e:
        messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")


if __name__ == "__main__":
    main()
