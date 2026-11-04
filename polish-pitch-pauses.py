"""Remove measured dead air from the final pitches; keep captions and video in sync."""
from pathlib import Path
import json,subprocess,math,re,wave,shutil
import numpy as np
root=Path(__file__).resolve().parent;build=root/'.local/pitch-v4';media=root/'dist/media'
def duration(p):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)],text=True).strip())
def stamp(t,separator='.'):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}{separator}{ms%1000:03}'
for cut,stem in [('general','general-v4'),('paypal','paypal-v2')]:
 timeline_path=root/'docs/pitch-v4'/('timeline-'+cut+'.json');timeline=json.loads(timeline_path.read_text())
 if timeline.get('pausePolishVersion')==1:continue
 video=media/(stem+'.mp4');length=duration(video);removals=[]
 for part in timeline['parts']:
  line=next(x for x in json.loads((root/'docs/pitch-v4'/(cut+'.json')).read_text(encoding='utf-8')) if x['title']==part['title'])
  aligned=json.loads((build/'aligned'/(cut+'-'+line['id']+'.json')).read_text())
  with wave.open(str(build/'audio'/cut/(line['id']+'.wav'))) as w:rate=w.getframerate();audio=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2).astype(float)/32768
  for prev,nxt in zip(aligned['words'],aligned['words'][1:]):
   if nxt['start']-prev['end']<.55:continue
   a=prev['end']+.12;b=nxt['start']-.12;piece=audio[int(a*rate):int(b*rate)]
   if len(piece) and 20*np.log10(np.sqrt(np.mean(piece**2))+1e-9)<-34:
    lo=math.ceil((part['start']+prev['end']+.14)*30)/30;hi=math.floor((part['start']+nxt['start']-.16)*30)/30
    if hi-lo>=.2:removals.append((lo,hi))
 removals.sort();keep=[];cursor=0
 for a,b in removals:keep.append((cursor,a));cursor=b
 keep.append((cursor,length));backup=build/'pre-pause';backup.mkdir(exist_ok=True)
 shutil.copy2(video,backup/(stem+'.mp4'))
 filters=[]
 for i,(a,b) in enumerate(keep):
  filters.append(f'[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[v{i}]')
  filters.append(f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,afade=t=in:d=0.004,afade=t=out:st={max(0,b-a-.004)}:d=0.004[a{i}]')
 filters.append(''.join(f'[v{i}][a{i}]' for i in range(len(keep)))+f'concat=n={len(keep)}:v=1:a=1[v][a]')
 target=build/(stem+'-paced.mp4')
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(video),'-filter_complex',';'.join(filters),'-map','[v]','-map','[a]','-r','30','-fps_mode','cfr','-c:v','libx264','-threads','2','-preset','veryfast','-crf','17','-c:a','aac','-b:a','192k','-movflags','+faststart',str(target)],check=True)
 target.replace(video)
 def mapped(t):return max(0,t-sum(max(0,min(t,b)-a) for a,b in removals if t>a))
 def rewrite(match):
  h,m,s,ms=map(int,match.groups());return stamp(mapped(h*3600+m*60+s+ms/1000),',' if ',' in match.group(0) else '.')
 for ext in ['srt','vtt']:
  p=media/(stem+'.'+ext);text=p.read_text(encoding='utf-8');shutil.copy2(p,backup/p.name);p.write_text(re.sub(r'(\d{2}):(\d{2}):(\d{2})[.,](\d{3})',rewrite,text),encoding='utf-8')
 for part in timeline['parts']:
  end=mapped(part['start']+part['duration']);part['start']=mapped(part['start']);part['duration']=end-part['start']
 timeline.update(duration=duration(video),pausePolishVersion=1,pauseEdits=[{'originalStart':a,'originalEnd':b,'removedSeconds':b-a} for a,b in removals])
 timeline_path.write_text(json.dumps(timeline,indent=2),encoding='utf-8');print(stem,'removed',len(removals),'quiet pauses; final',round(timeline['duration'],2),'seconds.',flush=True)
