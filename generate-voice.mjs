import {KokoroTTS} from 'kokoro-js';
import fs from 'node:fs/promises';
const tts=await KokoroTTS.from_pretrained('onnx-community/Kokoro-82M-v1.0-ONNX',{dtype:'q8',device:'cpu'});
await fs.mkdir('docs/voice-review',{recursive:true});
const sample='You find the course you need. Registration is open. But the last button never receives keyboard focus. You should not have to ask someone else to finish.';
for(const voice of (process.argv.some(a=>a.startsWith('--only='))?[]:['af_heart','af_bella'])){const audio=await tts.generate(sample,{voice,speed:1});await audio.save('docs/voice-review/'+voice+'.wav');console.log('Voice sample saved:',voice);}
if(process.argv.includes('--samples'))process.exit(0);
const folder=process.argv.includes('--paypal')?'narration-paypal':'narration-v2';
const lines=JSON.parse(await fs.readFile('docs/'+folder+'.json','utf8'));
await fs.mkdir('docs/'+folder,{recursive:true});
const only=process.argv.find(a=>a.startsWith('--only='))?.slice(7).split(',');
for(const line of lines){if(only&&!only.includes(line.id))continue;const audio=await tts.generate(line.text,{voice:'af_heart',speed:1});await audio.save('docs/'+folder+'/'+line.id+'.wav');console.log('Narration saved:',line.id);}
