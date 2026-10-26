"""Validate and package the user-facing documentation resources."""
import hashlib, json, re, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output/resources'
pdf=OUT/'Aero_Hardware_Implementation_Manual.pdf'
ppt=OUT/'Aero_System_Architecture_Presentation.pptx'
reader=PdfReader(pdf)
assert len(reader.pages)==40
assert len(list((OUT/'editable-diagrams').glob('*.mmd')))==13
with zipfile.ZipFile(ppt) as archive:
    assert archive.testzip() is None
    slides=[p for p in archive.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',p)]
    notes=[p for p in archive.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',p)]
    assert len(slides)==38 and len(notes)==38
    for name in archive.namelist():
        if name.endswith('.xml'):ET.fromstring(archive.read(name))
files=sorted(p for p in OUT.rglob('*') if p.is_file() and p.suffix!='.zip' and p.name!='manifest.json')
manifest={'date':'2026-10-26','pdf_pages':40,'slides':38,'diagrams':13,'files':[
    {'path':p.relative_to(OUT).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    for p in files]}
(OUT/'source/manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
target=OUT/'Aero_Complete_Project_Resources.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:
    for path in [*files,OUT/'source/manifest.json']:archive.write(path,path.relative_to(OUT).as_posix())
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
    for entry in manifest['files']:
        assert hashlib.sha256(archive.read(entry['path'])).hexdigest()==entry['sha256']
print(json.dumps({'pdf_pages':40,'ppt_slides':38,'ppt_notes':38,'diagrams':13,'zip_bytes':target.stat().st_size,'checks':'passed'}))
