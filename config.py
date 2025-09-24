"""
Configurazione per l'applicazione Chord Generator
"""

# Configurazione dell'interfaccia grafica
UI_CONFIG = {
    'window_title': 'Generatore di Accordi - Circolo delle Quinte',
    'window_size': '1200x800',
    'background_color': '#f0f0f0',
    'font_family': 'Arial',
    'title_font_size': 16,
    'chord_font_size': 10,
    'padding': 10
}

# Configurazione dei colori
COLORS = {
    'background': '#f0f0f0',
    'chord_background': '#e8f4fd',
    'chord_border': '#4a90e2',
    'text_primary': '#333333',
    'text_secondary': '#666666'
}

# Configurazione delle note
NOTE_NAMES = {
    'C': 'C',
    'C_SHARP': 'C#',
    'D': 'D', 
    'D_SHARP': 'D#',
    'E': 'E',
    'F': 'F',
    'F_SHARP': 'F#',
    'G': 'G',
    'G_SHARP': 'G#',
    'A': 'A',
    'A_SHARP': 'A#',
    'B': 'B'
}

# Configurazione dell'applicazione
APP_CONFIG = {
    'max_display_levels': 12,
    'default_root_note': 'C',
    'enable_scrolling': True,
    'show_position_numbers': True,
    'default_display_mode': 'notes',  # 'notes' o 'intervals'
    'enable_interval_analysis': True
}

# Configurazione degli intervalli
INTERVAL_CONFIG = {
    'interval_symbols': {
        'T': 'Tonic',
        'b2': 'Seconda minore',
        '2': 'Seconda maggiore',
        'b3': 'Terza minore',
        '3': 'Terza maggiore',
        '4': 'Quarta giusta',
        'b5': 'Quinta diminuita',
        '5': 'Quinta giusta',
        'b6': 'Sesta minore',
        '6': 'Sesta maggiore',
        'b7': 'Settima minore',
        '7': 'Settima maggiore'
    },
    'show_interval_names': False,  # Mostra nomi completi degli intervalli
    'interval_separator': ' - '
}
