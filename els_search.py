#!/usr/bin/env python3

import sys
import re
import os

# Built-in Hebrew to Amino Acid conversion
conversion_table = {
    'א': 'A',
    'ב': 'STOP',
    'ג': 'G',
    'ד': 'D',
    'ה': 'H',
    'ו': 'V',
    'ז': 'STOP',
    'ח': 'Q',
    'ט': 'T',
    'י': 'Y',
    'כ': 'K',
    'ל': 'L',
    'מ': 'M',
    'נ': 'N',
    'ס': 'S',
    'ע': 'I',
    'פ': 'P',
    'צ': 'Q',
    'ק': 'C',
    'ר': 'R',
    'ש': 'F',
    'ת': 'E'
}

EXPECTED_TORAH_LENGTH = 304805  # Standard Torah letter count (approximate without vowels)

def usage():
    print(f"""
Usage:
    python els_search.py --torah <torah_file.txt> --query <amino_acid_sequence_or_fasta_file> [--max_mismatches N]

Options:
    --torah <file>            Input cleaned Torah text file (required)
    --query <sequence/file>   Amino acid sequence (e.g., YIQ) or path to a FASTA file (required)
    --max_mismatches N        Allow up to N mismatches (default 0)
    -h, --help                Show this help message

Example:
    python els_search.py --torah torah_clean.txt --query YIQ --max_mismatches 1
    python els_search.py --torah torah_clean.txt --query mysequence.fasta
""")
    sys.exit(1)

def validate_torah_file(filepath):
    if not os.path.isfile(filepath):
        print(f"Error: Torah file '{filepath}' does not exist.")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    clean_text = ''.join([c for c in text if '\u05D0' <= c <= '\u05EA'])

    if len(text) != len(clean_text):
        print("Error: Torah file contains invalid characters (only Hebrew letters allowed).")
        sys.exit(1)

    if not (0.9 * EXPECTED_TORAH_LENGTH <= len(text) <= 1.1 * EXPECTED_TORAH_LENGTH):
        print(f"Warning: Torah length {len(text)} seems unusual (expected around {EXPECTED_TORAH_LENGTH}). Proceeding anyway.")

    return text

def convert_text(text, conversion_table):
    return ''.join([conversion_table.get(c, '?') for c in text])

def load_fasta(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    seq = ''.join(line.strip() for line in lines if not line.startswith('>'))
    return seq

def hamming_distance(seq1, seq2):
    return sum(c1 != c2 for c1, c2 in zip(seq1, seq2))

def find_els(text, search_term, skip, max_mismatches=0):
    found = []
    text_length = len(text)
    search_length = len(search_term)

    for i in range(text_length):
        indices = [i + j * skip for j in range(search_length)]
        if any(idx < 0 or idx >= text_length for idx in indices):
            continue

        candidate = ''.join(text[idx] for idx in indices)
        mismatches = hamming_distance(candidate, search_term)

        if mismatches <= max_mismatches:
            found.append((i, candidate, mismatches, skip))

    return found

def main():
    if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) < 5:
        usage()

    torah_file = None
    query_input = None
    max_mismatches = 0

    args = sys.argv[1:]
    while args:
        arg = args.pop(0)
        if arg == '--torah':
            torah_file = args.pop(0)
        elif arg == '--query':
            query_input = args.pop(0)
        elif arg == '--max_mismatches':
            max_mismatches = int(args.pop(0))
        else:
            print(f"Unknown argument: {arg}")
            usage()

    if not torah_file or not query_input:
        usage()

    print("Validating and loading Torah...")
    torah_text = validate_torah_file(torah_file)

    print("Converting Torah to amino acids...")
    converted_torah = convert_text(torah_text, conversion_table)

    if query_input.endswith('.fasta') or query_input.endswith('.fa'):
        print(f"Loading search sequence from {query_input}...")
        search_term = load_fasta(query_input)
    else:
        search_term = query_input

    search_length = len(search_term)
    torah_length = len(converted_torah)

    max_skip = torah_length // search_length
    print(f"Auto-calculating skip range: from -{max_skip} to +{max_skip}...")

    total_matches = []

    for skip in range(-max_skip, max_skip + 1):
        if skip == 0:
            continue  # Skip skip=0
        matches = find_els(converted_torah, search_term, skip, max_mismatches)
        total_matches.extend(matches)

    if total_matches:
        total_matches.sort(key=lambda x: (x[2], abs(x[3])))  # Sort by mismatches, then skip size
        print(f"Found {len(total_matches)} total matches:")
        for idx, candidate, mismatches, skip in total_matches:
            print(f"Position {idx}, Skip {skip}, Mismatches {mismatches}: {candidate}")
    else:
        print("No matches found.")

if __name__ == "__main__":
    main()
