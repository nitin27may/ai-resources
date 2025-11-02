// Service Worker for cache busting
const CACHE_VERSION = 'v1-' + new Date().getTime();
const CACHE_NAME = 'ai-resources-' + CACHE_VERSION;

// Install event - cache essential assets
self.addEventListener('install', (event) => {
  self.skipWaiting();
  console.log('Service Worker installing...');
});

// Activate event - clear old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME && cacheName.startsWith('ai-resources-')) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      return self.clients.claim();
    })
  );
});

// Fetch event - network first strategy for HTML, cache for assets
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  
  // Network first for HTML pages and blog posts
  if (event.request.headers.get('accept').includes('text/html') || 
      url.pathname.includes('/blog/')) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // Clone the response
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
          return response;
        })
        .catch(() => {
          return caches.match(event.request);
        })
    );
  } 
  // Cache first for static assets
  else if (url.pathname.match(/\.(js|css|png|jpg|jpeg|gif|svg|woff|woff2)$/)) {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          // Return cached version but fetch update in background
          fetch(event.request).then((response) => {
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, response);
            });
          });
          return cachedResponse;
        }
        return fetch(event.request).then((response) => {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
          return response;
        });
      })
    );
  } 
  // Network only for everything else
  else {
    event.respondWith(fetch(event.request));
  }
});
