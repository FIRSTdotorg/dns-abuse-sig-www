#!/usr/bin/env python3
"""Populate the v1 layout with authoritative Markdown, CSV, metadata and assets."""
from __future__ import annotations
from copy import deepcopy
import csv
from difflib import SequenceMatcher
import hashlib
import json
from pathlib import Path
import re
from zipfile import ZipFile
from lxml import etree as E
from markdown_it import MarkdownIt
from validate_matrix import validate

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
PKG = '{http://schemas.openxmlformats.org/package/2006/relationships}'
MD = MarkdownIt('commonmark', {'html': False})
FILES = [('01-introduction.md','Introduction'), ('02-terms.md','Terms'),
         ('03-examples-of-techniques.md','Examples of Techniques'),
         ('04-advice-for-incident-responders.md','Advice for Incident Responders'),
         ('05-abuse-matrices.md','Abuse Matrices'), ('06-acknowledgements.md','Acknowledgements')]
ASSETS = {'capability-yes.png':'word/media/image1.png', 'capability-no.png':'word/media/image2.png',
          'header.png':'word/media/image3.png', 'header-large.png':'word/media/image4.png',
          'header-portrait.png':'word/media/image9.png'}
ACTIONS = ['detect','mitigate','prevent']
XML_SPACE = '{http://www.w3.org/XML/1998/namespace}space'


def parse_xml(data):
    return E.fromstring(data,E.XMLParser(resolve_entities=False,no_network=True))


def visible(node):
    return ''.join(t.text or '' for t in node.iter(W+'t'))


def key(text):
    return re.sub(r'\s+', ' ', text.replace('\xa0',' ').replace('–','-')).strip()


def read_csv(path):
    with path.open(newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream))


def inputs(matrix):
    files = sorted([*(matrix/'content').glob('*.md'), *(matrix/'data').glob('*.csv'),
                    *(p for p in (matrix/'assets').iterdir() if not p.name.startswith('.')), matrix/'report.json'])
    if {p.name for p in (matrix/'content').glob('*.md')} != {name for name,_ in FILES}:
        raise ValueError('Expected the six mapped Markdown chapters; add an explicit layout mapping for new chapters')
    if {p.name for p in files if p.parent.name == 'assets'} != set(ASSETS):
        raise ValueError('Unknown or missing source asset; add an explicit template mapping')
    if {p.name for p in (matrix/'data').glob('*.csv')} != {'actions.csv','techniques.csv','stakeholders.csv','matrix.csv','version_history.csv'}:
        raise ValueError('Unknown or missing CSV source; add an explicit mapping')
    return {str(p.relative_to(matrix)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


def expand(text, data, seen):
    def include(match):
        kind, item_id, display = match.groups()
        if kind == 'action_label':
            return data['action'][item_id]['label']
        if kind == 'matrix':
            return match.group()
        if kind not in data or item_id not in data[kind]:
            raise ValueError(f'Unknown content include {match.group()}')
        identifier = kind,item_id
        if identifier in seen:
            raise ValueError(f'Duplicate definition include: {identifier}')
        seen.add(identifier)
        row = data[kind][item_id]
        return f"{display or row['label']} - {row['description']}"
    expanded = re.sub(r'\{\{(action|action_label|technique|stakeholder|matrix):([a-z0-9-]+)(?:\|([^}\n]+))?\}\}', include, text)
    if '{{' in re.sub(r'\{\{matrix:(detect|mitigate|prevent)\}\}', '', expanded):
        raise ValueError('Unresolved source include')
    return expanded


def blocks(text):
    result, lists, items = [], [], []
    serial = 0
    for token in MD.parse(text):
        if token.type in ('bullet_list_open','ordered_list_open'):
            serial += 1
            lists.append({'group':serial, 'ordered':token.type=='ordered_list_open',
                          'start':int(token.attrGet('start') or 1)})
        elif token.type in ('bullet_list_close','ordered_list_close'): lists.pop()
        elif token.type == 'list_item_open': items.append(True)
        elif token.type == 'list_item_close': items.pop()
        elif token.type in ('heading_open','paragraph_open'):
            kind = token.tag if token.type=='heading_open' else 'p'
        elif token.type == 'inline':
            marker = re.fullmatch(r'\{\{matrix:(detect|mitigate|prevent)\}\}',token.content)
            first = bool(items and items[-1])
            result.append({'kind':'matrix' if marker else kind, 'text':marker[1] if marker else token.content,
                           'list':len(lists) if first else 0, 'indent':len(lists),
                           **(lists[-1] if lists else {'group':None,'ordered':False,'start':1})})
            if items: items[-1] = False
        elif token.type not in ('heading_close','paragraph_close'):
            raise ValueError(f'Unsupported Markdown block: {token.type}. Use headings, paragraphs and lists.')
    return result


def inline(text):
    result = []
    bold = italic = False
    link = None
    for token in MD.parseInline(text)[0].children or []:
        if token.type == 'strong_open': bold = True
        elif token.type == 'strong_close': bold = False
        elif token.type == 'em_open': italic = True
        elif token.type == 'em_close': italic = False
        elif token.type == 'link_open':
            link = token.attrGet('href')
            if not re.match(r'^(https?://|mailto:)', link or ''):
                raise ValueError(f'Unsupported link target: {link}')
        elif token.type == 'link_close': link = None
        elif token.type in ('hardbreak','softbreak'):
            result.append(('\n' if token.type == 'hardbreak' else ' ', bold, italic, link))
        elif token.type in ('text','code_inline'):
            # Bare URLs remain clickable. Explicit Markdown links remove ambiguity.
            for part in re.split(r'(https?://[^\s<>]+)',token.content):
                target = part.rstrip('.,;)') if not link and part.startswith(('https://','http://')) else link
                if target and not link and len(target) < len(part):
                    result.extend([(target,bold,italic,target),(part[len(target):],bold,italic,None)])
                elif part:
                    result.append((part,bold,italic,target))
        else:
            raise ValueError(f'Unsupported inline Markdown: {token.type}')
    return result


def plain(text):
    return ''.join(part[0] for part in inline(text))


class Filler:
    def __init__(self, parts):
        self.parts = parts
        self.tree = parse_xml(parts['word/document.xml'])
        self.body = self.tree.find(W+'body')
        self.numbering = parse_xml(parts['word/numbering.xml'])
        self.drawing_id = max([0]+[int(x.get('id')) for name,value in parts.items() if name.endswith('.xml') for x in parse_xml(value).xpath('//*[local-name()="docPr"]') if x.get('id','').isdigit()])
        self.rels = parse_xml(parts['word/_rels/document.xml.rels'])
        self.hrefs = {r.get('Target'):r.get('Id') for r in self.rels if r.get('TargetMode') == 'External'}

    def relation(self, url):
        if url not in self.hrefs:
            existing = {r.get('Id') for r in self.rels}
            number = 1
            while f'rIdSource{number}' in existing: number += 1
            rid = f'rIdSource{number}'
            E.SubElement(self.rels,PKG+'Relationship',Id=rid,Target=url,TargetMode='External',
                         Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink')
            self.hrefs[url] = rid
        return self.hrefs[url]

    def paragraph(self, template, text, kind=None, list_level=None, ordered=False):
        p = deepcopy(template)
        ppr = p.find(W+'pPr')
        runs = [r for r in p.iter(W+'r') if visible(r)]
        run_properties=runs[0].find(W+'rPr') if runs else None
        if run_properties is None and ppr is not None: run_properties=ppr.find(W+'rPr')
        base=deepcopy(run_properties) if run_properties is not None else E.Element(W+'rPr')
        style = ppr.find(W+'pStyle') if ppr is not None else None
        structural = kind == 'header' or (kind is not None and kind.startswith('h') and kind != 'header') or (kind is None and style is not None and style.get(W+'val','').startswith('Heading'))
        # Heading/table-header weight belongs to the template; inline emphasis to the source.
        for child in list(base):
            if child.tag in (W+'i', W+'iCs', W+'u', W+'color', W+'rStyle') or (not structural and child.tag in (W+'b',W+'bCs')):
                base.remove(child)
        for child in list(p):
            if child.tag != W+'pPr': p.remove(child)
        if ppr is None:
            ppr = E.SubElement(p,W+'pPr')
        if kind == 'p' and style is not None and style.get(W+'val','').startswith('Heading'):
            ppr.remove(style)
        if kind and re.fullmatch('h[1-6]',kind):
            style = ppr.find(W+'pStyle')
            if style is None: style = E.SubElement(ppr,W+'pStyle')
            style.set(W+'val','Heading'+kind[1:])
        if list_level == 0:
            numbering = ppr.find(W+'numPr')
            if numbering is not None:
                ppr.remove(numbering)
                indent = ppr.find(W+'ind')
                if indent is not None: ppr.remove(indent)
        if list_level is not None and list_level:
            numbering = ppr.find(W+'numPr')
            if numbering is None:
                numbering = E.SubElement(ppr,W+'numPr')
                E.SubElement(numbering,W+'numId',{W+'val':'3' if ordered else '1'})
            depth = numbering.find(W+'ilvl')
            if depth is None: depth = E.SubElement(numbering,W+'ilvl')
            depth.set(W+'val',str(list_level-1))
        for value,bold,italic,href in inline(text):
            parent = p
            if href:
                parent = E.SubElement(p,W+'hyperlink',{R+'id':self.relation(href)})
            run = E.SubElement(parent,W+'r'); props = deepcopy(base); run.append(props)
            if bold: E.SubElement(props,W+'b',{W+'val':'1'})
            if italic: E.SubElement(props,W+'i',{W+'val':'1'})
            if href:
                E.SubElement(props,W+'color',{W+'val':'1155CC'})
                E.SubElement(props,W+'u',{W+'val':'single'})
            for n,line in enumerate(value.split('\n')):
                if n: E.SubElement(run,W+'br')
                E.SubElement(run,W+'t',{XML_SPACE:'preserve'}).text=line
        return p

    def fresh_icon(self, run, description=None):
        run = deepcopy(run)
        self.drawing_id += 1
        for properties in run.xpath('.//*[local-name()="docPr" or local-name()="cNvPr"]'):
            properties.set('id',str(self.drawing_id))
            if description is not None and E.QName(properties).localname == 'docPr': properties.set('descr',description)
        return run

    def assign_list(self, p, block, prototype, instances):
        if not block['list']:
            if block['indent']:
                properties=p.find(W+'pPr')
                for ind in list(properties.findall(W+'ind')): properties.remove(ind)
                E.SubElement(properties,W+'ind',{W+'left':str(block['indent']*360)})
            return
        old = prototype.find(W+'pPr/'+W+'numPr')
        old_id = old.find(W+'numId').get(W+'val') if old is not None else None
        old_level = old.find(W+'ilvl').get(W+'val','0') if old is not None and old.find(W+'ilvl') is not None else '0'
        candidates=[]
        for num in self.numbering.findall(W+'num'):
            abstract_id=num.find(W+'abstractNumId').get(W+'val')
            abstract=self.numbering.find(f'{W}abstractNum[@{W}abstractNumId="{abstract_id}"]')
            level=abstract.find(f'{W}lvl[@{W}ilvl="{old_level if num.get(W+"numId")==old_id else "0"}"]')
            if level is not None:
                fmt=level.find(W+'numFmt').get(W+'val')
                if (fmt != 'bullet') == block['ordered']:
                    candidates.append((num.get(W+'numId') != old_id,fmt != 'decimal' if block['ordered'] else False,abstract_id,level.get(W+'ilvl')))
        if not candidates: raise ValueError('No matching template list style')
        _,_,abstract_id,level=sorted(candidates)[0]
        if block['group'] not in instances:
            identifier=str(max(int(n.get(W+'numId')) for n in self.numbering.findall(W+'num'))+1)
            num=E.SubElement(self.numbering,W+'num',{W+'numId':identifier})
            E.SubElement(num,W+'abstractNumId',{W+'val':abstract_id})
            override=E.SubElement(num,W+'lvlOverride',{W+'ilvl':level})
            E.SubElement(override,W+'startOverride',{W+'val':str(block['start'])})
            instances[block['group']]=identifier,level
        identifier,level=instances[block['group']]
        properties=p.find(W+'pPr')
        numbering=E.SubElement(properties,W+'numPr')
        E.SubElement(numbering,W+'ilvl',{W+'val':level})
        E.SubElement(numbering,W+'numId',{W+'val':identifier})
        indent=prototype.find(W+'pPr/'+W+'ind')
        if indent is not None: properties.append(deepcopy(indent))
        else: E.SubElement(properties,W+'ind',{W+'left':str(block['list']*360),W+'hanging':'360'})

    def chapter(self, old, source):
        if not source: raise ValueError('An empty chapter is not allowed')
        # Matching chooses formatting prototypes only; no template body text survives.
        oldkeys = [key(visible(p)).casefold() for p in old]
        newkeys = [key(plain(b['text'])).casefold() for b in source]
        prototypes = {}
        for op,a,b,c,d in SequenceMatcher(None,oldkeys,newkeys,autojunk=False).get_opcodes():
            for n in range(c,d):
                if op == 'equal' or b-a == d-c:
                    prototypes[n] = old[a+n-c]
                else:
                    candidates = [p for p in old if p.find(W+'pPr/'+W+'pStyle') is None] or old
                    prototypes[n] = candidates[min(max(a-1,0),len(candidates)-1)]
        # Section properties are layout controls, independent of paragraph text.
        sections = [deepcopy(s) for p in old for s in p.findall(W+'pPr/'+W+'sectPr')]
        result, instances = [], {}
        for index,block in enumerate(source):
            if block['text'].startswith('Yes:') and len(list(prototypes[index].iter(W+'drawing'))) == 2:
                p = self.legend(prototypes[index],block['text'])
            else:
                prototype = prototypes[index]
                if block['kind']=='p' and prototype.find(W+'pPr/'+W+'pStyle') is not None:
                    prototype = next((p for p in old if p.find(W+'pPr/'+W+'pStyle') is None),prototype)
                p = self.paragraph(prototype,block['text'],block['kind'],0)
                self.assign_list(p,block,prototypes[index],instances)
            for s in p.findall(W+'pPr/'+W+'sectPr'): s.getparent().remove(s)
            result.append(p)
        for section in sections:
            result[-1].find(W+'pPr').append(section)
        return result

    def swap(self, old, new):
        position = self.body.index(old[0])
        for p in old: self.body.remove(p)
        for n,p in enumerate(new): self.body.insert(position+n,p)

    def cell(self, old, text, header=False):
        cell = deepcopy(old)
        prototype = cell.find(W+'p')
        for p in list(cell.findall(W+'p')): cell.remove(p)
        cell.append(self.paragraph(prototype,text,'header' if header else None))
        return cell

    def legend(self, old, text):
        match = re.fullmatch(r'Yes:\s*(.*?)\s+No:\s*(.*)',text, re.S)
        if not match: raise ValueError('Legend must specify both Yes: and No: source text')
        icons = [deepcopy(r) for r in old.iter(W+'r') if list(r.iter(W+'drawing'))]
        if len(icons) != 2: raise ValueError('Expected two template legend icons')
        p = self.paragraph(old,'')
        for index,(icon,value) in enumerate(zip(icons,match.groups())):
            if not index and '\nNo:' in text: value=value.removesuffix('\\')
            if index and '\nNo:' in text:
                run=E.SubElement(p,W+'r'); E.SubElement(run,W+'br')
            p.append(self.fresh_icon(icon,('Yes: ' if not index else 'No: ')+plain(value)))
            styled = self.paragraph(old,': '+value+' ')
            for run in list(styled):
                if run.tag != W+'pPr': p.append(run)
        return p

    def matrix(self, old, action, data, matrix_rows):
        table = deepcopy(old); rows = table.findall(W+'tr'); header = rows[0]
        stakeholders = list(data['stakeholder'].values()); techniques = list(data['technique'].values())
        if len(header.findall(W+'tc')) != len(stakeholders)+1:
            raise ValueError('Stakeholder count requires a reviewed column layout change')
        labels = [data['action'][action]['label']] + [r['label'] for r in stakeholders]
        for cell,label in zip(list(header.findall(W+'tc')), labels): header.replace(cell,self.cell(cell,label,True))
        icon_prototype = next(deepcopy(r) for r in old.iter(W+'r') if list(r.iter(W+'drawing')))
        for row in rows[1:]: table.remove(row)
        for n,technique in enumerate(techniques):
            row = deepcopy(rows[min(n+1,len(rows)-1)]); cells = row.findall(W+'tc')
            row.replace(cells[0],self.cell(cells[0],technique['label']))
            for cell,stakeholder in zip(cells[1:],stakeholders):
                entry = matrix_rows[action,technique['technique_id'],stakeholder['stakeholder_id']]
                note = entry['note'].strip()
                # N/A is a note presentation. A yes value always gets its check.
                na = entry['capability'] == 'no' and note.startswith('N/A')
                new = deepcopy(cell); prototype = new.find(W+'p')
                if na:
                    first,_,rest = note.partition(' ')
                    paragraph = self.paragraph(prototype,first+('  \n'+rest if rest else ''))
                else:
                    paragraph = self.paragraph(prototype,'('+note+')' if note else '')
                    icon = self.fresh_icon(icon_prototype,'Capability: '+entry['capability'])
                    for blip in icon.xpath('.//*[local-name()="blip"]'):
                        blip.set(R+'embed','rId44' if entry['capability']=='yes' else 'rId45')
                    index = 1 if paragraph.find(W+'pPr') is not None else 0
                    paragraph.insert(index,icon)
                    if note:
                        run=E.Element(W+'r'); E.SubElement(run,W+'br'); paragraph.insert(index+1,run)
                for p in list(new.findall(W+'p')): new.remove(p)
                new.append(paragraph); row.replace(cell,new)
            table.append(row)
        return table


def fill(template, destination, matrix):
    matrix = matrix.resolve()
    problems = validate(matrix)
    if problems: raise ValueError('\n'.join(problems))
    source_files = inputs(matrix)
    data = {}
    for kind, filename, identifier in [('action','actions.csv','action'), ('technique','techniques.csv','technique_id'), ('stakeholder','stakeholders.csv','stakeholder_id')]:
        data[kind] = {row[identifier]:row for row in read_csv(matrix/'data'/filename)}
    seen = set()
    chapters = {name:blocks(expand((matrix/'content'/name).read_text(),data,seen)) for name,_ in FILES}
    required = {(kind,identifier) for kind,rows in data.items() for identifier in rows}
    if seen != required: raise ValueError(f'Definitions missing from Terms: {sorted(required-seen)}')
    metadata = json.loads((matrix/'report.json').read_text())
    fields={'title','subtitle','website','language','history_heading','history_columns'}
    if set(metadata) != fields: raise ValueError('Unknown or missing report metadata field')
    if not isinstance(metadata['history_columns'],list) or len(metadata['history_columns']) != 3 or not all(isinstance(v,str) and v for v in metadata['history_columns']):
        raise ValueError('Expected three named history columns')
    with ZipFile(template) as archive:
        parts = {n:archive.read(n) for n in archive.namelist()}
        info = archive.infolist()
    builder = Filler(parts); original = list(builder.body)
    positions = {name:next(i for i,p in enumerate(original) if p.tag==W+'p' and visible(p).strip()==title) for name,title in FILES}
    stop = next(i for i,p in enumerate(original) if p.tag==W+'p' and visible(p).strip()=='Version History')
    # Fill table groups from explicit source markers, not template legends.
    abuse = chapters['05-abuse-matrices.md']
    groups = abuse[-9:]
    if [b['kind'] for b in groups] != ['h3','p','matrix']*3 or [groups[i]['text'] for i in (2,5,8)] != ACTIONS:
        raise ValueError('Abuse matrices must end with Detection/Mitigation/Prevention heading, legend and matrix includes')
    chapters['05-abuse-matrices.md'] = abuse[:-9]
    first_group = next(i for i,p in enumerate(original) if p.tag==W+'p' and visible(p).strip()=='Detection')
    rows = {(r['action'],r['technique_id'],r['stakeholder_id']):r for r in read_csv(matrix/'data/matrix.csv')}
    action_tables = builder.tree.findall('.//'+W+'tbl')[:3]
    for n,action in enumerate(ACTIONS):
        table = action_tables[n]; index = original.index(table)
        heading,legend = original[index-2:index]
        builder.body.replace(heading,builder.paragraph(heading,groups[n*3]['text'],'h3'))
        builder.body.replace(legend,builder.legend(legend,groups[n*3+1]['text']))
        builder.body.replace(table,builder.matrix(table,action,data,rows))
    for index,(name,title) in enumerate(FILES):
        start = positions[name]
        end = positions[FILES[index+1][0]] if index+1<len(FILES) else stop
        if name == '05-abuse-matrices.md': end = first_group
        # Empty section/page-break paragraphs are layout controls, not source text.
        old = [p for p in original[start:end] if p.tag==W+'p' and visible(p).strip()]
        builder.swap(old,builder.chapter(old,chapters[name]))
    for index,field in enumerate(('title','subtitle','website')):
        builder.body.replace(original[index],builder.paragraph(original[index],metadata[field]))
    # Version history belongs after acknowledgements, as in v1.3.
    history = builder.tree.findall('.//'+W+'tbl')[-1]
    builder.body.replace(original[stop],builder.paragraph(original[stop],metadata['history_heading'],'h2'))
    history_rows = history.findall(W+'tr')
    if len(metadata['history_columns']) != 3: raise ValueError('Expected three history columns')
    for cell,label in zip(list(history_rows[0].findall(W+'tc')),metadata['history_columns']):
        history_rows[0].replace(cell,builder.cell(cell,label,True))
    for row in history_rows[1:]: history.remove(row)
    versions = read_csv(matrix/'data/version_history.csv')
    for n,version in enumerate(versions):
        row = deepcopy(history_rows[min(n+1,len(history_rows)-1)])
        for cell,column in zip(list(row.findall(W+'tc')),('version','date','comment')):
            row.replace(cell,builder.cell(cell,version[column]))
        history.append(row)
    parts['word/document.xml'] = E.tostring(builder.tree,xml_declaration=True,encoding='UTF-8',standalone=True)
    parts['word/numbering.xml'] = E.tostring(builder.numbering,xml_declaration=True,encoding='UTF-8',standalone=True)
    parts['word/_rels/document.xml.rels'] = E.tostring(builder.rels,xml_declaration=True,encoding='UTF-8',standalone=True)
    # Match against original bytes, never against already replaced artwork.
    baseline_media={name:archive_bytes(template,target) for name,target in ASSETS.items()}
    for member,value in list(parts.items()):
        if member.startswith('word/media/'):
            for name,baseline in baseline_media.items():
                if value == baseline:
                    parts[member]=(matrix/'assets'/name).read_bytes()
                    break
    for member,value in list(parts.items()):
        if re.match(r'word/(header|footer)\d+\.xml$',member):
            tree=parse_xml(value)
            for p in tree.iter(W+'p'):
                texts=p.findall(W+'r/'+W+'t')
                text=''.join(t.text or '' for t in texts)
                replacement=None
                if text.startswith('Version 1.3'):
                    replacement=f"Version {versions[-1]['version']} ({versions[-1]['date']})"
                elif text.strip()=='DNS Abuse Techniques Matrix': replacement=metadata['title']
                if replacement and texts:
                    texts[0].text=replacement
                    for t in texts[1:]: t.text=''
                for link in p.findall(W+'hyperlink'):
                    texts=list(link.iter(W+'t'))
                    if texts and visible(link).strip().startswith('https://www.first.org/global/sigs/dns'):
                        texts[0].text=metadata['website']
                        for t in texts[1:]: t.text=''
                        relname='word/_rels/'+Path(member).name+'.rels'
                        relationships=parse_xml(parts[relname])
                        for relation in relationships:
                            if relation.get('Id') == link.get(R+'id'): relation.set('Target',metadata['website'])
                        parts[relname]=E.tostring(relationships,xml_declaration=True,encoding='UTF-8',standalone=True)
            if 'footer' in member:
                for node in tree.iter(W+'t'):
                    if node.text: node.text=re.sub(r'https?://[^\s]+',lambda _:metadata['website'],node.text)
            parts[member]=E.tostring(tree,xml_declaration=True,encoding='UTF-8',standalone=True)
    styles=parse_xml(parts['word/styles.xml'])
    for language in styles.iter(W+'lang'): language.set(W+'val',metadata['language'])
    parts['word/styles.xml']=E.tostring(styles,xml_declaration=True,encoding='UTF-8',standalone=True)
    # Word alternative header renditions reuse old drawing IDs. Allocate unique
    # IDs in the derived document without changing the immutable layout package.
    drawing_id=0
    for member,value in list(parts.items()):
        if not member.endswith('.xml'): continue
        tree=parse_xml(value)
        properties=tree.xpath('//*[local-name()="docPr" or local-name()="cNvPr"]')
        if properties:
            for node in properties:
                drawing_id+=1;node.set('id',str(drawing_id))
            parts[member]=E.tostring(tree,xml_declaration=True,encoding='UTF-8',standalone=True)
    with ZipFile(destination,'w') as output:
        for item in info: output.writestr(item,parts[item.filename])
    return source_files


def archive_bytes(path,member):
    with ZipFile(path) as archive: return archive.read(member)
