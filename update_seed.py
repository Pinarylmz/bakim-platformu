import os

with open('backend/seed.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the categories list in seed.py
import re

new_cats = '''    categories = [
        "Ana Rotor Sistemi",
        "Kuyruk Rotoru Sistemi",
        "Güç Aktarma",
        "Motor / Güç Ünitesi",
        "Uçuş Kontrol",
        "Elektronik/Aviyonik",
        "Gövde ve İniş",
        "Enerji ve Haberleşme"
    ]'''

# We will just replace the whole categories block. It's usually from categories = [ to ]
content = re.sub(r'categories = \[.*?\]', new_cats, content, flags=re.DOTALL)

with open('backend/seed.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated categories in seed.py")
