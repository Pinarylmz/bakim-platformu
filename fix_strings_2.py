import os

filepath = 'frontend/js/dashboard.js'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Fix corrupted strings aggressively
content = content.replace('Uua Hazǫr', 'Flight Ready')
content = content.replace('Uua Hazır', 'Flight Ready')
content = content.replace('Bakǫmda', 'Maintenance')
content = content.replace('Uyarǫ', 'Warning')
content = content.replace('Kritik', 'Critical')
content = content.replace('?HA bulunamadǫ', 'No UAVs found')
content = content.replace('ǽo^?', '🚁')
content = content.replace('HA', 'UAV')
content = content.replace('', '')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleaned dashboard.js completely.")
