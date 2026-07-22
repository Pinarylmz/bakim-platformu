import os

filepath = 'frontend/js/dashboard.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix corrupted strings
content = content.replace('?HA bulunamadǫ', 'No UAVs found')
content = content.replace('ǽo^?', '🚁')
content = content.replace('Uua Hazǫr', 'Flight Ready')
content = content.replace('Bakǫmda', 'Maintenance')
content = content.replace('Uyarǫ', 'Warning')
content = content.replace('Bu filtreye uygun para bulunamadǫ', 'No parts found for this filter')
content = content.replace('Kritik', 'Critical')
content = content.replace('health-Uyar', 'health-warning')
content = content.replace('\'C', '°C')
content = content.replace('SimǬlasyonu Balat', 'Start Simulation')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("dashboard.js corrupted strings fixed.")
