// Simple Auth Check
const token = localStorage.getItem('token');
if (!token) {
    window.location.href = 'index.html';
}


const API_BASE = 'http://localhost:8000';
let currentUAVs = [];
let currentParts = [];
let telemetryInterval = null;
let currentUavIdForTelemetry = null;
let isSimulationRunning = false;

async function fetchUAVs() {
    try {
        const response = await fetch(`${API_BASE}/uavs/`);
        if (response.ok) {
            currentUAVs = await response.json();
            renderUAVs();
        }
    } catch (error) {
        console.error("Failed to fetch UAVs", error);
    }
}


function renderUAVs() {
    const grid = document.getElementById('uavGrid');
    if (!grid) return;
    grid.innerHTML = '';
    
    if(currentUAVs.length === 0) {
        grid.innerHTML = `<p style="color: var(--text-secondary); grid-column: 1/-1;">No UAVs found. Click Seed Test Data to generate some.</p>`;
        return;
    }

    currentUAVs.forEach(uav => {
        const card = document.createElement('div');
        card.className = 'uav-card';
        card.style.cursor = 'pointer';
        
        let statusColor = 'var(--success-color)';
        const stat = (uav.status || 'Flight Ready');
        if (stat === 'Maintenance' || stat === 'Warning') statusColor = 'var(--warning-color)';
        if (stat === 'Critical' || stat === 'Error') statusColor = 'var(--error-color)';
        
        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div class="uav-icon">🚁</div>
                <span style="font-size: 12px; font-weight: 600; padding: 4px 8px; border-radius: 4px; background: ${statusColor}; color: white;">${stat}</span>
            </div>
            <h3 style="margin-top: 15px;">${uav.model_name}</h3>
            <p style="font-size: 13px; color: var(--text-secondary);">SN: ${uav.serial_number}</p>
            <p style="margin-top: 10px; font-size: 14px;"><span>Flight Hours</span>: <strong class="text-white">${uav.total_flight_hours} h</strong></p>
        `;
        
        card.addEventListener('click', () => {
            openPartsPanel(uav.serial_number, uav.model_name, uav.total_flight_hours, uav.status, uav.id);
        });
        
        grid.appendChild(card);
    });
}


const seedBtn = document.getElementById('seedBtn');
if (seedBtn) {
    seedBtn.addEventListener('click', async () => {
        if(confirm("Generate test data?")) {
            seedBtn.textContent = "Seeding...";
            try {
                alert("Please run 'python seed.py' in the backend terminal to seed data.");
                seedBtn.textContent = "Seed Test Data";
            } catch(e) {
                console.error(e);
            }
        }
    });
}

async function openPartsPanel(uavSerial, uavName, uavHours, uavStatus, internalId) {
    document.getElementById('panelUavName').textContent = uavName;
    document.getElementById('panelUavSerial').textContent = uavSerial;
    document.getElementById('panelUavHours').textContent = uavHours + " h";
    
    const statusEl = document.getElementById('panelUavStatus');
    statusEl.textContent = uavStatus || 'Flight Ready';
    statusEl.style.color = (uavStatus === 'Flight Ready') ? 'var(--success-color)' : ((uavStatus === 'Maintenance') ? 'var(--Warning-color)' : 'var(--error-color)');

    // Start telemetry
    currentUavIdForTelemetry = internalId;
    startTelemetryPolling();

    document.getElementById('partsPanel').classList.add('open');
    document.getElementById('partsList').innerHTML = '<p>Loading...</p>';
    
    try {
        const response = await fetch(`${API_BASE}/uavs/${uavSerial}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            const data = await response.json();
            currentParts = data.installed_parts.map(p => ({
                id: p.id,
                category: p.category ? p.category.name : "Hardware",
                name: p.name,
                serial_number: p.serial_number,
                status: p.status,
                current_usage_hours: p.current_flight_hours,
                lifespan_hours: p.max_flight_hours
            }));
            renderParts('all');
        } else {
            document.getElementById('partsList').innerHTML = '<p>Error loading parts.</p>';
        }
    } catch (error) {
        console.error("Failed to fetch parts", error);
        document.getElementById('partsList').innerHTML = '<p>Error loading parts.</p>';
    }
}

function renderParts(filter = 'all') {
    const list = document.getElementById('partsList');
    list.innerHTML = '';

    if (currentParts.length === 0) {
        list.innerHTML = '<p style="color: var(--text-secondary); text-align:center; margin-top: 20px;">No hardware parts are currently installed on this UAV.</p>';
        return;
    }

    const filtered = currentParts.filter(p => {
        const s = (p.status || '').toUpperCase();
        if (filter === 'Critical') return s === 'CRITICAL' || s === 'DAMAGED';
        if (filter === 'Warning') return s === 'WARNING';
        return true;
    });

    if (filtered.length === 0) {
        list.innerHTML = '<p style="color: var(--text-secondary); text-align:center; margin-top: 20px;">No parts found.</p>';
        return;
    }

    // Group by category
    const grouped = filtered.reduce((acc, part) => {
        if (!acc[part.category]) acc[part.category] = [];
        acc[part.category].push(part);
        return acc;
    }, {});

    for (const [category, parts] of Object.entries(grouped)) {
        const catGroup = document.createElement('div');
        catGroup.className = 'part-category-group';
        catGroup.innerHTML = `<h4>${category}</h4>`;
        
        parts.forEach(part => {
            const isCritical = (part.status.toUpperCase() !== 'OK');
            const ratio = (part.lifespan_hours > 0) ? (part.current_usage_hours / part.lifespan_hours) * 100 : 0;
            const healthClass = ratio > 90 ? 'health-Critical' : (ratio > 70 ? 'health-warningÃ½' : 'health-good');
            
            const partEl = document.createElement('div');
            partEl.id = `part-card-${part.serial_number}`;
            partEl.className = `part-item ${isCritical ? 'Critical-border' : ''}`;
            partEl.innerHTML = `
                <div class="part-info">
                    <strong>${part.name}</strong> 
                    <span class="serial-no">(${part.serial_number})</span>
                    <div id="part-status-${part.serial_number}" class="part-status ${isCritical ? 'text-red' : 'text-green'}">${part.status}</div>
                </div>
                <div class="part-health">
                    <div class="health-bar-bg">
                        <div class="health-bar-fill ${healthClass}" style="width: ${Math.min(ratio, 100)}%"></div>
                    </div>
                    <div class="health-stats">${part.current_usage_hours}h / ${part.lifespan_hours}h</div>
                </div>
            `;
            catGroup.appendChild(partEl);
        });
        list.appendChild(catGroup);
    }
}

// Telemetry Logic
function startTelemetryPolling() {
    if(telemetryInterval) clearInterval(telemetryInterval);
    fetchLatestTelemetry();
    telemetryInterval = setInterval(fetchLatestTelemetry, 3000);
}

function stopTelemetryPolling() {
    if(telemetryInterval) clearInterval(telemetryInterval);
}

async function fetchLatestTelemetry() {
    if(!currentUavIdForTelemetry) return;
    try {
        const res = await fetch(`${API_BASE}/telemetry/${currentUavIdForTelemetry}/latest`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if(res.ok) {
            const data = await res.json();
            document.getElementById('liveBattery').textContent = (data.battery_level !== null ? data.battery_level.toFixed(1) : '--') + '%';
            document.getElementById('liveTemp').textContent = (data.esc_temperature !== null ? data.esc_temperature.toFixed(1) : '--') + '°C';
            document.getElementById('liveVib').textContent = (data.vibration_level !== null ? data.vibration_level.toFixed(2) : '--');
            document.getElementById('liveRpm').textContent = (data.rpm_asymmetry !== null ? data.rpm_asymmetry.toFixed(2) : '--') + '%';
        }
    } catch(e) {
        console.error('Error fetching telemetry:', e);
    }
}

let simInterval = null;
document.body.addEventListener('click', (e) => {
    const toggleSimBtn = e.target.closest('#toggleSimulationBtn');
    if (toggleSimBtn) {
        isSimulationRunning = !isSimulationRunning;
        if(isSimulationRunning) {
            toggleSimBtn.textContent = 'Stop Simulation';
            toggleSimBtn.style.background = 'var(--error-color)';
            simInterval = setInterval(async () => {
                try {
                    const res = await fetch(`${API_BASE}/telemetry/${currentUavIdForTelemetry}/simulate`, {
                        method: 'POST',
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (res.ok) {
                        const data = await res.json();
                        // Update UI immediately with the new simulated data
                        document.getElementById('liveBattery').textContent = (data.battery_level !== null ? data.battery_level.toFixed(1) : '--') + '%';
                        document.getElementById('liveTemp').textContent = (data.esc_temperature !== null ? data.esc_temperature.toFixed(1) : '--') + '°C';
                        document.getElementById('liveVib').textContent = (data.vibration_level !== null ? data.vibration_level.toFixed(2) : '--');
                        document.getElementById('liveRpm').textContent = (data.rpm_asymmetry !== null ? data.rpm_asymmetry.toFixed(2) : '--') + '%';
                        
                        
                        // Local Simulation Logic for UI Testing with Hysteresis
                        const temp = data.esc_temperature || 0;
                        const vib = data.vibration_level || 0;
                        const bat = data.battery_level || 100;
                        
                        currentParts.forEach(p => {
                            let newStatus = p.status;
                            const name = (p.name || '').toLowerCase();
                            const category = (p.category || '').toLowerCase();
                            
                            // ESC or Motor Temperature Rules (with Hysteresis)
                            if (name.includes('esc') || name.includes('motor')) {
                                if (newStatus === 'Critical') {
                                    if (temp < 75) newStatus = 'Warning';
                                    if (temp < 65) newStatus = 'OK';
                                } else if (newStatus === 'Warning') {
                                    if (temp >= 80) newStatus = 'Critical';
                                    else if (temp < 65) newStatus = 'OK';
                                } else {
                                    if (temp >= 80) newStatus = 'Critical';
                                    else if (temp >= 70) newStatus = 'Warning';
                                }
                            }
                            
                            // Rotor or Hub Vibration Rules (with Hysteresis)
                            if (category.includes('rotor') || name.includes('rotor') || name.includes('hub')) {
                                if (newStatus === 'Critical') {
                                    if (vib < 0.75) newStatus = 'Warning';
                                    if (vib < 0.45) newStatus = 'OK';
                                } else if (newStatus === 'Warning') {
                                    if (vib >= 0.8) newStatus = 'Critical';
                                    else if (vib < 0.45) newStatus = 'OK';
                                } else {
                                    if (vib >= 0.8) newStatus = 'Critical';
                                    else if (vib >= 0.5) newStatus = 'Warning';
                                }
                            }

                            // Battery Rules (with Hysteresis)
                            if (name.includes('batarya') || name.includes('battery')) {
                                if (newStatus === 'Critical') {
                                    if (bat > 20) newStatus = 'Warning';
                                    if (bat > 35) newStatus = 'OK';
                                } else if (newStatus === 'Warning') {
                                    if (bat <= 15) newStatus = 'Critical';
                                    else if (bat > 35) newStatus = 'OK';
                                } else {
                                    if (bat <= 15) newStatus = 'Critical';
                                    else if (bat <= 30) newStatus = 'Warning';
                                }
                            }
                            
                            p.status = newStatus;
                        });
                        
                        // Re-render the parts using the currently active filter
                        const activeFilterBtn = document.querySelector('.filter-btn.active');
                        const currentFilter = activeFilterBtn ? activeFilterBtn.dataset.filter : 'All';
                        renderParts(currentFilter);
                    }
                } catch(e) { console.error(e); }
            }, 1000);
        } else {
            toggleSimBtn.textContent = 'Start Simulation';
            toggleSimBtn.style.background = '';
            if(simInterval) clearInterval(simInterval);
        }
    }
});

// Add UAV Modal Logic
const openAddUavModalBtn = document.getElementById('openAddUavModalBtn');
const closeAddUavModalBtn = document.getElementById('closeAddUavModalBtn');
const addUavModal = document.getElementById('addUavModal');
let html5QrcodeScannerUav = null;

if (openAddUavModalBtn && addUavModal) {
    openAddUavModalBtn.addEventListener('click', () => {
        addUavModal.classList.add('open');
        try {
            html5QrcodeScannerUav = new Html5QrcodeScanner("qr-reader-uav", { fps: 10, qrbox: {width: 250, height: 250} }, false);
            html5QrcodeScannerUav.render((decodedText) => {
                document.getElementById('newUavSerial').value = decodedText;
                html5QrcodeScannerUav.clear();
            });
        } catch(e) { console.log('QR Scanner init failed', e); }
    });
}

if (closeAddUavModalBtn && addUavModal) {
    closeAddUavModalBtn.addEventListener('click', () => {
        addUavModal.classList.remove('open');
        if(html5QrcodeScannerUav) {
            html5QrcodeScannerUav.clear().catch(err => console.log(err));
        }
    });
}

// Close modals when clicking outside their content
window.addEventListener('click', (e) => {
    if (e.target === addUavModal) {
        addUavModal.classList.remove('open');
        if(html5QrcodeScannerUav) {
            html5QrcodeScannerUav.clear().catch(err => console.log(err));
        }
    }
    const partsPanel = document.getElementById('partsPanel');
    if (e.target === partsPanel) {
        partsPanel.classList.remove('open');
        stopTelemetryPolling();
    }
});

const addUavForm = document.getElementById('addUavForm');
if(addUavForm) {
    addUavForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const serial = document.getElementById('newUavSerial').value;
        const model = document.getElementById('newUavModel').value;
        const errEl = document.getElementById('addUavError');
        errEl.textContent = '';
        
        try {
            const res = await fetch(`${API_BASE}/uavs/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    serial_number: serial,
                    model_name: model,
                    total_flight_hours: 0,
                    status: 'Flight Ready'
                })
            });
            
            if (res.ok) {
                addUavModal.classList.remove('open');
                document.getElementById('addUavForm').reset();
                fetchUAVs();
            } else {
                const data = await res.json();
                errEl.textContent = data.detail || 'Failed to create UAV';
            }
        } catch(err) {
            errEl.textContent = 'Network error.';
        }
    });
}

// Event Listeners
const closePanelBtn = document.getElementById('closePanelBtn');
if(closePanelBtn) {
    closePanelBtn.addEventListener('click', () => {
        document.getElementById('partsPanel').classList.remove('open');
        stopTelemetryPolling();
    });
}

document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        renderParts(e.target.dataset.filter);
    });
});

document.addEventListener('DOMContentLoaded', fetchUAVs);










const viewInInventoryBtn = document.getElementById('viewInInventoryBtn');
if (viewInInventoryBtn) {
    viewInInventoryBtn.addEventListener('click', () => {
        const serial = document.getElementById('panelUavSerial').textContent;
        if(serial && serial !== '--') {
            window.location.href = 'inventory.html?uav_id=' + encodeURIComponent(serial);
        }
    });
}
