import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import dns from 'node:dns/promises';
import {fileURLToPath} from 'node:url';
import {CONTRACTS,validateContract} from './lib/contracts.mjs';
import {runJourney} from './lib/runner.mjs';
export async function createServer({port=4174}={}){
 const root=path.resolve('dist'),reportsRoot=path.resolve('reports');let busy=false;
 const json=(res,status,value)=>{res.writeHead(status,{'Content-Type':'application/json','Cache-Control':'no-store'});res.end(JSON.stringify(value));};
 const server=http.createServer(async(req,res)=>{
 try{const base=`http://127.0.0.1:${server.address().port}`,url=new URL(req.url,base);
 if(url.pathname==='/api/status'){json(res,200,{localRunner:true,busy,version:1});return;}
 if(url.pathname==='/api/run'&&req.method==='POST'){
  if(req.headers.origin!==base&&req.headers.origin!==`http://localhost:${server.address().port}`){json(res,403,{error:'Open the local workspace to run a test.'});return;}
  if(!req.headers['content-type']?.startsWith('application/json')){json(res,415,{error:'JSON required.'});return;}
  if(busy){json(res,409,{error:'A run is already in progress.'});return;}
  let body='';for await(const chunk of req){body+=chunk;if(body.length>20000){json(res,413,{error:'Request too large.'});return;}}
  const input=JSON.parse(body);let target;let contract;
  if(input.fixture){if(!CONTRACTS[input.fixture]||!['broken','fixed'].includes(input.version))throw new Error('Unknown fixture.');contract=CONTRACTS[input.fixture];target=`${base}/fixtures/campus.html?journey=${input.fixture}&version=${input.version}`;}
  else{contract=validateContract(input.contract);target=new URL(input.url);if(!['http:','https:'].includes(target.protocol)||target.username||target.password)throw new Error('Use an HTTP(S) URL without credentials.');const addresses=await dns.lookup(target.hostname,{all:true});if(addresses.some(a=>/^(127\.|10\.|192\.168\.|169\.254\.|0\.|172\.(1[6-9]|2\d|3[01])\.|::1$|f[cd]|fe80)/i.test(a.address)))throw new Error('Use a public site URL, or one of the bundled local fixtures.');target=target.href;}
  busy=true;try{const id='run-'+crypto.randomUUID();const report=await runJourney({url:target,contract,outputDir:path.join(reportsRoot,id),id,assetPrefix:`/reports/${id}/`});json(res,200,{report});}finally{busy=false;}return;
 }
 if(req.method!=='GET'&&req.method!=='HEAD'){res.writeHead(405).end();return;}
 const reportAsset=url.pathname.startsWith('/reports/');const dir=reportAsset?reportsRoot:root;const relative=decodeURIComponent(reportAsset?url.pathname.slice(9):url.pathname);const filename=path.resolve(dir,'.'+path.sep+relative);if(!filename.startsWith(dir+path.sep)&&filename!==dir){res.writeHead(403).end();return;}
 const file=filename===dir?path.join(dir,'index.html'):filename;const data=await fs.readFile(file);const types={html:'text/html; charset=utf-8',js:'text/javascript',css:'text/css',json:'application/json',png:'image/png',webm:'video/webm',md:'text/markdown'};res.writeHead(200,{'Content-Type':types[file.split('.').pop()]||'application/octet-stream','X-Content-Type-Options':'nosniff'});res.end(req.method==='HEAD'?undefined:data);
 }catch(error){if(!res.headersSent)json(res,error.code==='ENOENT'?404:400,{error:error.code==='ENOENT'?'Not found':error.message});else res.end();}
 });await new Promise(resolve=>server.listen(port,'127.0.0.1',resolve));return server;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){const server=await createServer();console.log(`Can I Finish? Local runner: http://127.0.0.1:${server.address().port}`);}
