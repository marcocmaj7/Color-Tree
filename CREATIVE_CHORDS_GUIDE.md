# 🎵 Guida Creative Chord Patterns

## Come Utilizzare la Funzionalità Creative

### 1. Avvio dell'Applicazione
```bash
python chord_generator.py
```

### 2. Selezione di un Accordo
- Clicca su qualsiasi accordo nella Color Tree per selezionarlo
- L'accordo selezionato verrà evidenziato e memorizzato

### 3. Apertura della Finestra Creative
- Clicca il bottone **"🎵 Creative"** in basso a sinistra
- Si aprirà una nuova finestra con tutti i controlli

### 4. Controlli Disponibili

#### 🎵 **Playback Controls** (In Alto)
- **▶ PLAY** - Avvia la riproduzione del pattern selezionato
- **⏹ STOP** - Ferma la riproduzione
- **🔄 LOOP** - Abilita/disabilita la ripetizione continua

#### ⚙️ **Parameters** (Sotto i controlli di riproduzione)
- **🎼 Octave** - Regola l'ottava (2-6) con slider
- **⏱️ Duration** - Regola la durata delle note (0.1-1.0s) con slider
- I valori correnti sono mostrati in tempo reale

#### 🎼 **Pattern Selection** (Categorie di Pattern)

##### **Base Patterns**
- **Up** - Ascendente semplice (C→E→G→C)
- **Down** - Discendente semplice (C→G→E→C)
- **Up-Down** - Su poi giù (C→E→G→C→G→E)
- **Down-Up** - Giù poi su (C→G→E→C→E→G)

##### **Geometric Patterns**
- **Triangle** - Su-giù-su formando un triangolo melodico
- **Diamond** - Dentro-fuori-dentro (E→G→C→G→E)
- **Zigzag** - Alternanza estremi-centro (C→G→E→C)
- **Spiral** - Giri concentrici espandendosi

##### **Rhythmic Patterns**
- **Gallop** - Due note veloci + una lunga (ta-ta-TAA)
- **Triplet** - Gruppetti di tre note
- **Syncopated** - Enfasi sui tempi deboli
- **Stutter** - Ripetizione rapida della stessa nota

##### **Advanced Patterns**
- **Skip** - Salta note casualmente nel pattern
- **Ghost** - Include note "fantasma" a volume basso
- **Cascade** - Effetto "cascata" con note che si sovrappongono
- **Bounce** - "Rimbalza" tra note estreme

##### **Expressive Patterns**
- **Crescendo** - Volume crescente attraverso l'arpeggio
- **Diminuendo** - Volume decrescente
- **Accent First** - Prima nota accentata, altre morbide
- **Swing** - Timing swing su note alternate

#### 📊 **Status & Log** (In Basso)
- Mostra messaggi di stato e istruzioni
- Log delle azioni eseguite
- Feedback in tempo reale

### 5. Procedura di Utilizzo

1. **Seleziona un accordo** nella Color Tree principale
2. **Clicca "🎵 Creative"** per aprire la finestra
3. **Scegli un pattern** dalle categorie disponibili
4. **Regola i parametri** se necessario:
   - Ottava: 2 (basso) → 6 (alto)
   - Durata: 0.1s (veloce) → 1.0s (lento)
5. **Abilita LOOP** se vuoi ripetizione continua
6. **Clicca "▶ PLAY"** per iniziare la riproduzione
7. **Clicca "⏹ STOP"** per fermare quando vuoi

### 6. Caratteristiche Tecniche

- **Audio Real-time**: Riproduzione immediata con pygame
- **MIDI Support**: Output verso DAW se configurato
- **Pattern Engine**: 20 tipi di pattern diversi
- **Interface Responsive**: Controlli visivi in tempo reale
- **Scroll Support**: Finestra scorrevole per tutti i controlli

### 7. Risoluzione Problemi

#### I controlli non sono visibili?
- La finestra ha una scrollbar verticale - scorri verso il basso
- Assicurati che la finestra sia abbastanza grande (800x600)

#### L'audio non funziona?
- Installa pygame: `pip install pygame`
- Controlla che l'audio del sistema sia attivo

#### La finestra non si apre?
- Assicurati di aver selezionato un accordo prima di cliccare "Creative"
- Controlla che tutti i file siano nella stessa directory

### 8. Esempi di Utilizzo

#### Per Esplorazione Creativa:
1. Seleziona un accordo complesso (livello 8-11)
2. Prova pattern "Spiral" o "Cascade"
3. Regola la durata a 0.5s
4. Abilita LOOP per ascoltare continuamente

#### Per Studio Musicale:
1. Seleziona un accordo semplice (livello 2-4)
2. Prova pattern "Up" o "Down" per arpeggi
3. Regola l'ottava a 4-5
4. Durata 0.3s per velocità media

#### Per Effetti Speciali:
1. Seleziona qualsiasi accordo
2. Prova pattern "Stutter", "Ghost", o "Bounce"
3. Durata molto breve (0.1-0.2s)
4. Abilita LOOP per effetti continui

---

**Buon divertimento con i Creative Chord Patterns! 🎵✨**
