const CACHE_NAME = 'uav-mro-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/dashboard.html',
  '/fleet.html',
  '/inventory.html',
  '/damage_reports.html',
  '/css/style.css',
  '/css/responsive.css',
  '/js/i18n.js',
  '/js/fleet.js',
  '/js/inventory.js',
  '/js/damage_reports.js',
  '/js/sync.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(ASSETS_TO_CACHE))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Network-first strategy for API calls, Cache-first for static assets
self.addEventListener('fetch', (event) => {
  // If API request, try network first, then fail (let app handle offline logic via localStorage)
  if (event.request.url.includes('localhost:8000')) {
    event.respondWith(
      fetch(event.request).catch(() => {
        return new Response(JSON.stringify({ offline: true, error: "Network error" }), {
          headers: { 'Content-Type': 'application/json' }
        });
      })
    );
    return;
  }

  // Static files: Cache first, fallback to network
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request);
    })
  );
});
