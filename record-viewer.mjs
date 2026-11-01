import path from 'node:path';
import fs from 'node:fs/promises';
import {existsSync} from 'node:fs';
if(existsSync('.local/browsers'))process.env.PLAYWRIGHT_BROWSERS_PATH ||= path.resolve('.local/browsers');
const {runJourney}=await import('./lib/runner.mjs');
const dir=path.resolve('docs/viewer-recordings');
const contracts=[
 {id:'viewer-contract',name:'Inspect the real Apple task contract',steps:[{type:'tabTo',role:'button',name:'View contract { }',limit:20},{type:'press',key:'Enter'},{type:'expectVisible',role:'heading',name:'The task contract'},{type:'press',key:'Escape'},{type:'expectVisible',role:'heading',name:'The finish line is reachable.'}]},
 {id:'viewer-compare',name:'Compare the controlled registration fix',steps:[{type:'tabTo',role:'button',name:'See a controlled fix comparison ↗',limit:20},{type:'press',key:'Enter'},{type:'expectVisible',role:'heading',name:'The same contract. A different result.'}]},
 {id:'viewer-dialog',name:'Inspect the dialog task evidence',steps:[{type:'tabTo',role:'button',name:'02 Get past a dialog Escape, exit, continue 2',limit:12},{type:'press',key:'Enter'},{type:'expectVisible',role:'heading',name:'Dismiss updates and continue registration'}]},
 {id:'viewer-export',name:'Reach the regression test download with the keyboard',steps:[{type:'press',key:'Shift+Tab'},{type:'press',key:'Shift+Tab'},{type:'press',key:'Shift+Tab'},{type:'press',key:'Enter'}]}
];
for(const c of contracts){if(process.argv[2]&&process.argv[2]!==c.id)continue;const r=await runJourney({url:'http://127.0.0.1:4174/',contract:c,outputDir:dir,id:c.id,viewport:{width:1920,height:1080},keyDelayMs:150,screenshotFormat:'jpeg',tailHoldMs:4000});console.log(c.id,r.outcome,r.keyCount);}
