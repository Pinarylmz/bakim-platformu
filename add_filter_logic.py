import re

filepath = 'frontend/js/inventory.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add global state for inventory items
content = content.replace("const API_BASE = 'http://localhost:8000';", "const API_BASE = 'http://localhost:8000';\nlet currentInventory = [];")

# Update fetchInventory to store items globally
content = re.sub(
    r'const items = await response\.json\(\);\s*renderInventory\(items\);',
    r'currentInventory = await response.json();\n            renderInventory();',
    content
)

# Update renderInventory signature and filtering logic
new_render = '''
function renderInventory() {
    const tbody = document.getElementById('inventoryBody');
    tbody.innerHTML = '';
    
    // Filter logic
    const filterSelect = document.getElementById('filterUavSelect');
    let items = currentInventory;
    if (filterSelect && filterSelect.value !== 'all') {
        const targetId = parseInt(filterSelect.value);
        items = currentInventory.filter(item => item.uav_id === targetId);
    }
    
    if(items.length === 0) {
        tbody.innerHTML = <tr><td colspan="5" style="text-align:center; color: var(--text-secondary);">No parts found.</td></tr>;
        return;
    }
'''

content = re.sub(r'function renderInventory\(items\) \{\s*const tbody = document\.getElementById\(\'inventoryBody\'\);\s*tbody\.innerHTML = \'\';.*?return;\s*\}', new_render, content, flags=re.DOTALL)

# Add event listener for the filter dropdown at the end of the file
filter_logic = '''
document.addEventListener('DOMContentLoaded', async () => {
    // Wait for dropdown data to be fetched so filter can be populated
    await fetchDropdownData();
    await fetchInventory();

    const filterSelect = document.getElementById('filterUavSelect');
    if (filterSelect) {
        filterSelect.addEventListener('change', () => {
            renderInventory();
        });
    }
});
'''
if 'DOMContentLoaded' not in content:
    content += '\n' + filter_logic

# Update fetchDropdownData to populate filterUavSelect and handle URL params
dropdown_update = '''
        if (uavRes.ok) {
            const uavs = await uavRes.json();
            const uavSelect = document.getElementById('partUavId');
            const filterSelect = document.getElementById('filterUavSelect');
            
            const urlParams = new URLSearchParams(window.location.search);
            const targetSerial = urlParams.get('uav_id');
            
            uavs.forEach(u => {
                const opt = document.createElement('option');
                opt.value = u.id;
                opt.textContent = u.model_name + " (" + u.serial_number + ")";
                uavSelect.appendChild(opt);
                
                if (filterSelect) {
                    const fOpt = document.createElement('option');
                    fOpt.value = u.id;
                    fOpt.textContent = u.model_name + " (" + u.serial_number + ")";
                    filterSelect.appendChild(fOpt);
                    
                    if (targetSerial && u.serial_number === targetSerial) {
                        fOpt.selected = true;
                    }
                }
            });
        }
'''
content = re.sub(r'if \(uavRes\.ok\) \{.*?\}\s*\} catch', dropdown_update + '    } catch', content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Inventory JS updated with filtering logic.")
