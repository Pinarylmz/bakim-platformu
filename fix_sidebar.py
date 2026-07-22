import os
import glob
import re

for filepath in glob.glob('frontend/*.html'):
    if 'index.html' in filepath or 'register.html' in filepath:
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the redundant System Admin link from the nav-links ul
    content = re.sub(r'<li[^>]*><a href="users\.html"[^>]*>System Admin</a></li>\s*', '', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Removed redundant System Admin link.")
