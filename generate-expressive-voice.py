"""Render expressive, watermarked narration with the free Chatterbox model on CPU.
Use official ResembleAI/chatterbox weights. No paid API or personal voice recording.
"""
import argparse,gc,json,time,random
from pathlib import Path
import numpy as np
import torch,torchaudio
from accelerate import init_empty_weights
from safetensors.torch import load_file
from chatterbox.tts import ChatterboxTTS,Conditionals
from chatterbox.models.t3 import T3
from chatterbox.models.s3gen import S3Gen
from chatterbox.models.voice_encoder import VoiceEncoder
from chatterbox.models.tokenizers import EnTokenizer
parser=argparse.ArgumentParser();parser.add_argument('--weights',type=Path,required=True);parser.add_argument('--sample-only',action='store_true');parser.add_argument('--only');args=parser.parse_args()
torch.set_num_threads(4);torch.manual_seed(42);random.seed(42);np.random.seed(42)
print('Loading expressive CPU voice with dynamic int8 text decoder...',flush=True)
w=args.weights
ve=VoiceEncoder();ve.load_state_dict(load_file(w/'ve.safetensors'));ve.eval()
with init_empty_weights():t3=T3()
state=load_file(w/'t3_cfg.safetensors');t3.load_state_dict(state,assign=True);del state;gc.collect()
t3.eval();torch.ao.quantization.quantize_dynamic(t3.tfmr,{torch.nn.Linear},dtype=torch.qint8,inplace=True);gc.collect()
print('Text decoder ready.',flush=True)
with init_empty_weights():s3gen=S3Gen()
state=load_file(w/'s3gen.safetensors');s3gen.load_state_dict(state,strict=False,assign=True);del state;gc.collect()
missing=[n for n,p in s3gen.named_parameters() if p.is_meta]
if missing:raise RuntimeError('Unloaded speech parameters: '+str(missing[:4]))
s3gen.eval();tokenizer=EnTokenizer(str(w/'tokenizer.json'));conds=Conditionals.load(w/'conds.pt',map_location='cpu')
model=ChatterboxTTS(t3,s3gen,ve,tokenizer,'cpu',conds=conds)
print('Expressive voice and watermark ready.',flush=True)
def generate(text,out,emotion=.72):
 start=time.time();torch.manual_seed(42)
 wav=model.generate(text,exaggeration=emotion,cfg_weight=.3,temperature=.75)
 samples=wav.squeeze().numpy();active=np.flatnonzero(abs(samples)>.004)
 if len(active):samples=samples[max(0,active[0]-int(model.sr*.13)):min(len(samples),active[-1]+int(model.sr*.22))]
 out.parent.mkdir(parents=True,exist_ok=True);torchaudio.save(str(out),torch.from_numpy(samples).unsqueeze(0),model.sr)
 print('Rendered',out.name,round(len(samples)/model.sr,2),'audio seconds in',round(time.time()-start,1),'seconds',flush=True)
if args.sample_only:
 generate("You're ready to finish. The website isn't. One button. One barrier. And suddenly, you need someone else to step in. We built Can I Finish to change that.",Path('docs/voice-emotion/chatterbox-warm.wav'))
else:
 wanted=set(args.only.split(',')) if args.only else None
 for cut in ['general','paypal']:
  for line in json.loads(Path('docs/pitch-v4/'+cut+'.json').read_text(encoding='utf-8')):
   key=cut+'/'+line['id'];out=Path('docs/narration-pitch-v4')/cut/(line['id']+'.wav')
   if wanted and key not in wanted:continue
   if out.exists() and not wanted:continue
   generate(line['text'],out)
