#!/usr/bin/env python3

import requests
import re

books = [
    'Genesis',
    'Exodus',
    'Leviticus',
    'Numbers',
    'Deuteronomy'
]

def clean_hebrew(text):
    # Remove vowels (niqqud) and cantillation marks (te'amim)
    niqqud = re.compile(r"[\u0591-\u05BD\u05BF-\u05C7]")
    text = niqqud.sub('', text)
    # Remove non-letter characters (punctuation, spaces, etc.)
    text = ''.join([c for c in text if '\u05D0' <= c <= '\u05EA'])
    return text

def fetch_book(book_name):
    print(f"Fetching {book_name}...")
    full_text = ''
    for chapter in range(1, 151):  # no Torah book has more than 150 chapters
        url = f"https://www.sefaria.org/api/texts/{book_name}.{chapter}?lang=he&version=Tanach_with_Taamim"
        response = requests.get(url)
        if response.status_code != 200:
            break
        data = response.json()
        if 'he' not in data or not data['he']:
            break
        chapter_text = ''.join(data['he'])
        full_text += chapter_text
    return full_text

def main():
    torah_text = ''
    for book in books:
        book_text = fetch_book(book)
        torah_text += book_text

    print("Cleaning text...")
    clean_text = clean_hebrew(torah_text)

    output_file = 'torah_clean.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(clean_text)

    print(f"Saved cleaned Torah to {output_file}")

if __name__ == "__main__":
    main()
