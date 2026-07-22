const token = localStorage.getItem('token');
if (!token) { window.location.href = 'index.html'; }


const API_BASE = 'http://localhost:8000';
let html5QrcodeScanner = null;
let currentUAVs = []; // Store fetched UAVs

async function fetchReports() {
    try {
        const response = await fetch(`${API_BASE}/work-orders/`);
        if (response.ok) {
            const data = await response.json();
            renderReports(data);
        }
    } catch (error) {
        console.error("Failed to fetch reports", error);
    }
}

function renderReports(items) {
    const tbody = document.getElementById('reportsBody');
    tbody.innerHTML = '';
    
    if(items.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; color: var(--text-secondary);">No damage reports found.</td></tr>`;
        return;
    }

    items.forEach(item => {
        const tr = document.createElement('tr');
        const imgHtml = item.image_path ? `<a href="${API_BASE}${item.image_path}" target="_blank" class="img-link">View Image</a>` : 'No Image';
        
        tr.innerHTML = `
            <td><strong>${item.uav_id}</strong></td>
            <td>Part ID: ${item.part_id}</td>
            <td>${item.description}</td>
            <td>${imgHtml}</td>
            <td>
                <span style="color: ${item.status === 'Kapatıldı' ? 'var(--success-color)' : 'var(--warning-color)'}; font-weight:bold;">
                    ${item.status}
                </span>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Fetch UAVs for the Dropdown
async function fetchUAVDropdown() {
    try {
        const res = await fetch(`${API_BASE}/uavs/`, { headers: { 'Authorization': `Bearer ${token}` } });
        if (res.ok) {
            currentUAVs = await res.json();
            const select = document.getElementById('uavSerial');
            select.innerHTML = '<option value="" disabled selected>Select UAV...</option>';
            currentUAVs.forEach(u => {
                const opt = document.createElement('option');
                opt.value = u.id;
                opt.textContent = `${u.model_name} (${u.serial_number})`;
                // Store serial number in dataset for QR matching
                opt.dataset.serial = u.serial_number; 
                select.appendChild(opt);
            });
        }
    } catch(err) {
        console.error("Failed to fetch UAVs", err);
    }
}

// Modal Logic
const modal = document.getElementById('reportDamageModal');

document.getElementById('openReportModalBtn').addEventListener('click', () => {
    modal.classList.add('open');
    modal.style.display = 'flex';
    document.getElementById('formError').textContent = '';
    document.getElementById('damageReportForm').reset();
    document.getElementById('inventorySelect').innerHTML = '<option value="" disabled selected>Select UAV first to load parts...</option>';
    
    // Reset scanner view
    document.getElementById('qrScannerContainer').style.display = 'none';
    if(html5QrcodeScanner) {
        html5QrcodeScanner.clear().catch(e => console.log(e));
        html5QrcodeScanner = null;
    }
});

document.getElementById('closeReportModalBtn').addEventListener('click', () => {
    modal.classList.remove('open');
    modal.style.display = 'none';
    if (html5QrcodeScanner) {
        html5QrcodeScanner.clear().catch(e => console.log(e));
        html5QrcodeScanner = null;
    }
});

// Toggle QR Scanner
document.getElementById('toggleQrScannerBtn').addEventListener('click', () => {
    const container = document.getElementById('qrScannerContainer');
    if (container.style.display === 'none') {
        container.style.display = 'block';
        if (!html5QrcodeScanner) {
            html5QrcodeScanner = new Html5QrcodeScanner("qr-reader", { fps: 10, qrbox: {width: 250, height: 250} }, false);
            html5QrcodeScanner.render(onScanSuccess, onScanError);
        }
    } else {
        container.style.display = 'none';
        if (html5QrcodeScanner) {
            html5QrcodeScanner.clear().catch(e => console.log(e));
            html5QrcodeScanner = null;
        }
    }
});

function onScanSuccess(decodedText, decodedResult) {
    console.log(`Scan result: ${decodedText}`);
    
    // Find matching UAV option by serial number
    const select = document.getElementById('uavSerial');
    let found = false;
    Array.from(select.options).forEach(opt => {
        if(opt.dataset.serial === decodedText) {
            select.value = opt.value;
            found = true;
        }
    });
    
    if(found) {
        loadInstalledParts(select.value);
    } else {
        alert("Scanned UAV not found in the system.");
    }
    
    // Close scanner after success
    document.getElementById('toggleQrScannerBtn').click();
}

function onScanError(errorMessage) {
    // silently handle errors for continuous scanning
}

// UAV Dropdown Change Event
document.getElementById('uavSerial').addEventListener('change', (e) => {
    const val = e.target.value;
    if(val) {
        loadInstalledParts(val);
    }
});

async function loadInstalledParts(uav_id) {
    const select = document.getElementById('inventorySelect');
    select.innerHTML = '<option value="" disabled selected>Loading installed parts...</option>';
    
    try {
        const response = await fetch(`${API_BASE}/inventory/installed-parts/${uav_id}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            const parts = await response.json();
            
            select.innerHTML = '';
            if (parts.length === 0) {
                 select.innerHTML = '<option value="" disabled selected>No parts installed on this UAV</option>';
                 return;
            }
            parts.forEach(part => {
                const opt = document.createElement('option');
                opt.value = part.id;
                opt.textContent = `${part.name} (${part.serial_number})`;
                select.appendChild(opt);
            });
        } else {
            select.innerHTML = '<option value="" disabled selected>Failed to load parts.</option>';
        }
    } catch (e) {
        console.error("Error loading parts", e);
        select.innerHTML = '<option value="" disabled selected>Network error loading parts</option>';
    }
}

document.getElementById('damageReportForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const uavId = document.getElementById('uavSerial').value;
    const partId = document.getElementById('inventorySelect').value;
    const desc = document.getElementById('damageDescription').value;
    const urgency = document.getElementById('urgencyLevel').value;
    
    if (!uavId || !partId) {
        document.getElementById('formError').textContent = 'Please select a UAV and a damaged part.';
        return;
    }
    
    try {
        const payload = {
            uav_id: parseInt(uavId),
            part_id: parseInt(partId),
            description: desc,
            severity: urgency === "Critical" ? 1 : (urgency === "MODERATE" ? 2 : 4)
        };

        const response = await fetch(`${API_BASE}/work-orders/`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });
        
        if (response.ok) {
            modal.classList.remove('open');
            modal.style.display = 'none';
            fetchReports();
        } else {
            const data = await response.json();
            document.getElementById('formError').textContent = data.detail || 'Error saving report.';
        }
    } catch (e) {
        document.getElementById('formError').textContent = 'Network error.';
    }
});

// Init
fetchReports();
fetchUAVDropdown();


