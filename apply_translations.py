import re

filepath = 'frontend/js/inventory.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

translation_logic = '''
// Translation Map for English localization without breaking backend db
const translationMap = {
    // Categories
    "Ana Rotor Sistemi": "Main Rotor System",
    "Kuyruk Roturu Sistemi": "Tail Rotor System",
    "Kuyruk Rotoru Sistemi": "Tail Rotor System",
    "Güç Aktarma": "Power Transmission",
    "Motor / Güç Ünitesi": "Motor / Power Unit",
    "Uçuş Kontrol": "Flight Control",
    "Elektronik/Aviyonik": "Electronics/Avionics",
    "Gövde ve İniş": "Airframe & Landing",
    "Enerji ve Haberleşme": "Power & Communication",
    
    // Parts
    "Ana rotor kanatları (Titanium)": "Main Rotor Blades (Titanium)",
    "Kuyruk rotoru göbeği": "Tail Rotor Hub",
    "Ana dişli kutusu": "Main Gearbox",
    "Fırçasız motor (BLDC v3)": "Brushless Motor (BLDC v3)",
    "Uçuş kontrol kartı (FC)": "Flight Control Board (FC)",
    "Kamera/Gimbal Modülü": "Camera/Gimbal Module",
    "İniş takımı (Amortisörlü)": "Landing Gear (Shock Absorbing)",
    "LiPo/Li-Ion batarya": "LiPo/Li-Ion Battery"
};

function translateText(text) {
    if (!text) return text;
    return translationMap[text] || text;
}
'''

# Insert the translation logic at the top, just below API_BASE
content = content.replace("const API_BASE = 'http://localhost:8000';", "const API_BASE = 'http://localhost:8000';\n" + translation_logic)

# Update renderInventory to translate item.name
content = re.sub(
    r'<td>\$\{item\.name\}</td>',
    r'<td></td>',
    content
)

# Update fetchDropdownData to translate category name
content = re.sub(
    r'opt\.textContent = c\.name;',
    r'opt.textContent = translateText(c.name);',
    content
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Translations applied to inventory.js")
