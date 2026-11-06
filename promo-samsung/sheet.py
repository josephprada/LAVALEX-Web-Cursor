import sys,glob
from PIL import Image,ImageDraw,ImageFont
files=sys.argv[2:]; out=sys.argv[1]
w,h=270,480; cols=min(6,len(files)); rows=(len(files)+cols-1)//cols
S=Image.new('RGB',(cols*w,rows*(h+30)),'#111')
d=ImageDraw.Draw(S); f=ImageFont.truetype('fonts/Montserrat-800.ttf',20)
for i,fn in enumerate(files):
    im=Image.open(fn).convert('RGB').resize((w,h))
    x,y=(i%cols)*w,(i//cols)*(h+30); S.paste(im,(x,y+30)); d.text((x+8,y+4),fn.split('_')[-1][:-4]+'s',fill='#fff',font=f)
S.save(out)
