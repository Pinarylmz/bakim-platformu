const API_BASE = '';

async function fetchUsers() {
    try {
        const response = await fetch(`${API_BASE}/users/`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        if (response.ok) {
            const users = await response.json();
            renderUsers(users);
        } else if (response.status === 403) {
            document.getElementById('usersBody').innerHTML = '<tr><td colspan="5" style="color:var(--error-color);">Access Denied. Admins Only.</td></tr>';
            document.getElementById('pendingBody').innerHTML = '<tr><td colspan="4" style="color:var(--error-color);">Access Denied.</td></tr>';
            return;
        }
        
        const pendingRes = await fetch(`${API_BASE}/users/pending`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        if (pendingRes.ok) {
            const pendingUsers = await pendingRes.json();
            renderPending(pendingUsers);
        }
    } catch (e) {
        console.error("Fetch error", e);
    }
}

function renderPending(users) {
    const tbody = document.getElementById('pendingBody');
    tbody.innerHTML = '';
    
    if (users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4">No pending approvals.</td></tr>';
        return;
    }
    
    users.forEach(user => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${user.full_name || 'N/A'}</td>
            <td>${user.username}</td>
            <td>${new Date(user.created_at).toLocaleDateString()}</td>
            <td>
                <select id="role-${user.id}" style="padding: 5px; background: var(--input-bg); color: white; border: 1px solid var(--border-color); border-radius: 4px; margin-right: 10px;">
                    <option value="Technician">Technician</option>
                    <option value="Engineer">Engineer</option>
                    <option value="Admin">Admin</option>
                </select>
                <button class="btn-primary btn-sm" style="background-color:var(--success-color);" onclick="approveUser(${user.id}, 'Approved')">Approve</button>
                <button class="btn-primary btn-sm" style="background-color:var(--error-color);" onclick="approveUser(${user.id}, 'Rejected')">Reject</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function approveUser(id, status) {
    const role = document.getElementById(`role-${id}`) ? document.getElementById(`role-${id}`).value : 'Technician';
    
    try {
        const response = await fetch(`${API_BASE}/users/${id}/approve`, {
            method: 'PUT',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}` 
            },
            body: JSON.stringify({ role: role, approval_status: status })
        });
        
        if (response.ok) {
            fetchUsers();
        } else {
            alert(`Failed to ${status.toLowerCase()} user.`);
        }
    } catch (e) {
        alert("Network error.");
    }
}

function renderUsers(users) {
    const tbody = document.getElementById('usersBody');
    tbody.innerHTML = '';
    
    if (users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5">No active users.</td></tr>';
        return;
    }

    users.forEach(user => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${user.full_name || 'N/A'}</td>
            <td>${user.username}</td>
            <td><strong>${user.role}</strong></td>
            <td>${new Date(user.created_at).toLocaleDateString()}</td>
            <td>
                <button class="btn-primary btn-sm" style="background-color:var(--error-color);" onclick="deleteUser(${user.id})">Delete</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function deleteUser(id) {
    if(!confirm("Are you sure you want to delete this user?")) return;
    
    try {
        const response = await fetch(`${API_BASE}/users/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        if (response.ok) {
            fetchUsers();
        } else {
            alert("Failed to delete user. Cannot delete yourself.");
        }
    } catch (e) {
        alert("Network error.");
    }
}

// Modal Logic
const modal = document.getElementById('addUserModal');
document.getElementById('openAddUserModalBtn').addEventListener('click', () => {
    modal.classList.add('open');
});
document.getElementById('closeAddUserModalBtn').addEventListener('click', () => {
    modal.classList.remove('open');
});

document.getElementById('addUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const u = document.getElementById('newUsername').value;
    const p = document.getElementById('newPassword').value;
    const r = document.getElementById('newRole').value;
    
    try {
        const response = await fetch(`${API_BASE}/users/`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}` 
            },
            body: JSON.stringify({ username: u, password: p, role: r })
        });
        
        if (response.ok) {
            modal.classList.remove('open');
            document.getElementById('addUserForm').reset();
            fetchUsers();
        } else {
            const data = await response.json();
            document.getElementById('addUserError').textContent = data.detail || 'Error creating user.';
        }
    } catch (e) {
        document.getElementById('addUserError').textContent = 'Network error.';
    }
});

document.addEventListener('DOMContentLoaded', fetchUsers);
