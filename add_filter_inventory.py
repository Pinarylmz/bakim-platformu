import re

filepath = 'frontend/inventory.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

replacement = '''<div style="display: flex; gap: 10px; align-items: center;">
                <select id="filterUavSelect" style="padding: 8px 12px; border-radius: 6px; background: var(--input-bg); border: 1px solid var(--border-color); color: white;">
                    <option value="all">All UAVs</option>
                </select>
                <button id="openAddPartModalBtn" class="btn-primary" style="margin: 0;">+ Add New Part</button>
            </div>'''

content = re.sub(r'<button id="openAddPartModalBtn" class="btn-primary">\+ Add New Part</button>', replacement, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Inventory HTML updated with filter dropdown.")
