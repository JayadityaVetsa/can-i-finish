"""Prepare conversational pacing and align captions to the generated narration, locally."""
from pathlib import Path
import json,re,time,subprocess,hashlib,difflib,os
from faster_whisper import WhisperModel
root=Path(__file__).resolve().parent
build=root/'.local/pitch-v4';(build/'aligned').mkdir(exist_ok=True,parents=True)
model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2,download_root=os.environ.get('VOICE_ASR_CACHE',str(build/'asr-cache')))
def duration(p):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)],text=True).strip())
def norm(s):return re.sub('[^a-z0-9]','',s.lower().replace('’',"'"))
items=[(cut,x) for cut in ['general','paypal'] for x in json.loads((root/'docs/pitch-v4'/f'{cut}.json').read_text(encoding='utf-8'))]
done=set()
while len(done)<len(items):
 progress=False
 for cut,line in items:
  key=cut+'/'+line['id'];source=root/'docs/narration-pitch-v4'/cut/(line['id']+'.wav');result=build/'aligned'/(cut+'-'+line['id']+'.json')
  if key in done or not source.exists():continue
  try:raw_duration=duration(source)
  except:continue
  if raw_duration<1:continue
  digest=hashlib.sha256(source.read_bytes()).hexdigest();script_digest=hashlib.sha256(line['text'].encode()).hexdigest()
  if result.exists() and json.loads(result.read_text()).get('sourceHash')==digest and json.loads(result.read_text()).get('scriptHash')==script_digest:done.add(key);continue
  words=line['text'].split();rate=150/(len(words)/raw_duration*60)
  audio=build/'audio'/cut/(line['id']+'.wav');audio.parent.mkdir(parents=True,exist_ok=True)
  subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(source),'-af',f'rubberband=tempo={rate:.7f},highpass=f=65,loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-ac','2','-c:a','pcm_s16le',str(audio)],check=True)
  length=duration(audio);segments,_=model.transcribe(str(audio),language='en',word_timestamps=True,vad_filter=True,initial_prompt='Can I Finish, GOV dot UK, VoiceOver, Field Notes, PayPal sandbox Orders API.')
  heard=[]
  for segment in segments:
   heard.extend({'word':w.word.strip(),'start':w.start,'end':w.end} for w in (segment.words or []))
  matcher=difflib.SequenceMatcher(None,[norm(w) for w in words],[norm(w['word']) for w in heard],autojunk=False);anchors={}
  for block in matcher.get_matching_blocks():
   for k in range(block.size):anchors[block.a+k]=(heard[block.b+k]['start'],heard[block.b+k]['end'])
  coverage=len(anchors)/len(words)
  if coverage<.73:raise RuntimeError('Narration needs review: '+key+' word agreement '+str(round(coverage,2)))
  timings=[]
  for i,w in enumerate(words):
   if i in anchors:a,b=anchors[i]
   else:
    lo=max((k for k in anchors if k<i),default=-1);hi=min((k for k in anchors if k>i),default=len(words));left=anchors[lo][1] if lo>=0 else 0;right=anchors[hi][0] if hi<len(words) else length;span=max(.05,right-left)/(hi-lo);a=left+span*(i-lo-1);b=a+span
   timings.append({'word':w,'start':round(max(0,a),3),'end':round(min(length,max(a+.04,b)),3)})
  chunks=[];start=0
  for i,w in enumerate(words):
   count=i-start+1
   if count>=9 or (count>=3 and w.endswith(('.', '?','!'))) or i==len(words)-1:
    chunks.append({'text':' '.join(words[start:i+1]),'start':timings[start]['start'],'end':min(length,timings[i]['end']+.12)});start=i+1
  for i,cue in enumerate(chunks[:-1]):cue['end']=max(cue['start']+.2,min(cue['end'],chunks[i+1]['start']-.02))
  trim_end=min(length,timings[-1]['end']+.16)
  if length-trim_end>.2:
   trimmed=audio.with_name(audio.stem+'-trim.wav');subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(audio),'-t',str(trim_end),'-c:a','copy',str(trimmed)],check=True);trimmed.replace(audio);length=duration(audio)
  record={'cut':cut,'id':line['id'],'sourceHash':digest,'scriptHash':script_digest,'rawDuration':raw_duration,'tempo':rate,'duration':length,'wordAgreement':round(coverage,3),'heardWords':heard,'heard':' '.join(w['word'] for w in heard),'words':timings,'cues':chunks}
  result.write_text(json.dumps(record,indent=2),encoding='utf-8');done.add(key);progress=True;print('Aligned',key,'duration',round(length,1),'word agreement',round(coverage,2),flush=True)
 if not progress:time.sleep(5)
print('Both narration cuts prepared and aligned.',flush=True)
