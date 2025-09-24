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
        self.window.geometry("800x600")
        self.window.configure(bg='#f0f0f0')
        
        # Variabili per i controlli
        self.selected_pattern = tk.StringVar(value="up")
        self.octave_var = tk.IntVar(value=4)
        self.duration_var = tk.DoubleVar(value=0.3)
        self.loop_var = tk.BooleanVar(value=False)
        
        # Stato dei controlli
        self.is_playing = False
        
        # Inizializza i widget per evitare errori di linting
        self.play_btn = None
        self.stop_btn = None
        self.loop_check = None
        self.status_text = None
        
        self.setup_ui()
        self.update_controls()
        
        # Gestisce la chiusura della finestra
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """Configura l'interfaccia utente"""
        # Frame principale con scrollbar
        canvas = tk.Canvas(self.window, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame principale
        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Titolo
        title_label = tk.Label(main_frame, text="Creative Chord Patterns", 
                              font=('Arial', 16, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=(0, 20))
        
        # Informazioni sull'accordo selezionato
        self.create_chord_info(main_frame)
        
        # Controlli di riproduzione (spostati in alto per maggiore visibilità)
        self.create_playback_controls(main_frame)
        
        # Controlli di parametri
        self.create_parameter_controls(main_frame)
        
        # Controlli pattern
        self.create_pattern_controls(main_frame)
        
        # Area di stato
        self.create_status_area(main_frame)
        
        # Pack canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
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
        """Crea i controlli di riproduzione"""
        playback_frame = ttk.LabelFrame(parent, text="🎵 Playback Controls", padding="15")
        playback_frame.pack(fill='x', pady=(0, 20))
        
        # Bottoni di controllo
        button_frame = tk.Frame(playback_frame, bg='#f0f0f0')
        button_frame.pack(fill='x', pady=(0, 10))
        
        # Play button
        self.play_btn = tk.Button(button_frame, text="▶ PLAY", 
                                 font=('Arial', 14, 'bold'),
                                 bg='#4CAF50', fg='white',
                                 command=self.play_pattern,
                                 width=12, height=3,
                                 relief='raised', bd=3)
        self.play_btn.pack(side='left', padx=(0, 15))
        
        # Stop button
        self.stop_btn = tk.Button(button_frame, text="⏹ STOP", 
                                 font=('Arial', 14, 'bold'),
                                 bg='#f44336', fg='white',
                                 command=self.stop_pattern,
                                 width=12, height=3,
                                 relief='raised', bd=3)
        self.stop_btn.pack(side='left', padx=(0, 15))
        
        # Loop checkbox
        self.loop_check = tk.Checkbutton(button_frame, text="🔄 LOOP", 
                                        variable=self.loop_var,
                                        font=('Arial', 12, 'bold'),
                                        bg='#f0f0f0',
                                        relief='raised', bd=2)
        self.loop_check.pack(side='left', padx=(20, 0))
        
        # Label di istruzioni
        instruction_label = tk.Label(playback_frame, 
                                   text="💡 Select a pattern below, then click PLAY to start playback", 
                                   font=('Arial', 10, 'italic'), 
                                   fg='#666666', bg='#f0f0f0')
        instruction_label.pack(pady=(5, 0))
    
    def create_parameter_controls(self, parent):
        """Crea i controlli per i parametri"""
        param_frame = ttk.LabelFrame(parent, text="⚙️ Parameters", padding="15")
        param_frame.pack(fill='x', pady=(0, 20))
        
        # Ottava
        octave_frame = tk.Frame(param_frame, bg='#f0f0f0')
        octave_frame.pack(fill='x', pady=(0, 15))
        
        octave_label = tk.Label(octave_frame, text="🎼 Octave:", 
                               font=('Arial', 12, 'bold'), 
                               bg='#f0f0f0')
        octave_label.pack(side='left')
        
        octave_scale = tk.Scale(octave_frame, from_=2, to=6, 
                               variable=self.octave_var, orient='horizontal',
                               length=250, bg='#f0f0f0',
                               font=('Arial', 10),
                               highlightthickness=0)
        octave_scale.pack(side='left', padx=(15, 0))
        
        # Valore corrente ottava
        octave_value_label = tk.Label(octave_frame, text="4", 
                                     font=('Arial', 12, 'bold'), 
                                     bg='#e8f4fd', fg='#2196F3',
                                     width=3, relief='raised', bd=2)
        octave_value_label.pack(side='left', padx=(10, 0))
        
        # Aggiorna il valore quando cambia la scala
        def update_octave_value(*_):
            octave_value_label.config(text=str(int(self.octave_var.get())))
        self.octave_var.trace('w', update_octave_value)
        
        # Durata
        duration_frame = tk.Frame(param_frame, bg='#f0f0f0')
        duration_frame.pack(fill='x')
        
        duration_label = tk.Label(duration_frame, text="⏱️ Duration:", 
                                font=('Arial', 12, 'bold'), 
                                bg='#f0f0f0')
        duration_label.pack(side='left')
        
        duration_scale = tk.Scale(duration_frame, from_=0.1, to=1.0, 
                                 resolution=0.1, variable=self.duration_var, 
                                 orient='horizontal', length=250, bg='#f0f0f0',
                                 font=('Arial', 10),
                                 highlightthickness=0)
        duration_scale.pack(side='left', padx=(15, 0))
        
        # Valore corrente durata
        duration_value_label = tk.Label(duration_frame, text="0.3s", 
                                      font=('Arial', 12, 'bold'), 
                                      bg='#e8f4fd', fg='#2196F3',
                                      width=5, relief='raised', bd=2)
        duration_value_label.pack(side='left', padx=(10, 0))
        
        # Aggiorna il valore quando cambia la scala
        def update_duration_value(*_):
            duration_value_label.config(text=f"{self.duration_var.get():.1f}s")
        self.duration_var.trace('w', update_duration_value)
    
    def create_status_area(self, parent):
        """Crea l'area di stato"""
        status_frame = ttk.LabelFrame(parent, text="📊 Status & Log", padding="10")
        status_frame.pack(fill='both', expand=True)
        
        self.status_text = tk.Text(status_frame, height=8, width=80, 
                                  font=('Arial', 10), bg='#f8f8f8',
                                  relief='sunken', bd=2)
        self.status_text.pack(fill='both', expand=True, pady=(5, 0))
        
        # Scrollbar per il testo
        scrollbar = ttk.Scrollbar(status_frame, orient='vertical', command=self.status_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.status_text.config(yscrollcommand=scrollbar.set)
        
        # Messaggio iniziale
        self.log_message("🎵 Creative Chord Patterns ready!")
        self.log_message("📝 Instructions:")
        self.log_message("   1. Select a pattern from the categories below")
        self.log_message("   2. Adjust octave (2-6) and duration (0.1-1.0s) if needed")
        self.log_message("   3. Click ▶ PLAY to start playback")
        self.log_message("   4. Click ⏹ STOP to stop playback")
        self.log_message("   5. Enable 🔄 LOOP for continuous playback")
    
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
            self.log_message(f"Octave: {self.octave_var.get()}, Duration: {self.duration_var.get():.1f}s")
            if self.loop_var.get():
                self.log_message("Loop mode: ON")
            
            # Avvia la riproduzione in un thread separato
            self.pattern_engine.play_pattern(
                self.sound_cell,
                pattern_type,
                self.octave_var.get(),
                self.duration_var.get(),
                self.loop_var.get(),
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
            self.play_btn.config(state='disabled', text="▶ Playing...")
            self.stop_btn.config(state='normal')
        else:
            self.play_btn.config(state='normal', text="▶ Play")
            self.stop_btn.config(state='disabled')
    
    def log_message(self, message: str):
        """Aggiunge un messaggio all'area di stato"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
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
