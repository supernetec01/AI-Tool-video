"""Build a device-neutral, self-contained Jianying project from the shared timeline."""
from pathlib import Path
import json
import shutil
import uuid
import argparse
import subprocess
from PIL import ImageFont
import pyJianYingDraft as d

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'out/jianying-export'
DATA = json.loads((ROOT / 'out/jianying-timeline.json').read_text())
FPS, TOTAL = DATA['FPS'], DATA['TOTAL']
NAME = 'MomBite01-Editable'
COLORS = {'brown':'#4A3833','rose':'#CB8176','sage':'#51634B','muted':'#79685C'}

def us(f):
    return round(f * 1_000_000 / FPS)

def interval(f0, f1):
    return d.Timerange(us(f0), us(f1) - us(f0))

def rgb(color):
    color = COLORS.get(color, color).lstrip('#')
    return tuple(int(color[i:i+2],16)/255 for i in (0,2,4))

def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def build(smoke=False):
    name = 'MomBite01-SmokeTest' if smoke else NAME
    folder = OUT / 'Drafts'
    folder.mkdir(parents=True, exist_ok=True)
    # This generated staging directory is the only replaced output.
    script = d.DraftFolder(str(folder)).create_draft(name, 1080, 1920, fps=FPS, allow_replace=True)
    draft_dir = folder / name
    resources = draft_dir / 'Resources'
    resources.mkdir(exist_ok=True)
    assets=[(ROOT/'public/audio/soft-transition.wav','transition.wav')]
    if not smoke:
        assets += [(ROOT/'out/jianying-plate.mp4','plate.mp4'),(ROOT/'public/audio/morning-piano.wav','piano.wav')]
    else:
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(ROOT/'out/jianying-plate.mp4'),'-t','2','-an','-c:v','libx264','-threads','2','-crf','23',str(resources/'plate.mp4')],check=True)
    for src, dst in assets:
        shutil.copy2(src, resources/dst)
    script.append_track(d.TrackSpec(d.TrackType.video, name='01 · Cảnh (kéo, đổi thứ tự, đổi tốc độ)'))
    plate = d.VideoMaterial(str(resources/'plate.mp4'))
    shots = DATA['SHOTS'][:1] if smoke else DATA['SHOTS']
    for shot in shots:
        f0, f1 = shot['from'], shot['from'] + shot['duration']
        if smoke: f0, f1 = 0, 48
        script.add_segment(d.VideoSegment(plate, interval(f0,f1), source_timerange=interval(f0,f1), volume=0), '01 · Cảnh (kéo, đổi thứ tự, đổi tốc độ)')
    text_tracks = set()
    native_rows = []
    def text(shot, field, value, left, top, size, bold=False, color='brown', delay=0, background=None):
        if not value: return
        track = f'Chữ · {field}'
        if track not in text_tracks:
            script.append_track(d.TrackSpec(d.TrackType.text, name=track))
            text_tracks.add(track)
        f0=shot['from']+delay
        f1=shot['from']+shot['duration']
        font=ImageFont.truetype(str(ROOT/'public'/('NotoSans-Bold.ttf' if bold else 'NotoSans-Regular.ttf')), size)
        width=font.getlength(value)
        cx=left+width/2
        # Approximate native type placement. User can choose Noto Sans and fine-tune.
        cy=top+size*.70
        segment=d.TextSegment(value, interval(f0,f1),
            style=d.TextStyle(size=size/19.2, bold=bold, color=rgb(color), align=0),
            clip_settings=d.ClipSettings(transform_x=(cx-540)/540, transform_y=(960-cy)/960),
            background=d.TextBackground(color=background, round_radius=.5, width=.12,height=.16) if background else None)
        segment.add_animation(d.TextIntro.渐显, us(18 if shot['id']=='hook' else 34))
        segment.add_animation(d.TextOutro.渐隐, us(10))
        script.add_segment(segment, track)
        # pyJianYingDraft 0.3.1 creates a speed reference on TextSegment but
        # does not register it (unlike audio/video). Keep that reference valid.
        script.materials.speeds.append(segment.speed)
        native_rows.append({'shot':shot['id'],'field':field,'text':value,'from':f0,'to':f1,'x':left,'y':top,'font_px':size})
    def lines(shot, field, value, x, y, size, line_height, **kw):
        for i,line in enumerate(value.split('\n')):
            text(shot,f'{field} {i+1}',line,x,y+i*size*line_height,size,**kw)
    if smoke:
        text({'id':'test','from':0,'duration':48},'Kiểm tra','Thử sửa chữ tiếng Việt',76,1200,64,True)
    else:
        for s in shots:
            if s['id']=='hook':
                text(s,'Dòng nhỏ',s['tag'],78,1103,32,True,delay=2)
                text(s,'Tiêu đề 1','5',72,1153,112,True,'rose')
                text(s,'Tiêu đề 2','thực phẩm',168,1153,112,True)
                lines(s,'Lợi ích',s['benefit'],76,1325,84,1.23,bold=True,delay=4)
                text(s,'Lưu ý 1',s['safety'],78,1580,37,color='muted',delay=8)
            elif s['id']=='safe':
                text(s,'Tiêu đề 1',s['title'],76,966,78,True)
                text(s,'Tiêu đề 2',s['benefit'],76,1063.5,78,True)
                for i,value in enumerate(['Ăn đa dạng, đủ chất','Nấu chín thực phẩm','Vitamin bầu: theo bác sĩ']):
                    text(s,f'Nhắc nhở {i+1}',f'0{i+1}  {value}',78,1237+i*97,46,delay=10)
                text(s,'Lưu ý 1',s['safety'],78,1542,35,color='muted',delay=12)
            elif s['id']=='cta':
                text(s,'Dòng nhỏ','DINH DƯỠNG MẸ BẦU · 01',76,314,33,True,'rose')
                lines(s,'Tiêu đề',s['title'],76,440,96,1.28,bold=True,delay=2)
                lines(s,'Lợi ích',s['benefit'],76,875,49,1.55,color='sage',delay=6)
                lines(s,'Lưu ý',s['safety'],106,1192,40,1.6,delay=8,background='#F1E3D3')
                text(s,'Website','mombite.ai',76,1470,48,True,'sage',delay=10)
            else:
                text(s,'Dòng nhỏ',f"0{s['number']} / 05",76,1094,30,True,'rose')
                text(s,'Tiêu đề 1',s['title'],72,1140,79 if s['id']=='dairy' else 96,True,delay=2)
                text(s,'Dưỡng chất',s['tag'],105,1298,37,True,'#FFF9F1',delay=5,background='#51634B')
                lines(s,'Lợi ích',s['benefit'],76,1398,51,1.45,delay=8)
                lines(s,'Lưu ý',s['safety'],78,1600,40,1.5,color='muted',delay=12)
    if not smoke:
        script.append_track(d.TrackSpec(d.TrackType.audio,name='Nhạc nền piano · thay hoặc xóa'))
        piano=d.AudioMaterial(str(resources/'piano.wav'))
        script.add_segment(d.AudioSegment(piano,interval(0,TOTAL),volume=.65),'Nhạc nền piano · thay hoặc xóa')
    script.append_track(d.TrackSpec(d.TrackType.audio,name='Âm chuyển cảnh'))
    transition=d.AudioMaterial(str(resources/'transition.wav'))
    cues=[{'from':12,'duration':16,'volume':.12}] if smoke else DATA['SFX']
    for cue in cues:
        rng=interval(cue['from'],cue['from']+cue['duration'])
        script.add_segment(d.AudioSegment(transition,rng,volume=cue['volume']), 'Âm chuyển cảnh')
    script.save()
    content=json.loads((draft_dir/'draft_content.json').read_text())
    for group in ('videos','audios'):
        for material in content['materials'].get(group,[]):
            material['path']='Resources/'+Path(material['path']).name
    # No cloud-machine identifiers or paths are distributed.
    for key in ('platform','last_modified_platform'):
        content[key]={**content.get(key,{}),'os':'windows','app_version':'5.9.0','device_id':'','hard_disk_id':'','mac_address':''}
    write(draft_dir/'draft_content.json',content)
    meta=json.loads((draft_dir/'draft_meta_info.json').read_text())
    meta.update(draft_name=name,draft_id=str(uuid.uuid4()).upper(),tm_duration=content['duration'],draft_fold_path='',draft_root_path='',draft_cover='draft_cover.jpg')
    write(draft_dir/'draft_meta_info.json',meta)
    write(draft_dir/'editable-text.json',native_rows)
    cover_src=ROOT/'out/mombite-01.mp4'
    if not cover_src.is_file():cover_src=ROOT/'deliverables/mombite-01.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(cover_src),'-ss','3','-frames:v','1',str(draft_dir/'draft_cover.jpg')],check=True)
    return draft_dir

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    shutil.copytree(ROOT/'jianying',OUT,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    (OUT/'Fonts').mkdir(exist_ok=True)
    for name in ['NotoSans-Regular.ttf','NotoSans-Bold.ttf']:
        shutil.copy2(ROOT/'public'/name,OUT/'Fonts'/name)
    shutil.copy2(ROOT/'docs/OFL-NotoSans.txt',OUT/'Fonts/OFL-NotoSans.txt')
    for name in ['loi-thoai.txt','mombite-01.vi.srt']:
        source=ROOT/'out'/name
        if not source.is_file():source=ROOT/'deliverables'/name
        shutil.copy2(source,OUT/name)
    shutil.copy2(ROOT/'out/jianying-timeline.json',OUT/'jianying-timeline.json')
    shutil.copy2(ROOT/'docs/jianying-review.txt',OUT/'REVIEW.txt')
    for smoke in [False,True]:
        p=build(smoke)
        print('Built',p)
