"""
Pattern Engine per la riproduzione creativa di accordi
Gestisce tutti i pattern di riproduzione richiesti
"""

import random
import time
import threading
from typing import List, Callable, Optional
from dataclasses import dataclass
from enum import Enum
from chord_generator import Note, SoundCell, MIDIScaleGenerator, MusicalFigure, musical_figure_to_seconds


class PatternType(Enum):
    """Tipi di pattern disponibili"""
    # Pattern Base
    UP = "up"
    DOWN = "down"
    UP_DOWN = "up_down"
    DOWN_UP = "down_up"
    
    # Pattern Geometrici
    TRIANGLE = "triangle"
    DIAMOND = "diamond"
    ZIGZAG = "zigzag"
    SPIRAL = "spiral"
    
    # Pattern Ritmici
    GALLOP = "gallop"
    TRIPLET = "triplet"
    SYNCOPATED = "syncopated"
    STUTTER = "stutter"
    
    # Pattern Avanzati
    SKIP = "skip"
    GHOST = "ghost"
    CASCADE = "cascade"
    BOUNCE = "bounce"
    
    # Pattern Espressivi
    CRESCENDO = "crescendo"
    DIMINUENDO = "diminuendo"
    ACCENT_FIRST = "accent_first"
    SWING = "swing"
    
    # Pattern Random
    RANDOM_CHAOS = "random_chaos"
    RANDOM_RHYTHM = "random_rhythm"
    RANDOM_VOLUME = "random_volume"
    RANDOM_CHANGING = "random_changing"


@dataclass
class NoteEvent:
    """Rappresenta un evento di nota con timing e volume"""
    note: Note
    octave: int
    duration: float
    volume: float
    delay: float = 0.0


class PatternEngine:
    """Motore per la generazione e riproduzione di pattern creativi"""
    
    def __init__(self, midi_generator: MIDIScaleGenerator, midi_output=None):
        self.midi_generator = midi_generator
        self.midi_output = midi_output  # Aggiunto supporto MIDI
        self.is_playing = False
        self.is_looping = False
        self.stop_requested = False
        self.current_thread: Optional[threading.Thread] = None
        self.playback_id = 0
        
        # Parametri dinamici per aggiornamento in tempo reale
        self.current_sound_cell = None
        self.current_pattern_type = None
        self.current_octave = 4
        self.current_base_duration = 0.3
        self.current_loop = False
        self.current_reverse = False
        self.current_duration_octaves = 1
        self.current_playback_speed = 1.0
        self.current_bpm = 120
        self.current_pause_duration = 0.0
        self.param_lock = threading.Lock()
        
        # MIDI Effects parameters
        self.current_delay_enabled = False
        self.current_delay_time = 0.25
        self.current_delay_feedback = 0.3
        self.current_delay_mix = 0.5
        self.current_delay_type = "Standard"
        self.current_delay_repeats = 3
        self.current_octave_add = 0
        self.current_velocity_curve = "linear"
        self.current_velocity_intensity = 1.0
        self.current_accent_enabled = False
        self.current_accent_strength = 0.5
        self.current_accent_pattern = "every_beat"
        self.current_repeater_enabled = False
        self.current_repeat_count = 2
        self.current_repeat_timing = "immediate"
        self.current_chord_gen_enabled = False
        self.current_chord_variation = "inversion"
        self.current_voicing = "close"
    
    def update_parameters(self, sound_cell: SoundCell = None, pattern_type: PatternType = None,
                         octave: int = None, base_duration: float = None,
                         loop: bool = None, reverse: bool = None, duration_octaves: int = None,
                         playback_speed: float = None, bpm: int = None, pause_duration: float = None,
                         # MIDI Effects
                         delay_enabled: bool = None, delay_time: float = None, delay_feedback: float = None,
                         delay_mix: float = None, delay_type: str = None, delay_repeats: int = None,
                         octave_add: int = None, velocity_curve: str = None, velocity_intensity: float = None,
                         accent_enabled: bool = None, accent_strength: float = None, accent_pattern: str = None,
                         repeater_enabled: bool = None, repeat_count: int = None, repeat_timing: str = None,
                         chord_gen_enabled: bool = None, chord_variation: str = None, voicing: str = None):
        """Aggiorna i parametri in tempo reale durante la riproduzione"""
        with self.param_lock:
            if sound_cell is not None:
                self.current_sound_cell = sound_cell
            if pattern_type is not None:
                self.current_pattern_type = pattern_type
            if octave is not None:
                self.current_octave = octave
            if base_duration is not None:
                self.current_base_duration = base_duration
            if loop is not None:
                self.current_loop = loop
            if reverse is not None:
                self.current_reverse = reverse
            if duration_octaves is not None:
                self.current_duration_octaves = duration_octaves
            if playback_speed is not None:
                self.current_playback_speed = playback_speed
            if bpm is not None:
                self.current_bpm = bpm
            if pause_duration is not None:
                self.current_pause_duration = pause_duration
            
            # MIDI Effects
            if delay_enabled is not None:
                self.current_delay_enabled = delay_enabled
            if delay_time is not None:
                self.current_delay_time = delay_time
            if delay_feedback is not None:
                self.current_delay_feedback = delay_feedback
            if delay_mix is not None:
                self.current_delay_mix = delay_mix
            if delay_type is not None:
                self.current_delay_type = delay_type
            if delay_repeats is not None:
                self.current_delay_repeats = delay_repeats
            if octave_add is not None:
                self.current_octave_add = octave_add
            if velocity_curve is not None:
                self.current_velocity_curve = velocity_curve
            if velocity_intensity is not None:
                self.current_velocity_intensity = velocity_intensity
            if accent_enabled is not None:
                self.current_accent_enabled = accent_enabled
            if accent_strength is not None:
                self.current_accent_strength = accent_strength
            if accent_pattern is not None:
                self.current_accent_pattern = accent_pattern
            if repeater_enabled is not None:
                self.current_repeater_enabled = repeater_enabled
            if repeat_count is not None:
                self.current_repeat_count = repeat_count
            if repeat_timing is not None:
                self.current_repeat_timing = repeat_timing
            if chord_gen_enabled is not None:
                self.current_chord_gen_enabled = chord_gen_enabled
            if chord_variation is not None:
                self.current_chord_variation = chord_variation
            if voicing is not None:
                self.current_voicing = voicing
    
    def update_parameters_safe(self, sound_cell: SoundCell = None, pattern_type: PatternType = None,
                              octave: int = None, base_duration: float = None,
                              loop: bool = None, reverse: bool = None, duration_octaves: int = None,
                              playback_speed: float = None, bpm: int = None, pause_duration: float = None,
                              # MIDI Effects
                              delay_enabled: bool = None, delay_time: float = None, delay_feedback: float = None,
                              octave_add: int = None, velocity_curve: str = None, velocity_intensity: float = None,
                              accent_enabled: bool = None, accent_strength: float = None, accent_pattern: str = None,
                              repeater_enabled: bool = None, repeat_count: int = None, repeat_timing: str = None,
                              chord_gen_enabled: bool = None, chord_variation: str = None, voicing: str = None):
        """Aggiorna i parametri in modo sicuro, fermando la riproduzione se necessario"""
        # Se stiamo cambiando parametri critici, ferma la riproduzione corrente
        critical_changes = (sound_cell is not None or pattern_type is not None or 
                           octave is not None or base_duration is not None)
        
        if critical_changes and self.is_playing:
            self.stop_pattern()
            # Aspetta un momento per assicurarsi che il thread sia fermato
            time.sleep(0.05)
        
        self.update_parameters(sound_cell, pattern_type, octave, base_duration, 
                              loop, reverse, duration_octaves, playback_speed, bpm, pause_duration,
                              delay_enabled, delay_time, delay_feedback, octave_add, velocity_curve, velocity_intensity,
                              accent_enabled, accent_strength, accent_pattern, repeater_enabled, repeat_count, repeat_timing,
                              chord_gen_enabled, chord_variation, voicing)
    
    def get_current_parameters(self):
        """Ottiene i parametri correnti in modo thread-safe"""
        with self.param_lock:
            return {
                'sound_cell': self.current_sound_cell,
                'pattern_type': self.current_pattern_type,
                'octave': self.current_octave,
                'base_duration': self.current_base_duration,
                'loop': self.current_loop,
                'reverse': self.current_reverse,
                'duration_octaves': self.current_duration_octaves,
                'playback_speed': self.current_playback_speed,
                'bpm': self.current_bpm,
                'pause_duration': self.current_pause_duration,
                # MIDI Effects parameters
                'delay_enabled': self.current_delay_enabled,
                'delay_time': self.current_delay_time,
                'delay_feedback': self.current_delay_feedback,
                'delay_mix': self.current_delay_mix,
                'delay_type': self.current_delay_type,
                'delay_repeats': self.current_delay_repeats,
                'octave_add': self.current_octave_add,
                'velocity_curve': self.current_velocity_curve,
                'velocity_intensity': self.current_velocity_intensity,
                'accent_enabled': self.current_accent_enabled,
                'accent_strength': self.current_accent_strength,
                'accent_pattern': self.current_accent_pattern,
                'repeater_enabled': self.current_repeater_enabled,
                'repeat_count': self.current_repeat_count,
                'repeat_timing': self.current_repeat_timing,
                'chord_gen_enabled': self.current_chord_gen_enabled,
                'chord_variation': self.current_chord_variation,
                'voicing': self.current_voicing
            }
        
    def generate_pattern_notes(self, sound_cell: SoundCell, pattern_type: PatternType, 
                             octave: int = 4, base_duration: float = 0.3) -> List[NoteEvent]:
        """Genera una sequenza di note basata sul pattern selezionato"""
        notes = sound_cell.notes
        if not notes:
            return []
        
        # Genera le note base per l'ottava specificata
        base_notes = self._generate_base_notes(notes, octave, base_duration)
        
        if pattern_type == PatternType.UP:
            return self._pattern_up(base_notes, base_duration)
        elif pattern_type == PatternType.DOWN:
            return self._pattern_down(base_notes, base_duration)
        elif pattern_type == PatternType.UP_DOWN:
            return self._pattern_up_down(base_notes, base_duration)
        elif pattern_type == PatternType.DOWN_UP:
            return self._pattern_down_up(base_notes, base_duration)
        elif pattern_type == PatternType.TRIANGLE:
            return self._pattern_triangle(base_notes, base_duration)
        elif pattern_type == PatternType.DIAMOND:
            return self._pattern_diamond(base_notes, base_duration)
        elif pattern_type == PatternType.ZIGZAG:
            return self._pattern_zigzag(base_notes, base_duration)
        elif pattern_type == PatternType.SPIRAL:
            return self._pattern_spiral(base_notes, base_duration)
        elif pattern_type == PatternType.GALLOP:
            return self._pattern_gallop(base_notes, base_duration)
        elif pattern_type == PatternType.TRIPLET:
            return self._pattern_triplet(base_notes, base_duration)
        elif pattern_type == PatternType.SYNCOPATED:
            return self._pattern_syncopated(base_notes, base_duration)
        elif pattern_type == PatternType.STUTTER:
            return self._pattern_stutter(base_notes, base_duration)
        elif pattern_type == PatternType.SKIP:
            return self._pattern_skip(base_notes, base_duration)
        elif pattern_type == PatternType.GHOST:
            return self._pattern_ghost(base_notes, base_duration)
        elif pattern_type == PatternType.CASCADE:
            return self._pattern_cascade(base_notes, base_duration)
        elif pattern_type == PatternType.BOUNCE:
            return self._pattern_bounce(base_notes, base_duration)
        elif pattern_type == PatternType.CRESCENDO:
            return self._pattern_crescendo(base_notes, base_duration)
        elif pattern_type == PatternType.DIMINUENDO:
            return self._pattern_diminuendo(base_notes, base_duration)
        elif pattern_type == PatternType.ACCENT_FIRST:
            return self._pattern_accent_first(base_notes, base_duration)
        elif pattern_type == PatternType.SWING:
            return self._pattern_swing(base_notes, base_duration)
        elif pattern_type == PatternType.RANDOM_CHAOS:
            return self._pattern_random_chaos(base_notes, base_duration)
        elif pattern_type == PatternType.RANDOM_RHYTHM:
            return self._pattern_random_rhythm(base_notes, base_duration)
        elif pattern_type == PatternType.RANDOM_VOLUME:
            return self._pattern_random_volume(base_notes, base_duration)
        elif pattern_type == PatternType.RANDOM_CHANGING:
            return self._pattern_random_changing(base_notes, base_duration)
        else:
            return self._pattern_up(base_notes, base_duration)  # Default
    
    def _generate_base_notes(self, notes: List[Note], octave: int, base_duration: float = 0.3) -> List[NoteEvent]:
        """Genera le note base per l'ottava specificata"""
        base_notes = []
        for note in notes:
            # Per un accordo normale, tutte le note sono nella stessa ottava
            # Solo se ci sono più di 12 note diverse, allora aumenta l'ottava
            target_octave = octave
            base_notes.append(NoteEvent(
                note=note,
                octave=target_octave,
                duration=base_duration,  # Usa la durata passata come parametro
                volume=0.7
            ))
        return base_notes
    
    # Pattern Base
    def _pattern_up(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Ascendente semplice (C→E→G→C)"""
        result = []
        
        # Ripete le note dell'accordo nella stessa ottava
        for note in notes:
            result.append(NoteEvent(
                note=note.note,
                octave=note.octave,
                duration=base_duration,
                volume=note.volume
            ))
        
        return result
    
    def _pattern_down(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Discendente semplice (C→G→E→C)"""
        result = []
        
        # Note dell'accordo in ordine discendente nella stessa ottava
        for note in reversed(notes):
            result.append(NoteEvent(
                note=note.note,
                octave=note.octave,
                duration=base_duration,
                volume=note.volume
            ))
        
        return result
    
    def _pattern_up_down(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Su poi giù (C→E→G→C→G→E)"""
        result = []
        
        # Su
        for note in notes:
            result.append(NoteEvent(
                note=note.note,
                octave=note.octave,
                duration=base_duration,
                volume=note.volume
            ))
        
        # Aggiunge la nota radice (ripetizione)
        if notes:
            root_note = notes[0]
            result.append(NoteEvent(
                note=root_note.note,
                octave=root_note.octave,
                duration=base_duration,
                volume=root_note.volume
            ))
        
        # Giù (escludendo la prima nota per evitare duplicati)
        for note in reversed(notes[1:]):
            result.append(NoteEvent(
                note=note.note,
                octave=note.octave,
                duration=base_duration,
                volume=note.volume
            ))
        
        return result
    
    def _pattern_down_up(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Giù poi su (C→G→E→C→E→G)"""
        result = []
        
        # Giù - inizia con la nota radice
        if notes:
            root_note = notes[0]
            result.append(NoteEvent(
                note=root_note.note,
                octave=root_note.octave,
                duration=base_duration,
                volume=root_note.volume
            ))
        
        # Poi scende attraverso le note dell'accordo
        for note in reversed(notes):
            result.append(NoteEvent(
                note=note.note,
                octave=note.octave,
                duration=base_duration,
                volume=note.volume
            ))
        
        # Su (escludendo la prima nota per evitare duplicati)
        for note in notes[1:]:
            result.append(NoteEvent(
                note=note.note,
                octave=note.octave,
                duration=base_duration,
                volume=note.volume
            ))
        
        return result
    
    # Pattern Geometrici
    def _pattern_triangle(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Su-giù-su formando un triangolo melodico"""
        result = []
        # Su
        for note in notes:
            result.append(NoteEvent(
                note=note.note,
                octave=note.octave,
                duration=base_duration,
                volume=note.volume
            ))
        # Giù (escludendo la prima e ultima)
        for note in reversed(notes[1:-1]):
            result.append(NoteEvent(
                note=note.note,
                octave=note.octave,
                duration=base_duration,
                volume=note.volume
            ))
        # Su di nuovo (escludendo la prima)
        for note in notes[1:]:
            result.append(NoteEvent(
                note=note.note,
                octave=note.octave,
                duration=base_duration,
                volume=note.volume
            ))
        return result
    
    def _pattern_diamond(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Dentro-fuori-dentro (E→G→C→G→E)"""
        if len(notes) < 3:
            return self._pattern_up(notes, base_duration)
        
        result = []
        # Dentro: note centrali verso l'esterno
        mid = len(notes) // 2
        for i in range(mid, len(notes)):
            result.append(NoteEvent(
                note=notes[i].note,
                octave=notes[i].octave,
                duration=base_duration,
                volume=notes[i].volume
            ))
        for i in range(mid - 1, -1, -1):
            result.append(NoteEvent(
                note=notes[i].note,
                octave=notes[i].octave,
                duration=base_duration,
                volume=notes[i].volume
            ))
        return result
    
    def _pattern_zigzag(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Alternanza estremi-centro (C→G→E→C)"""
        if len(notes) < 3:
            return self._pattern_up(notes, base_duration)
        
        result = []
        left = 0
        right = len(notes) - 1
        
        while left <= right:
            if left == right:
                result.append(NoteEvent(
                    note=notes[left].note,
                    octave=notes[left].octave,
                    duration=base_duration,
                    volume=notes[left].volume
                ))
            else:
                # Estremo sinistro
                result.append(NoteEvent(
                    note=notes[left].note,
                    octave=notes[left].octave,
                    duration=base_duration,
                    volume=notes[left].volume
                ))
                # Estremo destro
                result.append(NoteEvent(
                    note=notes[right].note,
                    octave=notes[right].octave,
                    duration=base_duration,
                    volume=notes[right].volume
                ))
            left += 1
            right -= 1
        
        return result
    
    def _pattern_spiral(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Giri concentrici espandendosi"""
        if len(notes) < 3:
            return self._pattern_up(notes, base_duration)
        
        result = []
        # Inizia dal centro e si espande
        mid = len(notes) // 2
        result.append(NoteEvent(
            note=notes[mid].note,
            octave=notes[mid].octave,
            duration=base_duration,
            volume=notes[mid].volume
        ))
        
        # Espansione a spirale
        for radius in range(1, max(mid, len(notes) - mid)):
            # Aggiunge note a destra e sinistra del centro
            if mid + radius < len(notes):
                result.append(NoteEvent(
                    note=notes[mid + radius].note,
                    octave=notes[mid + radius].octave,
                    duration=base_duration,
                    volume=notes[mid + radius].volume
                ))
            if mid - radius >= 0:
                result.append(NoteEvent(
                    note=notes[mid - radius].note,
                    octave=notes[mid - radius].octave,
                    duration=base_duration,
                    volume=notes[mid - radius].volume
                ))
        
        return result
    
    # Pattern Ritmici
    def _pattern_gallop(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Due note veloci + una lunga (ta-ta-TAA)"""
        result = []
        for i, note in enumerate(notes):
            if i % 3 == 2:  # Ogni terza nota è lunga
                result.append(NoteEvent(
                    note=note.note,
                    octave=note.octave,
                    duration=base_duration * 2,
                    volume=note.volume
                ))
            else:  # Note veloci
                result.append(NoteEvent(
                    note=note.note,
                    octave=note.octave,
                    duration=base_duration * 0.5,
                    volume=note.volume
                ))
        return result
    
    def _pattern_triplet(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Gruppetti di tre note"""
        result = []
        for i in range(0, len(notes), 3):
            group = notes[i:i+3]
            for note in group:
                result.append(NoteEvent(
                    note=note.note,
                    octave=note.octave,
                    duration=base_duration * 0.7,
                    volume=note.volume,
                    delay=0.0
                ))
        return result
    
    def _pattern_syncopated(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Enfasi sui tempi deboli"""
        result = []
        for i, note in enumerate(notes):
            # Enfasi su note in posizioni dispari (tempi deboli)
            if i % 2 == 1:
                result.append(NoteEvent(
                    note=note.note,
                    octave=note.octave,
                    duration=base_duration * 1.2,
                    volume=note.volume * 1.3
                ))
            else:
                result.append(NoteEvent(
                    note=note.note,
                    octave=note.octave,
                    duration=base_duration * 0.8,
                    volume=note.volume * 0.7
                ))
        return result
    
    def _pattern_stutter(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Ripetizione rapida della stessa nota"""
        result = []
        for note in notes:
            # Ripete ogni nota 3 volte rapidamente
            for _ in range(3):
                result.append(NoteEvent(
                    note=note.note,
                    octave=note.octave,
                    duration=base_duration * 0.2,
                    volume=note.volume
                ))
        return result
    
    # Pattern Avanzati
    def _pattern_skip(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Salta note casualmente nel pattern"""
        result = []
        # Seleziona casualmente il 70% delle note
        num_notes = max(1, int(len(notes) * 0.7))
        selected_indices = random.sample(range(len(notes)), num_notes)
        selected_indices.sort()
        
        for idx in selected_indices:
            result.append(NoteEvent(
                note=notes[idx].note,
                octave=notes[idx].octave,
                duration=base_duration,
                volume=notes[idx].volume
            ))
        return result
    
    def _pattern_ghost(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Include note "fantasma" a volume basso"""
        result = []
        for i, note in enumerate(notes):
            # Note normali
            result.append(NoteEvent(
                note=note.note,
                octave=note.octave,
                duration=base_duration,
                volume=note.volume
            ))
            # Note fantasma (volume molto basso)
            if i < len(notes) - 1:
                result.append(NoteEvent(
                    note=note.note,
                    octave=note.octave,
                    duration=base_duration * 0.3,
                    volume=note.volume * 0.2
                ))
        return result
    
    def _pattern_cascade(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Effetto "cascata" con note che si sovrappongono"""
        result = []
        for i, note in enumerate(notes):
            result.append(NoteEvent(
                note=note.note,
                octave=note.octave,
                duration=base_duration * 1.5,
                volume=note.volume,
                delay=base_duration * 0.3 * i  # Ritardo crescente
            ))
        return result
    
    def _pattern_bounce(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Rimbalza tra note estreme"""
        if len(notes) < 2:
            return self._pattern_up(notes, base_duration)
        
        result = []
        left = 0
        right = len(notes) - 1
        
        while left <= right:
            # Nota sinistra
            result.append(NoteEvent(
                note=notes[left].note,
                octave=notes[left].octave,
                duration=base_duration,
                volume=notes[left].volume
            ))
            if left != right:
                # Nota destra
                result.append(NoteEvent(
                    note=notes[right].note,
                    octave=notes[right].octave,
                    duration=base_duration,
                    volume=notes[right].volume
                ))
            left += 1
            right -= 1
        
        return result
    
    # Pattern Espressivi
    def _pattern_crescendo(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Volume crescente attraverso l'arpeggio"""
        result = []
        for i, note in enumerate(notes):
            volume_factor = 0.3 + (0.7 * i / (len(notes) - 1)) if len(notes) > 1 else 0.7
            result.append(NoteEvent(
                note=note.note,
                octave=note.octave,
                duration=base_duration,
                volume=note.volume * volume_factor
            ))
        return result
    
    def _pattern_diminuendo(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Volume decrescente"""
        result = []
        for i, note in enumerate(notes):
            volume_factor = 1.0 - (0.7 * i / (len(notes) - 1)) if len(notes) > 1 else 0.7
            result.append(NoteEvent(
                note=note.note,
                octave=note.octave,
                duration=base_duration,
                volume=note.volume * volume_factor
            ))
        return result
    
    def _pattern_accent_first(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Prima nota accentata, altre morbide"""
        result = []
        for i, note in enumerate(notes):
            if i == 0:
                # Prima nota accentata
                result.append(NoteEvent(
                    note=note.note,
                    octave=note.octave,
                    duration=base_duration * 1.2,
                    volume=note.volume * 1.5
                ))
            else:
                # Altre note morbide
                result.append(NoteEvent(
                    note=note.note,
                    octave=note.octave,
                    duration=base_duration * 0.8,
                    volume=note.volume * 0.5
                ))
        return result
    
    def _pattern_swing(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Timing swing su note alternate"""
        result = []
        for i, note in enumerate(notes):
            if i % 2 == 0:
                # Note pari: durata normale
                result.append(NoteEvent(
                    note=note.note,
                    octave=note.octave,
                    duration=base_duration,
                    volume=note.volume
                ))
            else:
                # Note dispari: durata swing (più lunga)
                result.append(NoteEvent(
                    note=note.note,
                    octave=note.octave,
                    duration=base_duration * 1.5,
                    volume=note.volume
                ))
        return result
    
    # Pattern Random
    def _pattern_random_chaos(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Caos totale: ordine, durata e volume completamente casuali"""
        result = []
        # Mescola completamente le note
        shuffled_notes = notes.copy()
        random.shuffle(shuffled_notes)
        
        for note in shuffled_notes:
            # Durata casuale tra 0.1x e 2.0x la durata base
            random_duration = base_duration * random.uniform(0.1, 2.0)
            # Volume casuale tra 0.3 e 1.0
            random_volume = random.uniform(0.3, 1.0)
            # Ritardo casuale tra 0 e 0.5 secondi
            random_delay = random.uniform(0, 0.5)
            
            result.append(NoteEvent(
                note=note.note,
                octave=note.octave,
                duration=random_duration,
                volume=random_volume,
                delay=random_delay
            ))
        return result
    
    def _pattern_random_rhythm(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Ritmo casuale: note normali ma con durate e pause imprevedibili"""
        result = []
        for note in notes:
            # Durata casuale ma più controllata
            rhythm_multiplier = random.choice([0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0])
            random_duration = base_duration * rhythm_multiplier
            
            # Pausa casuale dopo ogni nota (50% probabilità)
            random_delay = random.uniform(0, 0.3) if random.random() < 0.5 else 0
            
            result.append(NoteEvent(
                note=note.note,
                octave=note.octave,
                duration=random_duration,
                volume=note.volume,
                delay=random_delay
            ))
        return result
    
    def _pattern_random_volume(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Volume casuale: note normali ma con volumi drammaticamente diversi"""
        result = []
        for note in notes:
            # Volume molto variabile: da pianissimo a fortissimo
            volume_levels = [0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
            random_volume = random.choice(volume_levels)
            
            # Leggera variazione di durata per enfatizzare il volume
            duration_multiplier = 0.8 + (random_volume * 0.4)  # Durata correlata al volume
            random_duration = base_duration * duration_multiplier
            
            result.append(NoteEvent(
                note=note.note,
                octave=note.octave,
                duration=random_duration,
                volume=random_volume
            ))
        return result
    
    def _pattern_random_changing(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Cambiamento continuo: ogni nota può essere sostituita casualmente"""
        result = []
        for note in notes:
            # 30% di probabilità di sostituire la nota con una casuale
            if random.random() < 0.3:
                # Sceglie una nota casuale dallo stesso accordo
                random_note = random.choice(notes)
                selected_note = random_note.note
                selected_octave = random_note.octave
            else:
                selected_note = note.note
                selected_octave = note.octave
            
            # Durata leggermente variabile
            random_duration = base_duration * random.uniform(0.8, 1.2)
            
            # Volume con piccole variazioni
            random_volume = note.volume * random.uniform(0.7, 1.0)
            
            result.append(NoteEvent(
                note=selected_note,
                octave=selected_octave,
                duration=random_duration,
                volume=random_volume
            ))
        return result
    
    def play_pattern(self, sound_cell: SoundCell, pattern_type: PatternType, 
                    octave: int = 4, base_duration: float = 0.3, 
                    loop: bool = False, reverse: bool = False, 
                    duration_octaves: int = 1, playback_speed: float = 1.0, 
                    bpm: int = 120, pause_duration: float = 0.0, callback: Optional[Callable] = None,
                    # MIDI Effects
                    delay_enabled: bool = False, delay_time: float = 0.25, delay_feedback: float = 0.3,
                    delay_mix: float = 0.5, delay_type: str = "quarter", delay_repeats: int = 3,
                    octave_add: int = 0, velocity_curve: str = "linear", velocity_intensity: float = 1.0,
                    accent_enabled: bool = False, accent_strength: float = 0.5, accent_pattern: str = "every_beat",
                    repeater_enabled: bool = False, repeat_count: int = 2, repeat_timing: str = "immediate",
                    chord_gen_enabled: bool = False, chord_variation: str = "inversion", voicing: str = "close"):
        """Riproduce un pattern con le note specificate"""
        if self.is_playing:
            self.stop_pattern()
        
        # Inizializza i parametri correnti
        self.update_parameters(sound_cell, pattern_type, octave, base_duration, loop, reverse, duration_octaves, playback_speed, bpm, pause_duration,
                              delay_enabled, delay_time, delay_feedback, delay_mix, delay_type, delay_repeats,
                              octave_add, velocity_curve, velocity_intensity, accent_enabled, accent_strength, accent_pattern, 
                              repeater_enabled, repeat_count, repeat_timing, chord_gen_enabled, chord_variation, voicing)
        
        self.is_playing = True
        self.is_looping = loop
        self.stop_requested = False
        self.playback_id += 1
        
        def play_worker():
            try:
                iteration_count = 0
                while not self.stop_requested and (not loop or self.is_looping):
                    # Ottieni i parametri correnti (potrebbero essere cambiati durante la riproduzione)
                    params = self.get_current_parameters()
                    current_sound_cell = params['sound_cell']
                    current_pattern_type = params['pattern_type']
                    current_octave = params['octave']
                    current_base_duration = params['base_duration']
                    current_reverse = params['reverse']
                    current_duration_octaves = params['duration_octaves']
                    current_playback_speed = params['playback_speed']
                    current_pause_duration = params['pause_duration']
                    
                    if not current_sound_cell or not current_pattern_type:
                        break
                    
                    # Genera le note del pattern per ogni ottava di durata
                    all_pattern_notes = []
                    
                    # Genera le note per tutte le ottave specificate (sia per MIDI che pygame)
                    for octave_offset in range(current_duration_octaves):
                        octave_to_use = current_octave + octave_offset
                        pattern_notes = self.generate_pattern_notes(current_sound_cell, current_pattern_type, octave_to_use, current_base_duration)
                        all_pattern_notes.extend(pattern_notes)
                    
                    # Debug info (commentato per ridurre output)
                    # if self.midi_output and self.midi_output.initialized and self.midi_output.output_port:
                    #     print(f"MIDI mode: Generated {len(all_pattern_notes)} notes for {current_duration_octaves} octaves")
                    # else:
                    #     print(f"Pygame mode: Generated {len(all_pattern_notes)} notes for {current_duration_octaves} octaves")
                    
                    # Applica reverse se richiesto
                    if current_reverse:
                        all_pattern_notes = list(reversed(all_pattern_notes))
                    
                    # Riproduce le note con timing corretto
                    for i, note_event in enumerate(all_pattern_notes):
                        if self.stop_requested:
                            break

                        # Calcola il numero MIDI
                        midi_note = self.midi_generator.note_to_midi_number(note_event.note, note_event.octave)

                        # Applica il ritardo se specificato (applica la velocità di riproduzione)
                        if note_event.delay > 0:
                            time.sleep(note_event.delay / current_playback_speed)

                        if self.stop_requested:
                            break

                        # La durata regola il tempo tra le note
                        adjusted_duration = note_event.duration / current_playback_speed
                        
                        # Riproduce la nota (ora non bloccante)
                        self._play_single_note(midi_note, adjusted_duration, note_event.volume, i, len(all_pattern_notes))
                        
                        # Il thread principale ora funge da metronomo, attendendo la durata della nota
                        # prima di passare alla successiva.
                        time.sleep(adjusted_duration)
                    
                    # Se non è in loop, esce dopo una volta
                    if not loop:
                        break
                    
                    # Non limitare le iterazioni per MIDI - permette loop completo
                    # Il controllo del loop è gestito dalla variabile loop e is_looping
                    
                    # Incrementa il contatore delle iterazioni per debug
                    iteration_count += 1
                    
                    # Aggiunge pausa tra le ripetizioni del pattern se specificata
                    if current_pause_duration > 0:
                        # Controlla se dobbiamo fermarci durante la pausa
                        pause_chunks = int(current_pause_duration / 0.01) + 1
                        for _ in range(pause_chunks):
                            if self.stop_requested:
                                break
                            time.sleep(0.01)
                
            except (OSError, RuntimeError, ValueError) as e:
                print(f"Errore nella riproduzione del pattern: {e}")
            finally:
                self.is_playing = False
                if callback:
                    callback()
        
        self.current_thread = threading.Thread(target=play_worker)
        self.current_thread.daemon = True
        self.current_thread.start()
    
    def _play_single_note(self, midi_note: int, step_duration: float, volume: float, note_index: int = 0, total_notes: int = 1):
        """Riproduce una singola nota in modo non bloccante con controlli di stop"""
        try:
            if self.stop_requested:
                return
            
            # Se MIDI è configurato, invia via MIDI
            if self.midi_output and self.midi_output.initialized and self.midi_output.output_port:
                if not isinstance(midi_note, int):
                    print(f"WARNING: midi_note in _play_single_note is not int: {type(midi_note)} = {midi_note}")
                    midi_note = int(midi_note) if isinstance(midi_note, (int, float)) else 60
                self._play_single_note_midi(midi_note, step_duration, volume, note_index, total_notes)
                return
                
            # Altrimenti usa pygame
            self._play_single_note_pygame(midi_note, step_duration, volume)
        except (OSError, RuntimeError, ValueError) as e:
            print(f"Errore nella riproduzione della nota: {e}")
    
    def _apply_midi_effects(self, midi_note: int, velocity: int, note_index: int = 0, total_notes: int = 1):
        """Applica gli effetti MIDI a una nota"""
        # Ottieni i parametri correnti
        params = self.get_current_parameters()
        
        # Ottava addition
        if params['octave_add'] != 0:
            midi_note += params['octave_add'] * 12
            midi_note = max(0, min(127, midi_note))  # Clamp to valid MIDI range
        
        # Velocity curve
        if params['velocity_curve'] != "linear":
            velocity = self._apply_velocity_curve(velocity, note_index, total_notes, params['velocity_curve'], params['velocity_intensity'])
        
        # Accent patterns
        if params['accent_enabled']:
            velocity = self._apply_accent_pattern(velocity, note_index, total_notes, params['accent_pattern'], params['accent_strength'])
        
        return midi_note, velocity
    
    def _apply_delay_effect(self, midi_note: int, velocity: int, duration: float):
        """Applica l'effetto delay (MIDI echo) con controlli avanzati"""
        params = self.get_current_parameters()
        
        if not params['delay_enabled']:
            return [(midi_note, velocity, duration)]
        
        # Parametri del delay
        feedback = params['delay_feedback']
        mix = params['delay_mix']
        delay_type = params['delay_type']
        try:
            max_repeats = int(params['delay_repeats'])  # Assicura che sia un intero
        except (ValueError, TypeError):
            max_repeats = 3  # Valore di default
        
        # Crea gli echi
        echoes = []
        
        # Nota originale (dry signal)
        if mix < 1.0:  # Se mix non è 100% wet
            echoes.append((midi_note, velocity, duration))
        
        # Genera gli echi
        current_velocity = velocity
        current_duration = duration
        
        for i in range(max_repeats):
            # Calcola la velocità dell'eco
            current_velocity = int(velocity * (feedback ** (i + 1)))
            if current_velocity < 10:  # Soglia minima
                break
            
            # Calcola la durata dell'eco
            current_duration = duration * (0.8 ** (i + 1))
            
            # Applica il tipo di delay
            if delay_type == "Ping-Pong":
                # Alterna canali (simulato con ottave diverse)
                channel_offset = 12 if i % 2 == 0 else -12
                echo_note = max(0, min(127, midi_note + channel_offset))
            elif delay_type == "Dotted":
                # Delay puntato (1.5x tempo)
                current_duration *= 1.5
                echo_note = midi_note
            elif delay_type == "Triplet":
                # Delay in terzine (0.67x tempo)
                current_duration *= 0.67
                echo_note = midi_note
            elif delay_type == "Reverse":
                # Echi al contrario (ottava più bassa)
                echo_note = max(0, min(127, midi_note - 12))
            elif delay_type == "Stutter":
                # Ripetizioni rapide con durata ridotta
                current_duration *= 0.3
                echo_note = midi_note
            else:  # Standard
                echo_note = midi_note
            
            # Aggiungi l'eco
            echoes.append((echo_note, current_velocity, current_duration))
        
        return echoes
    
    def _apply_repeater_effect(self, midi_note: int, velocity: int, duration: float):
        """Applica l'effetto note repeater"""
        params = self.get_current_parameters()
        
        if not params['repeater_enabled']:
            return [(midi_note, velocity, duration)]
        
        try:
            repeat_count = int(params['repeat_count'])  # Assicura che sia un intero
        except (ValueError, TypeError):
            repeat_count = 2  # Valore di default
        timing = params['repeat_timing']
        
        repeats = []
        
        for i in range(repeat_count):
            if timing == "immediate":
                # Ripetizione immediata
                repeat_duration = duration * 0.3
            elif timing == "staccato":
                # Staccato - note corte e separate
                repeat_duration = duration * 0.2
            elif timing == "legato":
                # Legato - note che si sovrappongono
                repeat_duration = duration * 0.8
            elif timing == "swing":
                # Swing - durata variabile
                repeat_duration = duration * (0.3 if i % 2 == 0 else 0.7)
            else:
                repeat_duration = duration * 0.5
            
            repeats.append((midi_note, velocity, repeat_duration))
        
        return repeats
    
    def _apply_velocity_curve(self, velocity: int, note_index: int, total_notes: int, curve_type: str, intensity: float):
        """Applica una curva di velocità alle note"""
        if curve_type == "linear":
            return velocity
        
        # Normalizza l'indice della nota (0-1)
        normalized_index = note_index / max(1, total_notes - 1) if total_notes > 1 else 0
        
        if curve_type == "exponential":
            # Curva esponenziale crescente
            curve_value = normalized_index ** (1 / intensity)
        elif curve_type == "logarithmic":
            # Curva logaritmica crescente
            curve_value = (normalized_index ** intensity) if intensity > 0 else normalized_index
        elif curve_type == "sine":
            # Curva sinusoidale
            import math
            curve_value = (math.sin(normalized_index * math.pi) + 1) / 2
        elif curve_type == "random":
            # Velocità casuale
            curve_value = random.random()
        else:
            curve_value = normalized_index
        
        # Applica la curva alla velocità
        new_velocity = int(velocity * curve_value * intensity)
        return max(1, min(127, new_velocity))
    
    def _apply_accent_pattern(self, velocity: int, note_index: int, total_notes: int, pattern: str, strength: float):
        """Applica pattern di accento alle note"""
        if pattern == "every_beat":
            # Accentua ogni nota
            accent_multiplier = 1.0 + strength
        elif pattern == "every_other":
            # Accentua ogni altra nota
            accent_multiplier = 1.0 + (strength if note_index % 2 == 0 else 0)
        elif pattern == "random":
            # Accentua casualmente
            accent_multiplier = 1.0 + (strength if random.random() < 0.3 else 0)
        elif pattern == "crescendo":
            # Crescendo - accentua di più verso la fine
            normalized_index = note_index / max(1, total_notes - 1) if total_notes > 1 else 0
            accent_multiplier = 1.0 + (strength * normalized_index)
        elif pattern == "diminuendo":
            # Diminuendo - accentua di più all'inizio
            normalized_index = note_index / max(1, total_notes - 1) if total_notes > 1 else 0
            accent_multiplier = 1.0 + (strength * (1 - normalized_index))
        else:
            accent_multiplier = 1.0
        
        new_velocity = int(velocity * accent_multiplier)
        return max(1, min(127, new_velocity))
    
    def _play_single_note_midi(self, midi_note: int, step_duration: float, volume: float, note_index: int = 0, total_notes: int = 1):
        """Invia messaggi MIDI NOTE ON e schedula NOTE OFF e delay in background."""
        try:
            if self.stop_requested:
                return

            params = self.get_current_parameters()
            velocity = int(volume * 127)
            
            # Calcola la durata del gate (es. 80% della durata del passo)
            gate_duration = step_duration * 0.8 

            # Applica effetti che modificano la nota base (non-temporali)
            midi_note, velocity = self._apply_midi_effects(midi_note, velocity, note_index, total_notes)

            # Gestione del segnale WET (delay) in background
            if params['delay_enabled'] and params['delay_mix'] > 0:
                echo_base_velocity = int(velocity * params['delay_mix'])
                self._play_delay_echoes_async(midi_note, echo_base_velocity, gate_duration, params) # Passa gate_duration

            # Gestione del segnale DRY (nota originale)
            dry_velocity = int(velocity * (1.0 - params['delay_mix']))
            
            if dry_velocity > 0:
                if params['repeater_enabled']:
                    self._play_repeater_async(midi_note, dry_velocity, gate_duration, params) # Passa gate_duration
                else:
                    self.midi_output.send_note_on(midi_note, dry_velocity)
                    
                    def note_off_worker(note, delay):
                        time.sleep(delay)
                        if not self.stop_requested:
                            self.midi_output.send_note_off(note)
                    
                    t = threading.Thread(target=note_off_worker, args=(midi_note, gate_duration)) # Usa gate_duration
                    t.daemon = True
                    t.start()
            # La funzione non attende (non è bloccante), il timing è gestito dal chiamante (play_worker)

        except (OSError, RuntimeError, AttributeError) as e:
            print(f"Errore nell'invio MIDI: {e}")

    def _play_delay_echoes_async(self, midi_note: int, velocity: int, duration: float, params: dict):
        """Genera e riproduce gli echi del delay in un thread separato, in modo sincrono all'interno del thread."""
        def delay_worker():
            delay_time = params['delay_time']
            feedback = params['delay_feedback']
            max_repeats = params['delay_repeats']
            delay_type = params['delay_type']
            playback_speed = params.get('playback_speed', 1.0)  # Get playback_speed safely

            # Calcola il tempo di delay effettivo in base al tipo prima del loop
            actual_delay_time = delay_time
            if delay_type == "Dotted":
                actual_delay_time *= 1.5
            elif delay_type == "Triplet":
                actual_delay_time *= 0.67

            # Applica la velocità di riproduzione al tempo di delay
            adjusted_delay_time = actual_delay_time / playback_speed if playback_speed > 0 else actual_delay_time

            for i in range(max_repeats):
                # Usa il tempo di delay calcolato e costante per ogni eco
                time.sleep(adjusted_delay_time)
                if self.stop_requested: return

                echo_velocity = int(velocity * (feedback ** (i + 1)))
                # Abbassa la soglia per permettere più ripetizioni a basso volume
                if echo_velocity < 2: break

                echo_duration = duration * (0.8 ** (i + 1))
                echo_note = self._get_echo_note(midi_note, i, delay_type)

                if params['repeater_enabled']:
                    repeated_echoes = self._apply_repeater_effect(echo_note, echo_velocity, echo_duration)
                    for r_note, r_vel, r_dur in repeated_echoes:
                        if self.stop_requested: break
                        self.midi_output.send_note_on(r_note, r_vel)
                        time.sleep(r_dur)
                        if not self.stop_requested:
                            self.midi_output.send_note_off(r_note)
                else:
                    self.midi_output.send_note_on(echo_note, echo_velocity)
                    time.sleep(echo_duration)
                    if not self.stop_requested:
                        self.midi_output.send_note_off(echo_note)

        t = threading.Thread(target=delay_worker)
        t.daemon = True
        t.start()

    def _play_repeater_async(self, midi_note: int, velocity: int, duration: float, params: dict):
        """Esegue l'effetto repeater in un thread separato."""
        def repeater_worker():
            repeated_notes = self._apply_repeater_effect(midi_note, velocity, duration)
            for r_note, r_vel, r_dur in repeated_notes:
                if self.stop_requested: break
                self.midi_output.send_note_on(r_note, r_vel)
                time.sleep(r_dur)
                if not self.stop_requested:
                    self.midi_output.send_note_off(r_note)

        t = threading.Thread(target=repeater_worker)
        t.daemon = True
        t.start()

    def _get_echo_note(self, base_note: int, echo_index: int, delay_type: str) -> int:
        """Calcola la nota MIDI per un eco in base al tipo di delay."""
        if delay_type == "Ping-Pong":
            offset = 12 if echo_index % 2 == 0 else -12
            return max(0, min(127, base_note + offset))
        elif delay_type == "Reverse":
            return max(0, min(127, base_note - 12))
        return base_note
    
    def _play_single_note_pygame(self, midi_note: int, step_duration: float, volume: float):
        """Riproduce una singola nota via pygame con gate duration."""
        try:
            if self.stop_requested:
                return

            # Calcola la durata del gate (es. 80% della durata del passo)
            gate_duration = step_duration * 0.8 
            
            # Calcola la frequenza dalla nota MIDI
            frequency = 440.0 * (2 ** ((midi_note - 69) / 12.0))
            
            # Crea un tono sinusoidale
            sample_rate = 22050
            frames = int(gate_duration * sample_rate) # Usa gate_duration per i frames
            
            # Genera onda sinusoidale usando numpy se disponibile
            try:
                import numpy as np
                t = np.linspace(0, gate_duration, frames, False) # Usa gate_duration
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
                
                # Riproduce il suono in un thread separato per non bloccare il metronomo
                import pygame
                sound = pygame.sndarray.make_sound(stereo_wave)
                
                def pygame_note_worker(s, d):
                    s.play()
                    time.sleep(d) # Attende la gate_duration
                    s.stop() # Ferma il suono dopo la gate_duration
                
                t = threading.Thread(target=pygame_note_worker, args=(sound, gate_duration))
                t.daemon = True
                t.start()
                
            except ImportError:
                # Fallback senza numpy
                import math
                import pygame
                arr = []
                for j in range(frames):
                    time_val = j / sample_rate
                    # Genera onda sinusoidale semplice
                    wave_val = math.sin(2 * np.pi * frequency * time_val)
                    
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
                
                sound = pygame.sndarray.make_sound(arr)
                
                def pygame_note_worker(s, d):
                    s.play()
                    time.sleep(d) # Attende la gate_duration
                    s.stop() # Ferma il suono dopo la gate_duration
                
                t = threading.Thread(target=pygame_note_worker, args=(sound, gate_duration))
                t.daemon = True
                t.start()
                
        except (OSError, RuntimeError, ValueError) as e:
            print(f"Errore nella riproduzione della nota: {e}")
    
    def stop_pattern(self):
        """Ferma la riproduzione del pattern"""
        self.stop_requested = True
        self.is_playing = False
        self.is_looping = False
        
        # Ferma TUTTE le note MIDI immediatamente
        if self.midi_output and self.midi_output.initialized and self.midi_output.output_port:
            self.midi_output.stop_all_notes()
        
        # Aspetta che il thread finisca prima di fermare i suoni pygame
        if self.current_thread and self.current_thread.is_alive():
            self.current_thread.join(timeout=0.2)
        
        # Ferma tutti i suoni pygame solo dopo che il thread è finito
        try:
            import pygame
            pygame.mixer.stop()
        except (OSError, RuntimeError, AttributeError):
            pass
    
    def is_pattern_playing(self) -> bool:
        """Controlla se un pattern è attualmente in riproduzione"""
        return self.is_playing
