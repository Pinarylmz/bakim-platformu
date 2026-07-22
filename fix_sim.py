import re

filepath = 'frontend/js/dashboard.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# We want to replace the partsRes fetch block with a local simulation logic that actually mutates currentParts
new_sim_logic = '''
                        // Local Simulation Logic for UI Testing
                        const temp = data.esc_temperature || 0;
                        const vib = data.vibration_level || 0;
                        const bat = data.battery_level || 100;
                        
                        currentParts.forEach(p => {
                            let newStatus = p.status;
                            const name = (p.name || '').toLowerCase();
                            const category = (p.category || '').toLowerCase();
                            
                            // ESC or Motor Temperature Rules
                            if (name.includes('esc') || name.includes('motor')) {
                                if (temp >= 80) newStatus = 'Critical';
                                else if (temp >= 70) newStatus = 'Warning';
                                else newStatus = 'OK';
                            }
                            
                            // Rotor or Hub Vibration Rules
                            if (category.includes('rotor') || name.includes('rotor') || name.includes('hub')) {
                                if (vib >= 0.8) newStatus = 'Critical';
                                else if (vib >= 0.5) newStatus = 'Warning';
                                else newStatus = 'OK';
                            }

                            // Battery Rules
                            if (name.includes('batarya') || name.includes('battery')) {
                                if (bat <= 15) newStatus = 'Critical';
                                else if (bat <= 30) newStatus = 'Warning';
                                else newStatus = 'OK';
                            }
                            
                            p.status = newStatus;
                        });
                        
                        // Re-render the parts using the currently active filter
                        const activeFilterBtn = document.querySelector('.filter-btn.active');
                        const currentFilter = activeFilterBtn ? activeFilterBtn.dataset.filter : 'All';
                        renderParts(currentFilter);
'''

# Replace the inner block of the simInterval where it fetched from API
content = re.sub(
    r'// Fetch the latest parts statuses to check thresholds.*?\}\s*\}', 
    new_sim_logic, 
    content, 
    flags=re.DOTALL
)

# Fix the renderParts status check to be case-insensitive to ensure filters work
content = content.replace("const isCritical = (part.status !== 'OK');", "const isCritical = (part.status.toUpperCase() !== 'OK');")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Simulation logic updated.")
