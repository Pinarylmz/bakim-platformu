import re

filepath = 'frontend/dashboard.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add the 'View in Inventory' button to the panel-header
replacement = '''<div class="panel-header">
                    <h2 id="panelUavName">Hardware Details</h2>
                    <div style="display:flex; align-items:center; gap: 15px;">
                        <button id="viewInInventoryBtn" class="btn-secondary" style="margin:0; font-size:12px; padding:6px 12px;">View in Inventory</button>
                        <button class="close-btn" id="closePanelBtn">&times;</button>
                    </div>
                </div>'''

content = re.sub(r'<div class="panel-header">\s*<h2 id="panelUavName">Hardware Details</h2>\s*<button class="close-btn" id="closePanelBtn">&times;</button>\s*</div>', replacement, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Dashboard HTML updated with View in Inventory button.")
