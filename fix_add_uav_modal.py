import re

filepath = 'frontend/dashboard.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

clean_modal = '''
        <!-- Add New UAV Modal -->
        <div class="parts-panel-overlay" id="addUavModal">
            <div class="parts-panel-content" style="max-width: 500px; height: auto; border-radius: 12px; margin: 15vh auto;">
                <div class="panel-header">
                    <h3>Add New UAV</h3>
                    <button class="close-btn" id="closeAddUavModalBtn">&times;</button>
                </div>
                
                <div class="panel-body" style="padding: 20px;">
                    <form id="addUavForm" style="display: flex; flex-direction: column; gap: 15px;">
                        <p id="addUavError" style="color: var(--error-color); margin: 0; font-size: 13px;"></p>
                        <div>
                            <label style="display:block; margin-bottom: 5px;">Serial Number / QR Code <span style="color:var(--error-color);">*</span></label>
                            <input type="text" id="newUavSerial" required placeholder="e.g. QR-HELI-002" style="width: 100%; padding: 10px; background: var(--input-bg); border: 1px solid var(--border-color); color: white; border-radius: 6px;">
                            <div id="qr-reader-uav" style="width:100%; margin-top: 10px;"></div>
                        </div>
                        <div>
                            <label style="display:block; margin-bottom: 5px;">Model Name <span style="color:var(--error-color);">*</span></label>
                            <input type="text" id="newUavModel" required placeholder="e.g. Beta-Y" style="width: 100%; padding: 10px; background: var(--input-bg); border: 1px solid var(--border-color); color: white; border-radius: 6px;">
                        </div>
                        <button type="submit" class="btn-primary" style="width: 100%; margin-top: 10px;">Create UAV</button>
                    </form>
                </div>
            </div>
        </div>
'''

# Find and replace the old addUavModal which contains the telemetry crap
# We look for <div class="parts-panel-overlay" id="addUavModal"> ... up to the end of the modal
content = re.sub(r'<div class="parts-panel-overlay" id="addUavModal">.*?</form>\s*</div>\s*</div>\s*</div>', clean_modal, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Add UAV Modal HTML cleaned.")
