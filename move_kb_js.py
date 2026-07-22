import re

filepath = 'frontend/js/dashboard.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract KB Logic block
# It starts at // Knowledge Base Logic and ends just before const viewInInventoryBtn
match = re.search(r'// Knowledge Base Logic.*?\}\);\s*\}\);', content, flags=re.DOTALL)
if match:
    kb_js = match.group(0)
    print("kb_js found, length:", len(kb_js))
    
    # Remove from dashboard.js
    content = content.replace(kb_js, '')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Append to auth.js
    auth_filepath = 'frontend/js/auth.js'
    with open(auth_filepath, 'a', encoding='utf-8') as auth_f:
        auth_f.write('\n\n' + kb_js + '\n')
    
    print("JS logic moved to auth.js.")
else:
    print("kb_js NOT found!")
