# Documentazione Tecnica - Chord Generator

## Architettura del Sistema

### Classi Principali

#### `Note` (Enum)
Rappresenta le 12 note cromatiche del sistema temperato:
- Valori: 0-11 (C=0, C#=1, ..., B=11)
- Utilizzo: Identificazione univoca delle note musicali

#### `Chord` (Dataclass)
Rappresenta un accordo musicale:
- `notes`: Lista delle note che compongono l'accordo
- `root`: Nota radice dell'accordo
- `__str__()`: Rappresentazione stringa per visualizzazione

#### `CircleOfFifths`
Gestisce il circolo delle quinte:
- `get_fifth_up(note)`: Calcola la quinta ascendente (7 semitoni)
- `get_fifth_down(note)`: Calcola la quinta discendente (-7 semitoni)
- `get_interval(root, semitones)`: Calcola intervalli generici

#### `ChordGenerator`
Genera la struttura triangolare degli accordi:
- `generate_triangular_chords(root_note)`: Genera tutti i 12 livelli
- `_build_chord_notes(root, level, position)`: Costruisce un accordo specifico

#### `ChordDisplayApp`
Interfaccia grafica Tkinter:
- Gestione dell'UI e interazione utente
- Visualizzazione degli accordi in formato triangolare
- Selezione della nota radice

## Algoritmo di Generazione

### Struttura Triangolare

La struttura segue il pattern:
```
Livello 1: 1 accordo
Livello 2: 2 accordi  
Livello 3: 3 accordi
...
Livello 12: 12 accordi
```

### Logica di Costruzione

Per ogni livello `n` e posizione `p`:

1. **Posizione 0**: Solo quinte discendenti
   - Aggiunge `n` quinte discendenti a sinistra della nota radice
   
2. **Posizione n**: Solo quinte ascendenti
   - Aggiunge `n` quinte ascendenti a destra della nota radice
   
3. **Posizioni intermedie**: Mix di quinte
   - Aggiunge `p` quinte discendenti a sinistra
   - Aggiunge `n-p` quinte ascendenti a destra

### Esempio di Costruzione

**Livello 3 (n=2):**
- Posizione 0: `[Bb, F, C]` (2 quinte discendenti)
- Posizione 1: `[F, C, G]` (1 quinta discendente, 1 ascendente)
- Posizione 2: `[C, G, D]` (2 quinte ascendenti)

## Gestione delle Note

### Circolo delle Quinte

Il circolo delle quinte è implementato tramite aritmetica modulare:
```python
def get_fifth_up(self, note: Note) -> Note:
    return Note((note.value + 7) % 12)

def get_fifth_down(self, note: Note) -> Note:
    return Note((note.value - 7) % 12)
```

### Mappatura Note

| Nota | Valore | Quinta Su | Quinta Giù |
|------|--------|-----------|------------|
| C    | 0      | G (7)     | F (5)      |
| C#   | 1      | G# (8)    | F# (6)     |
| D    | 2      | A (9)     | G (7)      |
| ...  | ...    | ...       | ...        |

## Interfaccia Utente

### Architettura Tkinter

```
ChordDisplayApp
├── setup_ui()
│   ├── main_frame
│   ├── root_frame (selezione nota)
│   └── chord_frame (visualizzazione)
├── generate_chords()
└── display_chords()
```

### Componenti UI

1. **Frame Principale**: Contenitore principale con padding
2. **Frame Selezione**: Combobox per nota radice + pulsante generazione
3. **Frame Accordi**: Canvas scrollabile per visualizzazione
4. **Scrollbar**: Navigazione verticale per livelli multipli

## Test e Qualità

### Test Unitari

- **TestCircleOfFifths**: Verifica calcoli quinte
- **TestChordGenerator**: Verifica generazione accordi
- **TestChord**: Verifica rappresentazione accordi

### Copertura Test

- ✅ Calcoli circolo delle quinte
- ✅ Struttura triangolare
- ✅ Generazione accordi per livelli 1-3
- ✅ Rappresentazione stringa accordi

### Best Practices Implementate

1. **Type Hints**: Completi per tutte le funzioni
2. **Docstring**: Documentazione per classi e metodi
3. **Error Handling**: Gestione eccezioni appropriata
4. **Modularità**: Separazione responsabilità per classe
5. **Testability**: Codice facilmente testabile
6. **Configurabilità**: Parametri configurabili

## Estensibilità

### Aggiunta Nuove Funzionalità

1. **Nuovi Tipi di Accordi**: Estendere `ChordGenerator`
2. **Visualizzazioni Alternative**: Creare nuove classi UI
3. **Esportazione Formati**: Implementare serializzatori
4. **Analisi Armonica**: Aggiungere analizzatori

### Esempi di Estensione

```python
class ExtendedChordGenerator(ChordGenerator):
    def generate_seventh_chords(self, root: Note):
        # Implementazione accordi di settima
        pass
    
    def generate_chord_inversions(self, chord: Chord):
        # Implementazione inversioni
        pass
```

## Performance

### Complessità Computazionale

- **Generazione Livello n**: O(n²)
- **Generazione Completa**: O(n³) dove n=12
- **Memoria**: O(n²) per storage accordi

### Ottimizzazioni

1. **Caching**: Cache per accordi già calcolati
2. **Lazy Loading**: Generazione on-demand per livelli alti
3. **Compressione**: Storage efficiente per note duplicate

## Sicurezza

### Validazione Input

- Controllo range note (0-11)
- Validazione parametri livello
- Sanitizzazione input utente

### Gestione Errori

- Eccezioni specifiche per errori musicali
- Fallback per input non validi
- Logging per debugging

## Compatibilità

### Versioni Python

- **Minima**: Python 3.7+
- **Testata**: Python 3.7, 3.8, 3.9, 3.10, 3.11
- **Raccomandata**: Python 3.9+

### Dipendenze

- **Tkinter**: Incluso in Python standard
- **Pillow**: Per eventuali estensioni grafiche
- **typing**: Per type hints (Python 3.5+)

## Deployment

### Installazione

```bash
# Sviluppo
pip install -r requirements.txt

# Produzione
pip install -e .
```

### Distribuzione

- **Wheel**: `python setup.py bdist_wheel`
- **Source**: `python setup.py sdist`
- **Executable**: PyInstaller per eseguibili standalone
