import re
import os

filepath = 'frontend/dashboard.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the kbModal HTML
match = re.search(r'<!-- Knowledge Base Modal -->\s*<div class="parts-panel-overlay" id="kbModal".*?<!-- Parts Tab -->.*?</div>\s*</div>\s*</div>\s*</div>', content, re.DOTALL)
if match:
    kb_html = match.group(0)
    print("kb_html found, length:", len(kb_html))
    
    html_files = [
        'frontend/inventory.html',
        'frontend/damage_reports.html',
        'frontend/personnel.html',
        'frontend/profile.html',
        'frontend/users.html'
    ]
    
    for hf in html_files:
        if os.path.exists(hf):
            with open(hf, 'r', encoding='utf-8') as hf_file:
                hf_content = hf_file.read()
            
            # If kbModal is already in the file, remove it first
            hf_content = re.sub(r'<!-- Knowledge Base Modal -->\s*<div class="parts-panel-overlay" id="kbModal".*?<!-- Parts Tab -->.*?</div>\s*</div>\s*</div>\s*</div>', '', hf_content, flags=re.DOTALL)
            
            # Insert just before </main> or </body>
            # We'll insert it before </main> or at the end
            if '</main>' in hf_content:
                hf_content = hf_content.replace('</main>', '\n' + kb_html + '\n</main>')
            else:
                hf_content = hf_content.replace('</body>', '\n' + kb_html + '\n</body>')
                
            with open(hf, 'w', encoding='utf-8') as hf_file:
                hf_file.write(hf_content)
    print("HTML files updated.")
else:
    print("kb_html NOT found!")
