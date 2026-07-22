import os

filepath = 'frontend/js/dashboard.js'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Ã' in line or 'ǫ' in line:
        print(f"Line {i+1}: {line.strip()}")
