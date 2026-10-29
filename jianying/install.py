#!/usr/bin/env python3
"""Install a device-neutral draft locally; Python standard library only.

No network, login, or fingerprint values are sent anywhere. Existing drafts are
never replaced. On Mac the bundled adapter reads a local plaintext donor only
on this computer and writes its platform metadata to the newly installed copy.
"""
import argparse
from pathlib import Path
import json
import os
import shutil
import sys
import tempfile
import uuid
import platform
import time

HERE=Path(__file__).resolve().parent
if sys.version_info < (3,10):
    raise SystemExit('Cần Python 3.10 trở lên. Hãy cập nhật Python rồi chạy lại bộ cài.')
sys.path.insert(0,str(HERE/'tools'))
import mac_draft
import windows_draft

def write(p,obj):
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')

def validate(template):
    content=json.loads((template/'draft_content.json').read_text(encoding='utf-8'))
    for kind in ('videos','audios'):
        for m in content['materials'].get(kind,[]):
            path=Path(m['path'])
            resolved=(template/path).resolve()
            if path.is_absolute() or not resolved.is_relative_to(template.resolve()):
                raise ValueError('Gói có đường dẫn tài nguyên không hợp lệ.')
            if not resolved.is_file():
                raise FileNotFoundError(f'Thiếu tài nguyên: {path}')
    for key in ('platform','last_modified_platform'):
        if any(content.get(key,{}).get(k) for k in ('device_id','hard_disk_id','mac_address')):
            raise ValueError('Gói phân phối không được chứa định danh thiết bị.')
    return content

def install_one(smoke=False,draft_root=None,donor=None,os_name=None):
    name='MomBite01-SmokeTest' if smoke else 'MomBite01-Editable'
    template=HERE/'Drafts'/name
    validate(template)
    system=os_name or platform.system()
    occupied_names=set()
    if system=='Windows':
        if windows_draft.jianying_running():
            raise RuntimeError('Hãy thoát hoàn toàn Jianying trước khi cài dự án.')
        root=Path(draft_root or windows_draft.default_draft_root()).expanduser().resolve()
    elif system=='Darwin':
        if mac_draft.jianying_running():
            raise RuntimeError('Hãy thoát hoàn toàn Jianying bằng Cmd+Q trước khi cài dự án.')
        root=Path(draft_root or mac_draft.DRAFT_ROOT).expanduser().resolve()
        mac_draft.DRAFT_ROOT=str(root)
        mac_draft.ROOT_META=str(root/'root_meta_info.json')
        # Resolve on the recipient's machine before making any installation.
        mac_draft._mac_platform(str(donor) if donor else None)
        if not Path(mac_draft.ROOT_META).is_file():
            raise FileNotFoundError('Chưa có thư viện dự án Jianying. Hãy mở ứng dụng một lần rồi thoát.')
        registry=json.loads(Path(mac_draft.ROOT_META).read_text(encoding='utf-8'))
        occupied_names.update(str(e.get('draft_name','')).casefold() for e in registry['all_draft_store'])
    else:
        raise RuntimeError('Cài đặt cần Windows hoặc macOS. Dùng --validate-only để kiểm tra gói trên Linux.')
    if not root.is_dir():
        raise FileNotFoundError('Không tìm thấy thư mục dự án. Dùng --draft-root theo Draft location trong cài đặt Jianying.')
    occupied_names.update(p.name.casefold() for p in root.iterdir())
    if name.casefold() in occupied_names:
        name += '-'+uuid.uuid4().hex[:8]
    final=(root/name).resolve()
    if final.exists():
        raise FileExistsError('Không ghi đè dự án có sẵn.')
    with tempfile.TemporaryDirectory(prefix='mombite-install-') as tmp:
        stage=Path(tmp)/name
        shutil.copytree(template,stage)
        content=json.loads((stage/'draft_content.json').read_text(encoding='utf-8'))
        for kind in ('videos','audios'):
            for m in content['materials'].get(kind,[]):
                m['path']=str(final/'Resources'/Path(m['path']).name)
        write(stage/'draft_content.json',content)
        meta=json.loads((stage/'draft_meta_info.json').read_text(encoding='utf-8'))
        actual_size=sum(p.stat().st_size for p in (stage/'Resources').iterdir() if p.is_file())
        meta.update(draft_name=name,draft_fold_path=str(final),draft_root_path=str(root),draft_cover=str(final/'draft_cover.jpg'),draft_id=str(uuid.uuid4()).upper(),tm_duration=content['duration'],draft_timeline_materials_size_=actual_size)
        for group in meta.get('draft_materials',[]):
            if group['type']==0:group['value']=mac_draft._material_records(content,int(time.time()*1_000_000))
        write(stage/'draft_meta_info.json',meta)
        if system=='Windows':
            installed=windows_draft.install(str(stage),name,str(root),bundle=False)
        else:
            info=mac_draft.macify(str(stage),name,bundle_media=False,donor_draft=str(donor) if donor else None)
            # macify sees final paths before the staged folder is moved. Measure
            # staged media instead, for accurate registry and metadata sizes.
            info['materials_size']=actual_size
            mac_meta=json.loads((stage/'draft_meta_info.json').read_text(encoding='utf-8'))
            mac_meta['draft_timeline_materials_size_']=actual_size
            write(stage/'draft_meta_info.json',mac_meta)
            mac_draft.install(str(stage),name,info)
            installed=str(final)
        installed_content=json.loads((Path(installed)/('draft_info.json' if system=='Darwin' else 'draft_content.json')).read_text(encoding='utf-8'))
        for kind in ('videos','audios'):
            for m in installed_content['materials'].get(kind,[]):
                p=Path(m['path'])
                if not p.is_file() or not p.resolve().is_relative_to(final):
                    raise RuntimeError('Tài nguyên sau cài đặt chưa hợp lệ.')
        print('Đã cài dự án:',installed)
        return Path(installed)

def main():
    parser=argparse.ArgumentParser(description='Cài dự án MomBite vào Jianying Desktop (không phải CapCut quốc tế).')
    parser.add_argument('--smoke',action='store_true',help='Cài dự án kiểm tra 2 giây trước.')
    parser.add_argument('--draft-root',help='Thư mục Draft location nếu bạn đã thay đường dẫn mặc định.')
    parser.add_argument('--donor',help='Mac: đường dẫn dự án JSON chưa mã hóa trên chính máy này.')
    parser.add_argument('--validate-only',action='store_true')
    args=parser.parse_args()
    try:
        if args.validate_only:
            for name in ['MomBite01-Editable','MomBite01-SmokeTest']:
                c=validate(HERE/'Drafts'/name)
                print('Hợp lệ:',name,'—',len(c['tracks']),'lớp;',c['duration']/1e6,'giây')
        else:
            install_one(args.smoke,args.draft_root,args.donor)
            print('Mở Jianying để kiểm tra dự án. Nếu chưa thấy, khởi động lại ứng dụng.')
    except Exception as e:
        print('Chưa cài được:',str(e),file=sys.stderr)
        return 1
    return 0

if __name__=='__main__':
    raise SystemExit(main())
