#!/usr/bin/env python3
"""
Esempio di utilizzo da riga di comando per Chord Generator
"""

import argparse
import sys
from chord_generator import ChordGenerator, Note

def main():
    """Funzione principale per CLI"""
    parser = argparse.ArgumentParser(
        description="Generatore di accordi basato sul circolo delle quinte",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi di utilizzo:
  python cli_example.py --root C --levels 5
  python cli_example.py --root G --levels 3 --format json
  python cli_example.py --root F --export chords.txt
        """
    )
    
    parser.add_argument(
        '--root', '-r',
        type=str,
        default='C',
        choices=[note.name.replace('_', '#') for note in Note],
        help='Nota radice per la generazione degli accordi (default: C)'
    )
    
    parser.add_argument(
        '--levels', '-l',
        type=int,
        default=12,
        choices=range(1, 13),
        help='Numero di livelli da generare (1-12, default: 12)'
    )
    
    parser.add_argument(
        '--format', '-f',
        type=str,
        choices=['text', 'json', 'csv'],
        default='text',
        help='Formato di output (default: text)'
    )
    
    parser.add_argument(
        '--display', '-d',
        type=str,
        choices=['notes', 'intervals'],
        default='notes',
        help='Tipo di visualizzazione: notes o intervals (default: notes)'
    )
    
    parser.add_argument(
        '--export', '-e',
        type=str,
        help='File di esportazione (opzionale)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Output verboso con informazioni aggiuntive'
    )
    
    args = parser.parse_args()
    
    try:
        # Converte la nota radice
        root_note_name = args.root.replace('#', '_SHARP')
        root_note = Note[root_note_name]
        
        # Genera gli accordi
        generator = ChordGenerator()
        levels = generator.generate_triangular_chords(root_note)
        
        # Limita i livelli se richiesto
        if args.levels < 12:
            levels = levels[:args.levels]
        
        # Genera l'output
        output = generate_output(levels, args.format, args.verbose, args.display)
        
        # Esporta o stampa
        if args.export:
            with open(args.export, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Accordi esportati in {args.export}")
        else:
            print(output)
            
    except Exception as e:
        print(f"Errore: {e}", file=sys.stderr)
        sys.exit(1)

def generate_output(levels, format_type, verbose, display_mode):
    """Genera l'output nel formato richiesto"""
    
    if format_type == 'json':
        return generate_json_output(levels, verbose, display_mode)
    elif format_type == 'csv':
        return generate_csv_output(levels, verbose, display_mode)
    else:
        return generate_text_output(levels, verbose, display_mode)

def generate_text_output(levels, verbose, display_mode):
    """Genera output in formato testo"""
    output = []
    
    if verbose:
        output.append("=== Generatore di Accordi - Circolo delle Quinte ===")
        output.append(f"Livelli generati: {len(levels)}")
        output.append(f"Totale accordi: {sum(len(level) for level in levels)}")
        output.append(f"Modalità visualizzazione: {display_mode}")
        output.append("")
    
    for i, level in enumerate(levels):
        output.append(f"Livello {i + 1}:")
        for j, chord in enumerate(level):
            if display_mode == "intervals":
                chord_text = chord.to_intervals_string()
            else:
                chord_text = str(chord)
            output.append(f"  {j + 1}. {chord_text}")
        output.append("")
    
    return "\n".join(output)

def generate_json_output(levels, verbose, display_mode):
    """Genera output in formato JSON"""
    import json
    
    data = {
        "levels": []
    }
    
    if verbose:
        data["metadata"] = {
            "total_levels": len(levels),
            "total_chords": sum(len(level) for level in levels),
            "display_mode": display_mode
        }
    
    for i, level in enumerate(levels):
        level_data = {
            "level": i + 1,
            "chords": []
        }
        
        for j, chord in enumerate(level):
            chord_data = {
                "position": j + 1,
                "notes": [note.name.replace('_', '#') for note in chord.notes],
                "root": chord.root.name.replace('_', '#'),
                "representation": str(chord),
                "intervals": chord.get_intervals(),
                "intervals_string": chord.to_intervals_string()
            }
            level_data["chords"].append(chord_data)
        
        data["levels"].append(level_data)
    
    return json.dumps(data, indent=2, ensure_ascii=False)

def generate_csv_output(levels, verbose, display_mode):
    """Genera output in formato CSV"""
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    if verbose:
        writer.writerow(["Livello", "Posizione", "Note", "Radice", "Rappresentazione", "Intervalli"])
    else:
        writer.writerow(["Livello", "Posizione", "Accordo"])
    
    for i, level in enumerate(levels):
        for j, chord in enumerate(level):
            if verbose:
                notes_str = " - ".join(note.name.replace('_', '#') for note in chord.notes)
                root_str = chord.root.name.replace('_', '#')
                intervals_str = chord.to_intervals_string()
                writer.writerow([i + 1, j + 1, notes_str, root_str, str(chord), intervals_str])
            else:
                if display_mode == "intervals":
                    chord_text = chord.to_intervals_string()
                else:
                    chord_text = str(chord)
                writer.writerow([i + 1, j + 1, chord_text])
    
    return output.getvalue()

if __name__ == "__main__":
    main()
