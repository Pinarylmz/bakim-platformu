import re

filepath = 'frontend/js/auth.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove everything after document.addEventListener('DOMContentLoaded', enforceRBAC);
marker = "document.addEventListener('DOMContentLoaded', enforceRBAC);"
if marker in content:
    content = content[:content.index(marker) + len(marker)] + "\n"

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("auth.js truncated properly.")
