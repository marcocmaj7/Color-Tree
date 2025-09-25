"""
Finestra per la riproduzione creativa di accordi con pattern
"""

import tkinter as tk
from tkinter import ttk
from pattern_engine import PatternEngine, PatternType
from chord_generator import SoundCell, MIDIScaleGenerator


class CreativeChordWindow:
    """Finestra separata per la riproduzione creativa di accordi"""
    
    def __init__(self, parent, sound_cell: SoundCell, midi_generator: MIDIScaleGenerator):
        self.parent = parent
        self.sound_cell = sound_cell
        self.midi_generator = midi_generator
        self.pattern_engine = PatternEngine(midi_generator)
        
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
        self.loop_var = tk.BooleanVar(value=False)
        self.reverse_var = tk.BooleanVar(value=False)
        
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
        
        # Configurazione stile
        self.setup_styles()
        self.setup_ui()
        self.update_controls()
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
        self.reverse_btn.pack(side='left', padx=(0, 0))
    
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
        note_duration_frame.pack(side='left', fill='x', expand=True)
        
        note_duration_label = tk.Label(note_duration_frame, text="⏱️ Note Duration", 
                                      font=('Segoe UI', 9, 'bold'), 
                                      bg='#f8f9fa', fg='#2c3e50')
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
            ])
        ]
        
        # Create grid layout for patterns
        for cat_idx, (cat_name, patterns) in enumerate(categories):
            # Category label
            cat_label = tk.Label(pattern_frame, text=f"📁 {cat_name}", 
                               font=('Segoe UI', 9, 'bold'), 
                               bg='#f8f9fa', fg='#34495e')
            cat_label.grid(row=cat_idx, column=0, sticky='w', pady=(5, 2), padx=(0, 10))
            
            # Pattern buttons for this category
            for pat_idx, (name, value, desc) in enumerate(patterns):
                btn = tk.Button(pattern_frame, text=name, 
                              font=('Segoe UI', 8),
                              bg='#ecf0f1', fg='#2c3e50',
                              relief='flat', bd=1,
                              command=lambda v=value: self.select_pattern(v),
                              cursor='hand2',
                              activebackground='#3498db',
                              activeforeground='white')
                btn.grid(row=cat_idx, column=pat_idx+1, padx=2, pady=2, sticky='ew')
                
                # Tooltip for description
                self.create_tooltip(btn, desc)
        
        # Configure grid weights
        for i in range(1, 6):  # 5 pattern columns
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
        self.selected_pattern.set(pattern_value)
        self.on_pattern_change()
    
    
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
    
    def toggle_reverse(self):
        """Toggle del reverse"""
        self.reverse_var.set(not self.reverse_var.get())
        if self.reverse_var.get():
            self.reverse_btn.config(bg='#e67e22', fg='white')
        else:
            self.reverse_btn.config(bg='#95a5a6', fg='white')
    
    def increase_start_octave(self):
        """Aumenta l'ottava di partenza"""
        current = self.start_octave_var.get()
        if current < 6:
            self.start_octave_var.set(current + 1)
    
    def decrease_start_octave(self):
        """Diminuisce l'ottava di partenza"""
        current = self.start_octave_var.get()
        if current > 2:
            self.start_octave_var.set(current - 1)
    
    def increase_duration_octaves(self):
        """Aumenta le ottave di durata"""
        current = self.duration_octaves_var.get()
        if current < 3:
            self.duration_octaves_var.set(current + 1)
    
    def decrease_duration_octaves(self):
        """Diminuisce le ottave di durata"""
        current = self.duration_octaves_var.get()
        if current > 1:
            self.duration_octaves_var.set(current - 1)
    
    def on_note_duration_change(self, event=None):
        """Gestisce il cambio di durata nota"""
        duration = self.note_duration_var.get()
        self.log_message(f"Note duration changed to: {duration}")
        # Suppress unused argument warning
        _ = event
    
    def get_note_duration_seconds(self):
        """Converte la durata nota in secondi"""
        duration_map = {
            "Whole": 2.0,
            "Half": 1.0,
            "Quarter": 0.5,
            "Eighth": 0.25,
            "Sixteenth": 0.125,
            "Thirty-Second": 0.0625
        }
        return duration_map.get(self.note_duration_var.get(), 0.5)
    
    
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
            
            # Avvia la riproduzione in un thread separato
            self.pattern_engine.play_pattern(
                self.sound_cell,
                pattern_type,
                self.start_octave_var.get(),
                self.get_note_duration_seconds(),
                self.loop_var.get(),
                self.reverse_var.get(),
                self.duration_octaves_var.get(),
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
