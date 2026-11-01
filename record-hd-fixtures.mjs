import path from 'node:path';import {existsSync} from 'node:fs';
if(existsSync('.local/browsers'))process.env.PLAYWRIGHT_BROWSERS_PATH ||= path.resolve('.local/browsers');
const {runJourney}=await import('./lib/runner.mjs');const {CONTRACTS}=await import('./lib/contracts.mjs');
for(const [journey,contract] of Object.entries(CONTRACTS)){for(const version of ['broken','fixed']){const r=await runJourney({url:`http://127.0.0.1:4174/fixtures/campus.html?journey=${journey}&version=${version}`,contract,outputDir:path.resolve('docs/film-fixtures'),id:`${journey}-${version}`,viewport:{width:1920,height:1080},screenshotFormat:'jpeg',keyDelayMs:150,tailHoldMs:1000});console.log(r.id,r.outcome,r.keyCount);}}
