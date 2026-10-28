"""Compare this editorial candidate with a released Git revision.

Run from this repository: python tools/verify_editorial_scope.py --base v1.5.9
Requires Python 3.9+ and Git; does not need Heroes III data or a VCMI runtime.
"""
from pathlib import Path
import argparse,json,subprocess
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--base',default='v1.5.9');args=parser.parse_args()
def previous(relative):
 result=subprocess.run(['git','-C',str(ROOT),'show',args.base+':'+relative],capture_output=True,check=True)
 return json.loads(result.stdout.decode('utf-8-sig'))
def current(relative):return json.loads((ROOT/relative).read_text(encoding='utf-8-sig'))
roster='Content/config/dragon-citadel/hero-roster.json';old=previous(roster);new=current(roster)
without_text=lambda obj:{key:{k:v for k,v in value.items() if k!='texts'} for key,value in obj.items()}
assert without_text(old)==without_text(new),'Hero mechanics changed'
assert set(old)==set(new) and len(new)==16
languages=['polish','english','german','chinese','japanese','russian','spanish','french'];allowed={roster};counts={}
for language in languages:
 relative=f'Content/translation/dragon-citadel/{language}.json';allowed.add(relative)
 before=previous(relative);after=current(relative);assert set(before)==set(after),'Translation keys changed'
 changes={key for key in before if before[key]!=after[key]}
 expected={f'hero.dragon-citadel.{hero}.biography' for hero in new}
 assert changes==expected,('Unexpected translation edits',language,changes.symmetric_difference(expected))
 assert len({after[key] for key in expected})==16,'Duplicate biographies'
 counts[language]=len(changes)
before=previous('mod.json');after=current('mod.json');before.pop('version');after.pop('version');assert before==after,'Non-version manifest change'
changed=subprocess.run(['git','-C',str(ROOT),'diff','--name-only',args.base,'--','Content'],capture_output=True,text=True,check=True).stdout.splitlines()
assert set(changed)==allowed,('Unexpected content files',set(changed).symmetric_difference(allowed))
print(json.dumps({'base':args.base,'heroMechanicsUnchanged':True,'mapsAndArtworkUnchanged':True,'biographiesChanged':counts,'onlyAllowedContentFilesChanged':True},indent=2))
