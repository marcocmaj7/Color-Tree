#!/usr/bin/env python3
"""
Script per installare le dipendenze necessarie per la Color Tree con funzionalità MIDI
"""

import subprocess
import sys
import os

def install_package(package):
    """Installa un pacchetto usando pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Installa tutte le dipendenze necessarie"""
    print("🎵 Installazione dipendenze per Color Tree MIDI...")
    
    # Lista delle dipendenze
    dependencies = [
        "pygame>=2.0.0",
        "numpy>=1.20.0",
        "Pillow>=9.0.0"
    ]
    
    success_count = 0
    total_count = len(dependencies)
    
    for dep in dependencies:
        print(f"\n📦 Installazione di {dep}...")
        if install_package(dep):
            print(f"✅ {dep} installato con successo")
            success_count += 1
        else:
            print(f"❌ Errore nell'installazione di {dep}")
    
    print(f"\n📊 Risultato: {success_count}/{total_count} dipendenze installate")
    
    if success_count == total_count:
        print("🎉 Tutte le dipendenze sono state installate con successo!")
        print("   Ora puoi eseguire: python chord_generator.py")
    else:
        print("⚠️  Alcune dipendenze non sono state installate.")
        print("   Prova a installarle manualmente:")
        for dep in dependencies:
            print(f"   pip install {dep}")

if __name__ == "__main__":
    main()
