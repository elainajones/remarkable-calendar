import os
import argparse
from datetime import datetime, timedelta

import dateparser
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


        pdf.set_draw_color(51, 51, 51)
        pdf.set_line_width(0.5)
        pdf.line(
            29.625 + x_off,
            7.74,
            29.625 + x_off,
            20.246,
        )

        # Grid
        pdf.set_draw_color(179, 179, 179)
        pdf.set_line_width(0.25)

        for x in range(24):
            pdf.line(
                7.63 + x_off,
                23.27580 + 5.5*x,
                101.13 + x_off,
                23.27 + 5.5*x,
            )
        for x in range(18):
            if x == 2:
                pdf.set_draw_color(102, 102, 102)
                pdf.set_line_width(0.5)
                pdf.line(
                    7.62500 + (5.5*x) + x_off,
                    23.40,
                    7.62500 + (5.5*x) + x_off,
                    149.62,
                )
            else:
                pdf.set_draw_color(179, 179, 179)
                pdf.set_line_width(0.25)
                pdf.line(
                    7.62500 + (5.5*x) + x_off,
                    23.3,
                    7.62500 + (5.5*x) + x_off,
                    149.75,
                )

        # Noon marker
        pdf.set_font(font_family, font_style, 12)
        pdf.set_line_width(1)
        pdf.set_draw_color(255, 255, 255)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(77, 77, 77)

        text = '12'
        width = pdf.get_string_width(text)

        pdf.set_xy((13.13+x_off)-(width/2), 82.5)
        pdf.cell(width, 2.6, text=text, align='C', fill=True, border=1)

    # Save
    pdf.output('temp.pdf')


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
