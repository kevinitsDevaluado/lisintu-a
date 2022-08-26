// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

var staticCacheName = "PWA-CPS-";
var filesToCache = [
    '/offline/',
    '/buscador_offline/',
    '/static/otros/img/logo_pwa.png',
    '/static/otros/img/logo_empresa_1.png',
    '/static/home/lib/tempusdominus/css/tempusdominus-bootstrap-4.min.css',
    '/static/home/lib/lightbox/css/lightbox.min.css',
    '/static/home/css/bootstrap.min.css',
    '/static/home/css/style.css',
    '/static/otros/css/style_cps.css',
    '/static/home/js/main.js',
    '/static/otros/js/mensajes.js',
    '/static/otros/js/idb.js',
    '/static/otros/js/idbop.js',
    '/static/otros/js/jquery.min.js',
    '/getdata/',
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("PWA-CPS-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache

self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('/offline/');
            })
    )
});


// Server full Cache
/*
self.addEventListener("fetch", function(event) {
    event.respondWith(
        fetch(event.request)
        .then(function(result) {
            return caches.open(staticCacheName)
            .then(function(c) {
                c.put(event.request.url, result.clone())
                return result;
            })
        })
        .catch(function(e){
            return caches.match(event.request);
        })
    )
});
*/