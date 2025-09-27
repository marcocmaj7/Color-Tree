"""
Finestra per la riproduzione creativa di accordi con pattern
"""

import tkinter as tk
from tkinter import ttk
import math
from pattern_engine import PatternEngine, PatternType
from chord_generator import SoundCell, MIDIScaleGenerator




class CreativeChordWindow:
    """Finestra separata per la riproduzione creativa di accordi"""
    
    def __init__(self, parent, sound_cell: SoundCell, midi_generator: MIDIScaleGenerator, midi_output=None):
        self.parent = parent
        self.sound_cell = sound_cell
        self.midi_generator = midi_generator
        self.midi_output = midi_output  # Aggiunto supporto MIDI
        self.pattern_engine = PatternEngine(midi_generator, midi_output)  # Passa MIDI al pattern engine
        
        # Crea la finestra
        self.window = tk.Toplevel(parent)
        self.window.title("Creative Chord Patterns")
        self.window.geometry("1000x700")
        self.window.configure(bg='#f8f9fa')
        self.window.resizable(False, False)  # Fixed size for single screen
        
        # Variabili per i controlli
        self.selected_pattern = tk.StringVar(value="up")
        self.start_octave_var = tk.IntVar(value=4)
        self.duration_octaves_var = tk.IntVar(value=1)
        self.note_duration_var = tk.StringVar(value="Quarter")
        self.bpm_var = tk.IntVar(value=120)
        self.playback_speed_var = tk.DoubleVar(value=1.0)
        self.loop_var = tk.BooleanVar(value=False)
        self.reverse_var = tk.BooleanVar(value=False)
        self.pause_duration_var = tk.StringVar(value="none")
        
        # Variabili per gli effetti MIDI
        self.delay_enabled_var = tk.BooleanVar(value=False)
        self.delay_time_var = tk.DoubleVar(value=0.25)
        self.delay_feedback_var = tk.DoubleVar(value=0.3)
        self.delay_mix_var = tk.DoubleVar(value=0.5)  # Mix dry/wet
        self.delay_type_var = tk.StringVar(value="Standard")  # Tipo di delay
        self.delay_velocity_var = tk.DoubleVar(value=0.8)  # Velocità echi
        self.delay_repeats_var = tk.IntVar(value=3)  # Numero ripetizioni
        self.octave_add_var = tk.IntVar(value=0)
        self.velocity_curve_var = tk.StringVar(value="linear")
        self.velocity_intensity_var = tk.DoubleVar(value=1.0)
        self.accent_enabled_var = tk.BooleanVar(value=False)
        self.accent_strength_var = tk.DoubleVar(value=0.5)
        self.accent_pattern_var = tk.StringVar(value="every_beat")
        self.repeater_enabled_var = tk.BooleanVar(value=False)
        self.repeat_count_var = tk.IntVar(value=2)
        self.repeat_timing_var = tk.StringVar(value="immediate")
        self.chord_gen_enabled_var = tk.BooleanVar(value=False)
        self.chord_variation_var = tk.StringVar(value="inversion")
        self.voicing_var = tk.StringVar(value="close")
        
        # Stato dei controlli
        self.is_playing = False
        
        # Inizializza i widget per evitare errori di linting
        self.play_btn = None
        self.stop_btn = None
        self.loop_btn = None
        self.reverse_btn = None
        self.start_octave_label = None
        self.duration_octaves_label = None
        self.note_duration_label = None
        self.bpm_label = None
        self.playback_speed_label = None
        self.octave_add_label = None

        # Pulsanti degli effetti MIDI
        self.delay_btn = None
        self.delay_type_button = None # Aggiunto per il nuovo pulsante "Tipo"
        
        # Pulsanti degli effetti MIDI
        self.delay_btn = None
        self.octave_btn = None
        self.velocity_btn = None
        self.accent_btn = None
        self.repeater_btn = None
        self.chord_gen_btn = None
        
        # Dizionario per tracciare i pulsanti pattern per l'evidenziazione
        self.pattern_buttons = {}
        
        # Configurazione stile
        self.setup_styles()
        self.setup_ui()
        self.update_controls()
        
        # L'evidenziazione viene gestita in initialize_highlighting()
        
        # Inizializza la visualizzazione della velocità e BPM
        self.update_speed_display()
        self.update_bpm_display()
        
        # Inizializza i pulsanti degli effetti
        self.initialize_effect_buttons()
        
        self.setup_keyboard_shortcuts()
        
        # Gestisce la chiusura della finestra
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Configura gli stili per l'interfaccia"""
        # Configurazione stile ttk
        style = ttk.Style()
        style.theme_use('clam')
        
        # Stile per i LabelFrame
        style.configure('Modern.TLabelframe', 
                       background='#f8f9fa',
                       borderwidth=1,
                       relief='solid')
        style.configure('Modern.TLabelframe.Label',
                       background='#f8f9fa',
                       foreground='#2c3e50',
                       font=('Segoe UI', 10, 'bold'))
        
        # Stile per i bottoni
        style.configure('Modern.TButton',
                       font=('Segoe UI', 9),
                       padding=(10, 5))
        
        # Stile per i radio button
        style.configure('Modern.TRadiobutton',
                       background='#f8f9fa',
                       foreground='#2c3e50',
                       font=('Segoe UI', 9))
    
    def setup_ui(self):
        """Configura l'interfaccia utente ottimizzata per una singola schermata"""
        # Frame principale senza scrollbar
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.pack(fill='both', expand=True)
        
        # Titolo principale
        title_frame = tk.Frame(main_frame, bg='#f8f9fa')
        title_frame.pack(fill='x', pady=(0, 15))
        
        title_label = tk.Label(title_frame, text="🎵 Creative Chord Patterns", 
                              font=('Segoe UI', 18, 'bold'), 
                              bg='#f8f9fa', fg='#2c3e50')
        title_label.pack(side='left')
        
        # Informazioni accordo compatte
        self.create_chord_info_compact(title_frame)
        
        # Layout a griglia per ottimizzare lo spazio
        content_frame = tk.Frame(main_frame, bg='#f8f9fa')
        content_frame.pack(fill='both', expand=True)
        
        # Colonna sinistra: Controlli e parametri
        left_column = tk.Frame(content_frame, bg='#f8f9fa')
        left_column.pack(side='left', fill='y', padx=(0, 10))
        
        # Controlli di riproduzione
        self.create_playback_controls(left_column)
        
        # Controlli di parametri
        self.create_parameter_controls(left_column)
        
        # Controlli effetti MIDI
        self.create_midi_effects_controls(left_column)
        
        # Colonna destra: Pattern selection e status
        right_column = tk.Frame(content_frame, bg='#f8f9fa')
        right_column.pack(side='right', fill='both', expand=True)
        
        # Controlli pattern compatti
        self.create_pattern_controls_compact(right_column)
        
        # Inizializza l'evidenziazione dei controlli
        self.initialize_highlighting()
    
    def initialize_highlighting(self):
        """Inizializza l'evidenziazione dei controlli con i valori predefiniti"""
        # Evidenzia il pattern iniziale
        initial_pattern = self.selected_pattern.get()
        if initial_pattern in self.pattern_buttons:
            self.highlight_selected_pattern(initial_pattern)
        
        # Evidenzia la pausa iniziale
        initial_pause = self.pause_duration_var.get()
        if initial_pause in self.pattern_buttons:
            self.highlight_selected_pause(initial_pause)
    
    def initialize_effect_buttons(self):
        """Inizializza i colori dei pulsanti degli effetti"""
        # Delay
        if hasattr(self, 'delay_btn') and hasattr(self, 'delay_type_button'):
            if self.delay_enabled_var.get():
                self.delay_btn.config(bg='#3498db', fg='white')
                self.delay_type_button.config(bg='#3498db', fg='white')
            else:
                self.delay_btn.config(bg='#95a5a6', fg='white')
                self.delay_type_button.config(bg='#95a5a6', fg='white')
        
        # Octave
        if hasattr(self, 'octave_btn'):
            if self.octave_add_var.get() != 0:
                self.octave_btn.config(bg='#9b59b6', fg='white')
            else:
                self.octave_btn.config(bg='#95a5a6', fg='white')
        
        # Velocity
        if hasattr(self, 'velocity_btn'):
            if self.velocity_curve_var.get() != "linear":
                self.velocity_btn.config(bg='#27ae60', fg='white')
            else:
                self.velocity_btn.config(bg='#95a5a6', fg='white')
        
        # Accent
        if hasattr(self, 'accent_btn'):
            if self.accent_enabled_var.get():
                self.accent_btn.config(bg='#e74c3c', fg='white')
            else:
                self.accent_btn.config(bg='#95a5a6', fg='white')
        
        # Repeater
        if hasattr(self, 'repeater_btn'):
            if self.repeater_enabled_var.get():
                self.repeater_btn.config(bg='#f39c12', fg='white')
            else:
                self.repeater_btn.config(bg='#95a5a6', fg='white')
        
        # Chord Generator
        if hasattr(self, 'chord_gen_btn'):
            if self.chord_gen_enabled_var.get():
                self.chord_gen_btn.config(bg='#9b59b6', fg='white')
            else:
                self.chord_gen_btn.config(bg='#95a5a6', fg='white')
    
    def create_chord_info_compact(self, parent):
        """Crea informazioni accordo compatte nel titolo"""
        info_frame = tk.Frame(parent, bg='#f8f9fa')
        info_frame.pack(side='right', padx=(20, 0))
        
        # Nome dell'accordo
        chord_name = self.sound_cell.__str__()
        chord_label = tk.Label(info_frame, text=f"Chord: {chord_name}", 
                              font=('Segoe UI', 12, 'bold'), 
                              bg='#f8f9fa', fg='#3498db')
        chord_label.pack(anchor='e')
        
        # Intervalli compatti
        intervals = self.sound_cell.to_intervals_string()
        intervals_label = tk.Label(info_frame, text=f"Intervals: {intervals}", 
                                 font=('Segoe UI', 9), 
                                 bg='#f8f9fa', fg='#7f8c8d')
        intervals_label.pack(anchor='e')
    
    def create_chord_info(self, parent):
        """Crea l'area informazioni sull'accordo"""
        info_frame = ttk.LabelFrame(parent, text="Selected Chord", padding="10")
        info_frame.pack(fill='x', pady=(0, 20))
        
        # Nome dell'accordo
        chord_name = self.sound_cell.__str__()
        chord_label = tk.Label(info_frame, text=f"Chord: {chord_name}", 
                              font=('Arial', 12, 'bold'), bg='#f0f0f0')
        chord_label.pack(anchor='w')
        
        # Intervalli
        intervals = self.sound_cell.to_intervals_string()
        intervals_label = tk.Label(info_frame, text=f"Intervals: {intervals}", 
                                 font=('Arial', 10), bg='#f0f0f0')
        intervals_label.pack(anchor='w')
        
        # Livello e posizione
        level_info = f"Level: {self.sound_cell.level}, Position: {self.sound_cell.position}"
        level_label = tk.Label(info_frame, text=level_info, 
                              font=('Arial', 10), bg='#f0f0f0')
        level_label.pack(anchor='w')
    
    def create_pattern_controls(self, parent):
        """Crea i controlli per la selezione del pattern"""
        pattern_frame = ttk.LabelFrame(parent, text="Pattern Selection", padding="10")
        pattern_frame.pack(fill='x', pady=(0, 20))
        
        # Pattern Base
        base_frame = ttk.LabelFrame(pattern_frame, text="Base Patterns", padding="5")
        base_frame.pack(fill='x', pady=(0, 10))
        
        base_patterns = [
            ("Up", "up", "Ascendente semplice (C→E→G→C)"),
            ("Down", "down", "Discendente semplice (C→G→E→C)"),
            ("Up-Down", "up_down", "Su poi giù (C→E→G→C→G→E)"),
            ("Down-Up", "down_up", "Giù poi su (C→G→E→C→E→G)")
        ]
        
        for i, (name, value, desc) in enumerate(base_patterns):
            self.create_pattern_radio(base_frame, name, value, desc, i, 0)
        
        # Pattern Geometrici
        geo_frame = ttk.LabelFrame(pattern_frame, text="Geometric Patterns", padding="5")
        geo_frame.pack(fill='x', pady=(0, 10))
        
        geo_patterns = [
            ("Triangle", "triangle", "Su-giù-su formando un triangolo melodico"),
            ("Diamond", "diamond", "Dentro-fuori-dentro (E→G→C→G→E)"),
            ("Zigzag", "zigzag", "Alternanza estremi-centro (C→G→E→C)"),
            ("Spiral", "spiral", "Giri concentrici espandendosi")
        ]
        
        for i, (name, value, desc) in enumerate(geo_patterns):
            self.create_pattern_radio(geo_frame, name, value, desc, i, 0)
        
        # Pattern Ritmici
        rhythm_frame = ttk.LabelFrame(pattern_frame, text="Rhythmic Patterns", padding="5")
        rhythm_frame.pack(fill='x', pady=(0, 10))
        
        rhythm_patterns = [
            ("Gallop", "gallop", "Due note veloci + una lunga (ta-ta-TAA)"),
            ("Triplet", "triplet", "Gruppetti di tre note"),
            ("Syncopated", "syncopated", "Enfasi sui tempi deboli"),
            ("Stutter", "stutter", "Ripetizione rapida della stessa nota")
        ]
        
        for i, (name, value, desc) in enumerate(rhythm_patterns):
            self.create_pattern_radio(rhythm_frame, name, value, desc, i, 0)
        
        # Pattern Avanzati
        advanced_frame = ttk.LabelFrame(pattern_frame, text="Advanced Patterns", padding="5")
        advanced_frame.pack(fill='x', pady=(0, 10))
        
        advanced_patterns = [
            ("Skip", "skip", "Salta note casualmente nel pattern"),
            ("Ghost", "ghost", "Include note 'fantasma' a volume basso"),
            ("Cascade", "cascade", "Effetto 'cascata' con note che si sovrappongono"),
            ("Bounce", "bounce", "'Rimbalza' tra note estreme")
        ]
        
        for i, (name, value, desc) in enumerate(advanced_patterns):
            self.create_pattern_radio(advanced_frame, name, value, desc, i, 0)
        
        # Pattern Espressivi
        expressive_frame = ttk.LabelFrame(pattern_frame, text="Expressive Patterns", padding="5")
        expressive_frame.pack(fill='x')
        
        expressive_patterns = [
            ("Crescendo", "crescendo", "Volume crescente attraverso l'arpeggio"),
            ("Diminuendo", "diminuendo", "Volume decrescente"),
            ("Accent First", "accent_first", "Prima nota accentata, altre morbide"),
            ("Swing", "swing", "Timing swing su note alternate")
        ]
        
        for i, (name, value, desc) in enumerate(expressive_patterns):
            self.create_pattern_radio(expressive_frame, name, value, desc, i, 0)
    
    def create_pattern_radio(self, parent, name, value, desc, row, col):
        """Crea un radio button per il pattern"""
        radio = tk.Radiobutton(parent, text=name, variable=self.selected_pattern, 
                              value=value, command=self.on_pattern_change,
                              font=('Arial', 9, 'bold'), bg='#f0f0f0')
        radio.grid(row=row, column=col, sticky='w', padx=(0, 10), pady=2)
        
        desc_label = tk.Label(parent, text=desc, font=('Arial', 8), 
                             fg='#666666', bg='#f0f0f0')
        desc_label.grid(row=row, column=col+1, sticky='w', padx=(0, 10), pady=2)
    
    def create_playback_controls(self, parent):
        """Crea i controlli di riproduzione con design moderno"""
        playback_frame = ttk.LabelFrame(parent, text="Playback Controls", 
                                       style='Modern.TLabelframe', padding="10")
        playback_frame.pack(fill='x', pady=(0, 15))
        
        # Bottoni di controllo in layout orizzontale
        button_frame = tk.Frame(playback_frame, bg='#f8f9fa')
        button_frame.pack(fill='x', pady=(0, 5))
        
        # Play button più piccolo
        self.play_btn = tk.Button(button_frame, text="▶", 
                                 font=('Segoe UI', 9, 'bold'),
                                 bg='#27ae60', fg='white',
                                 command=self.play_pattern,
                                 width=6, height=1,
                                 relief='flat', bd=0,
                                 cursor='hand2',
                                 activebackground='#2ecc71',
                                 activeforeground='white')
        self.play_btn.pack(side='left', padx=(0, 5))
        
        # Stop button più piccolo
        self.stop_btn = tk.Button(button_frame, text="■", 
                                 font=('Segoe UI', 9, 'bold'),
                                 bg='#e74c3c', fg='white',
                                 command=self.stop_pattern,
                                 width=6, height=1,
                                 relief='flat', bd=0,
                                 cursor='hand2',
                                 activebackground='#c0392b',
                                 activeforeground='white')
        self.stop_btn.pack(side='left', padx=(0, 10))
        
        # Loop button singolo
        self.loop_btn = tk.Button(button_frame, text="Loop", 
                                 font=('Segoe UI', 8, 'bold'),
                                 bg='#95a5a6', fg='white',
                                 command=self.toggle_loop,
                                 width=8, height=1,
                                 relief='flat', bd=0,
                                 cursor='hand2',
                                 activebackground='#7f8c8d',
                                 activeforeground='white')
        self.loop_btn.pack(side='left', padx=(0, 5))
        
        # Reverse button
        self.reverse_btn = tk.Button(button_frame, text="Reverse", 
                                    font=('Segoe UI', 8, 'bold'),
                                    bg='#95a5a6', fg='white',
                                    command=self.toggle_reverse,
                                    width=8, height=1,
                                    relief='flat', bd=0,
                                    cursor='hand2',
                                    activebackground='#7f8c8d',
                                    activeforeground='white')
        self.reverse_btn.pack(side='left', padx=(0, 10))
        
        # Playback Speed Control
        speed_frame = tk.Frame(button_frame, bg='#f8f9fa')
        speed_frame.pack(side='left', padx=(0, 0))
        
        # Speed label
        speed_label = tk.Label(speed_frame, text="Speed", 
                              font=('Segoe UI', 8, 'bold'), 
                              bg='#f8f9fa', fg='#2c3e50')
        speed_label.pack(side='left', padx=(0, 2))
        
        # Speed down button
        speed_down = tk.Button(speed_frame, text="◀", 
                              font=('Segoe UI', 8, 'bold'),
                              bg='#9b59b6', fg='white',
                              command=self.decrease_playback_speed,
                              width=3, height=1,
                              relief='flat', bd=0,
                              cursor='hand2',
                              activebackground='#8e44ad',
                              activeforeground='white')
        speed_down.pack(side='left', padx=(0, 2))
        
        # Speed value label
        self.playback_speed_label = tk.Label(speed_frame, text="1.0x", 
                                            font=('Segoe UI', 9, 'bold'), 
                                            bg='#9b59b6', fg='white',
                                            width=4, relief='flat')
        self.playback_speed_label.pack(side='left', padx=(2, 2))
        
        # Speed up button
        speed_up = tk.Button(speed_frame, text="▶", 
                            font=('Segoe UI', 8, 'bold'),
                            bg='#9b59b6', fg='white',
                            command=self.increase_playback_speed,
                            width=3, height=1,
                            relief='flat', bd=0,
                            cursor='hand2',
                            activebackground='#8e44ad',
                            activeforeground='white')
        speed_up.pack(side='left', padx=(2, 0))
    
    def create_parameter_controls(self, parent):
        """Crea i controlli per i parametri compatti"""
        param_frame = ttk.LabelFrame(parent, text="Parameters", 
                                    style='Modern.TLabelframe', padding="10")
        param_frame.pack(fill='x', pady=(0, 15))
        
        # Frame principale per i parametri in griglia
        params_frame = tk.Frame(param_frame, bg='#f8f9fa')
        params_frame.pack(fill='x')
        
        # Ottava Start
        start_octave_frame = tk.Frame(params_frame, bg='#f8f9fa')
        start_octave_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        start_octave_label = tk.Label(start_octave_frame, text="Start Octave", 
                                     font=('Segoe UI', 9, 'bold'), 
                               bg='#f8f9fa', fg='#2c3e50')
        start_octave_label.pack(anchor='center')
        
        start_octave_controls = tk.Frame(start_octave_frame, bg='#f8f9fa')
        start_octave_controls.pack(fill='x', pady=(2, 0))
        
        # Pulsanti freccia per ottava start
        start_octave_up = tk.Button(start_octave_controls, text="▲", 
                                   font=('Segoe UI', 8, 'bold'),
                                   bg='#3498db', fg='white',
                                   command=self.increase_start_octave,
                                   width=3, height=1,
                                   relief='flat', bd=0,
                                   cursor='hand2',
                                   activebackground='#2980b9',
                                   activeforeground='white')
        start_octave_up.pack(side='left', padx=(0, 2))
        
        self.start_octave_label = tk.Label(start_octave_controls, text="4", 
                                          font=('Segoe UI', 10, 'bold'), 
                                          bg='#3498db', fg='white',
                                          width=3, relief='flat')
        self.start_octave_label.pack(side='left', padx=(2, 2))
        
        start_octave_down = tk.Button(start_octave_controls, text="▼", 
                                     font=('Segoe UI', 8, 'bold'),
                                     bg='#3498db', fg='white',
                                     command=self.decrease_start_octave,
                                     width=3, height=1,
                                     relief='flat', bd=0,
                                     cursor='hand2',
                                     activebackground='#2980b9',
                                     activeforeground='white')
        start_octave_down.pack(side='left', padx=(2, 0))
        
        # Durata Ottave
        duration_octaves_frame = tk.Frame(params_frame, bg='#f8f9fa')
        duration_octaves_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        duration_octaves_label = tk.Label(duration_octaves_frame, text="Duration Octaves", 
                                         font=('Segoe UI', 9, 'bold'), 
                                bg='#f8f9fa', fg='#2c3e50')
        duration_octaves_label.pack(anchor='w', padx=(0, 0))
        
        duration_octaves_controls = tk.Frame(duration_octaves_frame, bg='#f8f9fa')
        duration_octaves_controls.pack(fill='x', pady=(2, 0))
        
        # Pulsanti freccia per durata ottave
        duration_octaves_up = tk.Button(duration_octaves_controls, text="▲", 
                                       font=('Segoe UI', 8, 'bold'),
                                       bg='#e67e22', fg='white',
                                       command=self.increase_duration_octaves,
                                       width=3, height=1,
                                       relief='flat', bd=0,
                                       cursor='hand2',
                                       activebackground='#d35400',
                                       activeforeground='white')
        duration_octaves_up.pack(side='left', padx=(0, 2))
        
        self.duration_octaves_label = tk.Label(duration_octaves_controls, text="1", 
                                              font=('Segoe UI', 10, 'bold'), 
                                              bg='#e67e22', fg='white',
                                              width=3, relief='flat')
        self.duration_octaves_label.pack(side='left', padx=(2, 2))
        
        duration_octaves_down = tk.Button(duration_octaves_controls, text="▼", 
                                         font=('Segoe UI', 8, 'bold'),
                                           bg='#e67e22', fg='white',
                                         command=self.decrease_duration_octaves,
                                         width=3, height=1,
                                         relief='flat', bd=0,
                                         cursor='hand2',
                                         activebackground='#d35400',
                                         activeforeground='white')
        duration_octaves_down.pack(side='left', padx=(2, 0))
        
        # Durata Note
        note_duration_frame = tk.Frame(params_frame, bg='#f8f9fa')
        note_duration_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        note_duration_label = tk.Label(note_duration_frame, text="Note Duration", 
                                      font=('Segoe UI', 9, 'bold'), 
                                      bg='#f8f9fa', fg='#2c3e50')
        note_duration_label.pack(anchor='center')
        
        note_duration_controls = tk.Frame(note_duration_frame, bg='#f8f9fa')
        note_duration_controls.pack(fill='x', pady=(2, 0))
        
        # Dropdown per durata note
        note_duration_options = ["Whole", "Half", "Quarter", "Eighth", "Sixteenth", "Thirty-Second"]
        note_duration_dropdown = ttk.Combobox(note_duration_controls, 
                                             textvariable=self.note_duration_var,
                                             values=note_duration_options,
                                             state="readonly",
                                             width=12,
                                             font=('Segoe UI', 9))
        note_duration_dropdown.pack(side='left')
        note_duration_dropdown.bind('<<ComboboxSelected>>', self.on_note_duration_change)
        
        # BPM Control
        bpm_frame = tk.Frame(params_frame, bg='#f8f9fa')
        bpm_frame.pack(side='left', fill='x', expand=True)
        
        bpm_label = tk.Label(bpm_frame, text="BPM", 
                            font=('Segoe UI', 9, 'bold'), 
                            bg='#f8f9fa', fg='#2c3e50')
        bpm_label.pack(anchor='center')
        
        bpm_controls = tk.Frame(bpm_frame, bg='#f8f9fa')
        bpm_controls.pack(fill='x', pady=(2, 0))
        
        # Pulsanti freccia per BPM
        bpm_down = tk.Button(bpm_controls, text="▼", 
                            font=('Segoe UI', 8, 'bold'),
                            bg='#27ae60', fg='white',
                            command=self.decrease_bpm,
                            width=3, height=1,
                            relief='flat', bd=0,
                            cursor='hand2',
                            activebackground='#229954',
                            activeforeground='white')
        bpm_down.pack(side='left', padx=(0, 2))
        
        self.bpm_label = tk.Label(bpm_controls, text="120", 
                                 font=('Segoe UI', 10, 'bold'), 
                                 bg='#27ae60', fg='white',
                                 width=4, relief='flat')
        self.bpm_label.pack(side='left', padx=(2, 2))
        
        # Binding per doppio click per inserimento manuale
        self.bpm_label.bind('<Double-Button-1>', self.on_bpm_double_click)
        
        bpm_up = tk.Button(bpm_controls, text="▲", 
                          font=('Segoe UI', 8, 'bold'),
                          bg='#27ae60', fg='white',
                          command=self.increase_bpm,
                          width=3, height=1,
                          relief='flat', bd=0,
                          cursor='hand2',
                          activebackground='#229954',
                          activeforeground='white')
        bpm_up.pack(side='left', padx=(2, 0))
        
        # Aggiorna i valori quando cambiano
        def update_start_octave_value(*_):
            self.start_octave_label.config(text=str(int(self.start_octave_var.get())))
        self.start_octave_var.trace('w', update_start_octave_value)
        
        def update_duration_octaves_value(*_):
            self.duration_octaves_label.config(text=str(int(self.duration_octaves_var.get())))
        self.duration_octaves_var.trace('w', update_duration_octaves_value)
    
    def create_midi_effects_controls(self, parent):
        """Crea i controlli per gli effetti MIDI compatti"""
        effects_frame = ttk.LabelFrame(parent, text="🎛️ MIDI Effects", 
                                     style='Modern.TLabelframe', padding="8")
        effects_frame.pack(fill='x', pady=(0, 15))
        
        # Layout a griglia uniforme 3x2
        effects_grid = tk.Frame(effects_frame, bg='#f8f9fa')
        effects_grid.pack(fill='both', expand=True)
        
        # Configurazione griglia uniforme
        for i in range(3):  # 3 righe
            effects_grid.grid_rowconfigure(i, weight=1, uniform="row")
        for j in range(2):  # 2 colonne
            effects_grid.grid_columnconfigure(j, weight=1, uniform="col")
        
        # Riga 1: Delay e Octave
        self.create_delay_controls_compact(effects_grid, 0, 0)
        self.create_octave_controls_compact(effects_grid, 0, 1)
        
        # Riga 2: Velocity e Accent
        self.create_velocity_controls_compact(effects_grid, 1, 0)
        self.create_accent_controls_compact(effects_grid, 1, 1)
        
        # Riga 3: Repeater e Chord Generator
        self.create_repeater_controls_compact(effects_grid, 2, 0)
        self.create_chord_gen_controls_compact(effects_grid, 2, 1)
    
    def create_delay_controls_compact(self, parent, row, col):
        """Crea i controlli per l'effetto Delay (MIDI Echo) con slider"""
        # Sottoriquadro colorato per Delay
        delay_frame = tk.Frame(parent, bg='#e8f4fd', relief='solid', bd=1)
        delay_frame.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        
        # Header con pulsante di attivazione
        delay_header = tk.Frame(delay_frame, bg='#e8f4fd')
        delay_header.pack(fill='x', padx=5, pady=3)
        
        self.delay_btn = tk.Button(delay_header, text="🎛️ Delay", 
                                 font=('Segoe UI', 9, 'bold'),
                                 bg='#95a5a6', fg='white',
                                 command=self.toggle_delay,
                                 width=10, height=1,
                                 relief='flat', bd=0,
                                 cursor='hand2',
                                 activebackground='#7f8c8d',
                                 activeforeground='white')
        self.delay_btn.pack(side='left')

        # Pulsante "Tipo" più piccolo alla destra di Delay
        self.delay_type_button = tk.Button(delay_header, text="Tipo",
                                          font=('Segoe UI', 8),
                                          bg='#3498db', fg='white',
                                          command=self.open_delay_type_dropdown,
                                          width=5, height=1,
                                          relief='flat', bd=0,
                                          cursor='hand2',
                                          activebackground='#2980b9',
                                          activeforeground='white')
        self.delay_type_button.pack(side='left', padx=(5,0))
        
        # Controlli delay con slider
        delay_controls = tk.Frame(delay_frame, bg='#e8f4fd')
        delay_controls.pack(fill='both', expand=True, padx=5, pady=(0, 5))

        def _create_slider(p, text, var, from_, to, is_int=False):
            slider_frame = tk.Frame(p, bg='#e8f4fd')
            slider_frame.pack(fill='x', expand=True, pady=1)
            
            label = tk.Label(slider_frame, text=text, font=('Segoe UI', 8), 
                             bg='#e8f4fd', fg='#2c3e50', width=8, anchor='w')
            label.pack(side='left')
            
            # Mostra il valore
            value_label = tk.Label(slider_frame, font=('Segoe UI', 8, 'bold'),
                                   bg='#e8f4fd', fg='#34495e', width=4)
            value_label.pack(side='right', padx=(2,0))

            def update_label(*_):
                if is_int:
                    value_label.config(text=f"{var.get()}")
                else:
                    value_label.config(text=f"{var.get():.2f}")
            var.trace_add('write', update_label)
            
            # Callback per aggiornare il valore e notificare il cambiamento
            def slider_callback(value):
                if is_int:
                    var.set(int(float(value)))
                else:
                    var.set(float(value))
                update_label()
                self.on_effect_change()

            slider = ttk.Scale(slider_frame, from_=from_, to=to,
                               orient='horizontal', variable=var,
                               command=slider_callback)
            slider.pack(side='right', fill='x', expand=True)
            update_label() # Set initial value

        _create_slider(delay_controls, "Mix", self.delay_mix_var, 0.0, 1.0)
        _create_slider(delay_controls, "Time", self.delay_time_var, 0.1, 2.0)
        _create_slider(delay_controls, "Feedback", self.delay_feedback_var, 0.0, 0.95)
        _create_slider(delay_controls, "Velocity", self.delay_velocity_var, 0.1, 1.0)
        _create_slider(delay_controls, "Repeats", self.delay_repeats_var, 1, 8, is_int=True)

        # Tipo di delay (dropdown)
        type_frame = tk.Frame(delay_controls, bg='#e8f4fd')
        type_frame.pack(fill='x', expand=True, pady=1)
        type_label = tk.Label(type_frame, text="Type", font=('Segoe UI', 8), 
                             bg='#e8f4fd', fg='#2c3e50', width=8, anchor='w')
        type_label.pack(side='left')
        
        self.type_combo = ttk.Combobox(type_frame, textvariable=self.delay_type_var,
                                      values=["Standard", "Ping-Pong", "Dotted", 
                                             "Triplet", "Reverse", "Stutter"],
                                      state="readonly", font=('Segoe UI', 8),
                                      width=12)
        self.type_combo.pack(side='right', fill='x', expand=True, padx=(5,0))
        self.type_combo.bind('<<ComboboxSelected>>', self.on_type_change)
        
        # Aggiungi un binding per il click diretto sul Combobox
        self.type_combo.bind('<Button-1>', self.on_combobox_click)
    
    def create_octave_controls_compact(self, parent, row, col):
        """Crea i controlli per l'aggiunta di ottave compatti"""
        # Sottoriquadro colorato per Octave
        octave_frame = tk.Frame(parent, bg='#f0f8ff', relief='solid', bd=1)
        octave_frame.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        
        # Header con pulsante di attivazione
        octave_header = tk.Frame(octave_frame, bg='#f0f8ff')
        octave_header.pack(fill='x', padx=5, pady=3)
        
        # Pulsante di attivazione octave (come loop/reverse)
        self.octave_btn = tk.Button(octave_header, text="Octave", 
                                  font=('Segoe UI', 8, 'bold'),
                                  bg='#95a5a6', fg='white',
                                  command=self.toggle_octave,
                                  width=8, height=1,
                                  relief='flat', bd=0,
                                  cursor='hand2',
                                  activebackground='#7f8c8d',
                                  activeforeground='white')
        self.octave_btn.pack(side='left')
        
        # Controlli ottava compatti
        octave_controls = tk.Frame(octave_frame, bg='#f0f8ff')
        octave_controls.pack(fill='x', padx=5, pady=(0, 5))
        
        # Pulsanti freccia per ottava
        octave_down = tk.Button(octave_controls, text="▼", 
                              font=('Segoe UI', 7, 'bold'),
                              bg='#9b59b6', fg='white',
                              command=self.decrease_octave_add,
                              width=2, height=1,
                              relief='flat', bd=0,
                              cursor='hand2',
                              activebackground='#8e44ad',
                              activeforeground='white')
        octave_down.pack(side='left', padx=(0, 1))
        
        self.octave_add_label = tk.Label(octave_controls, text="0", 
                                       font=('Segoe UI', 8, 'bold'), 
                                       bg='#9b59b6', fg='white',
                                       width=4, relief='flat')
        self.octave_add_label.pack(side='left', padx=(1, 1))
        
        octave_up = tk.Button(octave_controls, text="▲", 
                            font=('Segoe UI', 7, 'bold'),
                            bg='#9b59b6', fg='white',
                            command=self.increase_octave_add,
                            width=2, height=1,
                            relief='flat', bd=0,
                            cursor='hand2',
                            activebackground='#8e44ad',
                            activeforeground='white')
        octave_up.pack(side='left', padx=(1, 0))
        
        # Update label when value changes
        def update_octave_add_value(*_):
            val = self.octave_add_var.get()
            self.octave_add_label.config(text=f"{val:+d}")
        self.octave_add_var.trace('w', update_octave_add_value)
    
    def create_velocity_controls_compact(self, parent, row, col):
        """Crea i controlli per la curva di velocità compatti"""
        # Sottoriquadro colorato per Velocity
        velocity_frame = tk.Frame(parent, bg='#f0fff0', relief='solid', bd=1)
        velocity_frame.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        
        # Header con pulsante di attivazione
        velocity_header = tk.Frame(velocity_frame, bg='#f0fff0')
        velocity_header.pack(fill='x', padx=5, pady=3)
        
        # Pulsante di attivazione velocity (come loop/reverse)
        self.velocity_btn = tk.Button(velocity_header, text="Velocity", 
                                    font=('Segoe UI', 8, 'bold'),
                                    bg='#95a5a6', fg='white',
                                    command=self.toggle_velocity,
                                    width=8, height=1,
                                    relief='flat', bd=0,
                                    cursor='hand2',
                                    activebackground='#7f8c8d',
                                    activeforeground='white')
        self.velocity_btn.pack(side='left')
        
        # Controlli velocità compatti
        velocity_controls = tk.Frame(velocity_frame, bg='#f0fff0')
        velocity_controls.pack(fill='x', padx=5, pady=(0, 5))
        
        # Tipo di curva
        curve_frame = tk.Frame(velocity_controls, bg='#f0fff0')
        curve_frame.pack(side='left', fill='x', expand=True, padx=(0, 3))
        
        curve_label = tk.Label(curve_frame, text="Type", font=('Segoe UI', 7), 
                             bg='#f0fff0', fg='#7f8c8d')
        curve_label.pack(anchor='center')
        
        curve_dropdown = ttk.Combobox(curve_frame, 
                                    textvariable=self.velocity_curve_var,
                                    values=["linear", "exp", "log", "sine", "random"],
                                    state="readonly", width=8, font=('Segoe UI', 7))
        curve_dropdown.pack(fill='x')
        curve_dropdown.bind('<<ComboboxSelected>>', self.on_effect_change)
        
        # Intensità - knob style
        intensity_frame = tk.Frame(velocity_controls, bg='#f0fff0')
        intensity_frame.pack(side='left', fill='x', expand=True, padx=(3, 0))
        
        intensity_label = tk.Label(intensity_frame, text="Intensity", font=('Segoe UI', 7), 
                                 bg='#f0fff0', fg='#7f8c8d')
        intensity_label.pack(anchor='center')
        
        # Knob per intensità (0.1-2.0)
        intensity_knob_frame = tk.Frame(intensity_frame, bg='#f0fff0')
        intensity_knob_frame.pack(fill='x')
        
        intensity_down = tk.Button(intensity_knob_frame, text="◀", 
                                 font=('Segoe UI', 6, 'bold'),
                                 bg='#27ae60', fg='white',
                                 command=self.decrease_velocity_intensity,
                                 width=2, height=1,
                                 relief='flat', bd=0,
                                 cursor='hand2',
                                 activebackground='#229954',
                                 activeforeground='white')
        intensity_down.pack(side='left', padx=(0, 1))
        
        intensity_value = tk.Label(intensity_knob_frame, text="1.0", 
                                 font=('Segoe UI', 7, 'bold'), 
                                 bg='#27ae60', fg='white',
                                 width=6, relief='flat')
        intensity_value.pack(side='left', padx=(1, 1))
        
        intensity_up = tk.Button(intensity_knob_frame, text="▶", 
                               font=('Segoe UI', 6, 'bold'),
                               bg='#27ae60', fg='white',
                               command=self.increase_velocity_intensity,
                               width=2, height=1,
                               relief='flat', bd=0,
                               cursor='hand2',
                               activebackground='#229954',
                               activeforeground='white')
        intensity_up.pack(side='left', padx=(1, 0))
        
        # Update intensity label
        def update_intensity(*_):
            intensity_value.config(text=f"{self.velocity_intensity_var.get():.1f}")
        self.velocity_intensity_var.trace('w', update_intensity)
    
    def create_accent_controls_compact(self, parent, row, col):
        """Crea i controlli per i pattern di accento compatti"""
        # Sottoriquadro colorato per Accent
        accent_frame = tk.Frame(parent, bg='#fff5f5', relief='solid', bd=1)
        accent_frame.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        
        # Header con pulsante di attivazione
        accent_header = tk.Frame(accent_frame, bg='#fff5f5')
        accent_header.pack(fill='x', padx=5, pady=3)
        
        # Pulsante di attivazione accent (come loop/reverse)
        self.accent_btn = tk.Button(accent_header, text="Accent", 
                                  font=('Segoe UI', 8, 'bold'),
                                  bg='#95a5a6', fg='white',
                                  command=self.toggle_accent,
                                  width=8, height=1,
                                  relief='flat', bd=0,
                                  cursor='hand2',
                                  activebackground='#7f8c8d',
                                  activeforeground='white')
        self.accent_btn.pack(side='left')
        
        # Controlli accento compatti
        accent_controls = tk.Frame(accent_frame, bg='#fff5f5')
        accent_controls.pack(fill='x', padx=5, pady=(0, 5))
        
        # Pattern di accento
        pattern_frame = tk.Frame(accent_controls, bg='#fff5f5')
        pattern_frame.pack(side='left', fill='x', expand=True, padx=(0, 3))
        
        pattern_label = tk.Label(pattern_frame, text="Pattern", font=('Segoe UI', 7), 
                               bg='#fff5f5', fg='#7f8c8d')
        pattern_label.pack(anchor='center')
        
        pattern_dropdown = ttk.Combobox(pattern_frame, 
                                      textvariable=self.accent_pattern_var,
                                      values=["every_beat", "every_other", "random", "crescendo", "diminuendo"],
                                      state="readonly", width=8, font=('Segoe UI', 7))
        pattern_dropdown.pack(fill='x')
        pattern_dropdown.bind('<<ComboboxSelected>>', self.on_effect_change)
        
        # Forza accento - knob style
        strength_frame = tk.Frame(accent_controls, bg='#fff5f5')
        strength_frame.pack(side='left', fill='x', expand=True, padx=(3, 0))
        
        strength_label = tk.Label(strength_frame, text="Strength", font=('Segoe UI', 7), 
                                bg='#fff5f5', fg='#7f8c8d')
        strength_label.pack(anchor='center')
        
        # Knob per strength (0.1-1.0)
        strength_knob_frame = tk.Frame(strength_frame, bg='#fff5f5')
        strength_knob_frame.pack(fill='x')
        
        strength_down = tk.Button(strength_knob_frame, text="◀", 
                                font=('Segoe UI', 6, 'bold'),
                                bg='#e74c3c', fg='white',
                                command=self.decrease_accent_strength,
                                width=2, height=1,
                                relief='flat', bd=0,
                                cursor='hand2',
                                activebackground='#c0392b',
                                activeforeground='white')
        strength_down.pack(side='left', padx=(0, 1))
        
        strength_value = tk.Label(strength_knob_frame, text="0.5", 
                                font=('Segoe UI', 7, 'bold'), 
                                bg='#e74c3c', fg='white',
                                width=6, relief='flat')
        strength_value.pack(side='left', padx=(1, 1))
        
        strength_up = tk.Button(strength_knob_frame, text="▶", 
                              font=('Segoe UI', 6, 'bold'),
                              bg='#e74c3c', fg='white',
                              command=self.increase_accent_strength,
                              width=2, height=1,
                              relief='flat', bd=0,
                              cursor='hand2',
                              activebackground='#c0392b',
                              activeforeground='white')
        strength_up.pack(side='left', padx=(1, 0))
        
        # Update strength label
        def update_strength(*_):
            strength_value.config(text=f"{self.accent_strength_var.get():.1f}")
        self.accent_strength_var.trace('w', update_strength)
    
    def create_repeater_controls_compact(self, parent, row, col):
        """Crea i controlli per il ripetitore di note compatti"""
        # Sottoriquadro colorato per Repeater
        repeater_frame = tk.Frame(parent, bg='#fff8e1', relief='solid', bd=1)
        repeater_frame.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        
        # Header con pulsante di attivazione
        repeater_header = tk.Frame(repeater_frame, bg='#fff8e1')
        repeater_header.pack(fill='x', padx=5, pady=3)
        
        # Pulsante di attivazione repeater (come loop/reverse)
        self.repeater_btn = tk.Button(repeater_header, text="Repeater", 
                                    font=('Segoe UI', 8, 'bold'),
                                    bg='#95a5a6', fg='white',
                                    command=self.toggle_repeater,
                                    width=8, height=1,
                                    relief='flat', bd=0,
                                    cursor='hand2',
                                    activebackground='#7f8c8d',
                                    activeforeground='white')
        self.repeater_btn.pack(side='left')
        
        # Controlli repeater compatti
        repeater_controls = tk.Frame(repeater_frame, bg='#fff8e1')
        repeater_controls.pack(fill='x', padx=5, pady=(0, 5))
        
        # Numero di ripetizioni - arrow buttons
        count_frame = tk.Frame(repeater_controls, bg='#fff8e1')
        count_frame.pack(side='left', fill='x', expand=True, padx=(0, 3))
        
        count_label = tk.Label(count_frame, text="Count", font=('Segoe UI', 7), 
                             bg='#fff8e1', fg='#7f8c8d')
        count_label.pack(anchor='center')
        
        # Arrow buttons per count (1-8)
        count_knob_frame = tk.Frame(count_frame, bg='#fff8e1')
        count_knob_frame.pack(fill='x')
        
        count_down = tk.Button(count_knob_frame, text="◀", 
                             font=('Segoe UI', 6, 'bold'),
                             bg='#f39c12', fg='white',
                             command=self.decrease_repeat_count,
                             width=2, height=1,
                             relief='flat', bd=0,
                             cursor='hand2',
                             activebackground='#e67e22',
                             activeforeground='white')
        count_down.pack(side='left', padx=(0, 1))
        
        count_value = tk.Label(count_knob_frame, text="2", 
                             font=('Segoe UI', 7, 'bold'), 
                             bg='#f39c12', fg='white',
                             width=6, relief='flat')
        count_value.pack(side='left', padx=(1, 1))
        
        count_up = tk.Button(count_knob_frame, text="▶", 
                           font=('Segoe UI', 6, 'bold'),
                           bg='#f39c12', fg='white',
                           command=self.increase_repeat_count,
                           width=2, height=1,
                           relief='flat', bd=0,
                           cursor='hand2',
                           activebackground='#e67e22',
                           activeforeground='white')
        count_up.pack(side='left', padx=(1, 0))
        
        # Timing
        timing_frame = tk.Frame(repeater_controls, bg='#fff8e1')
        timing_frame.pack(side='left', fill='x', expand=True, padx=(3, 0))
        
        timing_label = tk.Label(timing_frame, text="Timing", font=('Segoe UI', 7), 
                              bg='#fff8e1', fg='#7f8c8d')
        timing_label.pack(anchor='center')
        
        timing_dropdown = ttk.Combobox(timing_frame, 
                                     textvariable=self.repeat_timing_var,
                                     values=["immediate", "staccato", "legato", "swing"],
                                     state="readonly", width=8, font=('Segoe UI', 7))
        timing_dropdown.pack(fill='x')
        timing_dropdown.bind('<<ComboboxSelected>>', self.on_effect_change)
        
        # Update count label
        def update_count(*_):
            count_value.config(text=str(self.repeat_count_var.get()))
        self.repeat_count_var.trace('w', update_count)
    
    def create_chord_gen_controls_compact(self, parent, row, col):
        """Crea i controlli per il generatore di accordi compatti"""
        # Sottoriquadro colorato per Chord Generator
        chord_gen_frame = tk.Frame(parent, bg='#f3e5f5', relief='solid', bd=1)
        chord_gen_frame.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        
        # Header con pulsante di attivazione
        chord_gen_header = tk.Frame(chord_gen_frame, bg='#f3e5f5')
        chord_gen_header.pack(fill='x', padx=5, pady=3)
        
        # Pulsante di attivazione chord generator (come loop/reverse)
        self.chord_gen_btn = tk.Button(chord_gen_header, text="Chord Gen", 
                                     font=('Segoe UI', 8, 'bold'),
                                     bg='#95a5a6', fg='white',
                                     command=self.toggle_chord_gen,
                                     width=8, height=1,
                                     relief='flat', bd=0,
                                     cursor='hand2',
                                     activebackground='#7f8c8d',
                                     activeforeground='white')
        self.chord_gen_btn.pack(side='left')
        
        # Controlli chord generator compatti
        chord_gen_controls = tk.Frame(chord_gen_frame, bg='#f3e5f5')
        chord_gen_controls.pack(fill='x', padx=5, pady=(0, 5))
        
        # Variazione accordo
        variation_frame = tk.Frame(chord_gen_controls, bg='#f3e5f5')
        variation_frame.pack(side='left', fill='x', expand=True, padx=(0, 3))
        
        variation_label = tk.Label(variation_frame, text="Variation", font=('Segoe UI', 7), 
                                 bg='#f3e5f5', fg='#7f8c8d')
        variation_label.pack(anchor='center')
        
        variation_dropdown = ttk.Combobox(variation_frame, 
                                        textvariable=self.chord_variation_var,
                                        values=["inversion", "extension", "substitution", "voicing"],
                                        state="readonly", width=8, font=('Segoe UI', 7))
        variation_dropdown.pack(fill='x')
        variation_dropdown.bind('<<ComboboxSelected>>', self.on_effect_change)
        
        # Voicing
        voicing_frame = tk.Frame(chord_gen_controls, bg='#f3e5f5')
        voicing_frame.pack(side='left', fill='x', expand=True, padx=(3, 0))
        
        voicing_label = tk.Label(voicing_frame, text="Voicing", font=('Segoe UI', 7), 
                               bg='#f3e5f5', fg='#7f8c8d')
        voicing_label.pack(anchor='center')
        
        voicing_dropdown = ttk.Combobox(voicing_frame, 
                                      textvariable=self.voicing_var,
                                      values=["close", "open", "drop2", "drop3", "spread"],
                                      state="readonly", width=8, font=('Segoe UI', 7))
        voicing_dropdown.pack(fill='x')
        voicing_dropdown.bind('<<ComboboxSelected>>', self.on_effect_change)
    
    def create_pattern_controls_compact(self, parent):
        """Crea i controlli pattern in formato compatto con tooltip"""
        pattern_frame = ttk.LabelFrame(parent, text="🎯 Pattern Selection", 
                                      style='Modern.TLabelframe', padding="15")
        pattern_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Pattern categories in a grid layout
        categories = [
            ("Base", [
                ("Up", "up", "Ascendente semplice"),
                ("Down", "down", "Discendente semplice"),
                ("Up-Down", "up_down", "Su poi giù"),
                ("Down-Up", "down_up", "Giù poi su")
            ]),
            ("Geometric", [
                ("Triangle", "triangle", "Triangolo melodico"),
                ("Diamond", "diamond", "Dentro-fuori-dentro"),
                ("Zigzag", "zigzag", "Alternanza estremi-centro"),
                ("Spiral", "spiral", "Giri concentrici")
            ]),
            ("Rhythmic", [
                ("Gallop", "gallop", "Due veloci + una lunga"),
                ("Triplet", "triplet", "Gruppetti di tre"),
                ("Syncopated", "syncopated", "Enfasi tempi deboli"),
                ("Stutter", "stutter", "Ripetizione rapida")
            ]),
            ("Advanced", [
                ("Skip", "skip", "Salta note casualmente"),
                ("Ghost", "ghost", "Note fantasma"),
                ("Cascade", "cascade", "Effetto cascata"),
                ("Bounce", "bounce", "Rimbalza tra estremi")
            ]),
            ("Expressive", [
                ("Crescendo", "crescendo", "Volume crescente"),
                ("Diminuendo", "diminuendo", "Volume decrescente"),
                ("Accent First", "accent_first", "Prima nota accentata"),
                ("Swing", "swing", "Timing swing")
            ]),
            ("Random", [
                ("Chaos", "random_chaos", "Caos totale - tutto casuale"),
                ("Random Rhythm", "random_rhythm", "Ritmo imprevedibile"),
                ("Random Volume", "random_volume", "Volumi drammatici"),
                ("Changing", "random_changing", "Note che cambiano continuamente")
            ]),
            ("Pause", [
                ("None", "none", "Nessuna pausa tra i loop (0.0s)"),
                ("0.1s", "0.1s", "Pausa 0.1 secondi"),
                ("0.25s", "0.25s", "Pausa 0.25 secondi"),
                ("0.5s", "0.5s", "Pausa 0.5 secondi"),
                ("1.0s", "1.0s", "Pausa 1.0 secondi"),
                ("1.5s", "1.5s", "Pausa 1.5 secondi"),
                ("2.0s", "2.0s", "Pausa 2.0 secondi"),
                ("3.0s", "3.0s", "Pausa 3.0 secondi")
            ])
        ]
        
        # Create grid layout for patterns
        for cat_idx, (cat_name, patterns) in enumerate(categories):
            # Category label
            cat_label = tk.Label(pattern_frame, text=f"📁 {cat_name}", 
                               font=('Segoe UI', 9, 'bold'), 
                               bg='#f8f9fa', fg='#34495e')
            cat_label.grid(row=cat_idx*2, column=0, sticky='w', pady=(5, 2), padx=(0, 10))
            
            # Special handling for Pause category (2 rows)
            if cat_name == "Pause":
                # First row of pause buttons (4 buttons)
                for pat_idx, (name, value, desc) in enumerate(patterns[:4]):
                    btn = tk.Button(pattern_frame, text=name, 
                                  font=('Segoe UI', 8),
                                  bg='#ecf0f1', fg='#2c3e50',
                                  relief='flat', bd=1,
                                  command=lambda v=value: self.select_pattern(v),
                                  cursor='hand2',
                                  activebackground='#3498db',
                                  activeforeground='white')
                    btn.grid(row=cat_idx*2, column=pat_idx+1, padx=2, pady=2, sticky='ew')
                    
                    # Salva il riferimento al pulsante per l'evidenziazione
                    self.pattern_buttons[value] = btn
                    
                    # Tooltip for description
                    self.create_tooltip(btn, desc)
                
                # Second row of pause buttons (4 buttons)
                for pat_idx, (name, value, desc) in enumerate(patterns[4:]):
                    btn = tk.Button(pattern_frame, text=name, 
                                  font=('Segoe UI', 8),
                                  bg='#ecf0f1', fg='#2c3e50',
                                  relief='flat', bd=1,
                                  command=lambda v=value: self.select_pattern(v),
                                  cursor='hand2',
                                  activebackground='#3498db',
                                  activeforeground='white')
                    btn.grid(row=cat_idx*2+1, column=pat_idx+1, padx=2, pady=2, sticky='ew')
                    
                    # Salva il riferimento al pulsante per l'evidenziazione
                    self.pattern_buttons[value] = btn
                    
                    # Tooltip for description
                    self.create_tooltip(btn, desc)
            else:
                # Pattern buttons for other categories (single row)
                for pat_idx, (name, value, desc) in enumerate(patterns):
                    btn = tk.Button(pattern_frame, text=name, 
                                  font=('Segoe UI', 8),
                                  bg='#ecf0f1', fg='#2c3e50',
                                  relief='flat', bd=1,
                                  command=lambda v=value: self.select_pattern(v),
                                  cursor='hand2',
                                  activebackground='#3498db',
                                  activeforeground='white')
                    btn.grid(row=cat_idx*2, column=pat_idx+1, padx=2, pady=2, sticky='ew')
                    
                    # Salva il riferimento al pulsante per l'evidenziazione
                    self.pattern_buttons[value] = btn
                    
                    # Tooltip for description
                    self.create_tooltip(btn, desc)
        
        # Configure grid weights
        for i in range(1, 5):  # 4 pattern columns per riga (massimo 4 pulsanti per riga)
            pattern_frame.grid_columnconfigure(i, weight=1)
    
    def create_tooltip(self, widget, text):
        """Crea un tooltip per un widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, 
                           font=('Segoe UI', 8),
                           bg='#2c3e50', fg='white',
                           relief='solid', bd=1,
                           padx=5, pady=3)
            label.pack()
            widget.tooltip = tooltip
        
        def on_leave(_):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
    
    def select_pattern(self, pattern_value):
        """Seleziona un pattern"""
        # Se è una selezione di pause, gestiscila separatamente
        if pattern_value in ["none", "0.1s", "0.25s", "0.5s", "1.0s", "1.5s", "2.0s", "3.0s"]:
            self.pause_duration_var.set(pattern_value)
            self.highlight_selected_pause(pattern_value)
            self.update_parameters_realtime()
        else:
            self.selected_pattern.set(pattern_value)
            self.highlight_selected_pattern(pattern_value)
            self.on_pattern_change()
            self.update_parameters_realtime()
    
    def highlight_selected_pattern(self, selected_value):
        """Evidenzia il pattern selezionato con colore blu trasparente"""
        # Reset solo i pulsanti dei pattern (non le pause)
        pause_values = ["none", "0.1s", "0.25s", "0.5s", "1.0s", "1.5s", "2.0s", "3.0s"]
        for value, btn in self.pattern_buttons.items():
            if value not in pause_values:  # Solo pattern, non pause
                btn.config(bg='#ecf0f1', fg='#2c3e50')
        
        # Evidenzia il pattern selezionato
        if selected_value in self.pattern_buttons:
            selected_btn = self.pattern_buttons[selected_value]
            selected_btn.config(bg='#3498db', fg='white')
    
    def highlight_selected_pause(self, selected_value):
        """Evidenzia la pausa selezionata con colore blu trasparente"""
        # Reset solo i pulsanti delle pause (non i pattern)
        pause_values = ["none", "0.1s", "0.25s", "0.5s", "1.0s", "1.5s", "2.0s", "3.0s"]
        for value, btn in self.pattern_buttons.items():
            if value in pause_values:  # Solo pause, non pattern
                btn.config(bg='#ecf0f1', fg='#2c3e50')
        
        # Evidenzia la pausa selezionata
        if selected_value in self.pattern_buttons:
            selected_btn = self.pattern_buttons[selected_value]
            selected_btn.config(bg='#3498db', fg='white')
    
    
    def setup_keyboard_shortcuts(self):
        """Configura le scorciatoie da tastiera"""
        self.window.bind('<space>', lambda e: self.toggle_playback())
        self.window.bind('<Escape>', lambda e: self.stop_pattern())
        self.window.bind('<Return>', lambda e: self.play_pattern())
        self.window.bind('<Control-l>', lambda e: self.toggle_loop())
        
        # Focus sulla finestra per ricevere i tasti
        self.window.focus_set()
    
    def toggle_playback(self):
        """Toggle tra play e stop"""
        if self.is_playing:
            self.stop_pattern()
        else:
            self.play_pattern()
    
    def toggle_loop(self):
        """Toggle del loop"""
        self.loop_var.set(not self.loop_var.get())
        if self.loop_var.get():
            self.loop_btn.config(bg='#3498db', fg='white')
        else:
            self.loop_btn.config(bg='#95a5a6', fg='white')
        self.update_pause_controls_state()
        self.update_parameters_realtime()
    
    def toggle_reverse(self):
        """Toggle del reverse"""
        self.reverse_var.set(not self.reverse_var.get())
        if self.reverse_var.get():
            self.reverse_btn.config(bg='#e67e22', fg='white')
        else:
            self.reverse_btn.config(bg='#95a5a6', fg='white')
        self.update_parameters_realtime()
    
    def increase_playback_speed(self):
        """Aumenta la velocità di riproduzione"""
        current = self.playback_speed_var.get()
        if current < 4.0:
            # Incrementi di 0.25x
            new_speed = min(4.0, current + 0.25)
            self.playback_speed_var.set(new_speed)
            self.update_speed_display()
            self.update_parameters_realtime()
    
    def decrease_playback_speed(self):
        """Diminuisce la velocità di riproduzione"""
        current = self.playback_speed_var.get()
        if current > 0.25:
            # Decrementi di 0.25x
            new_speed = max(0.25, current - 0.25)
            self.playback_speed_var.set(new_speed)
            self.update_speed_display()
            self.update_parameters_realtime()
    
    def update_speed_display(self):
        """Aggiorna la visualizzazione della velocità"""
        speed = self.playback_speed_var.get()
        self.playback_speed_label.config(text=f"{speed:.2f}x")
    
    def increase_bpm(self):
        """Aumenta il BPM"""
        current = self.bpm_var.get()
        if current < 200:
            self.bpm_var.set(current + 1)
            self.update_bpm_display()
            self.update_parameters_realtime()
    
    def decrease_bpm(self):
        """Diminuisce il BPM"""
        current = self.bpm_var.get()
        if current > 60:
            self.bpm_var.set(current - 1)
            self.update_bpm_display()
            self.update_parameters_realtime()
    
    def update_bpm_display(self):
        """Aggiorna la visualizzazione del BPM"""
        bpm = self.bpm_var.get()
        self.bpm_label.config(text=str(bpm))
    
    def on_bpm_double_click(self, event):
        """Gestisce il doppio click sul label BPM per inserimento manuale"""
        del event  # Ignora il parametro event non utilizzato
        # Crea una finestra di dialogo per inserire il BPM
        dialog = tk.Toplevel(self.window)
        dialog.title("Inserisci BPM")
        dialog.geometry("300x150")
        dialog.configure(bg='#f8f9fa')
        dialog.resizable(False, False)
        
        # Centra la finestra
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Frame principale
        main_frame = tk.Frame(dialog, bg='#f8f9fa', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Label di istruzione
        instruction_label = tk.Label(main_frame, 
                                   text="Inserisci il nuovo BPM (60-200):", 
                                   font=('Segoe UI', 10, 'bold'),
                                   bg='#f8f9fa', fg='#2c3e50')
        instruction_label.pack(pady=(0, 10))
        
        # Entry per il BPM
        bpm_entry = tk.Entry(main_frame, 
                            font=('Segoe UI', 12),
                            width=10,
                            justify='center',
                            relief='solid',
                            bd=1)
        bpm_entry.pack(pady=(0, 20))
        bpm_entry.insert(0, str(self.bpm_var.get()))
        bpm_entry.select_range(0, tk.END)
        bpm_entry.focus()
        
        # Frame per i bottoni
        button_frame = tk.Frame(main_frame, bg='#f8f9fa')
        button_frame.pack()
        
        def apply_bpm():
            try:
                new_bpm = int(bpm_entry.get())
                if 60 <= new_bpm <= 200:
                    self.bpm_var.set(new_bpm)
                    self.update_bpm_display()
                    self.update_parameters_realtime()
                    dialog.destroy()
                else:
                    # Mostra errore se BPM fuori range
                    error_label = tk.Label(main_frame, 
                                         text="BPM deve essere tra 60 e 200!",
                                         font=('Segoe UI', 9),
                                         fg='#e74c3c', bg='#f8f9fa')
                    error_label.pack(pady=(5, 0))
            except ValueError:
                # Mostra errore se non è un numero
                error_label = tk.Label(main_frame, 
                                     text="Inserisci un numero valido!",
                                     font=('Segoe UI', 9),
                                     fg='#e74c3c', bg='#f8f9fa')
                error_label.pack(pady=(5, 0))
        
        def cancel_bpm():
            dialog.destroy()
        
        # Bottoni
        apply_btn = tk.Button(button_frame, text="Applica", 
                             font=('Segoe UI', 9, 'bold'),
                             bg='#27ae60', fg='white',
                             command=apply_bpm,
                             width=8, height=1,
                             relief='flat', bd=0,
                             cursor='hand2',
                             activebackground='#229954',
                             activeforeground='white')
        apply_btn.pack(side='left', padx=(0, 10))
        
        cancel_btn = tk.Button(button_frame, text="Annulla", 
                              font=('Segoe UI', 9, 'bold'),
                              bg='#95a5a6', fg='white',
                              command=cancel_bpm,
                              width=8, height=1,
                              relief='flat', bd=0,
                              cursor='hand2',
                              activebackground='#7f8c8d',
                              activeforeground='white')
        cancel_btn.pack(side='left')
        
        # Binding per Enter e Escape
        bpm_entry.bind('<Return>', lambda e: apply_bpm())
        dialog.bind('<Escape>', lambda e: cancel_bpm())
    
    def increase_start_octave(self):
        """Aumenta l'ottava di partenza"""
        current = self.start_octave_var.get()
        if current < 6:
            self.start_octave_var.set(current + 1)
            self.update_parameters_realtime()
    
    def decrease_start_octave(self):
        """Diminuisce l'ottava di partenza"""
        current = self.start_octave_var.get()
        if current > 2:
            self.start_octave_var.set(current - 1)
            self.update_parameters_realtime()
    
    def increase_duration_octaves(self):
        """Aumenta le ottave di durata"""
        current = self.duration_octaves_var.get()
        if current < 7:  # Aumentato da 3 a 5 ottave
            self.duration_octaves_var.set(current + 1)
            self.update_parameters_realtime()
    
    def decrease_duration_octaves(self):
        """Diminuisce le ottave di durata"""
        current = self.duration_octaves_var.get()
        if current > 1:
            self.duration_octaves_var.set(current - 1)
            self.update_parameters_realtime()
    
    def on_note_duration_change(self, event=None):
        """Gestisce il cambio di durata nota"""
        del event  # Ignora il parametro event non utilizzato
        duration = self.note_duration_var.get()
        self.log_message(f"Note duration changed to: {duration}")
        self.update_parameters_realtime()
    
    def increase_octave_add(self):
        """Aumenta l'ottava da aggiungere"""
        current = self.octave_add_var.get()
        if current < 3:
            self.octave_add_var.set(current + 1)
            self.on_effect_change()
    
    def decrease_octave_add(self):
        """Diminuisce l'ottava da aggiungere"""
        current = self.octave_add_var.get()
        if current > -3:
            self.octave_add_var.set(current - 1)
            self.on_effect_change()
    
    def on_effect_change(self, event=None):
        """Gestisce il cambio di effetti MIDI"""
        del event  # Ignora il parametro event non utilizzato
        self.log_message("MIDI effects changed")
        self.update_parameters_realtime()
    
    # Metodi per i controlli knob compatti
    
    def on_type_change(self, event=None):
        """Callback per il tipo di delay"""
        del event  # Ignora il parametro event non utilizzato
        self.on_effect_change()
    
    def increase_delay_time(self):
        """Aumenta il tempo di delay"""
        current = self.delay_time_var.get()
        if current < 2.0:
            self.delay_time_var.set(min(2.0, current + 0.1))
            self.on_effect_change()
    
    def decrease_delay_time(self):
        """Diminuisce il tempo di delay"""
        current = self.delay_time_var.get()
        if current > 0.1:
            self.delay_time_var.set(max(0.1, current - 0.1))
            self.on_effect_change()
    
    def increase_delay_feedback(self):
        """Aumenta il feedback del delay"""
        current = self.delay_feedback_var.get()
        if current < 0.9:
            self.delay_feedback_var.set(min(0.9, current + 0.1))
            self.on_effect_change()
    
    def decrease_delay_feedback(self):
        """Diminuisce il feedback del delay"""
        current = self.delay_feedback_var.get()
        if current > 0.0:
            self.delay_feedback_var.set(max(0.0, current - 0.1))
            self.on_effect_change()
    
    def increase_velocity_intensity(self):
        """Aumenta l'intensità della velocità"""
        current = self.velocity_intensity_var.get()
        if current < 2.0:
            self.velocity_intensity_var.set(min(2.0, current + 0.1))
            self.on_effect_change()
    
    def decrease_velocity_intensity(self):
        """Diminuisce l'intensità della velocità"""
        current = self.velocity_intensity_var.get()
        if current > 0.1:
            self.velocity_intensity_var.set(max(0.1, current - 0.1))
            self.on_effect_change()
    
    def increase_accent_strength(self):
        """Aumenta la forza dell'accento"""
        current = self.accent_strength_var.get()
        if current < 1.0:
            self.accent_strength_var.set(min(1.0, current + 0.1))
            self.on_effect_change()
    
    def decrease_accent_strength(self):
        """Diminuisce la forza dell'accento"""
        current = self.accent_strength_var.get()
        if current > 0.1:
            self.accent_strength_var.set(max(0.1, current - 0.1))
            self.on_effect_change()
    
    def increase_repeat_count(self):
        """Aumenta il numero di ripetizioni"""
        current = self.repeat_count_var.get()
        if current < 8:
            self.repeat_count_var.set(current + 1)
            self.on_effect_change()
    
    def decrease_repeat_count(self):
        """Diminuisce il numero di ripetizioni"""
        current = self.repeat_count_var.get()
        if current > 1:
            self.repeat_count_var.set(current - 1)
            self.on_effect_change()
    
    # Metodi toggle per i pulsanti di attivazione effetti
    def toggle_delay(self):
        """Toggle del delay"""
        self.delay_enabled_var.set(not self.delay_enabled_var.get())
        if self.delay_enabled_var.get():
            self.delay_btn.config(bg='#3498db', fg='white')
            self.delay_type_button.config(bg='#3498db', fg='white')
        else:
            self.delay_btn.config(bg='#95a5a6', fg='white')
            self.delay_type_button.config(bg='#95a5a6', fg='white')
        self.on_effect_change()
    
    def open_delay_type_dropdown(self):
        """Apre il dropdown del tipo di delay usando un menu popup personalizzato"""
        try:
            # Crea un menu popup personalizzato
            delay_types = ["Standard", "Ping-Pong", "Dotted", "Triplet", "Reverse", "Stutter"]
            current_type = self.delay_type_var.get()
            
            # Ottieni la posizione del pulsante "Tipo"
            button_x = self.delay_type_button.winfo_rootx()
            button_y = self.delay_type_button.winfo_rooty() + self.delay_type_button.winfo_height()
            
            # Crea il menu popup
            popup_menu = tk.Menu(self.window, tearoff=0, font=('Segoe UI', 9))
            
            # Aggiungi le opzioni al menu con evidenziazione per quella selezionata
            for delay_type in delay_types:
                if delay_type == current_type:
                    # Evidenzia l'opzione attualmente selezionata
                    popup_menu.add_command(
                        label=f"✓ {delay_type}",
                        command=lambda dt=delay_type: self.select_delay_type(dt),
                        background='#e3f2fd',
                        foreground='#1976d2',
                        font=('Segoe UI', 9, 'bold')
                    )
                else:
                    popup_menu.add_command(
                        label=delay_type,
                        command=lambda dt=delay_type: self.select_delay_type(dt)
                    )
            
            # Mostra il menu
            popup_menu.tk_popup(button_x, button_y)
            
        except Exception as e:
            print(f"Errore nell'apertura del menu: {e}")
    
    def select_delay_type(self, delay_type):
        """Seleziona un tipo di delay dal menu popup"""
        try:
            self.delay_type_var.set(delay_type)
            self.on_type_change()
        except Exception as e:
            print(f"Errore nella selezione del tipo: {e}")
    
    def on_combobox_click(self, event):
        """Gestisce il click diretto sul Combobox"""
        try:
            # Forza l'apertura del dropdown
            self.type_combo.event_generate('<Down>')
        except Exception as e:
            print(f"Errore nell'apertura del Combobox: {e}")
    
    def toggle_octave(self):
        """Toggle dell'ottava"""
        # Toggle tra 0 e 1 per l'ottava
        if self.octave_add_var.get() == 0:
            self.octave_add_var.set(1)
            self.octave_btn.config(bg='#9b59b6', fg='white')
        else:
            self.octave_add_var.set(0)
            self.octave_btn.config(bg='#95a5a6', fg='white')
        self.on_effect_change()
    
    def toggle_velocity(self):
        """Toggle della velocity curve"""
        # Toggle tra linear e exponential per la velocity
        if self.velocity_curve_var.get() == "linear":
            self.velocity_curve_var.set("exponential")
            self.velocity_btn.config(bg='#27ae60', fg='white')
        else:
            self.velocity_curve_var.set("linear")
            self.velocity_btn.config(bg='#95a5a6', fg='white')
        self.on_effect_change()
    
    def toggle_accent(self):
        """Toggle dell'accento"""
        self.accent_enabled_var.set(not self.accent_enabled_var.get())
        if self.accent_enabled_var.get():
            self.accent_btn.config(bg='#e74c3c', fg='white')
        else:
            self.accent_btn.config(bg='#95a5a6', fg='white')
        self.on_effect_change()
    
    def toggle_repeater(self):
        """Toggle del repeater"""
        self.repeater_enabled_var.set(not self.repeater_enabled_var.get())
        if self.repeater_enabled_var.get():
            self.repeater_btn.config(bg='#f39c12', fg='white')
        else:
            self.repeater_btn.config(bg='#95a5a6', fg='white')
        self.on_effect_change()
    
    def toggle_chord_gen(self):
        """Toggle del chord generator"""
        self.chord_gen_enabled_var.set(not self.chord_gen_enabled_var.get())
        if self.chord_gen_enabled_var.get():
            self.chord_gen_btn.config(bg='#9b59b6', fg='white')
        else:
            self.chord_gen_btn.config(bg='#95a5a6', fg='white')
        self.on_effect_change()
    
    
    def update_parameters_realtime(self):
        """Aggiorna i parametri in tempo reale durante la riproduzione"""
        if self.is_playing:
            try:
                # Converte il pattern selezionato in PatternType
                pattern_type = PatternType(self.selected_pattern.get())
                
                # Aggiorna i parametri nel pattern engine
                self.pattern_engine.update_parameters(
                    sound_cell=self.sound_cell,
                    pattern_type=pattern_type,
                    octave=self.start_octave_var.get(),
                    base_duration=self.get_note_duration_seconds(),
                    loop=self.loop_var.get(),
                    reverse=self.reverse_var.get(),
                    duration_octaves=self.duration_octaves_var.get(),
                    playback_speed=self.playback_speed_var.get(),
                    bpm=self.bpm_var.get(),
                    pause_duration=self.get_pause_duration_seconds(),
                    # MIDI Effects
                    delay_enabled=self.delay_enabled_var.get(),
                    delay_time=self.delay_time_var.get(),
                    delay_feedback=self.delay_feedback_var.get(),
                    delay_mix=self.delay_mix_var.get(),
                    delay_type=self.delay_type_var.get(),
                    delay_velocity=self.delay_velocity_var.get(),
                    delay_repeats=self.delay_repeats_var.get(),
                    octave_add=self.octave_add_var.get(),
                    velocity_curve=self.velocity_curve_var.get(),
                    velocity_intensity=self.velocity_intensity_var.get(),
                    accent_enabled=self.accent_enabled_var.get(),
                    accent_strength=self.accent_strength_var.get(),
                    accent_pattern=self.accent_pattern_var.get(),
                    repeater_enabled=self.repeater_enabled_var.get(),
                    repeat_count=self.repeat_count_var.get(),
                    repeat_timing=self.repeat_timing_var.get(),
                    chord_gen_enabled=self.chord_gen_enabled_var.get(),
                    chord_variation=self.chord_variation_var.get(),
                    voicing=self.voicing_var.get()
                )
                
                self.log_message("Parameters updated in real-time")
            except (ValueError, RuntimeError) as e:
                self.log_message(f"Error updating parameters: {str(e)}")
    
    def change_chord(self, new_sound_cell: SoundCell):
        """Cambia l'accordo durante la riproduzione"""
        self.sound_cell = new_sound_cell
        
        # Aggiorna le informazioni dell'accordo nell'interfaccia
        self.update_chord_info()
        
        # Se sta riproducendo, aggiorna i parametri in tempo reale
        if self.is_playing:
            # Il MIDI viene ora inviato automaticamente dal pattern engine per ogni nota dell'arpeggio
            self.update_parameters_realtime()
            self.log_message(f"Chord changed to: {new_sound_cell.__str__()}")
    
    def update_chord_info(self):
        """Aggiorna le informazioni dell'accordo nell'interfaccia"""
        # Trova e aggiorna i label delle informazioni accordo
        for widget in self.window.winfo_children():
            self._update_chord_info_recursive(widget)
    
    def _update_chord_info_recursive(self, widget):
        """Aggiorna ricorsivamente le informazioni dell'accordo"""
        try:
            if hasattr(widget, 'cget') and widget.cget('text'):
                text = widget.cget('text')
                if text.startswith('Chord: '):
                    widget.config(text=f"Chord: {self.sound_cell.__str__()}")
                elif text.startswith('Intervals: '):
                    widget.config(text=f"Intervals: {self.sound_cell.to_intervals_string()}")
        except (AttributeError, tk.TclError):
            pass
        
        # Continua ricorsivamente per i widget figli
        try:
            for child in widget.winfo_children():
                self._update_chord_info_recursive(child)
        except (AttributeError, tk.TclError):
            pass
    
    def get_note_duration_seconds(self):
        """Converte la durata nota in secondi considerando il BPM"""
        # Durata base in secondi per ogni tipo di nota (a 120 BPM)
        duration_map = {
            "Whole": 2.0,      # 4 beats
            "Half": 1.0,       # 2 beats
            "Quarter": 0.5,    # 1 beat
            "Eighth": 0.25,    # 0.5 beats
            "Sixteenth": 0.125, # 0.25 beats
            "Thirty-Second": 0.0625 # 0.125 beats
        }
        
        # Durata base per il tipo di nota selezionato
        base_duration = duration_map.get(self.note_duration_var.get(), 0.5)
        
        # Applica il BPM (120 BPM è il riferimento)
        bpm = self.bpm_var.get()
        bpm_factor = 120.0 / bpm
        
        return base_duration * bpm_factor
    
    def get_pause_duration_seconds(self):
        """Converte la durata pausa in secondi"""
        pause_duration_map = {
            "none": 0.0,
            "0.1s": 0.1,
            "0.25s": 0.25,
            "0.5s": 0.5,
            "1.0s": 1.0,
            "1.5s": 1.5,
            "2.0s": 2.0,
            "3.0s": 3.0
        }
        return pause_duration_map.get(self.pause_duration_var.get(), 0.0)
    
    def on_pattern_change(self):
        """Gestisce il cambio di pattern"""
        pattern_name = self.selected_pattern.get()
        self.log_message(f"Pattern changed to: {pattern_name}")
        self.update_controls()
    
    def play_pattern(self):
        """Avvia la riproduzione del pattern"""
        if self.is_playing:
            self.log_message("Already playing. Stop first to change pattern.")
            return
        
        try:
            # Converte il pattern selezionato in PatternType
            pattern_type = PatternType(self.selected_pattern.get())
            
            # Avvia la riproduzione
            self.is_playing = True
            self.update_controls()
            
            self.log_message(f"Playing pattern: {pattern_type.value}")
            self.log_message(f"Start Octave: {self.start_octave_var.get()}, Duration Octaves: {self.duration_octaves_var.get()}")
            self.log_message(f"Note Duration: {self.note_duration_var.get()}")
            if self.loop_var.get():
                self.log_message("Loop mode: ON")
            if self.reverse_var.get():
                self.log_message("Reverse mode: ON")
            
            # Il MIDI viene ora inviato automaticamente dal pattern engine per ogni nota dell'arpeggio
            # Avvia la riproduzione in un thread separato
            self.pattern_engine.play_pattern(
                self.sound_cell,
                pattern_type,
                self.start_octave_var.get(),
                self.get_note_duration_seconds(),
                self.loop_var.get(),
                self.reverse_var.get(),
                self.duration_octaves_var.get(),
                self.playback_speed_var.get(),
                self.bpm_var.get(),
                self.get_pause_duration_seconds(),
                self.on_playback_finished,
                # MIDI Effects
                delay_enabled=self.delay_enabled_var.get(),
                delay_time=self.delay_time_var.get(),
                delay_feedback=self.delay_feedback_var.get(),
                delay_mix=self.delay_mix_var.get(),
                delay_type=self.delay_type_var.get(),
                delay_velocity=self.delay_velocity_var.get(),
                delay_repeats=self.delay_repeats_var.get(),
                octave_add=self.octave_add_var.get(),
                velocity_curve=self.velocity_curve_var.get(),
                velocity_intensity=self.velocity_intensity_var.get(),
                accent_enabled=self.accent_enabled_var.get(),
                accent_strength=self.accent_strength_var.get(),
                accent_pattern=self.accent_pattern_var.get(),
                repeater_enabled=self.repeater_enabled_var.get(),
                repeat_count=self.repeat_count_var.get(),
                repeat_timing=self.repeat_timing_var.get(),
                chord_gen_enabled=self.chord_gen_enabled_var.get(),
                chord_variation=self.chord_variation_var.get(),
                voicing=self.voicing_var.get()
            )
            
        except (ValueError, RuntimeError, OSError) as e:
            self.log_message(f"Error playing pattern: {str(e)}")
            self.is_playing = False
            self.update_controls()
    
    def stop_pattern(self):
        """Ferma la riproduzione del pattern"""
        if not self.is_playing:
            return
        
        self.pattern_engine.stop_pattern()
        self.is_playing = False
        self.update_controls()
        self.log_message("Playback stopped.")
    
    def on_playback_finished(self):
        """Callback chiamato quando la riproduzione finisce"""
        self.is_playing = False
        # Solo aggiorna i controlli se la finestra esiste ancora
        if self.is_window_open():
            self.update_controls()
        self.log_message("Playback finished.")
    
    def update_controls(self):
        """Aggiorna lo stato dei controlli"""
        try:
            if not self.window.winfo_exists():
                return
        except (tk.TclError, AttributeError):
            return

        if self.is_playing:
            if self.play_btn and self.play_btn.winfo_exists():
                self.play_btn.config(state='disabled', text="▶ Playing...", 
                                   bg='#95a5a6', cursor='arrow')
            if self.stop_btn and self.stop_btn.winfo_exists():
                self.stop_btn.config(state='normal', bg='#e74c3c', cursor='hand2')
        else:
            if self.play_btn and self.play_btn.winfo_exists():
                self.play_btn.config(state='normal', text="▶ Play", 
                                   bg='#27ae60', cursor='hand2')
            if self.stop_btn and self.stop_btn.winfo_exists():
                self.stop_btn.config(state='disabled', bg='#bdc3c7', cursor='arrow')
        
        self.update_pause_controls_state()
    
    def update_pause_controls_state(self):
        """Aggiorna lo stato dei controlli pause in base al loop"""
        try:
            if not self.window.winfo_exists():
                return
        except (tk.TclError, AttributeError):
            return
        
        is_loop_active = self.loop_var.get()
        selected_pause = self.pause_duration_var.get()
        
        # Pause options: none, 0.1s, 0.25s, 0.5s, 1.0s, 1.5s, 2.0s, 3.0s
        pause_options = ["none", "0.1s", "0.25s", "0.5s", "1.0s", "1.5s", "2.0s", "3.0s"]
        
        for option in pause_options:
            if option in self.pattern_buttons:
                try:
                    btn = self.pattern_buttons[option]
                    if not btn.winfo_exists():
                        continue
                    
                    if is_loop_active:
                        # Abilita i controlli pause quando il loop è attivo
                        if option == selected_pause:
                            # Mantieni l'evidenziazione della pausa selezionata
                            btn.config(state='normal', bg='#3498db', fg='white', cursor='hand2')
                        else:
                            btn.config(state='normal', bg='#ecf0f1', fg='#2c3e50', cursor='hand2')
                    else:
                        # Disabilita i controlli pause quando il loop non è attivo
                        btn.config(state='disabled', bg='#bdc3c7', fg='#7f8c8d', cursor='arrow')
                except tk.TclError:
                    # Il widget è stato distrutto
                    continue
    
    def log_message(self, message: str):
        """Aggiunge un messaggio all'area di stato (ora solo console)"""
        print(f"Creative Chord Patterns: {message}")
        self.window.update_idletasks()
    
    def on_closing(self):
        """Gestisce la chiusura della finestra"""
        if self.is_playing:
            self.stop_pattern()
        self.window.destroy()
    
    def show(self):
        """Mostra la finestra"""
        self.window.lift()
        self.window.focus_force()
    
    def get_window(self):
        """Restituisce la finestra per permettere al parent di accedervi"""
        return self.window
    
    def is_window_open(self):
        """Controlla se la finestra è ancora aperta"""
        try:
            return self.window.winfo_exists()
        except (tk.TclError, AttributeError):
            return False
