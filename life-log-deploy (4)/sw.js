/* Service Worker：强制网络优先，避免旧图标缓存 */
const SW_VER = 'life-log-sw-v3';
const ASSETS = [
  './',
  './index.html',
  './manifest.webmanifest?v=3',
  './icon-192.png?v=3',
  './icon-512.png?v=3',
  './icon-maskable-512.png?v=3',
  './apple-touch-icon.png?v=3',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(SW_VER)
      .then(c => c.addAll(ASSETS).catch(()=>{}))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== SW_VER).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

/* 图标与 manifest 永远走网络，其余资源网络优先、失败回落缓存 */
self.addEventListener('fetch', e => {
  const req = e.request;
  if(req.method !== 'GET') return;
  const url = new URL(req.url);
  const isIcon = /icon|manifest|apple-touch/i.test(url.pathname + url.search);

  if(isIcon){
    e.respondWith(
      fetch(req, {cache:'reload'}).catch(() => caches.match(req))
    );
    return;
  }
  e.respondWith(
    fetch(req).then(res => {
      const copy = res.clone();
      caches.open(SW_VER).then(c => c.put(req, copy)).catch(()=>{});
      return res;
    }).catch(() => caches.match(req).then(r => r || caches.match('./index.html')))
  );
});
