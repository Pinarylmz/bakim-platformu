import re

with open('frontend/js/dashboard.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if re.search(r'[^\x00-\x7F🚁]', line):  # Find anything that is not ASCII and not the helicopter emoji
        print(f"Line {i+1}: {line.strip()}")
