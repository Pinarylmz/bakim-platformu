import re
import os

html_files = [
    'frontend/dashboard.html',
    'frontend/inventory.html',
    'frontend/damage_reports.html',
    'frontend/personnel.html',
    'frontend/profile.html',
    'frontend/users.html',
    'frontend/index.html'
]

for hf in html_files:
    if os.path.exists(hf):
        with open(hf, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Remove sidebar button
        content = re.sub(r'<li><a href="#" id="openKbSidebarBtn">.*?Knowledge Base.*?</a></li>', '', content)
        
        # Remove kbModal block completely
        # It starts with <!-- Knowledge Base Modal --> or <div class="parts-panel-overlay" id="kbModal"
        # Since we added it, it's pretty standard.
        content = re.sub(r'<!-- Knowledge Base Modal -->\s*<div class="parts-panel-overlay" id="kbModal".*?<!-- Parts Tab -->.*?</div>\s*</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
        
        # Some versions might lack the HTML comment if I messed up previously
        content = re.sub(r'<div class="parts-panel-overlay" id="kbModal".*?<!-- Parts Tab -->.*?</div>\s*</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
        
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(content)

# Clean auth.js
auth_file = 'frontend/js/auth.js'
if os.path.exists(auth_file):
    with open(auth_file, 'r', encoding='utf-8') as f:
        auth_content = f.read()
        
    auth_content = re.sub(r'// Knowledge Base Logic\s*document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{.*?(?:renderKbParts.*?\}\);)?.*?\}\);', '', auth_content, flags=re.DOTALL)
    
    with open(auth_file, 'w', encoding='utf-8') as f:
        f.write(auth_content)

print("Knowledge Base fully removed from all files.")
