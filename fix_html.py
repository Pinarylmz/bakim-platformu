import os
import glob
import re

kb_sidebar_item = '<li><a href="#" id="openKbSidebarBtn">ℹ️ Knowledge Base</a></li>'

kb_modal_html = '''
<!-- Knowledge Base Modal -->
<div class="parts-panel-overlay" id="kbModal" style="display:none; z-index: 2000;">
    <div class="parts-panel-content" style="max-width: 600px; height: auto; border-radius: 12px; margin: 10vh auto; max-height: 80vh; overflow-y: auto;">
        <div class="panel-header" style="border-bottom: 1px solid var(--border-color); margin-bottom: 0;">
            <h3>ℹ️ Knowledge Base</h3>
            <button class="close-btn" id="closeKbBtn">&times;</button>
        </div>
        
        <div style="display: flex; background: var(--bg-color); border-bottom: 1px solid var(--border-color);">
            <button class="kb-tab-btn active" id="tabGuideBtn" style="flex:1; padding: 12px; border: none; background: none; color: white; cursor: pointer; border-bottom: 2px solid var(--primary-color);">Application Guide</button>
            <button class="kb-tab-btn" id="tabPartsBtn" style="flex:1; padding: 12px; border: none; background: none; color: var(--text-secondary); cursor: pointer; border-bottom: 2px solid transparent;">Part Dictionary</button>
        </div>

        <div class="panel-body" style="padding: 20px;">
            <!-- Guide Tab -->
            <div id="kbGuideTab" style="display: block;">
                <h4 style="margin-bottom: 15px; color: var(--primary-color);">How to Use the System</h4>
                <ol style="color: var(--text-secondary); line-height: 1.6; padding-left: 20px; display: flex; flex-direction: column; gap: 10px;">
                    <li><strong>Add a New UAV:</strong> Click "+ Add New UAV" on the dashboard. Enter the serial number and model name.</li>
                    <li><strong>Manage Parts:</strong> Navigate to the Inventory page. Use the "Add New Part" button to add a part to a specific UAV. Parts will automatically generate serial numbers if left blank.</li>
                    <li><strong>Report Damage:</strong> Go to "Damage Reports" and click "+ Report Damage". You can scan a QR code or manually select the UAV, then pick the installed part that is damaged.</li>
                    <li><strong>Approvals:</strong> If you are an Admin, you can approve or reject new user registrations from your Profile page under "Pending Approvals".</li>
                </ol>
            </div>

            <!-- Parts Tab -->
            <div id="kbPartsTab" style="display: none;">
                <input type="text" id="kbSearchInput" placeholder="Search for a part or category..." style="width: 100%; padding: 12px; margin-bottom: 15px; background: var(--input-bg); border: 1px solid var(--border-color); color: white; border-radius: 8px;">
                <div id="kbPartsList" style="display: flex; flex-direction: column; gap: 10px;">
                </div>
            </div>
        </div>
    </div>
</div>
'''

for filepath in glob.glob('frontend/*.html'):
    if 'index.html' in filepath or 'register.html' in filepath:
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add sidebar item if missing
    if 'id="openKbSidebarBtn"' not in content:
        content = content.replace('<li><a href="#" id="logoutBtn">', f'{kb_sidebar_item}\n            <li><a href="#" id="logoutBtn">')

    # 2. Add Modal HTML if missing, before </body>
    if 'id="kbModal"' not in content:
        content = content.replace('</body>', f'{kb_modal_html}\n</body>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Updated HTML for {filepath}")

