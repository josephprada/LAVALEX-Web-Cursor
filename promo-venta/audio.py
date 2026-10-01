# Banda sonora sintetizada (original) sincronizada con la animación. 44.1 kHz estéreo.
import numpy as np, wave
SR=44100; DUR=37.6; N=int(SR*DUR)
L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(7)
def add(sig,t,pan=0.0,g=1.0):
    i=int(t*SR); n=min(len(sig),N-i)
    if n<=0: return
    L[i:i+n]+=sig[:n]*g*(1-max(0,pan)); R[i:i+n]+=sig[:n]*g*(1+min(0,pan))
def env(n,a=0.005,d=0.2):
    t=np.arange(n)/SR; e=np.minimum(1,t/a)*np.exp(-t/d); return e
def lp(x,a):  # one-pole lowpass
    y=np.zeros_like(x); acc=0
    for i in range(len(x)): acc+=a*(x[i]-acc); y[i]=acc
    return y
def lpv(x,c):  # vectorised-ish one-pole via cumulative filter in blocks
    from scipy.signal import lfilter
    return lfilter([c],[1,-(1-c)],x)
try:
    import scipy; F=lpv
except ImportError:
    F=lp
def kick(g=1):
    n=int(.45*SR); t=np.arange(n)/SR; f=45+110*np.exp(-t*28)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)*g
def snare():
    n=int(.25*SR); t=np.arange(n)/SR
    return (rng.standard_normal(n)*.6*np.exp(-t*16)+np.sin(2*np.pi*190*t)*.4*np.exp(-t*20))
def hat(o=False):
    n=int((.18 if o else .05)*SR); x=rng.standard_normal(n); x=x-F(x,.3)
    return x*np.exp(-np.arange(n)/SR*(14 if o else 60))*.35
def saw(f,n):
    t=np.arange(n)/SR; return 2*((t*f)%1)-1
def pluck(f,dur=.22,g=.3,bright=.25):
    n=int(dur*SR); x=(saw(f,n)+saw(f*1.006,n))*.5; x=F(x,bright)
    return x*env(n,.003,dur*.45)*g
def pad(freqs,dur,g=.12):
    n=int(dur*SR); t=np.arange(n)/SR; x=sum(saw(f,n)+saw(f*1.004,n) for f in freqs)/len(freqs)
    x=F(x,.05); e=np.minimum(1,t/.4)*np.minimum(1,(dur-t)/.5); return x*e*g
def bass(f,dur,g=.35):
    n=int(dur*SR); t=np.arange(n)/SR; x=np.sin(2*np.pi*f*t)+.3*np.sin(4*np.pi*f*t)
    return x*np.minimum(1,t/.005)*np.exp(-t*3)*g
def noise_sweep(dur,f0,f1,g=.3,rev=False):
    n=int(dur*SR); x=rng.standard_normal(n); cs=np.linspace(f0,f1,n)
    y=np.zeros(n); acc=0
    for i in range(0,n,64):
        c=cs[i]; seg=x[i:i+64]
        for j in range(len(seg)): acc+=c*(seg[j]-acc); y[i+j]=acc
    e=np.sin(np.linspace(0,np.pi,n))**1.5
    return y*e*g*3
def boom(g=1):
    n=int(1.6*SR); t=np.arange(n)/SR; f=30+70*np.exp(-t*6)
    s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.2)
    nz=F(rng.standard_normal(n),.08)*np.exp(-t*5)*2
    return (s+nz)*g
def blip(f,g=.25,d=.09):
    n=int(d*SR); t=np.arange(n)/SR; ff=f*(1+1.5*np.exp(-t*60))
    return np.sin(2*np.pi*np.cumsum(ff)/SR)*np.exp(-t*30)*g
def drop_sfx():
    n=int(.35*SR); t=np.arange(n)/SR; f=600+1400*np.exp(-t*25)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*14)*.5
def shimmer(dur=1.0,g=.12):
    n=int(dur*SR); t=np.arange(n)/SR; x=np.zeros(n)
    for k,f in enumerate([2093,2637,3136,3951,4186]):
        x+=np.sin(2*np.pi*f*t+k)*np.exp(-((t-k*.08)*6)**2)
    return x*g
def whoosh(dur=.5,g=.35): return noise_sweep(dur,.02,.5,g)
def riser(dur,g=.25): return noise_sweep(dur,.01,.6,g)
N2F=lambda m:440*2**((m-69)/12)


W=1.15
I=lambda x:x/W
# ---------- INTRO ----------
add(riser(I(0.85),.12),0.0)
add(drop_sfx(),I(0.84),g=1.2); add(boom(.5),I(0.85))
add(pad([N2F(45),N2F(52),N2F(57)],5.4,.10),I(0.9))
add(noise_sweep(1.2,.01,.35,.22),I(1.05),pan=-.3); add(noise_sweep(1.2,.01,.35,.22),I(1.1),pan=.3)
add(riser(1.05,.3),I(1.25))
add(boom(1.1),I(2.45)); add(shimmer(1.2,.1),I(2.45))
for i,tt in enumerate([3.35,3.44,3.53,3.45,3.52,3.59,3.66]): add(blip(900+i*120,.12),I(tt),pan=(i-3)*.15)
notes=[64,67,69,71,72,74,76]
for i in range(7): add(blip(N2F(notes[i]+12),.22,.12),I(3.82+i*.075),pan=(i-3)*.2)
add(shimmer(1.4,.16),I(4.6))
add(pad([N2F(60),N2F(64),N2F(67),N2F(71)],2.0,.12),I(4.7))
add(whoosh(.7,.45),I(6.2)); add(noise_sweep(.8,.05,.02,.25),I(6.6))
# ---------- BEAT 6.1 - 32.4 ----------
BPM=120; b=60/BPM; T0=6.1
prog=[(57,[57,60,64]),(53,[53,57,60]),(48,[48,52,55]),(55,[55,59,62])]
end=32.4; nb=int((end-T0)/b)
for k in range(nb):
    t=T0+k*b
    if 11.2<=t<11.6 or 19.2<=t<19.6 or 26.6<=t<27.0: continue
    add(kick(.9),t)
    if k%2==1: add(snare(),t,g=.35)
    add(hat(),t+b/2,pan=.3); add(hat(),t,pan=-.3,g=.6)
    if k%4==3: add(hat(True),t+b/2,pan=.2)
    root,ch=prog[(k//4)%4]
    add(bass(N2F(root-12),b*.9),t); add(bass(N2F(root-12),b*.45,.22),t+b/2)
    for j in range(2):
        nt=ch[(k*2+j)%3]+12+(12 if (k*2+j)%4==3 else 0)
        add(pluck(N2F(nt),.2,.14),t+j*b/2,pan=(-.35 if j else .35))
    if k%4==0: add(pad([N2F(n+12) for n in ch],b*4,.07),t)
# accents
add(boom(1.0),6.2); add(shimmer(1.0,.12),6.25)
add(whoosh(.5,.35),6.5); add(boom(.6),6.85)
add(blip(1400,.22),7.4); add(blip(1760,.18),7.55)
add(whoosh(.3,.25),7.8); add(blip(1200,.2),8.05)
add(shimmer(1.0,.14),8.3)
add(riser(1.2,.3),10.4); add(noise_sweep(.5,.02,.6,.35),11.15); add(boom(.9),11.6)
for a in [11.65,14.3,16.95]: add(whoosh(.45,.4),a); add(blip(1300,.18),a+.4)
add(whoosh(.6,.5),19.15)
add(blip(900,.2),19.75); add(riser(.3,.2),19.75)
add(boom(1.4),20.05); add(shimmer(1.2,.16),20.1)
for i in range(8): add(blip(2000+i*300,.08,.05),20.1+i*.04,pan=(i%2-.5))
add(boom(.8),21.6); add(shimmer(.8,.12),21.8); add(boom(.6),21.95); add(boom(.5),22.2)
add(whoosh(.4,.3),23.2); add(blip(1300,.2),23.5)
add(noise_sweep(.5,.02,.6,.35),26.6); add(boom(1.0),27.0)
add(boom(.8),27.2); add(boom(.7),27.5); add(whoosh(.5,.3),27.7)
add(whoosh(.35,.3),28.4); add(blip(1500,.2),28.7)
add(boom(.6),29.0); add(shimmer(1.0,.14),29.05)
add(riser(.6,.3),32.0)
# ---------- END CARD (old 36.0 -> 32.6) ----------
O=32.6-36.0
add(boom(1.2),36.0+O); add(shimmer(1.5,.16),36.05+O)
add(pad([N2F(57),N2F(60),N2F(64),N2F(69)],4.6,.16),36.0+O)
for i in range(7): add(blip(N2F(notes[i]+12),.2,.12),36.4+O+i*.044,pan=(i-3)*.2)
add(pluck(N2F(81),1.5,.2,.2),37.4+O); add(pluck(N2F(76),1.5,.15,.2),37.4+O)
add(blip(1200,.2),37.5+O); add(shimmer(1.2,.14),38.9+O); add(bass(N2F(33),3.0,.4),36.0+O)
# master
mix=np.stack([L,R],1)
fade=np.ones(N); fo=int(0.6*SR); fade[-fo:]=np.linspace(1,0,fo); mix*=fade[:,None]
mix=np.tanh(mix*1.1)
mix/=np.max(np.abs(mix))/0.89
data=(mix*32767).astype(np.int16)
with wave.open('out/musica.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())
print('ok')
