import path from 'node:path';
import {existsSync} from 'node:fs';
import fs from 'node:fs/promises';
if(existsSync('.local/browsers'))process.env.PLAYWRIGHT_BROWSERS_PATH ||= path.resolve('.local/browsers');
const {runJourney}=await import('./lib/runner.mjs');
const contract={id:'checkout-handoff',name:'Reach PayPal sandbox checkout using the keyboard',goal:'Pay with PayPal',steps:[{type:'tabTo',role:'button',name:'Continue to PayPal sandbox',limit:18},{type:'press',key:'Enter'},{type:'expectVisible',role:'heading',name:'Pay with PayPal'}]};
const runs=[];
for(const version of ['broken','fixed']){const id='checkout-'+version;const report=await runJourney({url:'http://127.0.0.1:4174/checkout.html?version='+version,contract,outputDir:path.resolve('dist/evidence'),id,assetPrefix:'evidence/',viewport:{width:1920,height:1080},screenshotFormat:'jpeg',tailHoldMs:1500});report.fixture={journey:'checkout',version,publicPath:'checkout.html?version='+version};report.checkout={sandbox:true,stage:'merchant-to-PayPal-login',buyerApprovalTested:false,captureTested:false,description:'This keyboard contract ends at PayPal sign-in. It does not automate buyer approval or claim a completed payment.'};await fs.writeFile('dist/evidence/'+id+'.json',JSON.stringify(report,null,2));runs.push(report);console.log(id,report.outcome,report.keyCount);}
await fs.writeFile('dist/evidence/checkout.json',JSON.stringify({schemaVersion:1,generatedAt:new Date().toISOString(),runs},null,2));
