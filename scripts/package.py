from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
root=Path(__file__).resolve().parents[1]
target=root/'out/mombite-du-an.zip'
files=[]
for d in ['src','public','docs','scripts','jianying']:
 files.extend(p for p in (root/d).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
for f in ['.gitignore','.node-version','.python-version','requirements.txt','package.json','package-lock.json','tsconfig.json','remotion.config.ts','README.md','capture-style.cjs']:
 files.append(root/f)
with ZipFile(target,'w',compression=ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:
  z.write(p,Path('mombite-video')/p.relative_to(root))
with ZipFile(target) as z:
 assert z.testzip() is None
print(target, target.stat().st_size, 'bytes;',len(files),'files verified')
