// auth.js - Enforces RBAC on the frontend and handles Profile Dropdown

localStorage.removeItem('lang'); // Clean up unused language preference

function enforceRBAC() {
    const role = localStorage.getItem('role');
    const isIndexPage = window.location.pathname.includes('index.html') || window.location.pathname === '/';

    if (!role) {
        if (!isIndexPage) {
            window.location.href = 'index.html';
        }
        return;
    } else if (isIndexPage) {
        window.location.href = 'dashboard.html';
        return;
    }

    // Bind robust logout
    const logoutBtn = document.getElementById('logoutBtn');
    if(logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            try {
                localStorage.removeItem('token');
                localStorage.removeItem('role');
                localStorage.removeItem('lang');
                localStorage.clear();
                sessionStorage.clear();
                window.location.href = 'index.html';
            } catch(err) {
                console.error("Logout failed", err);
                window.location.href = 'index.html';
            }
        });
    }

console.log("Logged in as role:", role);

    // Hide User Management link for non-admins
    if (role !== 'Admin') {
        const usersLink = document.getElementById('navUsers');
        if (usersLink) usersLink.style.display = 'none';
        
        const adminTools = document.querySelectorAll('.admin-only');
        adminTools.forEach(b => b.style.display = 'none');
    } else {
        const adminTools = document.querySelectorAll('.admin-only');
        adminTools.forEach(b => b.style.display = 'block');
    }

    // Technician shouldn't see 'Approve' buttons
    if (role === 'Technician') {
        const approveBtns = document.querySelectorAll('.approve-wo-btn');
        approveBtns.forEach(b => b.style.display = 'none');
        
        const auditLink = document.getElementById('navAudit');
        if (auditLink) auditLink.style.display = 'none';
        
        const adminTools = document.querySelectorAll('.admin-only');
        adminTools.forEach(b => b.style.display = 'none');
    }
    
    if (role === 'Engineer') {
        const auditLink = document.getElementById('navAudit');
        if (auditLink) auditLink.style.display = 'none';
    }

    injectSidebarProfile();
}

function injectSidebarProfile() {
    if(window.location.pathname.includes('index.html') || window.location.pathname === '/') return;

    const API_BASE = '';
    
    fetch(`${API_BASE}/users/me`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    .then(res => res.json())
    .then(user => {
        if(!user.username) return;
        
        // Find sidebar list
        const navLinks = document.querySelector('.nav-links');
        if (!navLinks) return;

        // Insert Profile Box before Logout
        const profileHtml = `
            <li class="sidebar-profile" style="margin-top: 40px; border-top: 1px solid var(--border-color); padding-top: 15px;">
                <a href="profile.html" id="openProfileSidebarBtn" style="display:flex; flex-direction:column; align-items:flex-start; line-height: 1.4;">
                    <span style="font-weight: 800; color: white;">${user.full_name || user.username}</span>
                    <span style="font-size: 12px; color: var(--primary-color);">${user.role}</span>
                </a>
            </li>
        `;
        
        // Find logout button li
        const logoutLi = document.getElementById('logoutBtn').parentElement;
        logoutLi.insertAdjacentHTML('beforebegin', profileHtml);
        
    })
    .catch(err => console.error(err));
}

document.addEventListener('DOMContentLoaded', enforceRBAC);
