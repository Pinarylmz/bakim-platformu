import os

replacements = {
    'Approvend': 'Approved',
    'Uyar': 'Warning',
    'UuY': 'Uçuş',
    'niY': 'İniş',
    'Gvde/Yapsal': 'Gövde/Yapısal',
    'Enerji KaynaY': 'Enerji Kaynağı',
    'HaberleYme': 'Haberleşme',
    'GǬ': 'Güç',
    'onitesi': 'Ünitesi',
    'Takm': 'Takımı',
    'paralar': 'parçaları'
}

with open('backend/seed.py', 'r', encoding='utf-8') as f:
    c = f.read()
for k, v in replacements.items():
    c = c.replace(k, v)
with open('backend/seed.py', 'w', encoding='utf-8') as f:
    f.write(c)
