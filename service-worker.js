const CACHE_NAME = 'vicfile-cache-v3'; // Augmentez la version à chaque modification
const urlsToCache = [
    '/',
    '/static/css/styles.css',
    '/static/pages/convert/convert.html',
    '/static/pages/convert/browser.html',
    '/static/pages/metadata/metadata.html',
    '/static/pages/preview/preview.html',
    '/static/pages/iframe/iframe.html',
    '/static/main-pafe.html'

];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(urlsToCache);
        })
    );
});

self.addEventListener('activate', (event) => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) =>
            Promise.all(
                cacheNames.map((cacheName) => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        return caches.delete(cacheName);
                    }
                })
            )
        )
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
