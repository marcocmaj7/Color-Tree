#!/usr/bin/env python3
"""
Test script per verificare che il dropdown MIDI si apra esclusivamente verso l'alto
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Aggiungi il percorso del progetto per importare i moduli
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chord_generator import ColorTreeDisplayApp

def test_midi_dropdown():
    """Test per verificare il comportamento del dropdown MIDI"""
    print("Avvio test del dropdown MIDI...")
    
    try:
        # Crea l'applicazione
        app = ColorTreeDisplayApp()
        
        # Verifica che il dropdown sia configurato correttamente
        if hasattr(app, 'midi_combo') and app.midi_combo:
            print("✓ Combobox MIDI trovato")
            
            # Verifica che il postcommand sia configurato
            postcommand = app.midi_combo.cget('postcommand')
            if postcommand:
                print("✓ Postcommand configurato per apertura verso l'alto")
            else:
                print("✗ Postcommand non configurato")
                
            # Verifica che i binding siano configurati
            bindings = app.midi_combo.bind()
            if '<Button-1>' in bindings:
                print("✓ Binding per click configurato")
            else:
                print("✗ Binding per click non configurato")
                
            print("\nTest completato. Il dropdown MIDI dovrebbe:")
            print("- Aprirsi verso l'alto quando cliccato")
            print("- Selezionare e chiudere con UN SOLO CLICK del mouse")
            print("- Chiudersi quando si clicca fuori")
            print("- Funzionare solo con il mouse (nessuna tastiera necessaria)")
            print("\nClicca sul dropdown MIDI per testare il comportamento.")
            
        else:
            print("✗ Combobox MIDI non trovato")
            
        # Avvia l'applicazione per test manuale
        app.run()
        
    except Exception as e:
        print(f"Errore durante il test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_midi_dropdown()
