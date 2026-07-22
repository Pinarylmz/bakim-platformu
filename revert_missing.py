import os

replacements = {
    'Uçuşa Hazır': 'Flight Ready',
    'Onay Bekliyor': 'Pending Review',
    'Bakımda': 'Maintenance',
    '"Sorunsuz"': '"OK"',
    "'Sorunsuz'": "'OK'",
    '"Uyarı"': '"Warning"',
    "'Uyarı'": "'Warning'",
    '"Kritik"': '"Critical"',
    "'Kritik'": "'Critical'",
    '"Açık"': '"Open"',
    "'Açık'": "'Open'",
    '"Kapatıldı"': '"Closed"',
    "'Closed'": "'Closed'",
    '"Bekliyor"': '"Pending"',
    "'Bekliyor'": "'Pending'",
    '"Onaylandı"': '"Approved"',
    "'Onaylandı'": "'Approved'",
    '"Reddedildi"': '"Rejected"',
    "'Reddedildi'": "'Rejected'",
    
    # frontend/js/dashboard.js
    'İHA bulunamadı.': 'No UAVs found.',
    'Veriler yüklenirken hata oluştu.': 'Error loading dashboard data.',
    'Bu filtreye uygun parça bulunamadı.': 'No parts match this filter.',
    'Telemetri yükleniyor...': 'Loading telemetry...',
    'Telemetri hatası': 'Telemetry error',
    'Simülasyonu Başlat': 'Start Simulation',
    'Simülasyonu Durdur': 'Stop Simulation',
    'Telemetri yüklenirken ağ hatası oluştu.': 'Network error loading telemetry.',
    
    # frontend/js/personnel.js
    'Takip verisi bulunamadı.': 'No tracking data available.',
    'Aktif': 'Active',
    'Silindi': 'Deleted',
    
    # frontend/js/profile.js
    'Profil yüklenirken hata oluştu': 'Error loading profile',
    'Ağ hatası': 'Network error',
    'Son aktivite bulunamadı.': 'No recent activities found.',
    'Aktiviteler yüklenirken hata oluştu.': 'Error loading activities.',
    'Aktiviteler yüklenirken ağ hatası oluştu.': 'Network error while loading activities.',
    'Profil başarıyla güncellendi!': 'Profile updated successfully!',
    'Profil güncellenirken hata oluştu.': 'Error updating profile.',
    'Şifre başarıyla güncellendi!': 'Password updated successfully!',
    'Şifre güncellenirken hata oluştu (Mevcut şifrenizi kontrol edin)': 'Error updating password (Check current password)',
    'Şu an bekleyen onay yok.': 'No pending approvals at the moment.',
    'Bekleyen kullanıcılar alınırken hata oluştu.': 'Error fetching pending users.',
    'Mühendis': 'Engineer',
    'Teknisyen': 'Technician',
    'Onayla': 'Approve',
    'Reddet': 'Reject',
}

files_to_check = [
    'frontend/js/dashboard.js',
    'frontend/js/personnel.js',
    'frontend/js/profile.js',
    'backend/seed.py'
]

for filepath in files_to_check:
    if not os.path.exists(filepath): continue
    content = None
    for enc in ['utf-8', 'windows-1254', 'latin-1']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            pass
            
    if content:
        new_content = content
        for old, new in replacements.items():
            new_content = new_content.replace(old, new)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Reverted translation in {filepath}")
