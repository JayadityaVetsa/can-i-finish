from pathlib import Path
import json, html
root=Path(__file__).resolve().parent
timeline=json.loads((root/'docs/edit-timeline.json').read_text(encoding='utf-8'))
def stamp(t):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02}.{ms:03}'
cues=['WEBVTT',''];items=[]
for part in timeline['parts']:
    start=part['start'];end=start+part['duration']
    cues.extend([str(part['part']),f'{stamp(start)} --> {stamp(end)}',part['narration'],''])
    items.append(f'<h3>{html.escape(part["title"])}</h3><p>{html.escape(part["narration"])}</p>')
(root/'dist/media/demo.vtt').write_text('\n'.join(cues),encoding='utf-8')
page=root/'dist/demo.html';s=page.read_text(encoding='utf-8')
if '<track' not in s:s=s.replace('<source src="media/demo.mp4" type="video/mp4">','<source src="media/demo.mp4" type="video/mp4"><track kind="captions" src="media/demo.vtt" srclang="en" label="English">')
if 'Read the transcript' not in s:s=s.replace('<div class="facts">','<details style="margin-top:30px;border:1px solid #35425c;border-radius:8px;padding:20px"><summary style="cursor:pointer;color:#aadc79">Read the transcript</summary>'+''.join(items)+'</details><div class="facts">')
page.write_text(s,encoding='utf-8')
