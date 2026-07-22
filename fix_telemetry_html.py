import re

filepath = 'frontend/dashboard.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

telemetry_html = '''                
                <div style="display:flex; justify-content:space-between; align-items:center; padding: 15px 20px; background:var(--bg-color); border-bottom:1px solid var(--border-color);">
                    <div>
                        <h4 style="margin:0; color:var(--text-secondary); font-size:12px; text-transform:uppercase;">Serial No</h4>
                        <span id="panelUavSerial" style="font-weight:bold; color:white;">--</span>
                    </div>
                    <div>
                        <h4 style="margin:0; color:var(--text-secondary); font-size:12px; text-transform:uppercase;">Status</h4>
                        <span id="panelUavStatus" style="font-weight:bold; color:white;">--</span>
                    </div>
                    <div>
                        <h4 style="margin:0; color:var(--text-secondary); font-size:12px; text-transform:uppercase;">Total Hours</h4>
                        <span id="panelUavHours" style="font-weight:bold; color:white;">--</span>
                    </div>
                </div>

                <!-- Telemetry Stats Row -->
                <div style="display:flex; gap: 15px; padding: 15px 20px; border-bottom: 1px solid var(--border-color); background: rgba(0,0,0,0.2);">
                    <div style="flex:1; text-align:center;">
                        <span style="font-size:11px; color:var(--text-secondary); display:block; margin-bottom:5px;">BATTERY</span>
                        <strong id="liveBattery" style="color:var(--success-color); font-size:16px;">--</strong>
                    </div>
                    <div style="flex:1; text-align:center;">
                        <span style="font-size:11px; color:var(--text-secondary); display:block; margin-bottom:5px;">ESC TEMP</span>
                        <strong id="liveTemp" style="color:var(--warning-color); font-size:16px;">--</strong>
                    </div>
                    <div style="flex:1; text-align:center;">
                        <span style="font-size:11px; color:var(--text-secondary); display:block; margin-bottom:5px;">VIB LEVEL</span>
                        <strong id="liveVib" style="color:var(--error-color); font-size:16px;">--</strong>
                    </div>
                    <div style="flex:1; text-align:center;">
                        <span style="font-size:11px; color:var(--text-secondary); display:block; margin-bottom:5px;">RPM ASYM</span>
                        <strong id="liveRpm" style="color:var(--primary-color); font-size:16px;">--</strong>
                    </div>
                    <div style="display:flex; align-items:center;">
                        <button id="toggleSimulationBtn" class="btn-primary" style="margin:0; font-size:12px; padding:8px 12px;">Start Simulation</button>
                    </div>
                </div>
'''

if 'id="liveBattery"' not in content:
    content = re.sub(
        r'(<div class="panel-header">.*?</div>)', 
        r'\1' + '\n' + telemetry_html, 
        content, 
        flags=re.DOTALL
    )

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Telemetry HTML added.")
