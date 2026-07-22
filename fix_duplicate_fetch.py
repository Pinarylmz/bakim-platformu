import re

filepath = 'frontend/js/inventory.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the raw initial fetch calls
content = re.sub(r'// Initial Fetch\s*fetchInventory\(\);\s*fetchDropdownData\(\);\s*', '', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleaned duplicate initial fetch calls.")
