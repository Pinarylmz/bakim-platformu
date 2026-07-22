import re

filepath = 'frontend/dashboard.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the Guide Tab and Parts Tab contents with the requested info
new_tabs = '''
                <!-- Guide Tab -->
                <div id="kbGuideTab" style="display: block;">
                    <h4 style="margin-bottom: 15px; color: var(--primary-color);">How to Use the System</h4>
                    <ol style="color: var(--text-secondary); line-height: 1.6; padding-left: 20px; display: flex; flex-direction: column; gap: 10px;">
                        <li><strong>Dashboard & UAV Tracking:</strong> View all registered UAVs on the dashboard. Click on any UAV card to see its installed parts, live telemetry, and simulated health status.</li>
                        <li><strong>Add New UAV:</strong> Click "+ Add New UAV" on the dashboard to register a new drone.</li>
                        <li><strong>Inventory Management:</strong> Navigate to the "Inventory" tab to manage all parts. Use the "Filter by UAV" dropdown to quickly see parts assigned to a specific drone.</li>
                        <li><strong>Live Simulation:</strong> While viewing a UAV's hardware details, use the simulation tools to test how the system reacts to temperature and vibration warnings.</li>
                    </ol>
                </div>

                <!-- Parts Tab -->
                <div id="kbPartsTab" style="display: none; height: 300px; overflow-y: auto;">
                    <div style="display: flex; flex-direction: column; gap: 15px; color: var(--text-secondary); font-size: 14px;">
                        <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;">
                            <strong style="color: white; display: block; margin-bottom: 5px;">Main Rotor Blades (Main Rotor System)</strong>
                            Provides the primary lift and thrust for helicopter-type UAVs. Critical for flight stability.
                        </div>
                        <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;">
                            <strong style="color: white; display: block; margin-bottom: 5px;">ESC (Motor / Power Unit)</strong>
                            Electronic Speed Controller. Regulates the speed of the brushless motors based on flight control signals. Prone to overheating.
                        </div>
                        <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;">
                            <strong style="color: white; display: block; margin-bottom: 5px;">Brushless Motor (Motor / Power Unit)</strong>
                            High-efficiency motors driving the rotors. Monitored for temperature and vibration anomalies.
                        </div>
                        <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;">
                            <strong style="color: white; display: block; margin-bottom: 5px;">Flight Control Board / FC (Flight Control)</strong>
                            The brain of the UAV. Processes gyro/accelerometer data and pilot inputs to maintain stable flight.
                        </div>
                        <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;">
                            <strong style="color: white; display: block; margin-bottom: 5px;">LiPo/Li-Ion Battery (Power & Communication)</strong>
                            Primary power source. Status degrades based on battery level percentage. Monitored strictly below 30%.
                        </div>
                    </div>
                </div>
'''

content = re.sub(r'<!-- Guide Tab -->.*</div>\s*</div>\s*</div>\s*</div>', new_tabs.strip() + '\n            </div>\n        </div>\n    </div>', content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("KB HTML content updated.")
