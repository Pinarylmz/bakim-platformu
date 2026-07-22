import re

filepath = 'frontend/js/auth.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to add the console logs inside the DOMContentLoaded block
replacement = '''// Knowledge Base Logic
document.addEventListener('DOMContentLoaded', () => {
    const kbModal = document.getElementById('kbModal');
    const openKbSidebarBtn = document.getElementById('openKbSidebarBtn');
    const closeKbBtn = document.getElementById('closeKbBtn');
    const tabGuideBtn = document.getElementById('tabGuideBtn');
    const tabPartsBtn = document.getElementById('tabPartsBtn');
    const kbGuideTab = document.getElementById('kbGuideTab');
    const kbPartsTab = document.getElementById('kbPartsTab');
    const kbSearchInput = document.getElementById('kbSearchInput');

    if (!openKbSidebarBtn) {
        console.error('HATA: Knowledge Base butonu DOM icinde bulunamadi. ID uyusmazligi var!');
    } else {
        console.log('BASARILI: Knowledge Base butonu aktif edildi.');
    }
'''

content = re.sub(r'// Knowledge Base Logic\s*document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{\s*const kbModal = document\.getElementById\(\'kbModal\'\);\s*const openKbSidebarBtn.*?const kbSearchInput = document\.getElementById\(\'kbSearchInput\'\);', replacement, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Logs added to auth.js.")
