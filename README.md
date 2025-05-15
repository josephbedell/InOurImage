# InOurImage
code and docs for In Our Image Novel

```
./fetch_torah.py # downloads hebrew text of torah as torah_clean.txt
```
 
### Main Files

- **torah_clean.txt**: a cleaned version of the Torah text in hebrew.
    - 306,269 hebrew letters of the torah
    - Tanach_with_Taamim version from Sefaria (super traditional Masoretic text).
    - Strips: vowel points (niqqud), cantillation marks (musical marks), spaces, punctuation, anything non-letter
    - Leaves you only א to ת letters, perfect for your amino acid conversion.
- **conversion_table files**: different versions of the conversion from hebrew letters to amino acids

## Usage

```bash
python els_search.py --torah <torah_file.txt> --query <amino_acid_sequence_or_fasta_file> [--max_mismatches N]
```

### Options
| Option                | Description |
|:----------------------|:------------|
| `--torah <file>`       | Input cleaned Torah text file (**required**) |
| `--query <sequence/file>` | Amino acid sequence (e.g., `YIQ`) or path to a FASTA file (**required**) |
| `--max_mismatches N`   | Allow up to N mismatches (default `0`) |
| `-h, --help`           | Show this help message |

### Notes
- Searches skips from **-500 to +500** (excluding 0).
- Torah file must contain only Hebrew letters (א–ת).


