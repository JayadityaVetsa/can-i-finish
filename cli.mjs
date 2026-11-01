import path from 'node:path';
import fs from 'node:fs/promises';
import {existsSync} from 'node:fs';
if(existsSync('.local/browsers'))process.env.PLAYWRIGHT_BROWSERS_PATH ||= path.resolve('.local/browsers');
const {createServer}=await import('./server.mjs');
const {CONTRACTS}=await import('./lib/contracts.mjs');
const {runJourney}=await import('./lib/runner.mjs');
const args=process.argv.slice(2);
if(args[0]==='demo'){
 const server=await createServer({port:0});const base=`http://127.0.0.1:${server.address().port}`;const outputDir=path.resolve('dist/evidence');await fs.mkdir(outputDir,{recursive:true});const runs=[];
 try{for(const [journey,contract]of Object.entries(CONTRACTS)){for(const version of ['broken','fixed']){const id=`${journey}-${version}`;console.log(`Running ${id}...`);const report=await runJourney({url:`${base}/fixtures/campus.html?journey=${journey}&version=${version}`,contract,outputDir,id,assetPrefix:'evidence/'});report.fixture={journey,version,publicPath:`fixtures/campus.html?journey=${journey}&version=${version}`};await fs.writeFile(path.join(outputDir,`${id}.json`),JSON.stringify(report,null,2));runs.push(report);console.log(`${id}: ${report.outcome}, ${report.keyCount} key events, ${report.steps.length} evidence frames`);}}
  const summary={schemaVersion:1,generatedAt:new Date().toISOString(),provenance:'Executed by the local Playwright runner against controlled fixtures. No outcomes are hardcoded into the viewer.',runs};await fs.writeFile(path.join(outputDir,'demo.json'),JSON.stringify(summary,null,2));
  const correct=runs.every(r=>r.fixture.version==='fixed'?r.outcome==='passed':r.outcome==='blocked');if(!correct)process.exitCode=1;
 }finally{await new Promise(resolve=>server.close(resolve));}
}else if(args[0]==='run'&&args[1]&&args[2]){const contract=JSON.parse(await fs.readFile(args[2],'utf8'));const id='journey-'+Date.now();const report=await runJourney({url:args[1],contract,outputDir:path.resolve('reports',id),id,assetPrefix:`/reports/${id}/`});console.log(JSON.stringify({id,outcome:report.outcome,report:path.resolve('reports',id,`${id}.json`)}));process.exitCode=report.outcome==='passed'?0:1;}
else{console.log('Usage: npm run demo | node cli.mjs run <url> <contract.json>');process.exitCode=2;}
