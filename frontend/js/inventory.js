// Simple Auth Check
const token = localStorage.getItem('token');
if (!token) { window.location.href = 'index.html'; }


const API_BASE = 'http://localhost:8000';
let currentInventory = [];

// Translation Map for English localization without breaking backend db
const translationMap = {
    // Categories
    "Ana Rotor Sistemi": "Main Rotor System",
    "Kuyruk Roturu Sistemi": "Tail Rotor System",
    "Kuyruk Rotoru Sistemi": "Tail Rotor System",
    "Güç Aktarma": "Power Transmission",
    "Motor / Güç Ünitesi": "Motor / Power Unit",
    "Uçuş Kontrol": "Flight Control",
    "Elektronik/Aviyonik": "Electronics/Avionics",
    "Gövde ve İniş": "Airframe & Landing",
    "Enerji ve Haberleşme": "Power & Communication",
    
    // Parts
    "Ana rotor kanatları (Titanium)": "Main Rotor Blades (Titanium)",
    "Kuyruk rotoru göbeği": "Tail Rotor Hub",
    "Ana dişli kutusu": "Main Gearbox",
    "Fırçasız motor (BLDC v3)": "Brushless Motor (BLDC v3)",
    "Uçuş kontrol kartı (FC)": "Flight Control Board (FC)",
    "Kamera/Gimbal Modülü": "Camera/Gimbal Module",
    "İniş takımı (Amortisörlü)": "Landing Gear (Shock Absorbing)",
    "LiPo/Li-Ion batarya": "LiPo/Li-Ion Battery"
};

function translateText(text) {
    if (!text) return text;
    return translationMap[text] || text;
}


async function fetchInventory() {
    try {
        const response = await fetch(`${API_BASE}/inventory/installed-parts`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            currentInventory = await response.json();
            renderInventory();
        } else {
            console.error("Failed to fetch inventory");
        }
    } catch (error) {
        console.error("Network error.while fetching inventory", error);
    }
}

const categoryIdMap = {
    1: "Main Rotor System",
    2: "Tail Rotor System",
    3: "Power Transmission",
    4: "Motor / Power Unit",
    5: "Flight Control",
    6: "Electronics/Avionics",
    7: "Airframe & Landing",
    8: "Power & Communication"
};


function renderInventory() {
    const tbody = document.getElementById('inventoryBody');
    tbody.innerHTML = '';
    
    // Filter logic
    const filterSelect = document.getElementById('filterUavSelect');
    let items = currentInventory;
    if (filterSelect && filterSelect.value !== 'all') {
        const targetId = parseInt(filterSelect.value);
        items = currentInventory.filter(item => item.uav_id === targetId);
    }
    
    if(items.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; color: var(--text-secondary);">No parts found.</td></tr>`;
        return;
    }


    items.forEach(item => {
        const tr = document.createElement('tr');
        const isKritik = item.status.toUpperCase() !== 'OK';
        
        tr.innerHTML = `
            <td><strong style="color:var(--text-primary);">${item.serial_number}</strong></td>
            <td>${translateText(item.name)}</td>
            <td><span style="font-size: 12px; color: var(--text-secondary); background: var(--input-bg); padding: 4px 8px; border-radius: 4px;">${categoryIdMap[item.category_id] || 'CAT-' + item.category_id}</span></td>
            <td><span class="part-status ${isKritik ? 'text-red' : 'text-green'}">${item.status}</span></td>
            <td>
                <button class="btn-secondary btn-small delete-btn" data-id="${item.id}" style="color: var(--error-color); border-color: var(--error-color);"><i class="fas fa-trash"></i> Delete</button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    // Delete Events
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            if(confirm('Are you sure you want to delete this part?')) {
                const id = e.target.getAttribute('data-id');
                await deleteInventoryItem(id);
            }
        });
    });
}

async function deleteInventoryItem(id) {
    try {
        const response = await fetch(`${API_BASE}/inventory/installed-parts/${id}`, { 
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if(response.ok) fetchInventory();
    } catch(e) {
        console.error("Delete failed", e);
    }
}

// Add Part Modal Logic
const addPartModal = document.getElementById('addPartModal');
const openAddPartModalBtn = document.getElementById('openAddPartModalBtn');
const closeAddPartModalBtn = document.getElementById('closeAddPartModalBtn');
let html5QrcodeScannerPart = null;

if (openAddPartModalBtn && addPartModal) {
    openAddPartModalBtn.addEventListener('click', () => {
        document.getElementById('addPartForm').reset();
        document.getElementById('partError').textContent = '';
        addPartModal.style.display = 'flex';
        addPartModal.classList.add('open');
        
        try {
            if(!html5QrcodeScannerPart) {
                html5QrcodeScannerPart = new Html5QrcodeScanner("qr-reader", { fps: 10, qrbox: {width: 250, height: 250} }, false);
                html5QrcodeScannerPart.render((decodedText) => {
                    document.getElementById('partSerial').value = decodedText;
                    html5QrcodeScannerPart.clear();
                });
            }
        } catch(e) { console.log('QR Scanner init failed', e); }
    });
}

function closeAddPartModal() {
    if(addPartModal) {
        addPartModal.style.display = 'none';
        addPartModal.classList.remove('open');
        if(html5QrcodeScannerPart) {
            html5QrcodeScannerPart.clear().catch(e => console.log(e));
            html5QrcodeScannerPart = null;
        }
    }
}

if (closeAddPartModalBtn) {
    closeAddPartModalBtn.addEventListener('click', closeAddPartModal);
}

window.addEventListener('click', (e) => {
    if (e.target === addPartModal) {
        closeAddPartModal();
    }
});

const addPartForm = document.getElementById('addPartForm');
if (addPartForm) {
    addPartForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const errEl = document.getElementById('partError');
        errEl.textContent = '';
        
        const payload = {
            serial_number: document.getElementById('partSerial').value,
            name: document.getElementById('partName').value,
            category_id: parseInt(document.getElementById('partCategory').value),
            uav_id: parseInt(document.getElementById('partUavId').value),
            max_flight_hours: parseFloat(document.getElementById('partMaxHours').value),
            current_flight_hours: 0,
            current_cycles: 0,
            status: "OK",
            is_active: true
        };
        
        try {
            const res = await fetch(`${API_BASE}/inventory/installed-parts`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });
            
            if (res.ok) {
                closeAddPartModal();
                fetchInventory(); // Live update
            } else {
                const data = await res.json();
                errEl.textContent = data.detail || 'Failed to add part.';
            }
        } catch(err) {
            errEl.textContent = 'Network error.';
            console.error(err);
        }
    });
}

async function fetchDropdownData() {
    try {
        const [catRes, uavRes] = await Promise.all([
            fetch(`${API_BASE}/inventory/categories`, { headers: { 'Authorization': `Bearer ${token}` } }),
            fetch(`${API_BASE}/uavs/`, { headers: { 'Authorization': `Bearer ${token}` } })
        ]);
        
        if (catRes.ok) {
            const categories = await catRes.json();
            const catSelect = document.getElementById('partCategory');
            // Keep the default disabled option
            categories.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c.id;
                opt.textContent = translateText(c.name);
                catSelect.appendChild(opt);
            });
        }
        
        
        if (uavRes.ok) {
            const uavs = await uavRes.json();
            const uavSelect = document.getElementById('partUavId');
            const filterSelect = document.getElementById('filterUavSelect');
            
            const urlParams = new URLSearchParams(window.location.search);
            const targetSerial = urlParams.get('uav_id');
            
            uavs.forEach(u => {
                const opt = document.createElement('option');
                opt.value = u.id;
                opt.textContent = u.model_name + " (" + u.serial_number + ")";
                uavSelect.appendChild(opt);
                
                if (filterSelect) {
                    const fOpt = document.createElement('option');
                    fOpt.value = u.id;
                    fOpt.textContent = u.model_name + " (" + u.serial_number + ")";
                    filterSelect.appendChild(fOpt);
                    
                    if (targetSerial && u.serial_number === targetSerial) {
                        fOpt.selected = true;
                    }
                }
            });
        }
    } catch(err) {
        console.error("Failed to load dropdown data", err);
    }
}

// Init Language Support (If exists globally)
if(typeof setLanguage === 'function') {
    setLanguage(localStorage.getItem('lang') || 'EN');
}

document.addEventListener('DOMContentLoaded', async () => {
    // Wait for dropdown data to be fetched so filter can be populated
    await fetchDropdownData();
    await fetchInventory();

    const filterSelect = document.getElementById('filterUavSelect');
    if (filterSelect) {
        filterSelect.addEventListener('change', () => {
            renderInventory();
        });
    }
});
