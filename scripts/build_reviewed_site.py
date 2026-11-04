"""Render reviewed note bundles without LLM calls or Node dependencies."""
import os,sys,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'BlaBlaPaper'))
os.environ['BLABLA_HTML_LLM_REVIEW']='false'
from src.html_exporter import export_html_reports
def main():
    count=0
    for info in sorted((ROOT/'reviewed').glob('*/info.json')):
        result=export_html_reports(str(info.parent),site_title='DVFS 论文精读',output_root=str(ROOT/'preview'))
        print(result); count+=1
    if not count: raise SystemExit('No reviewed note bundles found')
if __name__=='__main__': main()
