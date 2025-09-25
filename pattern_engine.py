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
from chord_generator import Note, SoundCell, MIDIScaleGenerator


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
    
    def __init__(self, midi_generator: MIDIScaleGenerator):
        self.midi_generator = midi_generator
        self.is_playing = False
        self.is_looping = False
        self.stop_requested = False
        self.current_thread: Optional[threading.Thread] = None
        self.playback_id = 0
        
    def generate_pattern_notes(self, sound_cell: SoundCell, pattern_type: PatternType, 
                             octave: int = 4, base_duration: float = 0.3) -> List[NoteEvent]:
        """Genera una sequenza di note basata sul pattern selezionato"""
        notes = sound_cell.notes
        if not notes:
            return []
        
        # Genera le note base per l'ottava specificata
        base_notes = self._generate_base_notes(notes, octave)
        
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
        else:
            return self._pattern_up(base_notes, base_duration)  # Default
    
    def _generate_base_notes(self, notes: List[Note], octave: int) -> List[NoteEvent]:
        """Genera le note base per l'ottava specificata"""
        base_notes = []
        for i, note in enumerate(notes):
            # Calcola l'ottava corretta per ogni nota
            target_octave = octave + (i // 12)  # Aumenta l'ottava ogni 12 note
            base_notes.append(NoteEvent(
                note=note,
                octave=target_octave,
                duration=0.3,
                volume=0.7
            ))
        return base_notes
    
    # Pattern Base
    def _pattern_up(self, notes: List[NoteEvent], base_duration: float) -> List[NoteEvent]:
        """Ascendente semplice (C→E→G→C)"""
        result = []
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
        # Giù
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
    
    def play_pattern(self, sound_cell: SoundCell, pattern_type: PatternType, 
                    octave: int = 4, base_duration: float = 0.3, 
                    loop: bool = False, reverse: bool = False, 
                    duration_octaves: int = 1, callback: Optional[Callable] = None):
        """Riproduce un pattern con le note specificate"""
        if self.is_playing:
            self.stop_pattern()
        
        self.is_playing = True
        self.is_looping = loop
        self.stop_requested = False
        self.playback_id += 1
        current_playback_id = self.playback_id
        
        def play_worker():
            try:
                while not self.stop_requested and (not loop or self.is_looping):
                    # Genera le note del pattern per ogni ottava di durata
                    all_pattern_notes = []
                    for octave_offset in range(duration_octaves):
                        current_octave = octave + octave_offset
                        pattern_notes = self.generate_pattern_notes(sound_cell, pattern_type, current_octave, base_duration)
                        all_pattern_notes.extend(pattern_notes)
                    
                    # Applica reverse se richiesto
                    if reverse:
                        all_pattern_notes = list(reversed(all_pattern_notes))
                    
                    # Riproduce le note
                    for note_event in all_pattern_notes:
                        if self.stop_requested or self.playback_id != current_playback_id:
                            break
                        
                        # Calcola il numero MIDI
                        midi_note = self.midi_generator.note_to_midi_number(note_event.note, note_event.octave)
                        
                        # Applica il ritardo se specificato
                        if note_event.delay > 0:
                            time.sleep(note_event.delay)
                        
                        if self.stop_requested or self.playback_id != current_playback_id:
                            break
                        
                        # Riproduce la nota
                        self._play_single_note(midi_note, note_event.duration, note_event.volume)
                        
                        # Pausa tra le note
                        if not self.stop_requested and self.playback_id == current_playback_id:
                            time.sleep(base_duration * 0.1)
                    
                    # Se non è in loop, esce dopo una volta
                    if not loop:
                        break
                    
                    # Pausa tra le ripetizioni del pattern
                    if not self.stop_requested and self.is_looping:
                        time.sleep(base_duration * 0.5)
                
            except (OSError, RuntimeError, ValueError) as e:
                print(f"Errore nella riproduzione del pattern: {e}")
            finally:
                self.is_playing = False
                if callback:
                    callback()
        
        self.current_thread = threading.Thread(target=play_worker)
        self.current_thread.daemon = True
        self.current_thread.start()
    
    def _play_single_note(self, midi_note: int, duration: float, volume: float):
        """Riproduce una singola nota"""
        try:
            # Calcola la frequenza dalla nota MIDI
            frequency = 440.0 * (2 ** ((midi_note - 69) / 12.0))
            
            # Crea un tono sinusoidale
            sample_rate = 22050
            frames = int(duration * sample_rate)
            
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
                
                # Riproduce il suono
                import pygame
                sound = pygame.sndarray.make_sound(stereo_wave)
                sound.play()
                
            except ImportError:
                # Fallback senza numpy
                import math
                import pygame
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
                
                # Riproduce il suono
                sound = pygame.sndarray.make_sound(arr)
                sound.play()
                
        except (OSError, RuntimeError, ValueError) as e:
            print(f"Errore nella riproduzione della nota: {e}")
    
    def stop_pattern(self):
        """Ferma la riproduzione del pattern"""
        self.stop_requested = True
        self.is_playing = False
        self.is_looping = False
        
        # Ferma tutti i suoni pygame
        try:
            import pygame
            pygame.mixer.stop()
        except (OSError, RuntimeError, AttributeError):
            pass
        
        # Aspetta che il thread finisca
        if self.current_thread and self.current_thread.is_alive():
            self.current_thread.join(timeout=0.1)
    
    def is_pattern_playing(self) -> bool:
        """Controlla se un pattern è attualmente in riproduzione"""
        return self.is_playing
