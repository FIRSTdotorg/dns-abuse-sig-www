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
from PIL import Image, ImageChops, ImageStat, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL_DOCX_SHA = '81250da695c618c5db868b49760dc15c6a14e3ebedae1e97c8de7b243a7bc968'
REFERENCE_SHA = '1a4d37aacf7903e761dd6df89cae957cb02f7ecf2cb582137fccdb1af683ee77'


def body_chars(page):
    top, bottom = (85, 783) if page.height > page.width else (65, 530)
    return Counter(character for char in page.chars if top <= char['top'] < bottom
                   for character in unicodedata.normalize('NFKC', char['text'])
                   if not character.isspace())


def check(actual: Path, source: Path, reference: Path, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    if hashlib.sha256(reference.read_bytes()).hexdigest() != REFERENCE_SHA:
        raise ValueError('The immutable v1.3 reference PDF has changed')
    baseline = hashlib.sha256(source.read_bytes()).hexdigest() == ORIGINAL_DOCX_SHA
    failures = []
    report = {'baseline_source': baseline, 'pages': [], 'failures': failures,
              'note': 'Image differences require independent visual review. A passed check does not approve publication.'}
    with pdfplumber.open(reference) as original, pdfplumber.open(actual) as built:
        if len(built.pages) != 22:
            failures.append(f'Expected 22 pages, found {len(built.pages)}')
        expected_links = {link['uri'] for page in original.pages for link in page.hyperlinks if link.get('uri')}
        actual_links = {link['uri'] for page in built.pages for link in page.hyperlinks if link.get('uri')}
        if baseline and expected_links != actual_links:
            failures.append('Baseline hyperlink targets differ from v1.3')
        for number, (old, new) in enumerate(zip(original.pages, built.pages), 1):
            item = {'page': number, 'size': [new.width, new.height],
                    'baseline_body_matches': body_chars(old) == body_chars(new)}
            if abs(old.width-new.width) > 1 or abs(old.height-new.height) > 1:
                failures.append(f'Page {number}: page size/orientation differs from v1.3')
            if baseline and not item['baseline_body_matches']:
                failures.append(f'Page {number}: baseline body content differs from v1.3')
            if not new.extract_text():
                failures.append(f'Page {number}: blank or non-extractable text')
            for char in new.chars:
                if char['text'].strip() and (char['x0'] < -1 or char['x1'] > new.width+1 or char['top'] < -1 or char['bottom'] > new.height+1):
                    failures.append(f'Page {number}: text outside the page bounds')
                    break
            report['pages'].append(item)
    for name, pdf in [('reference', reference), ('generated', actual)]:
        directory = output / name
        directory.mkdir(exist_ok=True)
        subprocess.run(['pdftoppm', '-png', '-r', '100', str(pdf), str(directory / 'page')], check=True,
                       capture_output=True, timeout=180)
    for item in report['pages']:
        n = item['page']
        old = Image.open(output / 'reference' / f'page-{n:02d}.png').convert('RGB')
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
    print('22-page layout, text and hyperlink checks passed; review every comparison image.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pdf', type=Path, default=ROOT/'build/matrix/DNS-Abuse-Techniques-Matrix.pdf')
    p.add_argument('--source', type=Path, default=ROOT/'matrix/source/DNS-Abuse-Techniques-Matrix.docx')
    p.add_argument('--reference', type=Path, default=ROOT/'DNS-Abuse-Techniques-Matrix_v1.3.pdf')
    p.add_argument('--out', type=Path, default=ROOT/'build/matrix/review')
    a = p.parse_args(); check(a.pdf, a.source, a.reference, a.out)
if __name__ == '__main__':
    main()
