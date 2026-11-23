"""md -> docx 转换（宋体正文/黑体标题，实训文档规范）"""
import re, sys
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn

def set_font(run, name_cn, size, bold=False, color=None):
    run.font.name = 'Times New Roman'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name_cn)
    run.font.size = Pt(size)
    run.font.bold = bold
    if color: run.font.color.rgb = RGBColor(*color)

def add_table(doc, headers, rows):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.style = 'Table Grid'
    for i, h in enumerate(headers):
        cell = tbl.rows[0].cells[i]
        cell.text = ''
        r = cell.paragraphs[0].add_run(h)
        set_font(r, '黑体', 10.5, bold=True)
    for row in rows:
        cells = tbl.add_row().cells
        for i, v in enumerate(row):
            if i < len(cells):
                cells[i].text = ''
                r = cells[i].paragraphs[0].add_run(v)
                set_font(r, '宋体', 10.5)

def convert(md_path, docx_path, title):
    lines = open(md_path, encoding='utf-8').read().splitlines()
    doc = Document()
    # 标题
    h = doc.add_paragraph(); h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_font(h.add_run(title), '黑体', 18, bold=True)
    doc.add_paragraph()

    i, in_table, t_headers, t_rows = 0, False, [], []
    def flush_table():
        nonlocal in_table, t_headers, t_rows
        if t_headers:
            add_table(doc, t_headers, t_rows)
            doc.add_paragraph()
        in_table, t_headers, t_rows = False, [], []

    while i < len(lines):
        line = lines[i]
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if all(re.fullmatch(r':?-{2,}:?', c) for c in cells):
                i += 1; continue
            if not in_table:
                in_table, t_headers = True, cells
            else:
                t_rows.append(cells)
            i += 1; continue
        else:
            if in_table: flush_table()
        if not line.strip():
            i += 1; continue
        if line.startswith('# '):
            continue  # 主标题已单独处理
        m = re.match(r'^(#{2,4}) (.*)', line)
        if m:
            level = len(m.group(1))  # ##->1, ###->2, ####->3
            p = doc.add_heading('', level=level)
            set_font(p.add_run(m.group(2)), '黑体', {1:15, 2:13, 3:12}[level], bold=True,
                     color=(0x1F,0x3B,0x5C))
        elif line.startswith('- ') or line.startswith('* '):
            p = doc.add_paragraph(style='List Bullet')
            set_font(p.add_run(line[2:]), '宋体', 12)
        elif re.match(r'^\d+\. ', line):
            p = doc.add_paragraph(style='List Number')
            set_font(p.add_run(re.sub(r'^\d+\. ', '', line)), '宋体', 12)
        elif line.startswith('```'):
            # 代码块
            i += 1; code = []
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i]); i += 1
            p = doc.add_paragraph()
            set_font(p.add_run('\n'.join(code)), '宋体', 9, color=(0x33,0x33,0x33))
        else:
            p = doc.add_paragraph()
            pf = p.paragraph_format
            pf.first_line_indent = Pt(24)
            pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
            set_font(p.add_run(line), '宋体', 12)
        i += 1
    if in_table: flush_table()
    doc.save(docx_path)
    print('saved', docx_path)

if __name__ == '__main__':
    convert(sys.argv[1], sys.argv[2], sys.argv[3])
