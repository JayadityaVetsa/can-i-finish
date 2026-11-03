from pathlib import Path
import json,re,sys
root=Path(__file__).resolve().parent
paypal='--paypal' in sys.argv
timeline=json.loads((root/('docs/edit-timeline-paypal.json' if paypal else 'docs/edit-timeline-v2.json')).read_text(encoding='utf-8'))
stem='paypal-demo' if paypal else 'general-v2'
def stamp(t):
    ms=round(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
cues=[]
for part in timeline['parts']:
    words=part['narration'].split();start=part['start']
    for k in range(0,len(words),17):
        chunk=words[k:k+17];end=start+part['duration']*len(chunk)/len(words)
        cues.append(f'{len(cues)+1}\n{stamp(start)} --> {stamp(end)}\n'+ ' '.join(chunk));start=end
text='\n\n'.join(cues)
(root/f'dist/media/{stem}.vtt').write_text('WEBVTT\n\n'+text,encoding='utf-8')
(root/f'dist/media/{stem}.srt').write_text(re.sub(r'(\d\d:\d\d:\d\d)\.(\d{3})',r'\1,\2',text),encoding='utf-8')
(root/f'dist/media/{stem}-transcript.txt').write_text('\n\n'.join(p['narration'] for p in timeline['parts']),encoding='utf-8')
print('Captions and transcript:',stem)
