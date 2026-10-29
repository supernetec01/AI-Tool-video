from pathlib import Path
from unittest.mock import patch
import importlib.util
import json
import tempfile
import subprocess
import sys
from PIL import Image, ImageChops
ROOT=Path(__file__).resolve().parents[1]
BUNDLE=ROOT/'out/jianying-export'
results=[]
def log(s):results.append(s);print(s)
for name,count,seconds in [('MomBite01-Editable',8,60),('MomBite01-SmokeTest',1,2)]:
 p=BUNDLE/'Drafts'/name;c=json.loads((p/'draft_content.json').read_text())
 assert c['duration']==seconds*1_000_000
 assert c['canvas_config']['width']==1080 and c['canvas_config']['height']==1920 and c['fps']==24
 v=[t for t in c['tracks'] if t['type']=='video'][0]['segments']
 assert len(v)==count
 last=0
 for s in v:
  r=s['target_timerange'];assert r['start']==last
  assert s['source_timerange']==r
  last=r['start']+r['duration']
 assert last==seconds*1_000_000
 allids={m['id'] for a in c['materials'].values() if isinstance(a,list) for m in a if isinstance(m,dict) and 'id' in m}
 for t in c['tracks']:
  end=0
  for s in t['segments']:
   assert s['material_id'] in allids
   assert all(ref in allids for ref in s.get('extra_material_refs',[]))
   r=s['target_timerange'];assert r['start']>=end and r['duration']>0
   end=r['start']+r['duration'];assert end<=c['duration']
 for k in ('videos','audios'):
  for m in c['materials'].get(k,[]):assert (p/m['path']).is_file() and not Path(m['path']).is_absolute()
 assert '/workspace/' not in (p/'draft_content.json').read_text()
 for k in ('platform','last_modified_platform'):
  assert c[k]['app_id']==3704 and c[k]['app_source']=='lv'
  assert all(not c[k].get(x) for x in ('device_id','hard_disk_id','mac_address'))
 if count==8:
  texts='\n'.join(json.loads(t['content'])['text'] for t in c['materials']['texts'])
  for s in ('Cá hồi','CHOLINE','FOLATE','SẮT','PROTEIN · I-ỐT','axit folic được khuyến nghị.','Không có món ăn nào bảo đảm tăng IQ.'):
   assert s in texts,s
  assert len(c['materials']['texts'])==52
 log(f'PASS {name}: timeline, native text, material references, safe portable paths, device-neutral metadata')
# Exact still comparison for retained photo / brand pixels (not a native-app text render).
for frame,bottom in [(81,1055),(250,1055),(650,1055),(1250,905)]:
 original_path=ROOT/f'out/qa/f{frame}.png'
 if not original_path.is_file():
  original_path=ROOT/f'out/jianying-qa/original-f{frame}.png'
 original=Image.open(original_path).convert('RGB')
 plate=Image.open(ROOT/f'out/jianying-qa/plate-f{frame}.png').convert('RGB')
 box=(0,0,1080,bottom)
 diff=ImageChops.difference(original.crop(box),plate.crop(box))
 assert not diff.getbbox(),frame
 # The editable text region must be clean cream in plate.
 region=plate.crop((70,1110,950,1710))
 assert region.getextrema()==((255,255),(245,245),(234,234)),frame
log('PASS clean plate: retained photo/brand pixels exactly match 4 original stills; native text region empty')
spec=importlib.util.spec_from_file_location('mombite_install',BUNDLE/'install.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
with tempfile.TemporaryDirectory(prefix='mombite-windows-test-') as tmp:
 root=Path(tmp)
 with patch.object(module.windows_draft,'jianying_running',return_value=False):
  first=module.install_one(draft_root=root,os_name='Windows')
  before=(first/'draft_content.json').read_bytes()
  second=module.install_one(draft_root=root,os_name='Windows')
  assert first!=second and (first/'draft_content.json').read_bytes()==before
  smoke=module.install_one(smoke=True,draft_root=root,os_name='Windows')
  assert json.loads((smoke/'draft_content.json').read_text())['duration']==2_000_000
 with patch.object(module.windows_draft,'jianying_running',return_value=True):
  try:module.install_one(draft_root=root,os_name='Windows')
  except RuntimeError:pass
  else:raise AssertionError('Running app was not blocked')
log('PASS simulated Windows filesystem flow: media rebound inside draft; duplicate install preserves first; smoke install; running-app guard')
with tempfile.TemporaryDirectory(prefix='mombite-mac-test-') as tmp:
 root=Path(tmp)
 old=root/'existing-uuid';old.mkdir();(old/'sentinel.txt').write_text('preserve existing local work')
 old_entry={'draft_name':'MomBite01-Editable','draft_fold_path':str(old)}
 (root/'root_meta_info.json').write_text(json.dumps({'all_draft_store':[old_entry]}))
 # Synthetic test fixture only, never distributed or used as an actual Mac identity.
 with patch.object(module.mac_draft,'jianying_running',return_value=False), patch.object(module.mac_draft,'_mac_platform',return_value={'os':'mac','device_id':'TEST-FIXTURE-NOT-REAL','app_version':'11.2'}):
  installed=module.install_one(draft_root=root,os_name='Darwin')
  assert (installed/'draft_info.json').is_file()
  registry=json.loads((root/'root_meta_info.json').read_text())
  assert registry['all_draft_store'][0]['draft_name']==installed.name
  assert installed.name!='MomBite01-Editable'
  assert old_entry in registry['all_draft_store']
  assert (old/'sentinel.txt').read_text()=='preserve existing local work'
  meta=json.loads((installed/'draft_meta_info.json').read_text())
  assert len(next(g for g in meta['draft_materials'] if g['type']==0)['value'])==3
  size=sum(p.stat().st_size for p in (installed/'Resources').iterdir() if p.is_file())
  assert meta['draft_timeline_materials_size_']==size
  assert registry['all_draft_store'][0]['draft_timeline_materials_size']==size
 # With no donor and no usable plaintext drafts, adapter must stop instead of inventing identity.
 with tempfile.TemporaryDirectory(prefix='mombite-mac-missing-') as missing:
  with patch.object(module.mac_draft,'jianying_running',return_value=False):
   try:module.install_one(draft_root=missing,os_name='Darwin')
   except RuntimeError:pass
   else:raise AssertionError('Missing platform identity was not blocked')
log('PASS simulated Mac filesystem flow: local platform injection/registry/media registration; missing donor fails explicitly')
log('PASS Mac registry title collision: old title in UUID folder remains registered and its contents preserved')
fake=subprocess.Popen([sys.executable,'-c','import time; time.sleep(10)','--donor','/fake/JianyingPro/draft'])
try:
 assert not module.mac_draft.jianying_running(), 'Installer arguments falsely detected as app'
finally:
 fake.terminate();fake.wait(timeout=5)
log('PASS Mac process-name guard ignores installer command-line arguments containing JianyingPro')
log('LIMIT: no actual Jianying Windows/Mac application available. Native font geometry, app opening, editing and export must be checked with the included smoke project on the recipient machine.')
(BUNDLE/'VALIDATION.txt').write_text('\n'.join(results)+'\n',encoding='utf-8')
