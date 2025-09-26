"""
Finestra per la riproduzione creativa di accordi con pattern
"""

import tkinter as tk
from tkinter import ttk
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
        playback_frame = ttk.LabelFrame(parent, text="🎵 Playback Controls", 
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
        speed_label = tk.Label(speed_frame, text="⚡", 
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
        param_frame = ttk.LabelFrame(parent, text="⚙️ Parameters", 
                                    style='Modern.TLabelframe', padding="10")
        param_frame.pack(fill='x', pady=(0, 15))
        
        # Frame principale per i parametri in griglia
        params_frame = tk.Frame(param_frame, bg='#f8f9fa')
        params_frame.pack(fill='x')
        
        # Ottava Start
        start_octave_frame = tk.Frame(params_frame, bg='#f8f9fa')
        start_octave_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        start_octave_label = tk.Label(start_octave_frame, text="🎼 Start Octave", 
                                     font=('Segoe UI', 9, 'bold'), 
                               bg='#f8f9fa', fg='#2c3e50')
        start_octave_label.pack(anchor='w')
        
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
        
        duration_octaves_label = tk.Label(duration_octaves_frame, text="🎵 Duration Octaves", 
                                         font=('Segoe UI', 9, 'bold'), 
                                bg='#f8f9fa', fg='#2c3e50')
        duration_octaves_label.pack(anchor='w')
        
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
        
        note_duration_label = tk.Label(note_duration_frame, text="⏱️ Note Duration", 
                                      font=('Segoe UI', 9, 'bold'), 
                                      bg='#f8f9fa', fg='#9b59b6')
        note_duration_label.pack(anchor='w')
        
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
        
        bpm_label = tk.Label(bpm_frame, text="🎵 BPM", 
                            font=('Segoe UI', 9, 'bold'), 
                            bg='#f8f9fa', fg='#2c3e50')
        bpm_label.pack(anchor='w')
        
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
                    pause_duration=self.get_pause_duration_seconds()
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
                self.on_playback_finished
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
        self.update_controls()
        self.log_message("Playback finished.")
    
    def update_controls(self):
        """Aggiorna lo stato dei controlli"""
        if self.is_playing:
            self.play_btn.config(state='disabled', text="▶ Playing...", 
                               bg='#95a5a6', cursor='arrow')
            self.stop_btn.config(state='normal', bg='#e74c3c', cursor='hand2')
        else:
            self.play_btn.config(state='normal', text="▶ Play", 
                               bg='#27ae60', cursor='hand2')
            self.stop_btn.config(state='disabled', bg='#bdc3c7', cursor='arrow')
        
        # Aggiorna lo stato dei controlli pause
        self.update_pause_controls_state()
    
    def update_pause_controls_state(self):
        """Aggiorna lo stato dei controlli pause in base al loop"""
        is_loop_active = self.loop_var.get()
        selected_pause = self.pause_duration_var.get()
        
        # Pause options: none, 0.1s, 0.25s, 0.5s, 1.0s, 1.5s, 2.0s, 3.0s
        pause_options = ["none", "0.1s", "0.25s", "0.5s", "1.0s", "1.5s", "2.0s", "3.0s"]
        
        for option in pause_options:
            if option in self.pattern_buttons:
                btn = self.pattern_buttons[option]
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
