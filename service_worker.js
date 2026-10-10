// Lets Tobin's Spirit Guide work without an internet connection.
//
// The browser runs this file in the background. It saves a copy of every file
// the page needs, then uses this approach whenever the page asks for a file:
//
//     Online:  get the newest version from the internet and update the saved copy.
//     Offline: use the saved copy instead.
//
// Checking the internet first means any update you publish shows up the next
// time the page is opened with a connection, while still working offline.


const CACHE_NAME = 'tobins_spirit_guide';

// Every file the page needs, relative to this file.
const FILES_TO_SAVE = [
    './',
    'index.html',
    'web/style.css',
    'web/logic.js',
    'web/app.js',
    'web/manifest.json',
    'web/icons/icon_192.png',
    'web/icons/icon_512.png',
    'web/icons/apple_touch_icon.png',
    'functions/ghost_data.json',
];


// When first installed, save a copy of every file.
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(FILES_TO_SAVE))
    );
    // Start looking after the page right away instead of waiting for a reload.
    self.skipWaiting();
});


self.addEventListener('activate', (event) => {
    event.waitUntil(self.clients.claim());
});


// Whenever the page asks for a file, try the internet first, then the saved copy.
self.addEventListener('fetch', (event) => {
    if (event.request.method !== 'GET') {
        return;
    }

    event.respondWith(
        fetch(event.request)
            .then((response) => {
                // Only save good copies, never an error page.
                if (response.ok) {
                    const copy = response.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
                }
                return response;
            })
            .catch(() => caches.match(event.request))
    );
});
