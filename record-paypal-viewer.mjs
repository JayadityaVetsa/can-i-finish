import path from 'node:path';import {existsSync}from'node:fs';
if(existsSync('.local/browsers'))process.env.PLAYWRIGHT_BROWSERS_PATH ||= path.resolve('.local/browsers');
const {runJourney}=await import('./lib/runner.mjs');
const contract={name:'Inspect matched merchant checkout evidence',steps:[{type:'expectVisible',role:'heading',name:'Reach PayPal sandbox checkout using the keyboard'},{type:'tabTo',role:'button',name:'Compare before & after ↗',limit:24},{type:'press',key:'Enter'},{type:'expectVisible',role:'heading',name:'The same contract. A different result.'},...Array.from({length:15},()=>({type:'press',key:'ArrowDown'}))]};
const r=await runJourney({url:'http://127.0.0.1:4174/?journey=checkout&presentation=paypal',contract,outputDir:path.resolve('docs/paypal-film'),id:'film-checkout-viewer',viewport:{width:1920,height:1080},screenshotFormat:'jpeg',keyDelayMs:250,tailHoldMs:2000});console.log('Checkout viewer:',r.outcome,r.keyCount);
