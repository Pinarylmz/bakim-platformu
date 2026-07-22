// Offline Sync Manager
const SYNC_QUEUE_KEY = 'uav_sync_queue';

function getSyncQueue() {
    return JSON.parse(localStorage.getItem(SYNC_QUEUE_KEY) || '[]');
}

function saveToSyncQueue(endpoint, method, payloadData) {
    const queue = getSyncQueue();
    queue.push({
        id: Date.now(),
        endpoint: endpoint,
        method: method,
        payload: payloadData, // Expected to be an object or string
        timestamp: new Date().toISOString()
    });
    localStorage.setItem(SYNC_QUEUE_KEY, JSON.stringify(queue));
    updateOfflineBanner();
}

async function processSyncQueue() {
    if (!navigator.onLine) return;

    const queue = getSyncQueue();
    if (queue.length === 0) return;

    console.log(`Processing ${queue.length} items from sync queue...`);
    const remainingQueue = [];

    for (let item of queue) {
        try {
            // Reconstruct headers
            const headers = { 'Authorization': `Bearer ${localStorage.getItem('token')}` };
            let bodyData = item.payload;
            
            // If it's standard JSON
            if (typeof bodyData === 'object' && !(bodyData instanceof FormData)) {
                headers['Content-Type'] = 'application/json';
                bodyData = JSON.stringify(bodyData);
            }

            const response = await fetch(`http://localhost:8000${item.endpoint}`, {
                method: item.method,
                headers: headers,
                body: bodyData
            });

            if (!response.ok && response.status !== 401) {
                console.error("Failed to sync item", item, response.status);
                remainingQueue.push(item); // Keep in queue if backend rejected it (not auth error)
            } else {
                console.log("Successfully synced item", item.id);
            }
        } catch (e) {
            console.error("Network error during sync, keeping in queue", e);
            remainingQueue.push(item);
        }
    }

    localStorage.setItem(SYNC_QUEUE_KEY, JSON.stringify(remainingQueue));
    updateOfflineBanner();
}

function updateOfflineBanner() {
    const queue = getSyncQueue();
    let banner = document.getElementById('offlineBanner');
    
    if (!navigator.onLine || queue.length > 0) {
        if (!banner) {
            banner = document.createElement('div');
            banner.id = 'offlineBanner';
            banner.style.position = 'fixed';
            banner.style.bottom = '0';
            banner.style.left = '0';
            banner.style.width = '100%';
            banner.style.backgroundColor = 'var(--warning-color)';
            banner.style.color = '#000';
            banner.style.textAlign = 'center';
            banner.style.padding = '10px';
            banner.style.zIndex = '9999';
            banner.style.fontWeight = 'bold';
            document.body.appendChild(banner);
        }
        
        if (!navigator.onLine) {
            banner.innerHTML = `You are offline. Data is saved locally. (${queue.length} pending items)`;
        } else if (queue.length > 0) {
            banner.innerHTML = `Online. Syncing ${queue.length} pending items...`;
        }
    } else {
        if (banner) banner.remove();
    }
}

// Listeners
window.addEventListener('online', () => {
    updateOfflineBanner();
    processSyncQueue();
});
window.addEventListener('offline', updateOfflineBanner);

// Run on load
document.addEventListener('DOMContentLoaded', () => {
    updateOfflineBanner();
    processSyncQueue();
});
