import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { JSDOM } from 'jsdom';
const photos=JSON.parse(readFileSync('src/photos.json','utf8'));
function app(number='invalid'){
 const dom=new JSDOM('<div id="app"></div>',{url:'https://motorkita.example',runScripts:'outside-only'});
 const w=dom.window;w.scrollTo=()=>{};w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};w.HTMLDialogElement.prototype.close=function(){this.open=false;};
 const code=readFileSync('src/main.js','utf8').replace("import photos from './photos.json';",`const photos=${JSON.stringify(photos)};`).replace('import.meta.env.VITE_WHATSAPP_NUMBER',JSON.stringify(number));
 w.eval(code);return {w,d:w.document};
}
test('12 products have four distinct existing local photos and https source links',()=>{
 assert.equal(Object.keys(photos).length,12);
 for(const items of Object.values(photos)){assert.equal(items.length,4);assert.equal(new Set(items.map(x=>x.src)).size,4);for(const p of items){assert.ok(existsSync('public'+p.src));assert.ok(p.source.startsWith('https://'));}}
});
test('catalog, gallery cycling, credit preselection and favorite persistence',()=>{
 const {w,d}=app();assert.equal(d.querySelectorAll('.bike-card').length,12);
 d.querySelector('[data-detail="11"]').click();assert.ok(d.querySelector('dialog').open);assert.equal(d.querySelectorAll('[data-photo]').length,4);
 d.querySelector('.next').click();assert.equal(d.querySelector('#gallery-counter').textContent,'2 / 4');
 d.querySelector('[data-photo="3"]').click();d.querySelector('.next').click();assert.equal(d.querySelector('#gallery-counter').textContent,'1 / 4');
 d.querySelector('#simulate').click();assert.equal(d.querySelector('#bike-select').value,'11');assert.ok(d.querySelector('#monthly').textContent.includes('Rp'));
 d.querySelector('[data-page="catalog"]').click();d.querySelector('[data-save="9"]').click();assert.deepEqual(JSON.parse(w.localStorage.getItem('motorkita-saved')),[9]);
 d.querySelector('[data-page="saved"]').click();assert.equal(d.querySelectorAll('.bike-card').length,1);
 w.close();
});
test('new brand filters and WhatsApp missing-number state',()=>{
 const {w,d}=app();const brand=d.querySelector('#brand');brand.value='Yadea';brand.dispatchEvent(new w.Event('change'));assert.equal(d.querySelectorAll('.bike-card').length,1);
 d.querySelector('[data-detail="12"]').click();d.querySelector('dialog [data-order]').click();assert.ok(d.querySelector('dialog').textContent.includes('belum tersedia'));assert.equal(d.querySelectorAll('a[href^="https://wa.me/"]').length,0);w.close();
});
test('configured WhatsApp encodes selected motorcycle',()=>{
 const {w,d}=app('6281234567890');d.querySelector('[data-detail="9"]').click();const a=d.querySelector('dialog a.whatsapp');const url=new URL(a.href);assert.equal(url.pathname,'/6281234567890');assert.ok(url.searchParams.get('text').includes('TVS Ronin'));w.close();
});
test('hover popup opens with delay, dismisses and keyboard focus works',async()=>{
 const {w,d}=app();const card=d.querySelector('.bike-card');const enter=new w.Event('pointerenter');Object.defineProperty(enter,'pointerType',{value:'mouse'});card.dispatchEvent(enter);await new Promise(r=>setTimeout(r,360));assert.ok(card.classList.contains('peek'));card.dispatchEvent(new w.Event('pointerleave'));assert.ok(!card.classList.contains('peek'));card.querySelector('.photo-open').focus();assert.ok(card.classList.contains('peek'));card.dispatchEvent(new w.KeyboardEvent('keydown',{key:'Escape'}));assert.ok(!card.classList.contains('peek'));w.close();
});
