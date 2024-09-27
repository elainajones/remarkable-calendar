import os
import argparse
from datetime import datetime, timedelta

import dateparser
from PIL import ImageFont
from fpdf import FPDF


def main(date_start, date_end, save_path):
    date_days = (date_end - date_start).days

    # Paths
    script_path = os.path.realpath(__file__)
    template = os.path.join(
        os.path.dirname(script_path),
        'res',
        'template.pdf'
    )

    # Font
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

    for i in range(date_days):
        if i == 0:
            pdf.add_page()
            x_off = 0
        elif i % 2 == 0:
            pdf.add_page()
            x_off = 0
        else:
            x_off = 101.25884

        # Month day
        pdf.set_font(font_family, font_style, 52)
        pdf.set_text_color(51, 51, 51)

        text = (date_start + timedelta(days=i)).strftime('%d')
        width = pdf.get_string_width(text)

        pdf.set_xy((18.56500+x_off)-(width/2), 8.3)
        pdf.cell(width, 11.331, text=text, align='C')

        # Week name
        pdf.set_font(font_family, font_style, 22)
        pdf.set_text_color(51, 51, 51)

        text = (date_start + timedelta(days=i)).strftime('%A').upper()
        width = pdf.get_string_width(text)

        pdf.set_xy((33.5+x_off), 8.5)
        pdf.cell(width, 5.25, text=text, align='R')

        # Month name
        pdf.set_font(font_family, font_style, 16)
        pdf.set_text_color(51, 51, 51)

        text = (date_start + timedelta(days=i)).strftime('%B')
        width = pdf.get_string_width(text)

        pdf.set_xy((33.5+x_off), 15)
        pdf.cell(width, 5.75, text=text, align='R')

        # Noon marker
        pdf.set_font(font_family, font_style, 12)
        pdf.set_text_color(77, 77, 77)

        text = '12'
        width = pdf.get_string_width(text)

        pdf.set_xy((13.13+x_off)-(width/2), 82.5)
        pdf.cell(width, 2.6, text=text, align='C')

    # Save
    pdf.output('temp.pdf')



    #reader = PdfReader(template)
    #template = reader.pages[0]

    ## for i in range(1, date_days):
    ##     writer.add_page(template)
    #writer = PdfWriter()
    #writer.add_page(template)

    #i = 0
    #a = annotations.FreeText(
    #    text=
    #    rect=(50, 50, 100, 100),
    #    border_color='00000000',
    #    font='Gentium Plus',
    #    font_size='52pt',
    #    font_color='333333ff',
    #)
    #writer.add_annotation(page_number=i, annotation=a)


    #with open(save_path, 'wb') as f:
    #    writer.write(f)


if __name__ == '__main__':
    # Set default interval as string.
    start_date = f'{datetime.today().year}-01-01'
    end_date = f'{datetime.today().year + 1}-01-01'
    # Should be fine for most cases.
    script_path = os.path.realpath(__file__)
    save_path = os.path.join(
        os.path.dirname(script_path),
        'calendar.pdf'
    )

    parser = argparse.ArgumentParser(
        description='Remarkable 2 calender creator'
    )
    parser.add_argument('--start-date', default=start_date)
    parser.add_argument('--end-date', default=end_date)
    parser.add_argument('--out', default=save_path)

    args = parser.parse_args()
    # Convert user input date string to datetime obj
    start_date = dateparser.parse(args.start_date)
    end_date = dateparser.parse(args.end_date)
    save_path = args.out

    main(start_date, end_date, save_path)
