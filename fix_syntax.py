import os
import re

filepath = 'frontend/js/dashboard.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken strings caused by 'C -> °C replacement
content = content.replace("°Critical", "'Critical")
content = content.replace("°CRITICAL", "'CRITICAL")
content = content.replace("°Content-Type", "'Content-Type")

# Let's completely clean up the old corrupted Turkish strings that are back because my ix_strings_2.py didn't catch them due to encoding issues earlier
content = content.replace('UÃ§uÃ¾a HazÃ½r', 'Flight Ready')
content = content.replace('BakÃ½mda', 'Maintenance')
content = content.replace('UyarÃ½', 'Warning')
content = content.replace('Ã UAV bulunamadÃ½.', 'No UAVs found.')
content = content.replace('Bu filtreye uygun parÃ§a bulunamadÃ½.', 'No parts found.')
content = content.replace('SimÃ¼lasyonu BaÃ¾lat', 'Start Simulation')
content = content.replace('Ã‚Â°C', '°C')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed syntax errors in dashboard.js")
