from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_col(columns, key):
    ls_found = []
    for col in columns:
        if key.lower() in col.lower():
            ls_found.append(col)
    return ls_found