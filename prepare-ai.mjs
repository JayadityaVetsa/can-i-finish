import fs from 'node:fs/promises';
import {build} from 'esbuild';
await fs.mkdir('dist/vendor',{recursive:true});
await build({entryPoints:['node_modules/@huggingface/transformers/dist/transformers.web.js'],outfile:'dist/vendor/transformers.js',bundle:true,format:'esm',platform:'browser',minify:true});
for(const name of ['ort-wasm-simd-threaded.jsep.mjs','ort-wasm-simd-threaded.jsep.wasm','ort-wasm-simd-threaded.asyncify.mjs','ort-wasm-simd-threaded.asyncify.wasm'])await fs.copyFile('node_modules/onnxruntime-web/dist/'+name,'dist/vendor/'+name);
for(const name of await fs.readdir('node_modules/@huggingface/transformers/dist'))if(name.endsWith('.wasm')||name.startsWith('ort-'))await fs.copyFile('node_modules/@huggingface/transformers/dist/'+name,'dist/vendor/'+name);
console.log('Browser AI runtime copied.');
