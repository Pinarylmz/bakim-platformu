import re

filepath = 'frontend/js/dashboard.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

nav_logic = '''
const viewInInventoryBtn = document.getElementById('viewInInventoryBtn');
if (viewInInventoryBtn) {
    viewInInventoryBtn.addEventListener('click', () => {
        const serial = document.getElementById('panelUavSerial').textContent;
        if(serial && serial !== '--') {
            window.location.href = 'inventory.html?uav_id=' + encodeURIComponent(serial);
        }
    });
}
'''

if 'viewInInventoryBtn' not in content:
    content += '\n' + nav_logic

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Dashboard JS updated with navigation logic.")
