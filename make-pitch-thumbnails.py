"""Create original product-pitch thumbnails from actual browser evidence."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
root=Path(__file__).resolve().parent
font=Path('C:/Windows/Fonts/segoeuib.ttf')
if not font.exists():font=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
def f(n):return ImageFont.truetype(str(font),n)
for cut,stem,title,tag,evidence in [
 ('general','general-v4','THE LAST STEP.\nREACHABLE.','BUILD A WEB PEOPLE CAN FINISH.','govuk-bus-pass-027.jpg'),
 ('paypal','paypal-v2','READY TO BUY.\nABLE TO FINISH.','KEYBOARD EVIDENCE × PAYPAL SANDBOX','checkout-fixed-000.jpg')]:
 im=Image.new('RGB',(1920,1080),'#142a22');d=ImageDraw.Draw(im)
 d.rounded_rectangle((88,86,414,150),18,fill='#d2f58b');d.text((112,95),'Can I Finish?',font=f(37),fill='#142a22')
 d.text((90,270),title,font=f(108),fill='#f8faf4',spacing=13)
 d.text((95,640),tag,font=f(27),fill='#d2f58b')
 d.rounded_rectangle((1010,116,1850,970),30,fill='#e5eed9')
 source=Image.open(root/'dist/evidence'/evidence).convert('RGB')
 if cut=='paypal':source=source.crop((310,80,1630,930))
 else:source=source.crop((420,0,1500,1080))
 source=ImageOps.contain(source,(770,650));im.paste(source,(1045+(770-source.width)//2,170))
 d=ImageDraw.Draw(im)
 if cut=='paypal':
  d.text((1080,842),'18 → 4',font=f(70),fill='#142a22');d.text((1400,867),'KEY EVENTS',font=f(22),fill='#142a22')
 else:d.text((1110,861),'REAL GOV.UK JOURNEY',font=f(31),fill='#142a22')
 d.text((95,850),'Tab',font=f(38),fill='#d2f58b');d.text((225,850),'→',font=f(38),fill='#d2f58b');d.text((310,850),'Enter',font=f(38),fill='#d2f58b');d.text((500,850),'→',font=f(38),fill='#d2f58b');d.text((585,850),'Done.',font=f(38),fill='#d2f58b')
 im.save(root/'dist/media'/(stem+'-poster.jpg'),quality=94)

logo=Image.new('RGB',(768,512),'#142a22');d=ImageDraw.Draw(logo)
d.text((55,52),'KEYBOARD JOURNEY INTELLIGENCE',font=f(18),fill='#d2f58b')
d.text((52,160),'Can I',font=f(82),fill='#f8faf4');d.text((52,254),'Finish?',font=f(94),fill='#d2f58b')
d.rounded_rectangle((515,146,708,355),30,fill='#d2f58b');d.line((561,190,561,284,648,284),fill='#142a22',width=14);d.polygon([(651,284),(619,258),(619,310)],fill='#142a22')
d.line((55,413,710,413),fill='#48614c',width=2);d.text((55,439),'LET PEOPLE FINISH.',font=f(21),fill='#d2f58b')
logo.save(root/'dist/media/project-thumbnail.png')
