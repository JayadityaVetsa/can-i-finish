"""Edit real screen recordings into a concise 1080p narrated product demo."""
from pathlib import Path
import json, subprocess, textwrap, sys
root=Path(__file__).resolve().parent
build=root/'.local/video-build-v3';build.mkdir(parents=True,exist_ok=True)
out=root/'dist/media';out.mkdir(parents=True,exist_ok=True)
def run(args):
    subprocess.run(args,cwd=root,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def duration(p):
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],cwd=root,text=True).strip())
viewer=root/'docs/viewer-recordings';fixtures=root/'docs/film-fixtures';apple=root/'dist/evidence/apple-voiceover.webm'
def clip(file,start=0,end=None):
    d=duration(file);return (file,max(0,start),min(d,end if end is not None else d))
def tail(file,seconds):
    d=duration(file);return clip(file,max(0,d-seconds),d)
scenes=[
 [clip(fixtures/'registration-broken.webm',.1),clip(viewer/'viewer-compare.webm',.2)],
 [clip(apple,.7,20.5)],
 [clip(apple,20.5)],
 [clip(root/'docs/paypal-film/film-ai-proof.webm',.1),clip(viewer/'viewer-compare.webm',.1,8)],
 [clip(fixtures/'registration-broken.webm',.1),clip(viewer/'viewer-compare.webm',.1)],
 [clip(fixtures/'registration-fixed.webm',.1),clip(viewer/'viewer-compare.webm',.1)],
 [clip(fixtures/'dialog-broken.webm',.2),clip(fixtures/'dialog-fixed.webm',.1)],
 [clip(viewer/'viewer-export.webm',.1),tail(viewer/'viewer-contract.webm',6),clip(fixtures/'registration-fixed.webm',.1)]
]
lines=json.loads((root/'docs/narration-v3.json').read_text(encoding='utf-8'))
timeline=[];cursor=0
for i,(line,clips) in enumerate(zip(lines,scenes),1):
    audio=root/'docs/narration-v3'/f"{line['id']}.wav";length=duration(audio)+.28
    total=sum(end-start for _,start,end in clips)
    # Shorten source when needed; never slow it down to fill narration.
    rate=max(1,total/length)
    args=['ffmpeg','-y','-loglevel','error']
    for file,start,end in clips:args+=['-ss',str(start),'-t',str(end-start),'-i',str(file)]
    args+=['-i',str(audio)]
    sub=build/f'part-{i}.ass'
    words=line['text'].split()
    chunks=[' '.join(words[k:k+17]) for k in range(0,len(words),17)]
    def stamp(seconds):
        cs=round(seconds*100);return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
    cues=[];elapsed=0
    for chunk in chunks:
        end=elapsed+length*len(chunk.split())/len(words)
        caption='\\N'.join(textwrap.wrap(chunk,105))
        cues.append(f'Dialogue: 0,{stamp(elapsed)},{stamp(end)},Caption,,0,0,0,,{caption}')
        elapsed=end
    captions='\n'.join(cues)
    header=line['title']+('  ·  FOOTAGE CONDENSED' if i in [2,3] else '')
    sub.write_text(f'''[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Arial,27,&H00F5F6FA,&H00FFFFFF,&H00271912,&H00271912,0,0,0,0,100,100,0,0,1,0,0,2,120,120,15,1
Style: Header,Arial,17,&H0079DCAA,&H00FFFFFF,&H00271912,&H00271912,1,0,0,0,100,100,1,0,1,0,0,7,120,120,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:10:00.00,Header,,0,0,0,,{{\\pos(120,985)}}{header}
{captions}
''',encoding='utf-8')
    filters=[]
    for j in range(len(clips)):filters.append(f'[{j}:v]scale=1920:1080:flags=lanczos,fps=30,setsar=1,setpts=PTS-STARTPTS[v{j}]')
    streams=''.join(f'[v{j}]' for j in range(len(clips)))
    filters.append(streams+f'concat=n={len(clips)}:v=1:a=0,setpts=PTS/{rate:.6f},fps=30,scale=1728:972:flags=lanczos,pad=1920:1080:96:0:color=0x121929,tpad=stop_mode=clone:stop_duration=30,ass=.local/video-build-v3/part-{i}.ass[out]')
    filters.append(f'[{len(clips)}:a]aresample=48000,loudnorm=I=-16:TP=-1.5:LRA=11,apad[a]')
    output=build/f'part-{i}.mp4'
    args+=['-filter_complex',';'.join(filters),'-map','[out]','-map','[a]','-t',str(length),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-movflags','+faststart',str(output)]
    chosen={int(x) for x in sys.argv[1:]} if len(sys.argv)>1 else set(range(1,9))
    if i in chosen or not output.exists():run(args)
    timeline.append({'part':i,'start':round(cursor,3),'duration':round(length,3),'title':line['title'],'narration':line['text'],'sourceSpeed':round(rate,3),'clips':[{'file':str(f.relative_to(root)),'start':round(s,3),'end':round(e,3)} for f,s,e in clips]});cursor+=length
    print('Rendered',i,line['id'],round(length,1),'seconds',flush=True)
concat=build/'concat.txt';concat.write_text('\n'.join(f"file 'part-{i}.mp4'" for i in range(1,9)),encoding='utf-8')
run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-video_track_timescale','30000','-movflags','+faststart',str(out/'general-v3.mp4')])
run(['ffmpeg','-y','-loglevel','error','-ss','18','-i',str(out/'general-v3.mp4'),'-frames:v','1','-q:v','2',str(out/'general-v3-poster.jpg')])
(root/'docs/edit-timeline-v3.json').write_text(json.dumps({'durationSeconds':round(cursor,3),'resolution':'1920x1080','outputFrameRate':30,'browserSourceFrameRate':25,'narration':'Kokoro-82M v1.0 af_heart, locally synthesized','parts':timeline},indent=2),encoding='utf-8')
print('Completed',round(cursor,2),'seconds')
