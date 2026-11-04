"""Compose an original quiet instrumental bed; no third-party music assets."""
from pathlib import Path
import wave,numpy as np
sr=48000;out=Path('.local/pitch-v4/original-music.wav');out.parent.mkdir(parents=True,exist_ok=True)
chords=[[261.6256,329.6276,391.9954,493.8833],[220,261.6256,329.6276,391.9954],[174.6141,220,261.6256,329.6276],[195.9977,246.9417,293.6648,329.6276]]
with wave.open(str(out),'wb') as f:
 f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr)
 for second in range(180):
  t=(np.arange(sr,dtype=np.float64)+second*sr)/sr;beat=t/.6;bar=(beat//4).astype(int);y=np.zeros(sr)
  for ci,notes in enumerate(chords):
   mask=(bar%4)==ci;within=t%2.4;env=np.minimum(within/.12,1)*np.exp(-within/2.0)
   for j,hz in enumerate(notes):y+=mask*env*(.006*np.sin(2*np.pi*hz*t+j*.2)+.0015*np.sin(4*np.pi*hz*t))
  arptime=t%.3;envelope=(1-np.exp(-arptime*60))*np.exp(-arptime*10)
  for ci,notes in enumerate(chords):
   mask=(bar%4)==ci
   for j,hz in enumerate(notes):y+=mask*(((beat*2).astype(int)%4)==j)*.009*envelope*np.sin(2*np.pi*hz*2*t)
  fade=np.minimum(t/2,1)*np.minimum((180-t)/2,1);y*=fade
  stereo=np.stack([y,y*.98],axis=1);f.writeframes((np.clip(stereo,-1,1)*32767).astype('<i2').tobytes())
print('Original instrumental bed composed.',flush=True)
