"""Install this repo's skill; back up any existing version before replacement."""
import argparse, json, shutil, datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--skills-dir',type=Path,default=Path.home()/'.agents'/'skills')
    p.add_argument('--corpus',type=Path,action='append',help='Optional local corpus; repeat for multiple dated corpora')
    a=p.parse_args()
    if a.corpus and any(not (c/'inventory.json').exists() for c in a.corpus): p.error('A corpus lacks inventory.json')
    source=ROOT/'skill'/'electrocatalysis-evidence'
    target=a.skills_dir/'electrocatalysis-evidence'
    if target.exists():
        stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        backup=ROOT/'backups_local'/stamp/'electrocatalysis-evidence'
        backup.parent.mkdir(parents=True,exist_ok=True)
        shutil.copytree(target,backup)
        print(f'Existing skill backed up: {backup}')
    shutil.copytree(source,target,dirs_exist_ok=True)
    (target/'references'/'library-location.md').write_text(f'# Local library location\n\nLibrary root: `{ROOT.as_posix()}`.\n\nUse this local clone for cards, analysis and scripts. Do not publish this generated location file.\n',encoding='utf-8')
    if a.corpus:
        (ROOT/'local_config.json').write_text(json.dumps({'source_corpora':[str(c.resolve()) for c in a.corpus]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Skill installed: {target}')
if __name__=='__main__': main()
