# Documentazione Funzionalità Intervalli

## Panoramica

La funzionalità degli intervalli permette di visualizzare gli accordi generati sia come note musicali che come intervalli rispetto alla nota radice. Questo è particolarmente utile per l'analisi armonica e la comprensione della struttura degli accordi.

## Caratteristiche Principali

### 1. Visualizzazione Duale
- **Modalità Note**: Mostra gli accordi come note musicali (es. C - E - G)
- **Modalità Intervalli**: Mostra gli accordi come intervalli (es. T - 3 - 5)

### 2. Calcolo Automatico degli Intervalli
- Calcolo automatico degli intervalli rispetto alla nota radice
- Supporto per tutti i tipi di intervalli (maggiori, minori, diminuiti, aumentati)
- Gestione corretta delle note alterate

### 3. Simboli degli Intervalli
- `T` = Tonic (Tonica)
- `2` = Seconda maggiore
- `b3` = Terza minore
- `3` = Terza maggiore
- `4` = Quarta giusta
- `5` = Quinta giusta
- `b5` = Quinta diminuita
- `6` = Sesta maggiore
- `b6` = Sesta minore
- `7` = Settima maggiore
- `b7` = Settima minore

## Utilizzo

### Interfaccia Grafica

1. **Avvia l'applicazione**:
   ```bash
   python chord_generator.py
   ```

2. **Seleziona la modalità di visualizzazione**:
   - Usa i radio button "Note" o "Intervalli"
   - La visualizzazione cambia istantaneamente

3. **Cambia la nota radice**:
   - Usa il menu a tendina per selezionare la nota radice
   - Gli intervalli si aggiornano automaticamente

### Interfaccia CLI

```bash
# Visualizza note
python cli_example.py --root C --levels 5

# Visualizza intervalli
python cli_example.py --root C --levels 5 --display intervals

# Esporta in JSON con intervalli
python cli_example.py --root G --levels 3 --format json --display intervals
```

### Utilizzo come Libreria

```python
from chord_generator import ChordGenerator, Note, Chord

# Crea il generatore
generator = ChordGenerator()

# Genera accordi
levels = generator.generate_triangular_chords(Note.C)

# Visualizza come note
for level in levels[:3]:
    for chord in level:
        print(f"Note: {chord}")

# Visualizza come intervalli
for level in levels[:3]:
    for chord in level:
        print(f"Intervalli: {chord.to_intervals_string()}")
```

## Esempi Pratici

### Accordi Maggiori e Minori

```python
# Accordo maggiore (C-E-G)
major_chord = Chord([Note.C, Note.E, Note.G], Note.C)
print(f"Note: {major_chord}")           # C - E - G
print(f"Intervalli: {major_chord.to_intervals_string()}")  # T - 3 - 5

# Accordo minore (C-Eb-G)
minor_chord = Chord([Note.C, Note.D_SHARP, Note.G], Note.C)
print(f"Note: {minor_chord}")           # C - D# - G
print(f"Intervalli: {minor_chord.to_intervals_string()}")  # T - b3 - 5
```

### Accordi di Settima

```python
# Accordo di settima maggiore (C-E-G-B)
major_7th = Chord([Note.C, Note.E, Note.G, Note.B], Note.C)
print(f"Note: {major_7th}")             # C - E - G - B
print(f"Intervalli: {major_7th.to_intervals_string()}")  # T - 3 - 5 - 7

# Accordo di settima minore (C-E-G-Bb)
minor_7th = Chord([Note.C, Note.E, Note.G, Note.A_SHARP], Note.C)
print(f"Note: {minor_7th}")             # C - E - G - A#
print(f"Intervalli: {minor_7th.to_intervals_string()}")  # T - 3 - 5 - b7
```

### Accordi Alterati

```python
# Accordo con quinta diminuita (C-E-Gb)
dim_chord = Chord([Note.C, Note.E, Note.F_SHARP], Note.C)
print(f"Note: {dim_chord}")             # C - E - F#
print(f"Intervalli: {dim_chord.to_intervals_string()}")  # T - 3 - b5

# Accordo con sesta maggiore (C-E-G-A)
sixth_chord = Chord([Note.C, Note.E, Note.G, Note.A], Note.C)
print(f"Note: {sixth_chord}")           # C - E - G - A
print(f"Intervalli: {sixth_chord.to_intervals_string()}")  # T - 3 - 5 - 6
```

## Analisi degli Intervalli

### Metodi Disponibili

```python
chord = Chord([Note.C, Note.E, Note.G], Note.C)

# Ottieni lista degli intervalli
intervals = chord.get_intervals()
print(intervals)  # ['T', '3', '5']

# Ottieni stringa degli intervalli
interval_string = chord.to_intervals_string()
print(interval_string)  # T - 3 - 5
```

### Analisi Dettagliata

```python
def analyze_chord_intervals(chord):
    """Analizza gli intervalli di un accordo"""
    intervals = chord.get_intervals()
    
    analysis = {
        'has_third': '3' in intervals or 'b3' in intervals,
        'has_fifth': '5' in intervals or 'b5' in intervals,
        'has_seventh': '7' in intervals or 'b7' in intervals,
        'is_major': '3' in intervals,
        'is_minor': 'b3' in intervals,
        'is_diminished': 'b5' in intervals,
        'is_augmented': 'b5' in intervals and '3' in intervals
    }
    
    return analysis
```

## Configurazione

### File di Configurazione

```python
# config.py
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
    'show_interval_names': False,
    'interval_separator': ' - '
}
```

### Personalizzazione

```python
# Modifica il separatore degli intervalli
chord.to_intervals_string()  # T - 3 - 5

# Modifica la configurazione
INTERVAL_CONFIG['interval_separator'] = ' | '
chord.to_intervals_string()  # T | 3 | 5
```

## Esportazione

### Formato JSON

```json
{
  "levels": [
    {
      "level": 1,
      "chords": [
        {
          "position": 1,
          "notes": ["C"],
          "root": "C",
          "representation": "C",
          "intervals": ["T"],
          "intervals_string": "T"
        }
      ]
    }
  ]
}
```

### Formato CSV

```csv
Livello,Posizione,Note,Radice,Rappresentazione,Intervalli
1,1,C,C,C,T
2,1,"F - C",C,"F - C","4 - T"
2,2,"C - G",C,"C - G","T - 5"
```

## Best Practices

### 1. Utilizzo Consistente
- Usa sempre la stessa modalità di visualizzazione per confronti
- Mantieni la nota radice costante per analisi comparative

### 2. Analisi Armonica
- Usa gli intervalli per identificare il tipo di accordo
- Confronta gli intervalli per trovare pattern comuni

### 3. Esportazione
- Usa il formato JSON per dati strutturati
- Usa il formato CSV per analisi in fogli di calcolo

## Troubleshooting

### Problemi Comuni

1. **Intervalli non corretti**:
   - Verifica che la nota radice sia corretta
   - Controlla che le note siano nell'ordine giusto

2. **Simboli non riconosciuti**:
   - Verifica la configurazione degli intervalli
   - Controlla che i simboli siano supportati

3. **Visualizzazione errata**:
   - Verifica la modalità di visualizzazione selezionata
   - Controlla la configurazione dell'applicazione

### Debug

```python
# Debug degli intervalli
chord = Chord([Note.C, Note.E, Note.G], Note.C)
print(f"Note: {chord.notes}")
print(f"Root: {chord.root}")
print(f"Intervalli: {chord.get_intervals()}")
print(f"Stringa: {chord.to_intervals_string()}")
```

## Sviluppi Futuri

- [ ] Supporto per intervalli composti
- [ ] Analisi armonica avanzata
- [ ] Esportazione in formato MIDI
- [ ] Visualizzazione sul pentagramma
- [ ] Supporto per accordi estesi (9, 11, 13)
