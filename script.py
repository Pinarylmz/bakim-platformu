import os

replacements = {
    'Flight Ready': 'Flight Ready',
    'Pending Review': 'Pending Review',
    'Maintenance': 'Maintenance',
    '"OK"': '"OK"',
    "'OK'": "'OK'",
    '"Warning"': '"Warning"',
    "'Warning'": "'Warning'",
    '"Warning"': '"Warning"',
    '"Critical"': '"Critical"',
    "'Critical'": "'Critical'",
    '"Critical"': '"Critical"',
    '"Open"': '"Open"',
    "'Open'": "'Open'",
    '"Closed"': '"Closed"',
    "'Kapatıldı'": "'Kapatıldı'",
    '"Pending"': '"Pending"',
    "'Pending'": "'Pending'",
    '"Approved"': '"Approved"',
    "'Approved'": "'Approved'",
    '"Rejected"': '"Rejected"',
    "'Rejected'": "'Rejected'",
}

def process_file(filepath):
    encodings = ['utf-8', 'windows-1254', 'cp1252']
    content = None
    used_encoding = None
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                content = f.read()
            used_encoding = enc
            break
        except UnicodeDecodeError:
            continue
            
    if content is None:
        return
        
    new_content = content
    for old, new in replacements.items():
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root, dirs, files in os.walk('.'):
    if 'venv' in root or '.git' in root or '.gemini' in root:
        continue
    for file in files:
        if file.endswith('.py') or file.endswith('.js') or file.endswith('.html'):
            process_file(os.path.join(root, file))
