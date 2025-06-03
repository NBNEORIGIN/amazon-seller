"""
Text Utilities for Stake Processors
-----------------------------------
Shared text wrapping and grammar/typo checking functions.
"""
import textwrap
import re
from datetime import datetime
import pandas as pd

def split_line_to_fit(line, max_chars):
    """Split a single line into lines that fit max_chars."""
    return textwrap.wrap(line, width=max_chars)

def check_grammar_and_typos(line):
    """Perform grammar and typo checks on a single text line."""
    # a. Spaces before commas or periods
    if line and re.search(r"\s+[,\.]", line):
        print(f"Warning: Extra space before comma/period: '{line}'")
    # b. Future death dates (try to find DD/MM/YYYY or MM/DD/YYYY)
    date_pattern = r'(\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b)'
    if line:
        for match in re.findall(date_pattern, line):
            try:
                dt = datetime.strptime(match, "%d/%m/%Y")
            except ValueError:
                try:
                    dt = datetime.strptime(match, "%m/%d/%Y")
                except ValueError:
                    continue
            if dt.year > datetime.now().year:
                print(f"Warning: Future year found: '{match}' in '{line}'")
    # c. Capitalization of names (for potential name lines)
    if line and len(line.split()) <= 6 and not line.istitle():
        print(f"Warning: Name not title case: '{line}'")
