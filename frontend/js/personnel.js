const token = localStorage.getItem('token');
if (!token) {
    window.location.href = 'index.html';
}


const API_BASE = '';

async function fetchTrackingData() {
    const role = localStorage.getItem('role');
    const tbody = document.getElementById('trackingBody');
    
    if (role !== 'Admin') {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--error-color);">Access Denied</td></tr>';
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/users/tracking`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (res.ok) {
            const users = await res.json();
            tbody.innerHTML = '';
            
            if (users.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--text-secondary);">No tracking data found.</td></tr>';
                return;
            }
            
            users.forEach(u => {
                const tr = document.createElement('tr');
                const date = new Date(u.created_at).toLocaleString();
                const totalMinutes = u.total_time_spent || 0;
                
                let timeDisplay = `${totalMinutes} m`;
                if (totalMinutes >= 60) {
                    const hours = Math.floor(totalMinutes / 60);
                    const mins = totalMinutes % 60;
                    timeDisplay = `${hours}h ${mins}m`;
                }

                let actionCell = '<td></td>';
                if (u.username !== 'admin') {
                    actionCell = `<td><button class="delete-user-btn" data-id="${u.id}" style="background: transparent; color: var(--error-color); border: 1px solid var(--error-color); padding: 4px 8px; border-radius: 4px; cursor: pointer;">Delete</button></td>`;
                }

                tr.innerHTML = `
                    <td><strong>${u.full_name || u.username}</strong> <br> <span style="font-size: 12px; color: var(--text-secondary);">@${u.username}</span></td>
                    <td><span style="font-weight: 600; color: ${u.role === 'Admin' ? 'var(--error-color)' : 'var(--success-color)'};">${u.role || 'Unassigned'}</span></td>
                    <td>${date}</td>
                    <td><span style="background: var(--input-bg); padding: 4px 8px; border-radius: 6px; font-weight: 500;">${timeDisplay}</span></td>
                    ${actionCell}
                `;
                tbody.appendChild(tr);
            });
            
            // Attach event listeners for delete buttons
            document.querySelectorAll('.delete-user-btn').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    const id = e.target.getAttribute('data-id');
                    if (confirm("Bu kullanıcıyı silmek istediğinize emin misiniz?")) {
                        try {
                            const delRes = await fetch(`${API_BASE}/users/${id}`, {
                                method: 'DELETE',
                                headers: { 'Authorization': `Bearer ${token}` }
                            });
                            if (delRes.ok) {
                                fetchTrackingData();
                            } else {
                                const errData = await delRes.json();
                                alert(errData.detail || "Silme işlemi başarısız oldu.");
                            }
                        } catch (err) {
                            alert("Bağlantı hatası.");
                        }
                    }
                });
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--error-color);">Error fetching data.</td></tr>';
        }
    } catch (err) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--error-color);">Network error.</td></tr>';
    }
}

document.addEventListener('DOMContentLoaded', fetchTrackingData);


