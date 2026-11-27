#!/usr/bin/env python3
"""Check v1 page geometry, links and baseline content; render all-page comparisons."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import unicodedata
import pdfplumber
from zipfile import ZipFile
from lxml import etree as E
from pypdf import PdfReader
import re
from io import BytesIO
from fill_docx_template import FILES, expand, blocks, inline, plain, read_csv, inputs
from PIL import Image, ImageChops, ImageStat, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
REFERENCE_SHA = '1a4d37aacf7903e761dd6df89cae957cb02f7ecf2cb582137fccdb1af683ee77'


def body_chars(page):
    top, bottom = (85, 783) if page.height > page.width else (65, 530)
    return Counter(character for char in page.chars if top <= char['top'] < bottom
                   for character in unicodedata.normalize('NFKC', char['text'])
                   if not character.isspace())


def compare_markers(old, new):
    """Compare all original red/green capability images in their page positions."""
    expected = [m for m in old.images if m['srcsize'] == (12, 12)]
    remaining = [m for m in new.images if m['srcsize'] == (12, 12)]
    mismatches = 0
    max_dx = max_dy = 0
    for marker in expected:
        if not remaining:
            mismatches += 1
            continue
        candidate = min(remaining, key=lambda m: abs(m['x0']-marker['x0']) + abs(m['top']-marker['top']))
        remaining.remove(candidate)
        dx, dy = abs(candidate['x0']-marker['x0']), abs(candidate['top']-marker['top'])
        max_dx, max_dy = max(max_dx, dx), max(max_dy, dy)
        def red(image):
            data = image['stream'].get_data()
            return sum(data[::3]) > sum(data[1::3])
        if red(marker) != red(candidate) or dx > 8 or dy > 20:
            mismatches += 1
    return {'count': len(expected), 'mismatches': mismatches + len(remaining),
            'max_horizontal_shift_pt': round(max_dx, 3), 'max_vertical_shift_pt': round(max_dy, 3)}


def normalize(text):
    return ''.join(unicodedata.normalize('NFKC', text).split())


def authored_expectations(matrix):
    """Read content independently of the filled Word document or its mapping."""
    data={}
    for kind,filename,identifier in [('action','actions.csv','action'),('technique','techniques.csv','technique_id'),('stakeholder','stakeholders.csv','stakeholder_id')]:
        data[kind]={r[identifier]:r for r in read_csv(matrix/'data'/filename)}
    expected,urls=[],set()
    legends=0;seen=set()
    def add(value):
        expected.append(plain(value))
        urls.update(href for _,_,_,href in inline(value) if href)
    for name,_ in FILES:
        for block in blocks(expand((matrix/'content'/name).read_text(),data,seen)):
            if block['kind']=='matrix': continue
            if name=='05-abuse-matrices.md' and block['text'].startswith('Yes:'):
                legend=re.fullmatch(r'Yes:\s*(.*?)\s+No:\s*(.*)',block['text'],re.S)
                if not legend: raise ValueError('Invalid source legend')
                legends+=1
                for value in legend.groups(): add(value.removesuffix('\\'))
            else: add(block['text'])
    matrix_rows=read_csv(matrix/'data/matrix.csv')
    for row in matrix_rows:
        if row['note']: add(row['note'])
    for kind,rows in data.items():
        for row in rows.values(): add(row['label'])
    for row in read_csv(matrix/'data/version_history.csv'):
        for value in row.values(): add(value)
    metadata=json.loads((matrix/'report.json').read_text())
    for field in ('title','subtitle','website','history_heading'): add(metadata[field])
    for label in metadata['history_columns']: add(label)
    counts=Counter({False:legends,True:legends})
    for row in matrix_rows:
        if not (row['capability']=='no' and row['note'].startswith('N/A')):
            counts[row['capability']=='no']+=1
    return expected,urls,counts


def source_coverage(actual, matrix):
    """Check canonical source text, links and yes/no values against actual PDF layers."""
    expected,urls,expected_colors=authored_expectations(matrix)
    metadata=json.loads((matrix/'report.json').read_text())
    versions=read_csv(matrix/'data/version_history.csv')
    reader=PdfReader(actual)
    text=''.join(p.extract_text() or '' for p in reader.pages)
    full=normalize(text);flow=full
    # Permit a source paragraph to continue past page furniture.
    furniture=[metadata['title'],metadata['website'],'TLP:CLEAR',
               f"Version {versions[-1]['version']} ({versions[-1]['date']})"]
    for fragment in sorted(furniture,key=len,reverse=True): flow=flow.replace(normalize(fragment),'')
    flow=re.sub(r'\d+of\d+', '', flow)
    missing=[v for v in expected if v.strip() and normalize(v) not in full and normalize(v) not in flow]
    with pdfplumber.open(actual) as pdf:
        links={link['uri'] for page in pdf.pages for link in page.hyperlinks if link.get('uri')}
        symbols=[image for page in pdf.pages for image in page.images if 3 <= image['width'] <= 12 and 3 <= image['height'] <= 12]
        actual_colors=Counter(sum(m['stream'].get_data()[::3]) > sum(m['stream'].get_data()[1::3]) for m in symbols)
    failures=[]
    if missing: failures.append('Authored source text missing from PDF: '+repr(missing[:4]))
    if urls-links: failures.append('Authored link targets missing from PDF: '+repr(sorted(urls-links)))
    if actual_colors != expected_colors: failures.append(f'Source capability symbols differ: expected {dict(expected_colors)}, found {dict(actual_colors)}')
    return failures, {'source_paragraphs':len(expected),'source_links':len(urls),'source_symbols':sum(expected_colors.values()),'source_text_missing':len(missing)}


def check(actual: Path, template: Path, reference: Path, output: Path, matrix: Path = ROOT/"matrix") -> None:
    output.mkdir(parents=True, exist_ok=True)
    if hashlib.sha256(reference.read_bytes()).hexdigest() != REFERENCE_SHA:
        raise ValueError('The immutable v1.3 reference PDF has changed')
    manifest=json.loads(actual.with_suffix('.build.json').read_text())
    if inputs(matrix) != manifest['sources'] or hashlib.sha256(template.read_bytes()).hexdigest() != manifest['template_sha256']:
        raise ValueError('Sources or template changed after the build; rerun make pdf')
    scripts=Path(__file__).parent
    current_generator=hashlib.sha256((scripts/'build_docx_pdf.py').read_bytes()+(scripts/'fill_docx_template.py').read_bytes()).hexdigest()
    if current_generator != manifest['generator_sha256']:
        raise ValueError('Generator changed after the build; rerun make pdf')
    if hashlib.sha256(actual.read_bytes()).hexdigest() != manifest['pdf_sha256']:
        raise ValueError('PDF differs from its build record')
    failures,coverage=source_coverage(actual,matrix)
    report = {'source_coverage':coverage, 'pages': [], 'failures': failures,
              'note': 'Content edits may repaginate. Every comparison requires independent review.'}
    with pdfplumber.open(reference) as original, pdfplumber.open(actual) as built:
        report['reference_pages']=len(original.pages);report['generated_pages']=len(built.pages)
        groups=[]
        for page in built.pages:
            orientation=page.height > page.width
            if not groups or groups[-1][0] != orientation: groups.append((orientation,[]))
            groups[-1][1].append(page)
        if [g[0] for g in groups] != [True,False,True]:
            failures.append('Expected portrait narrative, landscape matrices and portrait closing sections')
        index=0
        for region,(_,pages) in enumerate(groups):
            reference_range=[(0,7),(7,20),(20,22)][min(region,2)]
            for offset,new in enumerate(pages):
                number=index+1;index+=1
                ref_index=reference_range[0]+offset
                old=original.pages[min(ref_index,reference_range[1]-1)]
                item = {'page': number, 'reference_page':ref_index+1 if ref_index < reference_range[1] else None,
                        'size': [new.width, new.height],
                        'matches_original_body': body_chars(old) == body_chars(new),
                        'capability_symbols':compare_markers(old,new)}
                if abs(old.width-new.width) > 1 or abs(old.height-new.height) > 1:
                    failures.append(f'Page {number}: page size/orientation differs from v1.3')
                rules = [line for line in new.lines
                         if new.height-80 < line['top'] < new.height-35
                         and line['x1']-line['x0'] > new.width*.7 and abs(line['y1']-line['y0']) < 1]
                item['footer_rule_present']=bool(rules)
                if not rules: failures.append(f'Page {number}: footer separator missing')
                footer=new.crop((0,new.height-75,new.width,new.height)).extract_text() or ''
                counter=re.search(r'(?<!\d)(\d+)\s*of\s*(\d+)(?!\d)',footer)
                item['footer_page_number']=[int(counter[1]),int(counter[2])] if counter else None
                if item['footer_page_number'] != [number,len(built.pages)]:
                    failures.append(f'Page {number}: incorrect footer page number')
                if not body_chars(new): failures.append(f'Page {number}: no body content')
                if any(c['text'].strip() and (c['x0'] < -1 or c['x1'] > new.width+1 or c['top'] < -1 or c['bottom'] > new.height+1) for c in new.chars):
                    failures.append(f'Page {number}: text outside the page bounds')
                report['pages'].append(item)
    for name, pdf in [('reference', reference), ('generated', actual)]:
        directory = output / name
        directory.mkdir(exist_ok=True)
        subprocess.run(['pdftoppm', '-png', '-r', '100', str(pdf), str(directory / 'page')], check=True,
                       capture_output=True, timeout=180)
    for item in report['pages']:
        n = item['page']
        reference_page=item['reference_page']
        old = (Image.open(output / 'reference' / f'page-{reference_page:02d}.png').convert('RGB')
               if reference_page else Image.new('RGB',Image.open(output/'generated'/f'page-{n:02d}.png').size,'white'))
        new = Image.open(output / 'generated' / f'page-{n:02d}.png').convert('RGB')
        # Google rounds A4 dimensions; normalize the sub-point page-box difference.
        resized = new.resize(old.size, Image.Resampling.LANCZOS)
        difference = ImageChops.difference(old, resized)
        item['mean_pixel_difference'] = round(sum(ImageStat.Stat(difference).mean)/3/255, 6)
        difference.save(output / f'diff-{n:02d}.png')
        pair = Image.new('RGB', (old.width*2, old.height+30), 'white')
        pair.paste(old, (0,30)); pair.paste(resized, (old.width,30))
        ImageDraw.Draw(pair).text((10,8), f'Page {n}: v1.3 reference (left), generated from DOCX (right)', fill='black')
        pair.save(output / f'compare-{n:02d}.png')
    (output / 'layout-report.json').write_text(json.dumps(report, indent=2)+'\n')
    if failures:
        raise ValueError('\n'.join(failures))
    print('Source coverage, layout and hyperlink checks passed; review every comparison image.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pdf', type=Path, default=ROOT/'build/matrix/DNS-Abuse-Techniques-Matrix.pdf')
    p.add_argument('--matrix-dir',type=Path,default=ROOT/'matrix')
    p.add_argument('--template', type=Path, default=ROOT/'matrix/templates/DNS-Abuse-Techniques-Matrix.docx')
    p.add_argument('--reference', type=Path, default=ROOT/'DNS-Abuse-Techniques-Matrix_v1.3.pdf')
    p.add_argument('--out', type=Path, default=ROOT/'build/matrix/review')
    a = p.parse_args(); check(a.pdf, a.template, a.reference, a.out,a.matrix_dir)
if __name__ == '__main__':
    main()
