import fs from 'node:fs/promises';
await fs.mkdir('.local/pitch-v4/raw',{recursive:true});
function sanitize(value){if(typeof value==='string'&&value.startsWith('https://www.sandbox.paypal.com/')){const url=new URL(value);url.search='';url.hash='';return url.href;}if(Array.isArray(value))return value.map(sanitize);if(value&&typeof value==='object')return Object.fromEntries(Object.entries(value).map(([k,v])=>[k,sanitize(v)]));return value;}
for(const name of ['checkout-broken.json','checkout-fixed.json','checkout.json']){const file='dist/evidence/'+name;const raw=await fs.readFile(file,'utf8');await fs.writeFile('.local/pitch-v4/raw/'+name,raw);await fs.writeFile(file,JSON.stringify(sanitize(JSON.parse(raw)),null,2));}
console.log('Sandbox approval query strings removed from published reports; originals preserved privately.');
