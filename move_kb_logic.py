import os
import re

auth_file = 'frontend/js/auth.js'
with open(auth_file, 'r', encoding='utf-8') as f:
    auth_content = f.read()

# Remove the KB Logic from auth.js completely
auth_content = re.sub(r'// Global Knowledge Base Logic.*', '', auth_content, flags=re.DOTALL)
with open(auth_file, 'w', encoding='utf-8') as f:
    f.write(auth_content)


dash_file = 'frontend/js/dashboard.js'
with open(dash_file, 'r', encoding='utf-8') as f:
    dash_content = f.read()

kb_js_logic = '''
// Knowledge Base Logic
document.addEventListener('DOMContentLoaded', () => {
    const kbModal = document.getElementById('kbModal');
    const openKbSidebarBtn = document.getElementById('openKbSidebarBtn');
    const closeKbBtn = document.getElementById('closeKbBtn');
    const tabGuideBtn = document.getElementById('tabGuideBtn');
    const tabPartsBtn = document.getElementById('tabPartsBtn');
    const kbGuideTab = document.getElementById('kbGuideTab');
    const kbPartsTab = document.getElementById('kbPartsTab');
    const kbSearchInput = document.getElementById('kbSearchInput');

    const kbPartsData = [
        { category: "Ana Rotor Sistemi", parts: ["Ana rotor kanatları", "Rotor göbeği (hub)", "Swashplate", "Pitch link'ler", "Rotor mili (mast)", "Lead-lag damperleri"] },
        { category: "Kuyruk Rotoru Sistemi", parts: ["Kuyruk rotoru kanatları", "Kuyruk rotoru göbeği", "Kuyruk tahrik şaftı", "Kuyruk dişli kutusu", "Kuyruk kumanda bağlantıları"] },
        { category: "Güç Aktarma", parts: ["Ana dişli kutusu", "Kayış-kasnak sistemi", "Tek yönlü rulman (freewheel)", "Tahrik şaftları"] },
        { category: "Motor / Güç Ünitesi", parts: ["Fırçasız motor (BLDC)", "ESC", "Yakıtlı Motor", "Yakıt sistemi", "Egzoz"] },
        { category: "Uçuş Kontrol", parts: ["Servo motorlar", "Uçuş kontrol kartı (FC)", "IMU/Gyro", "Kumanda çubukları"] },
        { category: "Elektronik/Aviyonik", parts: ["Kablo tesisatı", "GPS/Barometre", "Telemetri/Anten", "Kamera/Gimbal"] },
        { category: "Gövde ve İniş", parts: ["Ana şasi", "Kaplama panelleri (canopy)", "Amortisörler", "İniş takımı"] },
        { category: "Enerji ve Haberleşme", parts: ["LiPo/Li-Ion batarya", "Yakıt tankı", "RC alıcı/verici", "Data link"] }
    ];

    function renderKbParts(filterText = '') {
        const list = document.getElementById('kbPartsList');
        if(!list) return;
        list.innerHTML = '';
        const lowerFilter = filterText.toLowerCase();

        kbPartsData.forEach(cat => {
            const filteredParts = cat.parts.filter(p => p.toLowerCase().includes(lowerFilter) || cat.category.toLowerCase().includes(lowerFilter));
            
            if (filteredParts.length > 0) {
                const catDiv = document.createElement('div');
                catDiv.style.marginBottom = '15px';
                catDiv.innerHTML = '<h5 style="color: var(--primary-color); margin-bottom: 8px;">' + cat.category + '</h5>';
                
                filteredParts.forEach(p => {
                    const partDiv = document.createElement('div');
                    partDiv.style.padding = '8px';
                    partDiv.style.background = 'var(--bg-color)';
                    partDiv.style.border = '1px solid var(--border-color)';
                    partDiv.style.borderRadius = '4px';
                    partDiv.style.marginBottom = '5px';
                    partDiv.style.color = 'var(--text-secondary)';
                    partDiv.style.fontSize = '13px';
                    partDiv.textContent = p;
                    catDiv.appendChild(partDiv);
                });
                list.appendChild(catDiv);
            }
        });
        
        if (list.innerHTML === '') {
            list.innerHTML = '<p style="color: var(--text-secondary); text-align: center;">No parts found.</p>';
        }
    }

    if(openKbSidebarBtn && kbModal) {
        openKbSidebarBtn.addEventListener('click', (e) => {
            e.preventDefault();
            kbModal.style.display = 'flex';
            renderKbParts();
        });
    }

    if(closeKbBtn && kbModal) {
        closeKbBtn.addEventListener('click', () => {
            kbModal.style.display = 'none';
        });
    }

    // Modal dışındaki karanlık alana tıklayınca kapanma (Global listener olarak ekliyoruz)
    window.addEventListener('click', (e) => {
        if(e.target === kbModal) {
            kbModal.style.display = 'none';
        }
    });

    if(tabGuideBtn && tabPartsBtn && kbGuideTab && kbPartsTab) {
        tabGuideBtn.addEventListener('click', () => {
            tabGuideBtn.classList.add('active');
            tabGuideBtn.style.borderBottomColor = 'var(--primary-color)';
            tabGuideBtn.style.color = 'white';
            
            tabPartsBtn.classList.remove('active');
            tabPartsBtn.style.borderBottomColor = 'transparent';
            tabPartsBtn.style.color = 'var(--text-secondary)';
            
            kbGuideTab.style.display = 'block';
            kbPartsTab.style.display = 'none';
        });

        tabPartsBtn.addEventListener('click', () => {
            tabPartsBtn.classList.add('active');
            tabPartsBtn.style.borderBottomColor = 'var(--primary-color)';
            tabPartsBtn.style.color = 'white';
            
            tabGuideBtn.classList.remove('active');
            tabGuideBtn.style.borderBottomColor = 'transparent';
            tabGuideBtn.style.color = 'var(--text-secondary)';
            
            kbGuideTab.style.display = 'none';
            kbPartsTab.style.display = 'block';
        });
    }

    if(kbSearchInput) {
        kbSearchInput.addEventListener('input', (e) => {
            renderKbParts(e.target.value);
        });
    }
});
'''

if '// Knowledge Base Logic' not in dash_content:
    with open(dash_file, 'a', encoding='utf-8') as f:
        f.write('\n' + kb_js_logic)

print("Moved KB Logic to dashboard.js")
