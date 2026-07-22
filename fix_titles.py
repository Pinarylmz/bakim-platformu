import os
import glob

for filepath in glob.glob('frontend/*.html'):
    if not os.path.isfile(filepath): continue
    content = None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        with open(filepath, 'r', encoding='latin-1') as f:
            content = f.read()
            
    # Fix the title tags that got corrupted
    content = content.replace('UAV Bak"mda', 'UAV Bakımda')
    content = content.replace('UAV Bakmda', 'UAV Bakımda')
    content = content.replace('UAV Bakmda', 'UAV Bakımda')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
