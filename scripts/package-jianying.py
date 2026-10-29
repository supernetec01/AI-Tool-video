from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json

root=Path(__file__).resolve().parents[1]
bundle=root/'out/jianying-export'
output=root/'out/MomBite01-Jianying.zip'
files=sorted(p for p in bundle.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and p.name!='CHECKSUMS.json')
checks={str(p.relative_to(bundle)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
(bundle/'CHECKSUMS.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
files.append(bundle/'CHECKSUMS.json')
with ZipFile(output,'w',compression=ZIP_DEFLATED,compresslevel=6) as z:
    for p in files:z.write(p,Path('MomBite01-Jianying')/p.relative_to(bundle))
with ZipFile(output) as z:
    assert z.testzip() is None
print(f'ZIP verified: {output} — {len(files)} files, {output.stat().st_size} bytes')
