import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Find the specific corrupted string the user mentioned and remove it.
    # The user mentioned 'Ã¢ÂœÂˆÃ¯Â¸Â'. We can just use a regex to strip all 'Ã' and its garbage.
    # A safe way is to replace the exact HTML that renders the icon.
    content = re.sub(r'<div class="uav-icon">.*?</div>', '<div class="uav-icon">🚁</div>', content)
    
    # Also clean up any lingering 'ǫ', 'Ǭ', ''
    content = re.sub(r'[ǫǬ]', '', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

clean_file('frontend/js/dashboard.js')
print("dashboard.js cleaned.")
