#!/usr/bin/env python3
"""Replace hyperbolic phrases in HTML/MD files with neutral alternatives based on config/stopwords.json"""

import json
import re
from pathlib import Path

stop_path = Path('config/stopwords.json')
if not stop_path.exists():
    print('Stopword list not found')
    exit(1)

mappings = json.loads(stop_path.read_text(encoding='utf-8'))

# Pre-compile regex patterns (case-insensitive, whole word)
patterns = [(re.compile(rf"\b{re.escape(src)}\b", re.IGNORECASE), repl) for src, repl in mappings.items()]

files = [*Path('.').rglob('*.html'), *Path('.').rglob('*.md')]

changed_files = 0
for file in files:
    text = file.read_text(encoding='utf-8', errors='ignore')
    original = text
    for pattern, repl in patterns:
        text = pattern.sub(repl, text)
    if text != original:
        file.write_text(text, encoding='utf-8')
        changed_files += 1
        print(f"Cleaned: {file}")

print(f"\nCompleted language clean-up. Files modified: {changed_files}") 