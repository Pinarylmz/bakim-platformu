import os

replacements = {
    'Flight Ready': 'Flight Ready',
    'Pending Review': 'Pending Review',
    'Maintenance': 'Maintenance',
    '"OK"': '"OK"',
    "'OK'": "'OK'",
    '"Warning"': '"Warning"',
    "'Warning'": "'Warning'",
    '"Critical"': '"Critical"',
    "'Critical'": "'Critical'",
    '"Open"': '"Open"',
    "'Open'": "'Open'",
    '"Closed"': '"Closed"',
    "'Closed'": "'Closed'", # ensure it remains closed
    '"Pending"': '"Pending"',
    "'Pending'": "'Pending'",
    '"Approved"': '"Approved"',
    "'Approved'": "'Approved'",
    '"Rejected"': '"Rejected"',
    "'Rejected'": "'Rejected'",
    
    # frontend/js/dashboard.js
    'No UAVs found.': 'No UAVs found.',
    'Error loading dashboard data.': 'Error loading dashboard data.',
    'No parts match this filter.': 'No parts match this filter.',
    'Loading telemetry...': 'Loading telemetry...',
    'Telemetry error': 'Telemetry error',
    'Start Simulation': 'Start Simulation',
    'Stop Simulation': 'Stop Simulation',
    'Network error loading telemetry.': 'Network error loading telemetry.',
    
    # frontend/js/inventory.js
    'No parts found in inventory.': 'No parts found in inventory.',
    'Error fetching inventory.': 'Error fetching inventory.',
    'Part added successfully!': 'Part added successfully!',
    'Error adding part': 'Error adding part',
    'İHA\'lar yüklenemedi': 'Failed to load UAVs',
    'Failed to load Categories': 'Failed to load Categories',
    
    # frontend/js/damage_reports.js
    'No damage reports found.': 'No damage reports found.',
    'View Image': 'View Image',
    'No Image': 'No Image',
    'Resolved': 'Resolved',
    'Select UAV...': 'Select UAV...',
    'Select UAV first to load parts...': 'Select UAV first to load parts...',
    'Scanned UAV not found in the system.': 'Scanned UAV not found in the system.',
    'Loading installed parts...': 'Loading installed parts...',
    'No parts installed on this UAV': 'No parts installed on this UAV',
    'Failed to load parts.': 'Failed to load parts.',
    'Network error loading parts': 'Network error loading parts',
    'Please select a UAV and a damaged part.': 'Please select a UAV and a damaged part.',
    'Error saving report.': 'Error saving report.',
    'Failed to fetch reports': 'Failed to fetch reports',
    'İHA\'lar alınamadı': 'Failed to fetch UAVs',
    
    # frontend/js/personnel.js
    'No tracking data available.': 'No tracking data available.',
    'Active': 'Active',
    'Deleted': 'Deleted',
    
    # frontend/js/profile.js
    'Error loading profile': 'Error loading profile',
    'Network error': 'Network error',
    'No recent activities found.': 'No recent activities found.',
    'Error loading activities.': 'Error loading activities.',
    'Network error while loading activities.': 'Network error while loading activities.',
    'Profile updated successfully!': 'Profile updated successfully!',
    'Error updating profile.': 'Error updating profile.',
    'Password updated successfully!': 'Password updated successfully!',
    'Error updating password (Check current password)': 'Error updating password (Check current password)',
    'No pending approvals at the moment.': 'No pending approvals at the moment.',
    'Error fetching pending users.': 'Error fetching pending users.',
    'Engineer': 'Engineer',
    'Technician': 'Technician',
    'Approve': 'Approve',
    'Reject': 'Reject',
    
    # backend routes
    'Username already registered': 'Username already registered',
    'Incorrect username or password': 'Incorrect username or password',
    'Inactive user': 'Inactive user',
    'Your account is pending Admin approval.': 'Your account is pending Admin approval.',
    'Invalid token': 'Invalid token',
    'User not found or inactive': 'User not found or inactive',
    'Not enough permissions': 'Not enough permissions',
    'UAV not found or in maintenance': 'UAV not found or in maintenance',
    'UAV not found': 'UAV not found',
    'Work Order not found': 'Work Order not found',
    'Work Order already closed': 'Work Order already closed',
    'Part not found': 'Part not found',
    'Part uninstalled successfully.': 'Part uninstalled successfully.',
    'A UAV with this Serial Number/QR already exists.': 'A UAV with this Serial Number/QR already exists.',
    'İHA Flight Ready değil. Lütfen önce bekleyen iş emirlerini kapatın.': 'UAV is not Flight Ready. Clear pending work orders first.',
    'Telemetry processed. Alerts generated if thresholds exceeded.': 'Telemetry processed. Alerts generated if thresholds exceeded.',
    'User not found': 'User not found',
    'User {approval.approval_status} successfully': 'User {approval.approval_status} successfully',
    'Cannot delete yourself': 'Cannot delete yourself',
    'User deleted successfully': 'User deleted successfully',
    'Incorrect current password': 'Incorrect current password',
    'Password updated successfully': 'Password updated successfully',
}

for root, dirs, files in os.walk('.'):
    if 'venv' in root or '.git' in root or '.gemini' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith('.py') or file.endswith('.js') or file.endswith('.html'):
            filepath = os.path.join(root, file)
            # avoid translating i18n.js since we will delete it
            if file == 'i18n.js':
                continue
                
            content = None
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                continue
            
            new_content = content
            for old, new in replacements.items():
                new_content = new_content.replace(old, new)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Reverted translation in {filepath}")
