import path from 'node:path';import {existsSync} from 'node:fs';
if(existsSync('.local/browsers'))process.env.PLAYWRIGHT_BROWSERS_PATH ||= path.resolve('.local/browsers');
const {runJourney}=await import('./lib/runner.mjs');
for(const [id,url,heading]of [['film-ai-proof','ai-evidence.html','A suggestion to review. A task to rerun.'],['film-payment-proof','payment-evidence.html','A completed payment. Verified with PayPal.']]){
 const steps=[{type:'expectVisible',role:'heading',name:heading},...Array.from({length:22},()=>({type:'press',key:'ArrowDown'})),{type:'press',key:'Tab'},{type:'press',key:'Tab'}];const report=await runJourney({url:'http://127.0.0.1:4174/'+url,contract:{name:'Inspect saved evidence: '+id,steps},outputDir:path.resolve('docs/paypal-film'),id,viewport:{width:1920,height:1080},keyDelayMs:300,screenshotFormat:'jpeg',tailHoldMs:2000});console.log(id,report.outcome);
}
