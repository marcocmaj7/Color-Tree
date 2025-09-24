# Generatore di Accordi - Circolo delle Quinte

Un'applicazione Python per generare accordi seguendo il circolo delle quinte in una struttura triangolare.

## Caratteristiche

- **Struttura triangolare**: 12 livelli che rappresentano le 12 note cromatiche
- **Circolo delle quinte**: Calcolo automatico delle quinte ascendenti e discendenti
- **Interfaccia grafica**: Visualizzazione intuitiva degli accordi generati
- **Selezione nota radice**: Possibilità di cambiare la nota di partenza
- **Visualizzazione duale**: Mostra accordi sia come note che come intervalli (T, 3, 5, b7, etc.)
- **🎵 Riproduzione MIDI**: Clicca su qualsiasi box per ascoltare la scala corrispondente
- **Interfaccia CLI**: Comando da riga di comando con opzioni avanzate
- **Architettura modulare**: Codice ben strutturato seguendo le best practices Python

## Struttura del Progetto

```
├── chord_generator.py      # Applicazione principale
├── test_chord_generator.py # Test unitari
├── requirements.txt        # Dipendenze
└── README.md              # Documentazione
```

## Come Funziona

### Livello 1
- Solo la nota radice (es. C)

### Livello 2
- C F (quinta discendente)
- C G (quinta ascendente)

### Livello 3
- C F Bb (due quinte discendenti)
- C F G (una quinta discendente, una ascendente)
- C D G (una quinta ascendente, una terza maggiore)

E così via per tutti i 12 livelli...

## Visualizzazione degli Intervalli

L'app supporta due modalità di visualizzazione:

### Modalità Note
Mostra gli accordi come note musicali:
```
C - E - G
F - C - G
```

### Modalità Intervalli
Mostra gli accordi come intervalli rispetto alla nota radice:
```
T - 3 - 5
4 - T - 5
```

**Simboli degli intervalli:**
- `T` = Tonic (Tonica)
- `2` = Seconda maggiore
- `b3` = Terza minore
- `3` = Terza maggiore
- `4` = Quarta giusta
- `5` = Quinta giusta
- `b7` = Settima minore
- `7` = Settima maggiore

## Installazione

1. Assicurati di avere Python 3.7+ installato
2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
   
   Oppure usa lo script di installazione automatica:
   ```bash
   python install_dependencies.py
   ```

### Dipendenze per la funzionalità MIDI

Per la riproduzione audio, sono necessarie le seguenti librerie:
- `pygame>=2.0.0` - Per la riproduzione audio
- `numpy>=1.20.0` - Per l'elaborazione dei segnali audio

## Utilizzo

### Esecuzione dell'applicazione
```bash
python chord_generator.py
```

### Funzionalità MIDI

L'applicazione ora supporta la riproduzione audio delle scale:
- **Clicca su qualsiasi box** per ascoltare la scala corrispondente
- Le note vengono riprodotte in sequenza con la nota radice più forte
- La riproduzione avviene in un thread separato per non bloccare l'interfaccia

### Test della funzionalità MIDI
```bash
python test_midi.py
```

### Esecuzione da riga di comando
```bash
# Visualizza note
python cli_example.py --root C --levels 5

# Visualizza intervalli
python cli_example.py --root C --levels 5 --display intervals

# Esporta in JSON
python cli_example.py --root G --levels 3 --format json --export chords.json
```

### Esecuzione dei test
```bash
python test_chord_generator.py
```

## Architettura

### Classi Principali

- **`Note`**: Enum per le 12 note cromatiche
- **`Chord`**: Rappresenta un accordo con le sue note
- **`CircleOfFifths`**: Gestisce il circolo delle quinte
- **`ChordGenerator`**: Genera la struttura triangolare degli accordi
- **`ChordDisplayApp`**: Interfaccia grafica Tkinter

### Best Practices Implementate

1. **Type Hints**: Utilizzo completo dei type hints per migliore leggibilità
2. **Dataclasses**: Uso di `@dataclass` per classi semplici
3. **Enum**: Utilizzo di Enum per le note musicali
4. **Separazione delle responsabilità**: Ogni classe ha una responsabilità specifica
5. **Test unitari**: Copertura completa con test automatizzati
6. **Documentazione**: Docstring per tutte le classi e metodi
7. **Gestione errori**: Gestione appropriata delle eccezioni
8. **Interfaccia pulita**: UI intuitiva e responsive

## Esempi di Output

### Modalità Note

#### Livello 1
```
C
```

#### Livello 2
```
F - C    C - G
```

#### Livello 3
```
Bb - F - C    F - C - G    C - G - D
```

### Modalità Intervalli

#### Livello 1
```
T
```

#### Livello 2
```
4 - T    T - 5
```

#### Livello 3
```
b7 - 4 - T    4 - T - 5    T - 5 - 2
```

## Sviluppi Futuri

- [x] ~~Esportazione degli accordi in formato MIDI~~ ✅ Implementato
- [ ] Visualizzazione delle note sul pentagramma
- [ ] Generazione di progressioni armoniche
- [ ] Supporto per diverse tonalità e modi
- [ ] Integrazione con sintetizzatori
- [ ] Controlli di volume e velocità per la riproduzione MIDI
- [ ] Salvataggio delle scale in file MIDI

## Contributi

I contributi sono benvenuti! Per favore:
1. Fork del repository
2. Crea un branch per la tua feature
3. Aggiungi test per le nuove funzionalità
4. Assicurati che tutti i test passino
5. Crea una Pull Request

## Licenza

Questo progetto è rilasciato sotto licenza MIT.
