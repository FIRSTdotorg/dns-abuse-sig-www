"""Integration checks: editable input, unchanged source and stable same-tool output."""
import hashlib
import importlib.util
import os
from pathlib import Path
import shutil
import tempfile
import time
import unittest
from zipfile import ZipFile
from lxml import etree as ET
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('docx_pdf', ROOT/'matrix/scripts/build_docx_pdf.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

class DocxPdfIntegration(unittest.TestCase):
    def test_source_edit_and_repeatability(self):
        source = ROOT/'matrix/source/DNS-Abuse-Techniques-Matrix.docx'
        original_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        soffice = os.environ.get('SOFFICE') or shutil.which('soffice')
        self.assertTrue(soffice, 'LibreOffice is required for integration tests')
        with tempfile.TemporaryDirectory(prefix='matrix-test-') as temporary:
            work = Path(temporary)
            first, second, edited = [work/name for name in ('first.pdf', 'second.pdf', 'edited.pdf')]
            builder.render(source, first, soffice)
            time.sleep(1.1)  # Catch creation-time metadata that differs between builds.
            builder.render(source, second, soffice)
            self.assertEqual(first.read_bytes(), second.read_bytes(), 'Same-tool builds must be deterministic')
            self.assertNotIn('/CreationDate', PdfReader(first).metadata)
            self.assertEqual(len(PdfReader(first).pages), 22)
            changed = work/'changed.docx'
            with ZipFile(source) as original, ZipFile(changed, 'w') as output:
                for info in original.infolist():
                    data = original.read(info.filename)
                    if info.filename == 'word/document.xml':
                        xml = ET.fromstring(data)
                        text = next(xml.iter(builder.W+'t'))
                        self.assertEqual(text.text, 'DNS Abuse Techniques Matrix')
                        text.text = 'DNS Abuse Techniques Report'
                        data = ET.tostring(xml, encoding='UTF-8', xml_declaration=True, standalone=True)
                    output.writestr(info, data)
            builder.render(changed, edited, soffice)
            self.assertNotEqual(first.read_bytes(), edited.read_bytes())
            self.assertIn('DNS Abuse Techniques Report', PdfReader(edited).pages[0].extract_text())
            self.assertEqual(len(PdfReader(edited).pages), 22)
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), original_hash)

if __name__ == '__main__':
    unittest.main()
