import os
from fpdf import FPDF

script_path = os.path.realpath(__file__)

fix_font_y_pos = {
    22: -1.2,
    16: -1,
    42: 1.1,
}

font_file = os.path.join(
    os.path.dirname(script_path),
    'res',
    'GentiumPlus-6.200',
    'GentiumPlus-Regular.ttf'
)
font_family = 'Gentium Plus'
font_style = ''

pdf = FPDF('P', 'mm', 'A4')
pdf.add_font(family=font_family, style=font_style, fname=font_file)

pdf.add_page()

pdf.set_font(font_family, font_style, 22)
pdf.set_xy(33.65895, 6.86112+fix_font_y_pos[22])

text = 'MONDAY'
width = pdf.get_string_width(text)

pdf.cell(width, text=text, align='C', center=False)

pdf.set_font(font_family, font_style, 16)
pdf.set_xy(33.65895, 14.28800+fix_font_y_pos[16])

text = 'January'
width = pdf.get_string_width(text)

pdf.cell(width, text=text, align='C', center=False)


pdf.set_font(font_family, font_style, 42)
pdf.set_xy(11.59348, 4.427+fix_font_y_pos[42])

text = '23'
width = pdf.get_string_width(text)

pdf.cell(width, text=text, align='C', center=False)

box_size=5.5
box_count=1
x = 6
y = 22.56688
line_width = 0.25
pdf.set_draw_color(26, 26, 26)
pdf.set_line_width(line_width)
pdf.line(
    x,
    y,
    x,
    y+ box_size * box_count,
)
pdf.line(
    x,
    y,
    x+ box_size * box_count,
    y,
)
pdf.line(
    x+box_size * box_count,
    y,
    x+box_size * box_count,
    y+ box_size * box_count,
)
pdf.line(
    x,
    y+ box_size * box_count,
    x+ box_size * box_count,
    y + box_size * box_count,
)
pdf.output('foo.pdf')
