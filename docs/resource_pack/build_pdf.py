"""Render the verified project content as a vector PDF manual."""
import json, math, re
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
    Spacer, PageBreak, Table, TableStyle, Flowable, KeepTogether)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'output/resources'
DATA = json.loads((ROOT/'tmp/resource-pack/content.json').read_text(encoding='utf-8'))
for name, file in [('Aero','arial.ttf'),('Aero-Bold','arialbd.ttf'),('Aero-Italic','ariali.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(Path('C:/Windows/Fonts')/file)))
pdfmetrics.registerFontFamily('Aero', normal='Aero', bold='Aero-Bold', italic='Aero-Italic')
NAVY=HexColor('#132C46'); TEAL=HexColor('#087E8B'); GRAY=HexColor('#4C6073'); LIGHT=HexColor('#EDF5F7')
W,H=595.28,841.89
ST={
 'title':ParagraphStyle('Title',fontName='Aero-Bold',fontSize=38,leading=43,textColor=NAVY,spaceAfter=20),
 'sub':ParagraphStyle('Subtitle',fontName='Aero',fontSize=17,leading=24,textColor=GRAY,spaceAfter=16),
 'h1':ParagraphStyle('Chapter',fontName='Aero-Bold',fontSize=23,leading=28,textColor=NAVY,spaceAfter=14),
 'summary':ParagraphStyle('Summary',fontName='Aero-Bold',fontSize=11.5,leading=16,textColor=TEAL,spaceAfter=13),
 'body':ParagraphStyle('Body',fontName='Aero',fontSize=10.2,leading=15,textColor=NAVY,spaceAfter=10,splitLongWords=True),
 'small':ParagraphStyle('Small',fontName='Aero',fontSize=8.2,leading=11.5,textColor=GRAY,spaceAfter=8,splitLongWords=True),
 'cell':ParagraphStyle('Cell',fontName='Aero',fontSize=8.5,leading=12,textColor=NAVY,splitLongWords=True),
 'cellh':ParagraphStyle('CellHead',fontName='Aero-Bold',fontSize=8.7,leading=12,textColor=white),
 'callout':ParagraphStyle('Callout',fontName='Aero-Bold',fontSize=10,leading=14,textColor=NAVY,backColor=LIGHT,borderPadding=10,spaceBefore=8,spaceAfter=16),
 'ref':ParagraphStyle('Reference',fontName='Aero',fontSize=8,leading=10.5,textColor=GRAY,spaceAfter=5,splitLongWords=True),
}

def clean(s):
    return str(s).replace('\u2011','-').replace('\u2013','-').replace('\u2014',' - ').replace('\u2192','->').replace('\u2194','<->')
def para(s,style='body'):
    return Paragraph(escape(clean(s)).replace('\n','<br/>'),ST[style])

def sides(a,b):
    ax,ay=a['x']+a['w']/2,a['y']+a['h']/2
    bx,by=b['x']+b['w']/2,b['y']+b['h']/2
    dx,dy=bx-ax,by-ay
    if abs(dx)>abs(dy)*1.25:
        return (a['x']+(a['w'] if dx>0 else 0),ay),(b['x']+(0 if dx>0 else b['w']),by)
    return (ax,a['y']+(a['h'] if dy>0 else 0)),(bx,b['y']+(0 if dy>0 else b['h']))

class Diagram(Flowable):
    def __init__(self,spec):
        Flowable.__init__(self);self.spec=spec;self.width=499;self.height=260
    def draw(self):
        c=self.canv;c.saveState();s=.499
        c.translate(0,255);c.scale(s,-s)
        def text(label,x,y,size=20,center=True):
            lines=clean(label).split('\n')
            c.saveState();c.translate(x,y);c.scale(1,-1)
            c.setFillColor(NAVY);c.setFont('Aero',size)
            for j,line in enumerate(lines):
                yy=(len(lines)-1)*size*.6-j*size*1.2
                if center:c.drawCentredString(0,yy,line)
                else:c.drawString(0,yy,line)
            c.restoreState()
        def arrow(x1,y1,x2,y2,label='',dashed=False):
            c.setStrokeColor(TEAL);c.setLineWidth(2.2);c.setDash(6,4) if dashed else c.setDash()
            c.line(x1,y1,x2,y2);c.setDash()
            angle=math.atan2(y2-y1,x2-x1);L=11
            p=c.beginPath();p.moveTo(x2,y2);p.lineTo(x2-L*math.cos(angle-.45),y2-L*math.sin(angle-.45));p.lineTo(x2-L*math.cos(angle+.45),y2-L*math.sin(angle+.45));p.close()
            c.setFillColor(TEAL);c.drawPath(p,fill=1,stroke=0)
            if label:
                mx,my=(x1+x2)/2,(y1+y2)/2
                lines=clean(label).split('\n')
                if abs(y1-y2)<15 and d['kind']!='sequence':
                    limit=max(65,abs(x1-x2)-12);wrapped=[]
                    for part in lines:
                        line=''
                        for word in part.split():
                            test=(line+' '+word).strip()
                            if line and pdfmetrics.stringWidth(test,'Aero',17)>limit:wrapped.append(line);line=word
                            else:line=test
                        wrapped.append(line)
                    lines=wrapped;label='\n'.join(lines)
                tw=max(pdfmetrics.stringWidth(z,'Aero',17) for z in lines)+8
                c.setFillColor(white);c.rect(mx-tw/2,my-(22*len(lines)+10),tw,22*len(lines)+4,fill=1,stroke=0)
                text(label,mx,my-(12+(len(lines)-1)*10),17)
        d=self.spec
        if d['kind']=='sequence':
            n=len(d['actors']);xs=[100+i*800/(n-1) for i in range(n)]
            for i,label in enumerate(d['actors']):
                c.setFillColor(LIGHT);c.setStrokeColor(NAVY);c.rect(xs[i]-95,10,190,65,fill=1,stroke=1)
                text(label,xs[i],48,19)
                c.setDash(6,5);c.line(xs[i],75,xs[i],485);c.setDash()
            step=370/max(len(d['steps']),1)
            for j,(a,b,label) in enumerate(d['steps']):
                y=105+j*step
                if a==b:
                    c.setStrokeColor(TEAL);c.setLineWidth(2);c.line(xs[a],y,xs[a]+45,y);c.line(xs[a]+45,y,xs[a]+45,y+22)
                    arrow(xs[a]+45,y+22,xs[a],y+22)
                    tw=pdfmetrics.stringWidth(clean(label),'Aero',16)
                    text(label,min(xs[a]+9,990-tw),y-10,16,False)
                else:arrow(xs[a],y+15,xs[b],y+15,f'{j+1}. {label}')
        else:
            byid={n['id']:n for n in d['nodes']}
            for e in d['edges']:
                a,b=sides(byid[e['a']],byid[e['b']])
                if d['id']=='state' and {e['a'],e['b']}=={'run','pause'}:
                    off=-24 if e['a']=='run' else 24;a=(a[0],a[1]+off);b=(b[0],b[1]+off)
                arrow(*a,*b,e['label'],e['style']=='dashed')
                if d['id']=='architecture' and e['a'] in {'radio','rx','laptop','bridge'}:arrow(*b,*a)
            for n in d['nodes']:
                c.setFillColor(LIGHT);c.setStrokeColor(NAVY);c.setLineWidth(1.8)
                x,y,w,h=n['x'],n['y'],n['w'],n['h']
                if n['kind']=='ellipse':c.ellipse(x,y,x+w,y+h,fill=1,stroke=1)
                elif n['kind']=='diamond':
                    p=c.beginPath();p.moveTo(x+w/2,y);p.lineTo(x+w,y+h/2);p.lineTo(x+w/2,y+h);p.lineTo(x,y+h/2);p.close();c.drawPath(p,fill=1,stroke=1)
                else:c.rect(x,y,w,h,fill=1,stroke=1)
                text(n['label'],x+w/2,y+h/2+7,20 if w>=200 else 18)
        c.restoreState()

class Manual(BaseDocTemplate):
    def __init__(self,path):
        super().__init__(str(path),pagesize=(W,H),leftMargin=48,rightMargin=48,topMargin=54,bottomMargin=50,title='Aero Ground Station - Hardware Implementation and System Architecture',author='Aero Ground Station project',pageCompression=1)
        frame=Frame(48,50,W-96,H-104,id='main',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='report',frames=frame,onPage=self.page))
    def page(self,c,doc):
        c.saveState()
        if doc.page>1:
            c.setFont('Aero',8);c.setFillColor(GRAY);c.drawString(48,H-30,'AERO GROUND STATION  /  IMPLEMENTATION MANUAL')
            c.setStrokeColor(HexColor('#D5E3E8'));c.line(48,H-38,W-48,H-38)
        c.setFont('Aero',8);c.setFillColor(GRAY);c.drawString(48,28,'26 October 2026  |  Project evidence + technical references')
        c.drawRightString(W-48,28,str(doc.page));c.restoreState()
    def afterFlowable(self,f):
        if isinstance(f,Paragraph) and f.style.name=='Chapter' and f.getPlainText()!='Contents':
            txt=f.getPlainText();key=re.sub('[^a-zA-Z0-9]','',txt)
            self.canv.bookmarkPage(key);self.canv.addOutlineEntry(txt,key,0,False)
            self.notify('TOCEntry',(0,txt,self.page,key))

def table(rows):
    count=len(rows[0]); widths=([110,389] if count==2 else [110]+[(499-110)/(count-1)]*(count-1))
    cells=[[para(v,'cellh' if i==0 else 'cell') for v in row] for i,row in enumerate(rows)]
    t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,LIGHT]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.8,TEAL)]))
    return t

story=[Spacer(1,70),para('AERO / PROJECT RESOURCE PACK','summary'),para('Aero Ground Station','title'),para(DATA['subtitle'],'sub'),Spacer(1,24),para('Disaster-management drone\n3-inch quadcopter + ArduCopter + ELRS + laptop vision','sub'),Spacer(1,30),para('Hardware, power and wiring • Radio and MAVLink • Video capture • AI detection • UML • Test and commissioning evidence','body'),Spacer(1,35),para('Evidence status','summary'),para('This manual separates implemented application behavior, user-reported bench checks, historical parameter files and proposed additions. It is not a flight-clearance certificate. GPS fix, video capture hardware and full aircraft validation remain subject to verification.','callout'),para(DATA['date'],'small'),PageBreak(),para('Contents','h1')]
toc=TableOfContents();toc.levelStyles=[ParagraphStyle('TOC0',fontName='Aero',fontSize=10,leading=17,textColor=NAVY,leftIndent=0,firstLineIndent=0,spaceBefore=1)]
story += [toc,PageBreak()]
for i,sec in enumerate(DATA['sections'],1):
    story += [para(f'{i:02d}  {sec["title"]}','h1'),para(sec['summary'],'summary')]
    if sec.get('diagram'):
        d=DATA['diagrams'][sec['diagram']]
        story += [Diagram(d),para(d['caption'],'small'),Spacer(1,5)]
    story += [para(p) for p in sec['paragraphs']]
    if sec.get('table'):story += [table(sec['table']),Spacer(1,12)]
    for b in sec.get('bullets',[]):story += [para('- '+b)]
    if sec.get('callout'):story += [para(sec['callout'],'callout')]
    if i==len(DATA['sections']):
        for sid,title,url in DATA['sources']:
            story += [Paragraph(f'<b>{sid}  {escape(title)}</b><br/><link href="{escape(url)}" color="#087E8B">{escape(url)}</link>',ST['ref'])]
    elif sec.get('sources'):
        story += [para('Reference keys: '+', '.join(sec['sources'])+' (links in Section 37).','small')]
    if i<len(DATA['sections']):story.append(PageBreak())

OUT.mkdir(parents=True,exist_ok=True)
target=OUT/'Aero_Hardware_Implementation_Manual.pdf'
Manual(target).multiBuild(story)
print(target)
