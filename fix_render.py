import sys

with open('frontend/js/dashboard.js', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's completely rewrite renderUAVs to ensure NO syntax errors.
import re

new_render = '''
function renderUAVs() {
    const grid = document.getElementById('uavGrid');
    if (!grid) return;
    grid.innerHTML = '';
    
    if(currentUAVs.length === 0) {
        grid.innerHTML = '<p style="color: var(--text-secondary); grid-column: 1/-1;">No UAVs found. Click Seed Test Data to generate some.</p>';
        return;
    }

    currentUAVs.forEach(uav => {
        const card = document.createElement('div');
        card.className = 'uav-card';
        card.style.cursor = 'pointer';
        
        let statusColor = 'var(--success-color)';
        const stat = (uav.status || 'Flight Ready');
        if (stat === 'Maintenance' || stat === 'Warning') statusColor = 'var(--warning-color)';
        if (stat === 'Critical' || stat === 'Error') statusColor = 'var(--error-color)';
        
        card.innerHTML = 
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div class="uav-icon">🚁</div>
                <span style="font-size: 12px; font-weight: 600; padding: 4px 8px; border-radius: 4px; background: \; color: white;">\</span>
            </div>
            <h3 style="margin-top: 15px;">\</h3>
            <p style="font-size: 13px; color: var(--text-secondary);">SN: \</p>
            <p style="margin-top: 10px; font-size: 14px;"><span>Flight Hours</span>: <strong class="text-white">\ h</strong></p>
        ;
        
        card.addEventListener('click', () => {
            openPartsPanel(uav.serial_number, uav.model_name, uav.total_flight_hours, uav.status, uav.id);
        });
        
        grid.appendChild(card);
    });
}
'''

# Find the old renderUAVs block and replace it
content = re.sub(r'function renderUAVs\(\).*?if\(typeof setLanguage === \'function\'\)[^\n]*\n\}', new_render, content, flags=re.DOTALL)

with open('frontend/js/dashboard.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("renderUAVs safely replaced.")
