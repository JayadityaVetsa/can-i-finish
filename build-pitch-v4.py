"""Edit the rewritten pitches from actual recordings and speech-aligned captions."""
from pathlib import Path
import json,subprocess,textwrap,time,shutil,sys,hashlib
import numpy as np
root=Path(__file__).resolve().parent;build=root/'.local/pitch-v4';media=root/'dist/media';media.mkdir(exist_ok=True)
film=root/'docs/film-pitch-v4';manifest={x['id']:x for x in json.loads((film/'manifest.json').read_text())}
def run(args):subprocess.run(args,cwd=root,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def duration(p):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)],cwd=root,text=True).strip())
font=build/'brand-bold.ttf'
if not font.exists():
 for candidate in [Path('C:/Windows/Fonts/segoeuib.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')]:
  if candidate.exists():shutil.copyfile(candidate,font);break
font_rel=font.relative_to(root).as_posix()
def card(name,title,small,seconds=3):
 out=build/(name+'.mp4')
 if out.exists():return out
 (build/(name+'.txt')).write_text(title,encoding='utf-8');(build/(name+'-small.txt')).write_text(small,encoding='utf-8')
 filt=f"drawbox=x=110:y=270:w=5:h=310:color=0x142a22:t=fill,drawtext=fontfile={font_rel}:textfile=.local/pitch-v4/{name}-small.txt:fontsize=22:fontcolor=0x4c633f:x=145:y=190,drawtext=fontfile={font_rel}:textfile=.local/pitch-v4/{name}.txt:fontsize=92:line_spacing=14:fontcolor=0x142a22:x=145:y=315,drawtext=fontfile={font_rel}:text='Can I Finish?':fontsize=28:fontcolor=0x142a22:x=145:y=850,fade=t=in:st=0:d=0.12"
 run(['ffmpeg','-y','-loglevel','error','-f','lavfi','-i',f'color=c=0xd2f58b:s=1920x1080:r=30:d={seconds}','-vf',filt,'-c:v','libx264','-threads','2','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',str(out)]);return out
intro=card('intro-general',"YOU’RE READY.\nTHE WEBSITE ISN’T.",'THE LAST STEP SHOULD BELONG TO EVERYONE',3)
payintro=card('intro-paypal','READY TO BUY.\nABLE TO FINISH.','MAKE THE LAST STEP REACHABLE',3)
outro=card('outro','LET PEOPLE\nFINISH.','FIND THE BARRIER. PROVE THE REPAIR.',5)
def clip(p,start=0,end=None):
 d=duration(p);start=min(max(0,start),max(0,d-.15));return(p,start,min(d,end if end is not None else d))
def shot(name,start=0,seconds=None):
 m=manifest[name];a=m['start']+start;b=min(m['end'],a+seconds) if seconds else m['end'];return clip(film/(name+'.webm'),a,b)
def native(name,start=0,end=None):return clip(root/'dist/evidence'/name,start,end)
apple=root/'dist/evidence/apple-voiceover.webm';cancel=root/'docs/paypal-film/film-cancellation.webm'
general=[
 [clip(intro),native('govuk-bus-pass.webm',22,24),clip(apple,max(0,duration(apple)-5),max(0,duration(apple)-1.8)),native('checkout-broken.webm',.2,8),shot('home',0,3)],
 [shot('home'),shot('gov-viewer'),shot('comparison'),shot('export')],
 [native('govuk-bus-pass.webm',6,25),shot('gov-viewer')],
 [clip(apple,4,9),clip(apple,22,28),clip(apple,30,37.5)],
 [native('checkout-broken.webm',.5,8),shot('ai'),native('checkout-fixed.webm',.3),shot('comparison')],
 [shot('export'),shot('comparison'),shot('ai'),shot('gov-viewer',1,4)],
 [shot('close'),shot('home',0,4),clip(outro)]
]
paypal=[
 [clip(payintro),shot('store'),native('checkout-broken.webm',.4,8),shot('comparison')],
 [shot('store'),shot('payment'),native('checkout-fixed.webm',.3)],
 [native('checkout-broken.webm',.3),shot('comparison'),shot('ai'),shot('store',0,4)],
 [shot('ai'),native('checkout-fixed.webm',.3),shot('comparison'),shot('export',0,4)],
 [native('checkout-fixed.webm',3),shot('payment'),shot('store'),shot('payment',2)],
 [clip(cancel,.5),shot('store'),shot('comparison',1,3)],
 [shot('comparison'),shot('export'),shot('close',1),clip(outro)]
]
def stamp(t):
 cs=round(t*100);return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
# Keep original recordings intact; omit blank loading frames from the presentation.
content_cache={}
def content_ranges(source):
 if source in content_cache:return content_cache[source]
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-vf','scale=192:108,fps=10','-f','rawvideo','-pix_fmt','gray','-'])
 frames=np.frombuffer(raw,np.uint8).reshape(-1,108,192);ranges=[];start=None
 for i,frame in enumerate(frames):
  good=frame.std()>12
  if good and start is None:start=i/10
  if not good and start is not None:
   if i/10-start>.2:ranges.append((start,i/10))
   start=None
 if start is not None:ranges.append((start,len(frames)/10))
 content_cache[source]=ranges
 return ranges

def clean_clips(clips):
 cleaned=[]
 for source,a,b in clips:
  for lo,hi in content_ranges(source):
   left=max(a,lo+.08 if lo else 0);right=min(b,hi-.08)
   if right-left>.15:cleaned.append((source,left,right))
 if not cleaned:raise RuntimeError('No visible footage in scene')
 return cleaned

items={cut:json.loads((root/'docs/pitch-v4'/f'{cut}.json').read_text(encoding='utf-8')) for cut in ['general','paypal']}
completed=set();finalized=set();info={}
while len(finalized)<2:
 progress=False
 for cut,scenes in [('general',general),('paypal',paypal)]:
  outdir=build/('video-'+cut);outdir.mkdir(exist_ok=True)
  for index,(line,clips) in enumerate(zip(items[cut],scenes),1):
   key=(cut,index);alignment=build/'aligned'/(cut+'-'+line['id']+'.json')
   if key in completed or not alignment.exists():continue
   original_clips=clips
   aligned=json.loads(alignment.read_text())
   source_audio=root/'docs/narration-pitch-v4'/cut/(line['id']+'.wav')
   if aligned.get('scriptHash')!=hashlib.sha256(line['text'].encode()).hexdigest() or not source_audio.exists() or aligned.get('sourceHash')!=hashlib.sha256(source_audio.read_bytes()).hexdigest():continue
   length=aligned['duration']+.32
   if index==7:length+=2
   def cue_at(prefix):return next(c['start'] for c in aligned['cues'] if c['text'].startswith(prefix))
   groups=None
   if cut=='general' and index==1:
    bounds=[0,cue_at('A bus-pass'),cue_at('A tool'),cue_at('A checkout'),cue_at('We built'),length]
    groups=[[clip(intro)],[native('govuk-bus-pass.webm',22,24)],[clip(apple,max(0,duration(apple)-5),max(0,duration(apple)-1.8))],[native('checkout-broken.webm',0)],[shot('home',0,3)]]
   elif cut=='general' and index==5:
    bounds=[0,cue_at('The focus'),cue_at('The AI'),cue_at('Change'),cue_at('the PayPal'),length]
    groups=[[native('checkout-broken.webm')],[shot('comparison',0,2.5)],[shot('ai')],[native('checkout-fixed.webm')],[shot('comparison',1.5)]]
   elif cut=='paypal' and index==3:
    bounds=[0,cue_at('Can I Finish'),cue_at('The report'),length]
    groups=[[native('checkout-broken.webm')],[shot('comparison')],[shot('ai')]]
   elif cut=='paypal' and index==4:
    bounds=[0,cue_at('Then the same'),cue_at('Same task'),length]
    groups=[[shot('ai')],[native('checkout-fixed.webm')],[shot('comparison')]]
   elif cut=='paypal' and index==5:
    bounds=[0,cue_at('Here is'),cue_at('the receipt.'),length]
    groups=[[native('checkout-fixed.webm')],[shot('payment')],[shot('payment',2)]]
   target_durations=[]
   if groups:
    clips=[]
    for group,left,right in zip(groups,bounds,bounds[1:]):
     clean=clean_clips(group);span=sum(b-a for _,a,b in clean)
     for source,a,b in clean:clips.append((source,a,b));target_durations.append((right-left)*(b-a)/span)
   else:clips=clean_clips(clips)
   total=sum(b-a for _,a,b in clips);rate=max(1,total/length)
   input_speeds=[max(1,(b-a)/target) for (_,a,b),target in zip(clips,target_durations)] if target_durations else []
   if input_speeds:rate=max(input_speeds)
   ass=outdir/f'part-{index}.ass'
   cues=[]
   for cue in aligned['cues']:
    caption='\\N'.join(textwrap.wrap(cue['text'],90))
    cues.append(f"Dialogue: 0,{stamp(cue['start'])},{stamp(cue['end'])},Caption,,0,0,0,,{caption}")
   label=line['title']+(' · SEQUENCE CONDENSED' if rate>1.03 or clips!=original_clips else '')
   ass.write_text('''[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Arial,31,&H00F5FAF4,&H00FFFFFF,&H00222A14,&H00222A14,0,0,0,0,100,100,0,0,1,0,0,2,120,120,20,1
Style: Header,Arial,17,&H008BF5D2,&H00FFFFFF,&H00222A14,&H00222A14,1,0,0,0,100,100,1,0,1,0,0,7,120,120,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''+f'Dialogue: 0,0:00:00.00,0:10:00.00,Header,,0,0,0,,{{\\pos(120,966)}}{label}\n'+'\n'.join(cues),encoding='utf-8')
   output=outdir/f'part-{index}.mp4';audio=build/'audio'/cut/(line['id']+'.wav')
   args=['ffmpeg','-y','-loglevel','error']
   for file,a,b in clips:args+=['-ss',str(a),'-t',str(b-a),'-i',str(file)]
   args+=['-i',str(audio)];filters=[]
   for j,(source,_,_) in enumerate(clips):
    crop='crop=1408:792:256:0,' if source.name in ['store.webm','checkout-broken.webm','checkout-fixed.webm','ai.webm','payment.webm'] else 'crop=1664:936:242:100,' if source.name in ['comparison.webm','gov-viewer.webm','export.webm'] else ''
    timing=f',setpts=PTS/{input_speeds[j]:.7f},tpad=stop_mode=clone:stop_duration={length:.4f},trim=duration={target_durations[j]:.6f},setpts=PTS-STARTPTS' if target_durations else ''
    filters.append(f'[{j}:v]'+crop+f'scale=1920:1080:flags=lanczos,fps=30,setsar=1,setpts=PTS-STARTPTS'+timing+f'[v{j}]')
   filters.append(''.join(f'[v{j}]' for j in range(len(clips)))+f'concat=n={len(clips)}:v=1:a=0,setpts=PTS/{(1 if target_durations else rate):.7f},fps=30,scale=1680:945:flags=lanczos,pad=1920:1080:120:0:color=0x142a22,tpad=stop_mode=clone:stop_duration={max(4,length-total+1):.4f},ass={ass.relative_to(root).as_posix()}[out]')
   filters.append(f'[{len(clips)}:a]apad[a]')
   args+=['-filter_complex',';'.join(filters),'-map','[out]','-map','[a]','-t',str(length),'-c:v','libx264','-threads','2','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-movflags','+faststart',str(output)]
   run(args);completed.add(key);info[key]={'duration':duration(output),'alignment':aligned,'sourceSpeed':rate,'loadingFramesRemoved':clips!=original_clips,'clips':[{'file':str(f.relative_to(root)),'start':a,'end':b,**({'targetDuration':target_durations[k]} if target_durations else {})} for k,(f,a,b) in enumerate(clips)]};progress=True;print('Edited',cut,index,'duration',round(length,1),flush=True)
  if cut not in finalized and all((cut,i) in completed for i in range(1,8)):
   stem='general-v4' if cut=='general' else 'paypal-v2';listing=outdir/'concat.txt';listing.write_text('\n'.join(f"file 'part-{i}.mp4'" for i in range(1,8)),encoding='utf-8');joined=outdir/'joined.mp4';run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(joined)])
   length=duration(joined);music=build/'original-music.wav';filters=f'[1:a]volume=0.42,afade=t=in:st=0:d=2,afade=t=out:st={max(0,length-3)}:d=3[bed];[0:a][bed]amix=inputs=2:duration=first:normalize=0[a]'
   run(['ffmpeg','-y','-loglevel','error','-i',str(joined),'-i',str(music),'-filter_complex',filters,'-map','0:v','-map','[a]','-vf','fps=30','-c:v','libx264','-threads','2','-preset','veryfast','-crf','17','-fps_mode','cfr','-c:a','aac','-b:a','192k','-t',str(length),'-movflags','+faststart',str(media/(stem+'.mp4'))])
   run(['ffmpeg','-y','-loglevel','error','-ss','25','-i',str(media/(stem+'.mp4')),'-frames:v','1','-q:v','2',str(media/(stem+'-poster.jpg'))])
   def st(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
   allcues=[];timeline=[];cursor=0
   for i,line in enumerate(items[cut],1):
    row=info[(cut,i)];timeline.append({'part':i,'start':cursor,'duration':row['duration'],'title':line['title'],'narration':line['text'],'sourceSpeed':row['sourceSpeed'],'loadingFramesRemoved':row['loadingFramesRemoved'],'clips':row['clips'],'wordAgreement':row['alignment']['wordAgreement']})
    for cue in row['alignment']['cues']:allcues.append((cursor+cue['start'],cursor+cue['end'],cue['text']))
    cursor+=row['duration']
   vtt='WEBVTT\n\n'+'\n\n'.join(f'{i}\n{st(a)} --> {st(b)}\n{text}' for i,(a,b,text) in enumerate(allcues,1))
   (media/(stem+'.vtt')).write_text(vtt,encoding='utf-8');(media/(stem+'.srt')).write_text('\n\n'.join(f'{i}\n{st(a).replace(".",",")} --> {st(b).replace(".",",")}\n{text}' for i,(a,b,text) in enumerate(allcues,1)),encoding='utf-8');(media/(stem+'-transcript.txt')).write_text('\n\n'.join(x['text'] for x in items[cut]),encoding='utf-8')
   (root/'docs/pitch-v4'/('timeline-'+cut+'.json')).write_text(json.dumps({'duration':length,'resolution':'1920x1080','fps':30,'narration':'Chatterbox, expressive setting 0.72; conversational pacing normalized to 150 words/minute','music':'Original procedurally composed instrumental bed','parts':timeline},indent=2),encoding='utf-8')
   finalized.add(cut);progress=True;print('FINISHED',stem,round(length,2),'seconds',flush=True)
 if not progress:time.sleep(5)

subprocess.run([sys.executable,str(root/'make-pitch-thumbnails.py')],check=True)
