// Service Worker for JSDOM - Offline-First Architecture
const CACHE_NAME = 'jsdom-v1';
const OFFLINE_CACHE = [
    '/',
    '/dashboard.html',
    '/index.html',
    '/tasks.html',
    '/schedule/baseline.html',
    '/schedule/lookahead.html',
    '/assets/index.json',
    '/tasks_from_plans.json'
];

// Install - Cache core assets
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            console.log('Caching offline assets');
            return cache.addAll(OFFLINE_CACHE);
        })
    );
    self.skipWaiting();
});

// Activate - Clean up old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Fetch - Serve from cache when offline
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            // Return cached version or fetch from network
            return response || fetch(event.request).then(fetchResponse => {
                // Cache blueprints and images for offline use
                if (event.request.url.includes('/blueprints/') || 
                    event.request.url.includes('.jpg') ||
                    event.request.url.includes('.png')) {
                    return caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, fetchResponse.clone());
                        return fetchResponse;
                    });
                }
                return fetchResponse;
            }).catch(() => {
                // Return offline page if network fails
                if (event.request.destination === 'document') {
                    return caches.match('/dashboard.html');
                }
            });
        })
    );
});

// Background Sync - Queue data when offline
self.addEventListener('sync', event => {
    if (event.tag === 'sync-problem-logs') {
        event.waitUntil(syncProblemLogs());
    }
});

async function syncProblemLogs() {
    // Get queued problem logs from IndexedDB
    const problems = await getQueuedProblems();
    
    for (const problem of problems) {
        try {
            await fetch('/api/problems', {
                method: 'POST',
                body: JSON.stringify(problem),
                headers: { 'Content-Type': 'application/json' }
            });
            // Remove from queue after successful sync
            await removeFromQueue(problem.id);
        } catch (err) {
            console.error('Sync failed:', err);
        }
    }
}

// Helper functions for IndexedDB (simplified)
async function getQueuedProblems() {
    // In production, use IndexedDB
    return JSON.parse(localStorage.getItem('problemLogs') || '[]');
}

async function removeFromQueue(id) {
    const problems = JSON.parse(localStorage.getItem('problemLogs') || '[]');
    const filtered = problems.filter(p => p.id !== id);
    localStorage.setItem('problemLogs', JSON.stringify(filtered));
}

