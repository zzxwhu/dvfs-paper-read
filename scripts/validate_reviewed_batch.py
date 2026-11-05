"""Check a reviewed batch's report, figure, equation and source integrity."""
from pathlib import Path
import argparse,json,re,sys
from import_blablapaper import _quartz_document
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--batch',default='reviewed/batch-2026-11-05.json')
args=parser.parse_args()
batch=json.loads((ROOT/args.batch).read_text(encoding='utf-8'))
reports=['ELI5_notes.md','paper_notes.md','figs_notes.md','translation_notes.md']
errors=[];n=0;images=set()
for p in batch['papers']:
    slug=p['slug'];source=ROOT/'reviewed'/slug;dest=ROOT/'content/DVFS'/slug
    info=json.loads((source/'info.json').read_text(encoding='utf-8'))
    assert info['source_sha256']==p['sha256']
    for report in reports:
        a=source/report;b=dest/report;n+=1
        if not a.is_file() or not b.is_file():errors.append(f'missing {slug}/{report}');continue
        text=a.read_text(encoding='utf-8')
        expected=_quartz_document(text,info,report,'DVFS,CPU,E902',p['sha256'])
        if expected!=b.read_text(encoding='utf-8'):errors.append(f'stale import {slug}/{report}')
        if '\ufffd' in text:errors.append(f'encoding replacement {slug}/{report}')
        for link in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text):
            if not (a.parent/link).is_file() or not (b.parent/link).is_file():errors.append(f'broken image {slug}/{link}')
            images.add((slug,link))
    main=(source/'paper_notes.md').read_text(encoding='utf-8')
    for token in ['阶段0','阶段1','阶段2','阶段3','阶段4','阶段7','阶段9','阶段11','阶段12','阶段13','论文页面','未运行']:
        if token not in main:errors.append(f'{slug} missing {token}')
    if len(list((source/'images').glob('original-*.png')))!=info['embedded_figures']:errors.append(f'{slug} crop count mismatch')
    if len(list((source/'images').glob('equation-*.png')))!=info['equations_count']:errors.append(f'{slug} equation count mismatch')
    if not (source/'evidence_record.json').is_file():errors.append(f'{slug} no evidence record')
if errors:
    print('\n'.join(errors));sys.exit(1)
assert sum(json.loads((ROOT/'reviewed'/p['slug']/'info.json').read_text(encoding='utf-8'))['embedded_figures'] for p in batch['papers'])==batch['figure_crops']
print(json.dumps(dict(status='passed',new_papers=len(batch['papers']),reports=n,unique_images=len(images),original_crops=batch['figure_crops'],equations=batch['equation_images']),ensure_ascii=True))
