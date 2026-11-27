"""Unit tests for the Markdown/CSV to DOCX template bridge."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from zipfile import ZipFile

from lxml import etree as ET

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "matrix/scripts"
sys.path.insert(0, str(SCRIPTS))
import fill_docx_template as filler  # noqa: E402

W = filler.W
R = filler.R
PKG = filler.PKG


def text(node: ET._Element) -> str:
    return "".join(item.text or "" for item in node.iter(W + "t"))


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def document_xml(path: Path) -> ET._Element:
    with ZipFile(path) as archive:
        return ET.fromstring(archive.read("word/document.xml"))


def relationships(path: Path) -> ET._Element:
    with ZipFile(path) as archive:
        return ET.fromstring(archive.read("word/_rels/document.xml.rels"))


def paragraphs(document: ET._Element) -> list[ET._Element]:
    return list(document.iter(W + "p"))


def matrix_cell(document: ET._Element, action: str, technique: str, stakeholder: str) -> ET._Element:
    for table in document.iter(W + "tbl"):
        rows = table.findall(W + "tr")
        if not rows or not rows[0].findall(W + "tc"):
            continue
        headers = rows[0].findall(W + "tc")
        if text(headers[0]).strip().casefold() != action.casefold():
            continue
        stakeholder_index = next(
            (index for index, cell in enumerate(headers)
             if text(cell).strip().casefold() == stakeholder.casefold()),
            None,
        )
        if stakeholder_index is None:
            continue
        for row in rows[1:]:
            cells = row.findall(W + "tc")
            if cells and text(cells[0]).strip().casefold() == technique.casefold():
                return cells[stakeholder_index]
    raise AssertionError(f"Could not find {action}/{technique}/{stakeholder} matrix cell")


def rel_target_by_id(rels: ET._Element, relation_id: str) -> str | None:
    for relation in rels:
        if relation.get("Id") == relation_id:
            return relation.get("Target")
    return None


class FillTemplateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="matrix-fill-test-")
        self.addCleanup(self.temporary.cleanup)
        self.work = Path(self.temporary.name)
        self.matrix = self.work / "matrix"
        self.copy_fixture()
        self.template = ROOT / "matrix/templates/DNS-Abuse-Techniques-Matrix.docx"

    def copy_fixture(self) -> None:
        self.matrix.mkdir(parents=True)
        for name in ("content", "data", "assets"):
            shutil.copytree(ROOT / "matrix" / name, self.matrix / name)
        shutil.copy2(ROOT / "matrix/report.json", self.matrix / "report.json")
        stable_labels = {
            "actions.csv": {"detect": "Detection"},
            "techniques.csv": {"dga-domains": "DGA domains"},
            "stakeholders.csv": {
                "registrars": "Registrars",
                "domain-registrants": "Domain Registrants",
            },
        }
        id_columns = {
            "actions.csv": "action",
            "techniques.csv": "technique_id",
            "stakeholders.csv": "stakeholder_id",
        }
        for filename, labels in stable_labels.items():
            path = self.matrix / "data" / filename
            rows = read_rows(path)
            for row in rows:
                if row[id_columns[filename]] in labels:
                    row["label"] = labels[row[id_columns[filename]]]
            write_rows(path, rows)

    def fill(self, template: Path | None = None) -> Path:
        output = self.work / "filled.docx"
        filler.fill(template or self.template, output, self.matrix)
        return output

    def test_prose_insertion_replaces_and_removes_template_text(self) -> None:
        chapter = self.matrix / "content/01-introduction.md"
        chapter.write_text("## Introduction\n\nInserted source prose canary.\n", encoding="utf-8")

        output = self.fill()
        body_text = text(document_xml(output))

        self.assertIn("Inserted source prose canary.", body_text)
        self.assertNotIn("This report from the", body_text)

    def test_csv_note_and_capability_control_matching_matrix_cell(self) -> None:
        path = self.matrix / "data/matrix.csv"
        rows = read_rows(path)
        target = next(row for row in rows if row["action"] == "detect"
                      and row["technique_id"] == "dga-domains"
                      and row["stakeholder_id"] == "registrars")
        target["capability"] = "no"
        target["note"] = "edited note canary"
        write_rows(path, rows)

        output = self.fill()
        cell = matrix_cell(document_xml(output), "Detection", "DGA domains", "Registrars")

        self.assertIn("edited note canary", text(cell))
        embeds = [blip.get(R + "embed") for blip in cell.iter()
                  if blip.tag.endswith("blip")]
        self.assertIn("rId45", embeds)
        self.assertNotIn("rId44", embeds)

    def test_new_csv_note_uses_template_cell_font(self):
        path=self.matrix/"data/matrix.csv"
        rows=read_rows(path)
        target=next(r for r in rows if (r['action'],r['technique_id'],r['stakeholder_id'])==('detect','dga-domains','network-operators'))
        target.update(capability='yes',note='New source note')
        write_rows(path,rows)
        cell=matrix_cell(document_xml(self.fill()),'Detection','DGA domains','Network Operators')
        run=next(r for r in cell.iter(W+'r') if 'New source note' in text(r))
        self.assertEqual(run.find(W+'rPr/'+W+'sz').get(W+'val'),'12')

    def test_na_note_is_icon_free_but_yes_capability_has_yes_icon(self) -> None:
        path = self.matrix / "data/matrix.csv"
        rows = read_rows(path)
        target = next(row for row in rows if row["action"] == "detect"
                      and row["technique_id"] == "dga-domains"
                      and row["stakeholder_id"] == "domain-registrants")
        target.update(capability="no",note="N/A (source fixture)")
        write_rows(path,rows)

        no_output = self.fill()
        no_cell = matrix_cell(document_xml(no_output), "Detection", "DGA domains", "Domain Registrants")
        no_embeds = [item.get(R + "embed") for item in no_cell.iter()
                     if item.tag.endswith("blip")]
        self.assertEqual(no_embeds, [])
        self.assertIn("N/A", text(no_cell))

        target["capability"] = "yes"
        write_rows(path, rows)
        yes_output = self.work / "yes.docx"
        filler.fill(self.template, yes_output, self.matrix)
        yes_cell = matrix_cell(document_xml(yes_output), "Detection", "DGA domains", "Domain Registrants")
        yes_embeds = [item.get(R + "embed") for item in yes_cell.iter()
                      if item.tag.endswith("blip")]
        self.assertIn("rId44", yes_embeds)
        self.assertNotIn("rId45", yes_embeds)

    def test_changed_link_target_uses_new_relationship_not_old_target(self) -> None:
        chapter = self.matrix / "content/03-examples-of-techniques.md"
        old = "https://example.org/old-source-link"
        new = "https://example.org/new-source-link"
        source = chapter.read_text(encoding="utf-8") + f"\nA [source label](<{old}>) for this fixture.\n"
        chapter.write_text(source.replace(old,new),encoding="utf-8")

        output = self.fill()
        document = document_xml(output)
        rels = relationships(output)
        used_ids = {link.get(R + "id") for link in document.iter(W + "hyperlink")}
        used_targets = {rel_target_by_id(rels, relation_id) for relation_id in used_ids}

        self.assertIn(new, used_targets)
        self.assertNotIn(old, used_targets)

    def test_metadata_and_csv_definitions_render_into_document(self) -> None:
        metadata_path = self.matrix / "report.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata.update(title="Matrix title canary", history_heading="History heading canary",
                        history_columns=["Column one canary", "Column two canary", "Column three canary"],
                        website="https://example.org/metadata-site-canary")
        metadata_path.write_text(json.dumps(metadata), encoding="utf-8")

        techniques_path = self.matrix / "data/techniques.csv"
        techniques = read_rows(techniques_path)
        technique = next(row for row in techniques if row["technique_id"] == "dga-domains")
        technique.update(label="DGA label canary", description="DGA description canary")
        write_rows(techniques_path, techniques)

        actions_path = self.matrix / "data/actions.csv"
        actions = read_rows(actions_path)
        detect = next(row for row in actions if row["action"] == "detect")
        detect.update(label="Detect action label canary", description="Action description canary")
        write_rows(actions_path, actions)

        output = self.fill()
        document = document_xml(output)
        all_text = text(document)
        self.assertIn("Matrix title canary", all_text)
        self.assertIn("History heading canary", all_text)
        self.assertIn("Column one canary", all_text)
        self.assertIn("Column two canary", all_text)
        self.assertIn("Column three canary", all_text)
        self.assertIn("DGA label canary", all_text)
        self.assertIn("DGA description canary", all_text)
        self.assertIn("Detect action label canary", all_text)
        self.assertIn("Action description canary", all_text)

        with ZipFile(output) as archive:
            member_names = archive.namelist()
            header_footer_links = set()
            for member in member_names:
                if not re.fullmatch(r"word/(header|footer)\d+\.xml", member):
                    continue
                link_tree = ET.fromstring(archive.read(member))
                rel_member = f"word/_rels/{Path(member).name}.rels"
                if rel_member not in member_names:
                    self.assertFalse(list(link_tree.iter(W+"hyperlink")))
                    continue
                rel_tree = ET.fromstring(archive.read(rel_member))
                rel_map = {item.get("Id"): item.get("Target") for item in rel_tree}
                for link in link_tree.iter(W + "hyperlink"):
                    relation_id = link.get(R + "id")
                    if relation_id:
                        header_footer_links.add(rel_map.get(relation_id))
        self.assertIn(metadata["website"], header_footer_links)

    def test_source_ordered_list_start_is_preserved_as_decimal_numbering(self) -> None:
        chapter = self.matrix / "content/06-acknowledgements.md"
        chapter.write_text(
            "## Acknowledgements\n\n3. First source number canary.\n4. Second source number canary.\n",
            encoding="utf-8",
        )

        output = self.fill()
        document = document_xml(output)
        source_paragraphs = {text(paragraph): paragraph for paragraph in paragraphs(document)
                             if "source number canary" in text(paragraph)}
        self.assertEqual(set(source_paragraphs), {
            "First source number canary.", "Second source number canary."
        })
        num_ids = []
        for paragraph in source_paragraphs.values():
            num_id = paragraph.find(W + "pPr/" + W + "numPr/" + W + "numId")
            self.assertIsNotNone(num_id)
            num_ids.append(num_id.get(W + "val"))
        self.assertEqual(len(set(num_ids)), 1)

        with ZipFile(output) as archive:
            numbering = ET.fromstring(archive.read("word/numbering.xml"))
        number = next(item for item in numbering.findall(W + "num") if item.get(W + "numId") == num_ids[0])
        override = number.find(W + "lvlOverride/" + W + "startOverride")
        self.assertIsNotNone(override)
        self.assertEqual(override.get(W + "val"), "3")
        abstract_id = number.find(W + "abstractNumId").get(W + "val")
        abstract = numbering.find(f'{W}abstractNum[@{W}abstractNumId="{abstract_id}"]')
        level = abstract.find(f'{W}lvl[@{W}ilvl="0"]')
        self.assertEqual(level.find(W + "numFmt").get(W + "val"), "decimal")

    def test_all_authored_assets_propagate_and_drawing_ids_are_unique(self) -> None:
        from PIL import Image
        for index,asset in enumerate(sorted((self.matrix/'assets').glob('*.png'))):
            image=Image.open(asset).convert('RGB')
            image.putpixel((0,0),(index+10,index+30,index+50))
            image.save(asset)
        output = self.fill()
        expected = {
            "capability-yes.png": "word/media/image1.png",
            "capability-no.png": "word/media/image2.png",
            "header.png": "word/media/image3.png",
            "header-large.png": "word/media/image4.png",
            "header-portrait.png": "word/media/image9.png",
        }
        with ZipFile(output) as archive:
            for asset, member in expected.items():
                with self.subTest(asset=asset):
                    self.assertEqual(archive.read(member), (self.matrix / "assets" / asset).read_bytes())

            docpr_ids = []
            cnvpr_ids = []
            for member in archive.namelist():
                if member.endswith(".xml"):
                    tree = ET.fromstring(archive.read(member))
                    docpr_ids.extend(node.get("id") for node in tree.xpath("//*[local-name()='docPr']"))
                    cnvpr_ids.extend(node.get("id") for node in tree.xpath("//*[local-name()='cNvPr']"))
        self.assertEqual(len(docpr_ids), len(set(docpr_ids)))
        self.assertEqual(len(cnvpr_ids), len(set(cnvpr_ids)))

    def test_key_icons_survive_neighbouring_source_insertions(self):
        chapter=self.matrix/'content/05-abuse-matrices.md'
        original=chapter.read_text()
        for before in (True,False):
            with self.subTest(before=before):
                if before:
                    authored=original.replace('Yes:','A new source explanation before the key.\n\nYes:',1)
                else:
                    authored=original.replace('\n- **DGAs**','\nA new source explanation after the key.\n\n- **DGAs**',1)
                chapter.write_text(authored)
                document=document_xml(self.fill())
                key_paragraph=next(p for p in document.iter(W+'p') if 'detect / mitigate / prevent the threat' in text(p))
                self.assertEqual(len(list(key_paragraph.iter(W+'drawing'))),2)

    def test_unknown_csv_field_is_rejected_instead_of_ignored(self):
        path=self.matrix/'data/actions.csv'
        rows=read_rows(path)
        for row in rows: row['unmapped_field']='Must not be silently ignored'
        write_rows(path,rows)
        with self.assertRaisesRegex(ValueError,'expected columns'):
            self.fill()

    def test_missing_csv_definition_include_fails(self) -> None:
        chapter = self.matrix / "content/02-terms.md"
        source = chapter.read_text(encoding="utf-8")
        marker = re.search(r"\{\{technique:dga-domains(?:\|[^}]+)?\}\}",source).group()
        self.assertIn(marker, source)
        chapter.write_text(source.replace(marker, "Removed definition include."), encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "Definitions missing from Terms"):
            self.fill()

    def test_corrupted_template_chapter_text_does_not_leak(self) -> None:
        corrupted = self.work / "corrupted-template.docx"
        canary = "TEMPLATE_BODY_CORRUPTION_CANARY"
        with ZipFile(self.template) as original, ZipFile(corrupted, "w") as output:
            for info in original.infolist():
                data = original.read(info.filename)
                if info.filename == "word/document.xml":
                    document = ET.fromstring(data)
                    paragraphs = list(document.iter(W + "p"))
                    intro_index = next(i for i, paragraph in enumerate(paragraphs)
                                       if text(paragraph).strip() == "Introduction")
                    target = next(paragraph for paragraph in paragraphs[intro_index + 1:]
                                  if text(paragraph).strip())
                    first_text = next(target.iter(W + "t"))
                    first_text.text = canary
                    data = ET.tostring(document, xml_declaration=True, encoding="UTF-8", standalone=True)
                output.writestr(info, data)

        result = self.fill(corrupted)
        self.assertNotIn(canary, text(document_xml(result)))

    def test_template_hash_is_unchanged_after_fill(self) -> None:
        before = hashlib.sha256(self.template.read_bytes()).hexdigest()

        self.fill()

        after = hashlib.sha256(self.template.read_bytes()).hexdigest()
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
