import re

filepath = 'frontend/js/dashboard.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'(// Knowledge Base Logic.*?)(const viewInInventoryBtn)', content, flags=re.DOTALL)
if match:
    kb_js = match.group(1)
    
    # Remove from dashboard.js
    content = content.replace(kb_js, '\n\n')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Append to auth.js
    auth_filepath = 'frontend/js/auth.js'
    with open(auth_filepath, 'a', encoding='utf-8') as auth_f:
        auth_f.write('\n\n' + kb_js + '\n')
    
    print("JS logic successfully moved to auth.js")
else:
    print("kb_js NOT found via second regex!")
