import path from 'node:path';import {existsSync}from'node:fs';
if(existsSync('.local/browsers'))process.env.PLAYWRIGHT_BROWSERS_PATH ||= path.resolve('.local/browsers');
const {runJourney}=await import('./lib/runner.mjs');
const contract={name:'Cancel sandbox sign-in and return to the merchant',steps:[{type:'tabTo',role:'button',name:'Continue to PayPal sandbox',limit:18},{type:'press',key:'Enter'},{type:'expectVisible',role:'link',name:'Cancel and return to Test Store'},{type:'tabTo',role:'link',name:'Cancel and return to Test Store',limit:24},{type:'press',key:'Enter'},{type:'expectVisible',role:'heading',name:'Sandbox checkout cancelled'}]};
const r=await runJourney({url:'http://127.0.0.1:4174/checkout.html?version=fixed',contract,outputDir:path.resolve('docs/paypal-film'),id:'film-cancellation',viewport:{width:1920,height:1080},screenshotFormat:'jpeg',keyDelayMs:180,tailHoldMs:2000});console.log('Cancellation task:',r.outcome,r.keyCount);
