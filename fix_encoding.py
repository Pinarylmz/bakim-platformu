import os

replacements = {
    'HA bulunamad': 'UAV not found',
    'Para bulunamad': 'Part not found',
    'Para baaryla skld.': 'Part uninstalled successfully.',
    'Kullanc ad zaten kaytl': 'Username already registered',
    'Hatal kullanc ad veya ifre': 'Incorrect username or password',
    'Pasif kullanc': 'Inactive user',
    'Hesabnz Ynetici onay bekliyor.': 'Your account is pending Admin approval.',
    'Geersiz token': 'Invalid token',
    'Kullanc bulunamad veya pasif': 'User not found or inactive',
    'Not enough permissions': 'Not enough permissions',
    'HA bulunamad veya bakmda': 'UAV not found or in maintenance',
    'mri bulunamad': 'Work Order not found',
    'mri zaten kapatlm': 'Work Order already closed',
    'Bu Seri Numaras/QR ile bir HA zaten mevcut.': 'A UAV with this Serial Number/QR already exists.',
    'HA Uua Hazr deil. Ltfen nce bekleyen i emirlerini kapatn.': 'İHA Flight Ready değil. Lütfen önce bekleyen iş emirlerini kapatın.',
    'Telemetri ilendi. Eikler aldysa uyarlar oluturuldu.': 'Telemetry processed. Alerts generated if thresholds exceeded.',
    'Kullanc bulunamad': 'User not found',
    'Kullanc baaryla {approval.approval_status}': 'User {approval.approval_status} successfully',
    'Kendi hesabnz silemezsiniz': 'Cannot delete yourself',
    'Kullanc baaryla silindi': 'User deleted successfully',
    'Mevcut ifre hatal': 'Incorrect current password',
    'ifre baaryla gncellendi': 'Password updated successfully'
}

for root, dirs, files in os.walk('backend/routers'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            # Try reading with different encodings, fallback to latin-1 to preserve bytes
            content = None
            for enc in ['utf-8', 'windows-1254', 'latin-1']:
                try:
                    with open(filepath, 'r', encoding=enc) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    pass
            
            if content:
                # Direct string fixes for garbled output from previous PowerShell replacements
                for k, v in replacements.items():
                    content = content.replace(k, v)
                
                # Specifically replace the bad 0xdd bytes if they exist by catching them manually
                # 0xdd is 'Ý' in latin-1, but the terminal showed it differently.
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed {filepath}")
