import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import {safeAsset} from '../dist/report.js';
const report=JSON.parse(await fs.readFile('dist/evidence/apple-voiceover.json','utf8'));
test('real Apple journey reaches the actual support article',()=>{assert.equal(report.outcome,'passed');assert.equal(new URL(report.url).hostname,'www.apple.com');assert.equal(new URL(report.steps.at(-1).url).hostname,'support.apple.com');assert.match(report.steps.at(-1).note,/Turn on and practice VoiceOver on iPhone.*passed/);assert.ok(report.steps.some(s=>s.focus?.name==='Learn more about VoiceOver'));assert.ok(report.steps.some(s=>s.focus?.name==='iPhone, Set up VoiceOver'));assert.equal(report.findings.length,0);});
test('Apple frames retain valid hashes and full-HD capture metadata',async()=>{assert.deepEqual(report.engine.viewport,{width:1920,height:1080});for(const step of report.steps){assert.equal(safeAsset(step.screenshot),step.screenshot);const bytes=await fs.readFile('dist/'+step.screenshot);assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),step.sha256);}assert.ok((await fs.stat('dist/'+report.artifacts.video)).size>10000);});
