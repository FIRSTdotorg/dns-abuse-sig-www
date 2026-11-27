"""Rendered integration checks for the authoritative Markdown and CSV pipeline."""
import csv
import hashlib
import os
from pathlib import Path
import shutil
import sys
import tempfile
import time
import unittest
from collections import Counter
from pypdf import PdfReader
import pdfplumber

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'matrix/scripts'))
from build_docx_pdf import render
from fill_docx_template import inputs, plain
from check_pdf_layout import normalize, source_coverage


def colors(path):
    with pdfplumber.open(path) as pdf:
        return Counter(sum(m['stream'].get_data()[::3]) > sum(m['stream'].get_data()[1::3])
                       for p in pdf.pages for m in p.images if 3 <= m['width'] <= 12 and 3 <= m['height'] <= 12)


class SourcePdfIntegration(unittest.TestCase):
    def test_authored_sources_repeatability_and_template_integrity(self):
        template=ROOT/'matrix/templates/DNS-Abuse-Techniques-Matrix.docx'
        template_hash=hashlib.sha256(template.read_bytes()).hexdigest()
        soffice=os.environ.get('SOFFICE') or shutil.which('soffice')
        self.assertTrue(soffice,'LibreOffice is required for integration tests')
        with self.assertRaises(ValueError): render(template,template,'not-called')
        with tempfile.TemporaryDirectory(prefix='matrix-source-test-') as temporary:
            work=Path(temporary); source=work/'matrix';source.mkdir()
            for directory in ('content','data','assets'): shutil.copytree(ROOT/'matrix'/directory,source/directory)
            shutil.copyfile(ROOT/'matrix/report.json',source/'report.json')
            first,second,edited=[work/name for name in ('first.pdf','second.pdf','edited.pdf')]
            fixture=source/'data/matrix.csv'
            with fixture.open(newline='') as stream: fixture_rows=list(csv.DictReader(stream))
            fixture_entry=next(r for r in fixture_rows if (r['action'],r['technique_id'],r['stakeholder_id'])==('detect','dga-domains','network-operators'))
            fixture_entry.update(capability='no',note='')
            with fixture.open('w',newline='') as stream:
                writer=csv.DictWriter(stream,fieldnames=list(fixture_rows[0]));writer.writeheader();writer.writerows(fixture_rows)
            before=inputs(source)
            render(template,first,soffice,source)
            time.sleep(1.1)
            render(template,second,soffice,source)
            self.assertEqual(first.read_bytes(),second.read_bytes())
            self.assertNotIn('/CreationDate',PdfReader(first).metadata)
            sizes=[p.mediabox.height > p.mediabox.width for p in PdfReader(first).pages]
            self.assertTrue(sizes[0] and sizes[-1] and not all(sizes))
            self.assertEqual(inputs(source),before)
            with self.assertRaises(ValueError): render(template,source/'content/01-introduction.md',soffice,source)
            intro=source/'content/01-introduction.md'
            intro.write_text(intro.read_text().replace('## Introduction\n','## Introduction\n\nProseSourceProof comes from the Markdown authoring source.\n',1))
            examples=source/'content/03-examples-of-techniques.md'
            chunks=examples.read_text().strip().split('\n\n');removed=plain(chunks.pop())
            examples.write_text('\n\n'.join(chunks)+'\n')
            path=source/'data/matrix.csv'
            with path.open(newline='') as stream: rows=list(csv.DictReader(stream))
            entry=next(r for r in rows if (r['action'],r['technique_id'],r['stakeholder_id'])==('detect','dga-domains','network-operators'))
            self.assertEqual(entry['capability'],'no')
            entry.update(capability='yes',note='CsvSourceProof')
            with path.open('w',newline='') as stream:
                writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
            changed=inputs(source)
            render(template,edited,soffice,source)
            text=normalize(''.join(p.extract_text() or '' for p in PdfReader(edited).pages))
            self.assertIn('ProseSourceProof',text)
            self.assertIn('CsvSourceProof',text)
            self.assertNotIn(normalize(removed),text)
            self.assertEqual(colors(edited),colors(first)+Counter({False:1})-Counter({True:1}))
            failures,_=source_coverage(edited,source)
            self.assertEqual(failures,[])
            self.assertEqual(inputs(source),changed)
        self.assertEqual(hashlib.sha256(template.read_bytes()).hexdigest(),template_hash)

if __name__=='__main__': unittest.main()
