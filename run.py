#!/usr/bin/env python3
"""
Script di avvio rapido per Chord Generator
"""

import sys
import os

# Aggiunge la directory corrente al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chord_generator import main

if __name__ == "__main__":
    main()
