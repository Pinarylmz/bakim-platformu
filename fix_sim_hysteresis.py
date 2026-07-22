import re

filepath = 'frontend/js/dashboard.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_logic = '''
                        // Local Simulation Logic for UI Testing with Hysteresis
                        const temp = data.esc_temperature || 0;
                        const vib = data.vibration_level || 0;
                        const bat = data.battery_level || 100;
                        
                        currentParts.forEach(p => {
                            let newStatus = p.status;
                            const name = (p.name || '').toLowerCase();
                            const category = (p.category || '').toLowerCase();
                            
                            // ESC or Motor Temperature Rules (with Hysteresis)
                            if (name.includes('esc') || name.includes('motor')) {
                                if (newStatus === 'Critical') {
                                    if (temp < 75) newStatus = 'Warning';
                                    if (temp < 65) newStatus = 'OK';
                                } else if (newStatus === 'Warning') {
                                    if (temp >= 80) newStatus = 'Critical';
                                    else if (temp < 65) newStatus = 'OK';
                                } else {
                                    if (temp >= 80) newStatus = 'Critical';
                                    else if (temp >= 70) newStatus = 'Warning';
                                }
                            }
                            
                            // Rotor or Hub Vibration Rules (with Hysteresis)
                            if (category.includes('rotor') || name.includes('rotor') || name.includes('hub')) {
                                if (newStatus === 'Critical') {
                                    if (vib < 0.75) newStatus = 'Warning';
                                    if (vib < 0.45) newStatus = 'OK';
                                } else if (newStatus === 'Warning') {
                                    if (vib >= 0.8) newStatus = 'Critical';
                                    else if (vib < 0.45) newStatus = 'OK';
                                } else {
                                    if (vib >= 0.8) newStatus = 'Critical';
                                    else if (vib >= 0.5) newStatus = 'Warning';
                                }
                            }

                            // Battery Rules (with Hysteresis)
                            if (name.includes('batarya') || name.includes('battery')) {
                                if (newStatus === 'Critical') {
                                    if (bat > 20) newStatus = 'Warning';
                                    if (bat > 35) newStatus = 'OK';
                                } else if (newStatus === 'Warning') {
                                    if (bat <= 15) newStatus = 'Critical';
                                    else if (bat > 35) newStatus = 'OK';
                                } else {
                                    if (bat <= 15) newStatus = 'Critical';
                                    else if (bat <= 30) newStatus = 'Warning';
                                }
                            }
                            
                            p.status = newStatus;
                        });
'''

# We need to replace the old local simulation logic with the new one.
# It matches from // Local Simulation Logic up to p.status = newStatus;\n                        });
content = re.sub(
    r'// Local Simulation Logic for UI Testing\s+const temp.*?p\.status = newStatus;\s+\}\);',
    new_logic.strip(),
    content,
    flags=re.DOTALL
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Hysteresis added to simulation logic.")
