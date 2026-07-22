import re

filepath = 'frontend/dashboard.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to find the <div class="parts-panel-overlay" id="addUavModal"> block
match = re.search(r'<div class="parts-panel-overlay" id="addUavModal">.*?</div>\s*</div>\s*</div>', content, re.DOTALL)
if match:
    print(match.group(0))
else:
    print("addUavModal not found!")
