#!/usr/bin/env python3
"""Render the original editable DOCX, preserving its v1 page system."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from zipfile import ZipFile
from lxml import etree as ET
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, ByteStringObject

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'matrix/source/DNS-Abuse-Techniques-Matrix.docx'
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def prepare(source: Path, destination: Path) -> None:
    """Materialize Google Docs layout values for LibreOffice in a render-only copy.

    No text, link target, image, or tracked source is changed. These small
    compatibility adjustments are measured against the original v1.3 PDF.
    """
    with ZipFile(source) as original, ZipFile(destination, 'w') as output:
        for info in original.infolist():
            data = original.read(info.filename)
            if info.filename in ('word/document.xml', 'word/styles.xml',
                                 'word/header2.xml', 'word/header3.xml', 'word/header4.xml', 'word/footer4.xml'):
                tree = ET.fromstring(data, ET.XMLParser(resolve_entities=False, no_network=True))
                if info.filename in ('word/document.xml', 'word/styles.xml'):
                    # Google applies the inherited 115% value; LO otherwise uses 100%.
                    for spacing in tree.iter(W + 'spacing'):
                        if spacing.get(W + 'lineRule') == 'auto' and spacing.get(W + 'line') is None:
                            spacing.set(W + 'line', '276')
                if info.filename == 'word/document.xml':
                    sections = list(tree.iter(W + 'sectPr'))
                    tables = tree.findall('.//' + W + 'tbl')
                    if len(sections) != 3 or len(tables) != 4:
                        raise ValueError('Unexpected document structure. Review layout compatibility rules.')
                    margin = sections[0].find(W + 'pgMar')
                    margin.set(W + 'bottom', str(int(margin.get(W + 'bottom')) + 120))
                    for link in tree.iter(W + 'hyperlink'):
                        if ''.join(link.itertext()).endswith('/authoritative-name-server-en'):
                            run = ET.Element(W + 'r')
                            ET.SubElement(run, W + 'br')
                            link.addprevious(run)
                    for table, after in zip(tables[:3], ('60', '120', '80')):
                        for spacing in table.iter(W + 'spacing'):
                            if spacing.get(W + 'after') == '120':
                                spacing.set(W + 'after', after)
                        for rule in table.iter(W + 'cantSplit'):
                            rule.set(W + 'val', '1')
                    for table in tables[:3]:
                        for cell in table.find(W + 'tr').findall(W + 'tc'):
                            if ''.join(cell.itertext()).startswith('Law Enforcement'):
                                properties = cell.find(W + 'tcPr')
                                margins = properties.find(W + 'tcMar')
                                if margins is None:
                                    margins = ET.SubElement(properties, W + 'tcMar')
                                right = margins.find(W + 'right')
                                if right is None:
                                    right = ET.SubElement(margins, W + 'right')
                                right.set(W + 'w', '90')
                                right.set(W + 'type', 'dxa')
                    # The source final footer uses cached '20 of 22'; restarting
                    # the section additionally creates a phantom even page in LO.
                    numbering = sections[2].find(W + 'pgNumType')
                    if numbering is not None:
                        sections[2].remove(numbering)
                else:
                    if 'header' in info.filename:
                        for run in tree.iter(W + 'r'):
                            text_nodes = list(run.iter(W + 't'))
                            if text_nodes and not ''.join(node.text or '' for node in text_nodes).strip():
                                for highlight in list(run.iter(W + 'highlight')):
                                    highlight.getparent().remove(highlight)
                    if info.filename == 'word/header4.xml':
                        # An obsolete off-page 1.1 shape is ignored by Google Docs.
                        for alternate in tree.xpath('//*[local-name()="AlternateContent"]'):
                            if 'Version 1.1' in ''.join(alternate.itertext()):
                                alternate.getparent().remove(alternate)
                    for fonts in tree.iter(W + 'rFonts'):
                        for key, value in list(fonts.attrib.items()):
                            if value == 'Fira Sans Light':
                                fonts.set(key, 'Fira Sans')
                            elif value == 'Open Sans SemiBold':
                                fonts.set(key, 'Open Sans')
                        if 'header' in info.filename:
                            bold = fonts.getparent().find(W + 'b')
                            if bold is not None:
                                bold.set(W + 'val', '0')
                    if 'header' in info.filename:
                        for shape in tree.xpath('//*[local-name()="bodyPr"]'):
                            shape.set('lIns', '0')
                            shape.set('wrap', 'none')
                data = ET.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
            output.writestr(info, data)


def render(source: Path, destination: Path, soffice: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    before = hashlib.sha256(source.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix='matrix-docx-') as temporary:
        work = Path(temporary)
        prepared = work / 'matrix.docx'
        prepare(source, prepared)
        fonts = work / 'fonts'
        fonts.mkdir()
        with ZipFile(source) as original:
            for name in original.namelist():
                if name.startswith('word/fonts/') and name.endswith('.ttf'):
                    (fonts / Path(name).name).write_bytes(original.read(name))
        environment = os.environ.copy()
        # LibreOffice loads DOCX embedded fonts. Fontconfig also exposes them to
        # Linux's text layout stack without installing fonts into the user's OS.
        if os.name == 'posix' and not __import__('sys').platform == 'darwin':
            config = work / 'fonts.conf'
            config.write_text(f'<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd">'
                              f'<fontconfig><include ignore_missing="yes">/etc/fonts/fonts.conf</include>'
                              f'<dir>{fonts}</dir><cachedir>{work / "font-cache"}</cachedir></fontconfig>')
            environment['FONTCONFIG_FILE'] = str(config)
        options = json.dumps({'UseTaggedPDF': {'type': 'boolean', 'value': 'true'},
                              'UseLosslessCompression': {'type': 'boolean', 'value': 'true'},
                              'ExportBookmarks': {'type': 'boolean', 'value': 'true'}})
        completed = subprocess.run([soffice, '-env:UserInstallation=' + (work / 'profile').as_uri(),
                                    '--headless', '--convert-to', 'pdf:writer_pdf_Export:' + options,
                                    '--outdir', str(work), str(prepared)],
                                   env=environment, capture_output=True, text=True, timeout=180)
        pdf = prepared.with_suffix('.pdf')
        if completed.returncode or not pdf.is_file():
            raise RuntimeError('DOCX export failed:\n' + completed.stdout + completed.stderr)
        # Remove volatile export metadata only. Page content, tags and links remain.
        writer = PdfWriter(clone_from=PdfReader(pdf))
        writer.metadata = {key: value for key, value in (writer.metadata or {}).items()
                           if key not in ('/CreationDate', '/ModDate')}
        writer.root_object.pop('/Metadata', None)
        version = subprocess.check_output([soffice, '--version'], text=True).strip()
        digest = hashlib.sha256(source.read_bytes() + Path(__file__).read_bytes() + version.encode()).digest()[:16]
        writer._ID = ArrayObject([ByteStringObject(digest), ByteStringObject(digest)])
        writer.compress_identical_objects(remove_duplicates=False, remove_unreferenced=True)
        with destination.open('wb') as stream:
            writer.write(stream)
        destination.with_suffix('.build.json').write_text(json.dumps({
            'source': str(source.relative_to(ROOT)) if source.is_relative_to(ROOT) else source.name,
            'source_sha256': before, 'renderer': version,
            'generator_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'pdf_sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
        }, indent=2) + '\n')
    if hashlib.sha256(source.read_bytes()).hexdigest() != before:
        raise RuntimeError('Source DOCX changed during build')
    print(destination)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--out', type=Path, default=ROOT / 'build/matrix/DNS-Abuse-Techniques-Matrix.pdf')
    parser.add_argument('--soffice', default=os.environ.get('SOFFICE', shutil.which('soffice')))
    args = parser.parse_args()
    if not args.soffice:
        parser.error('LibreOffice soffice is required. Set SOFFICE or add it to PATH.')
    render(args.source.resolve(), args.out.resolve(), args.soffice)

if __name__ == '__main__':
    main()
