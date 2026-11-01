import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {validateContract} from './contracts.mjs';
const require=createRequire(import.meta.url);
export async function runJourney({url,contract,outputDir,id,assetPrefix='',headed=false,viewport={width:1280,height:900},keyDelayMs=90,screenshotFormat='png',tailHoldMs=1000}){
 validateContract(contract);await fs.mkdir(outputDir,{recursive:true});
 const browser=await chromium.launch({headless:!headed});const context=await browser.newContext({viewport,reducedMotion:'reduce',recordVideo:{dir:outputDir,size:viewport}});
 const page=await context.newPage();page.setDefaultTimeout(3500);const started=Date.now();
 const report={schemaVersion:1,id,createdAt:new Date().toISOString(),task:contract.name,contract,url,outcome:'blocked',engine:{name:'Playwright keyboard journey runner',playwright:require('playwright/package.json').version,browser:browser.version(),platform:process.platform,viewport},steps:[],findings:[],limits:['One Chromium viewport and keyboard sequence; no WCAG certification.','A focus cycle alone is not proof of a keyboard trap.','Names in focus observations are approximate; target matching uses Playwright accessible roles/names.'],artifacts:{}};
 async function stableRead(fn){for(let attempt=0;attempt<4;attempt++){try{return await fn();}catch(error){if(attempt===3||!/Execution context was destroyed|Cannot find context|navigation/i.test(error.message))throw error;await page.waitForLoadState('domcontentloaded',{timeout:15000});await page.waitForTimeout(150);}}}
 async function observe(key,phase,note=''){
  const focus=await stableRead(()=>page.evaluate(()=>{let e=document.activeElement;const chain=[];while(e?.shadowRoot?.activeElement){chain.push(e.tagName.toLowerCase());e=e.shadowRoot.activeElement;}if(!e)return null;const s=getComputedStyle(e),r=e.getBoundingClientRect();const labelled=e.getAttribute('aria-labelledby')?.split(/\s+/).map(id=>document.getElementById(id)?.textContent||'').join(' ');const label=e.id?[...document.querySelectorAll('label')].find(l=>l.htmlFor===e.id)?.textContent:'';return {tag:e.tagName.toLowerCase(),id:e.id||null,role:e.getAttribute('role')||null,name:(e.getAttribute('aria-label')||labelled||label||e.textContent||e.getAttribute('placeholder')||'').trim().replace(/\s+/g,' ').slice(0,180),tabIndex:e.tabIndex,focusVisible:e.matches(':focus-visible'),outline:`${s.outlineWidth} ${s.outlineStyle} ${s.outlineColor}`,rect:{x:r.x,y:r.y,width:r.width,height:r.height},shadowHosts:chain,dialogOpen:!!document.querySelector('[role=dialog]:not([hidden])')&&[...document.querySelectorAll('[role=dialog]')].some(d=>d.getBoundingClientRect().width>0)};}));
  const filename=`${id}-${String(report.steps.length).padStart(3,'0')}.${screenshotFormat==='jpeg'?'jpg':'png'}`;const file=path.join(outputDir,filename);await stableRead(()=>page.screenshot({path:file,type:screenshotFormat,...(screenshotFormat==='jpeg'?{quality:88}:{}),timeout:15000}));const bytes=await fs.readFile(file);report.steps.push({index:report.steps.length,key,phase,note,elapsedMs:Date.now()-started,url:page.url(),focus,screenshot:assetPrefix+filename,sha256:crypto.createHash('sha256').update(bytes).digest('hex')});
 }
 async function press(key,phase,note){await page.keyboard.press(key);await page.waitForTimeout(keyDelayMs);await page.waitForLoadState('domcontentloaded',{timeout:10000});await observe(key,phase,note);}
 async function targetDetails(target){if(!await target.count())return null;return target.first().evaluate(e=>({tag:e.tagName.toLowerCase(),id:e.id||null,role:e.getAttribute('role'),tabIndex:e.tabIndex,html:e.outerHTML.slice(0,1600)}));}
 try{
  const response=await page.goto(url,{waitUntil:'domcontentloaded',timeout:30000});if(response&&response.status()>=400)throw new Error(`Page returned HTTP ${response.status()}`);await page.waitForLoadState('load',{timeout:8000}).catch(()=>{});await observe('Start','navigation','Fresh browser context. No mouse clicks or locator.focus().');
  let failed=false;
  for(let stepIndex=0;stepIndex<contract.steps.length;stepIndex++){
   const step=contract.steps[stepIndex];const phase=`${stepIndex+1}. ${step.type}`;
   if(step.type==='press'){await press(step.key,phase);continue;}
   const target=page.getByRole(step.role,{name:step.name,exact:true});
   if(step.type==='tabTo'){
    let reached=false;const seen=new Map();
    for(let n=0;n<step.limit;n++){
     if(await target.count()===1&&await target.evaluate(e=>e===document.activeElement)){reached=true;break;}
     await press('Tab',phase,`Find ${step.role} “${step.name}” using sequential keyboard navigation.`);const f=report.steps.at(-1).focus;const signature=JSON.stringify([f?.tag,f?.id,f?.name]);seen.set(signature,(seen.get(signature)||0)+1);
    }
    if(!reached&&await target.count()===1)reached=await target.evaluate(e=>e===document.activeElement);
    if(!reached){const details=await targetDetails(target);const repetitions=Math.max(0,...seen.values());report.findings.push({code:'TARGET_NOT_REACHED',title:'The task target was not reached',severity:'blocker',summary:`${step.limit} Tab presses did not focus “${step.name}”. This result applies to this bounded sequence.`,target:details,stepIndex,evidenceStep:report.steps.length-1,observations:[details?.tabIndex===-1?'The target is present with tabIndex -1.':details?'The target exists in the rendered page.':'No matching accessible target was found.',repetitions>1?`The same focus stop occurred ${repetitions} times.`:'No repeated focus stop was observed.'],suggestedFix:details?.tag==='div'?'Use a native button for this action. Keep it in sequential focus order and preserve Enter/Space activation.':'Review the task contract, reachable controls, keyboard shortcuts, and any modal exit path.'});failed=true;break;}
   }else{
    await target.waitFor({state:step.type==='expectVisible'?'visible':'hidden',timeout:10000}).catch(()=>{});
    const visible=await target.count()===1&&await target.isVisible();const passed=step.type==='expectVisible'?visible:!visible;
    await observe('Assert',phase,`${step.type}: ${step.role} “${step.name}” — ${passed?'passed':'failed'}`);
    if(!passed){const escaped=step.type==='expectHidden'&&contract.steps[stepIndex-1]?.key==='Escape';if(escaped){for(let n=0;n<6;n++)await press(n===3?'Shift+Tab':'Tab','Diagnostic probe','Inspect focus after the failed Escape; these keys are not a replacement pass condition.');}
     report.findings.push({code:escaped?'DIALOG_DID_NOT_DISMISS':'ASSERTION_FAILED',title:escaped?'Escape did not dismiss the dialog':'The expected task state was not observed',severity:'blocker',summary:escaped?'The dialog remained visible after Escape. Additional Tab and Shift+Tab probes stayed within its controls. A human should check whether another documented exit exists.':`Expected ${step.role} “${step.name}” to be ${step.type==='expectVisible'?'visible':'hidden'}.`,target:await targetDetails(target),stepIndex,evidenceStep:report.steps.length-1,observations:escaped?['Escape was pressed while focus was inside the dialog.','The dialog remained visible.','This is an observed journey failure, not an automatic WCAG verdict.']:[],suggestedFix:escaped?'Provide a keyboard-operable close button, support Escape where appropriate, and restore focus to the trigger. Keep the modal’s normal focus containment.':'Check the activation handler and the contract’s expected result.'});failed=true;break;}
   }
  }
  if(!failed)report.outcome='passed';await page.waitForTimeout(tailHoldMs);
 }catch(error){report.outcome='error';report.findings.push({code:'RUN_ERROR',title:'The browser run could not finish',severity:'error',summary:error.message,evidenceStep:Math.max(0,report.steps.length-1)});}
 finally{const video=page.video();await context.close();if(video){const videoPath=await video.path();const name=`${id}.webm`;await fs.rename(videoPath,path.join(outputDir,name));report.artifacts.video=assetPrefix+name;}await browser.close();}
 report.durationMs=Date.now()-started;report.keyCount=report.steps.filter(s=>!['Start','Assert'].includes(s.key)).length;
 report.reproduction=['Open '+url,`Use a fresh browser context; viewport ${viewport.width} × ${viewport.height}.`,...report.steps.filter(s=>!['Start','Assert'].includes(s.key)).map(s=>s.key),`Observed result: ${report.outcome}`];
 await fs.writeFile(path.join(outputDir,`${id}.json`),JSON.stringify(report,null,2));return report;
}
