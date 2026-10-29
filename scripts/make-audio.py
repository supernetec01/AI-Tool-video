from pathlib import Path
import numpy as np
import wave
root=Path(__file__).resolve().parents[1]
sr=48000; total=60; mix=np.zeros(sr*total,dtype=np.float64)
def note(midi,start,length,amp):
 n=min(int(length*sr),len(mix)-int(start*sr))
 if n<=0:return
 t=np.arange(n)/sr;f=440*2**((midi-69)/12)
 env=(1-np.exp(-t*55))*np.exp(-t/(1.25+length*.12))
 sig=sum((1/(k**2.4))*np.sin(2*np.pi*f*k*t)*np.exp(-t*k*.12) for k in range(1,7))*env
 mix[int(start*sr):int(start*sr)+n]+=amp*sig
# Original Cmaj7–Am7–Fmaj7–G6 harmonic progression. Sparse, soft, no drums.
chords=[[48,55,59,64],[45,52,55,60],[41,48,52,57],[43,50,55,59]]
beat=60/72
for bar in range(18):
 start=bar*4*beat
 chord=chords[bar%4]
 for j,m in enumerate(chord):note(m,start+j*.10,4.7,.08 if j else .11)
 for j,k in enumerate([1,2,3,2]):note(chord[k]+12,start+j*beat,2.7,.047)
 if bar%2==0:
  for j,m in enumerate([76,74,72,71] if bar%4==0 else [72,69,67,64]):note(m,start+j*beat,2.8,.035)
# Light, deterministic early-room reflections.
for lag,gain in [(0.053,.10),(.113,.07),(.223,.04)]:
 d=int(sr*lag); mix[d:]+=mix[:-d].copy()*gain
mix/=max(1,np.max(np.abs(mix))/.55)
t=np.arange(len(mix))/sr
mix*=np.minimum(t/1.8,1)*np.minimum((60-t)/3,1)
def save(path,a):
 with wave.open(str(path),'w') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes(np.column_stack([a,a*.99]).clip(-1,1).__mul__(32767).astype('<i2').tobytes())
save(root/'public/audio/morning-piano.wav',mix)
rng=np.random.default_rng(77);t=np.arange(int(sr*2/3))/sr
noise=rng.standard_normal(len(t));noise=np.convolve(noise,np.ones(30)/30,mode='same')
env=np.sin(np.pi*np.minimum(t/(2/3),1))**3
swish=noise*env*.19
save(root/'public/audio/soft-transition.wav',swish)
print('Original 60s piano music and 0.667s transition sound generated')
