import time

filepath = 'backend/routers/auth.py'
with open(filepath, 'a', encoding='utf-8') as f:
    f.write('\n# Trigger reload\n')

print("auth.py touched to trigger reload.")
