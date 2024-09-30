import os
import argparse
from datetime import datetime, timedelta

import dateparser
from fpdf import FPDF


def main(date_start, date_end, save_path):
    date_days = (date_end - date_start).days
    script_path = os.path.realpath(__file__)

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

    date_links = {}

    month = None
    link_id = None
    for i in range(date_days):
        date = (date_start + timedelta(days=i)).strftime('%F')
        m = (date_start + timedelta(days=i)).strftime('%B')
        if not month == m:
            pdf.add_page()
            link_id = pdf.add_link()
            pdf.set_link(link_id)
            month = m

            # Separator line
            pdf.set_draw_color(26, 26, 26)
            pdf.set_line_width(0.5)
            pdf.line(
                35.44223,
                7.74,
                35.44223,
                20.246,
            )

            # Month name
            text = (date_start + timedelta(days=i)).strftime('%B')

            pdf.set_font(font_family, font_style, 42)
            pdf.set_text_color(26, 26, 26)

            width = pdf.get_string_width(text)
            pdf.set_xy(35.44223+5, 7)
            pdf.cell(width, 14.25, text=text, align='R')

            # Month number
            text = (date_start + timedelta(days=i)).strftime('%m')

            pdf.set_font(font_family, font_style, 22)
            pdf.set_text_color(26, 26, 26)

            width = pdf.get_string_width(text)
            pdf.set_xy(35.44223-(4+width), 8.5)
            pdf.cell(width, 5.25, text=text, align='L')

            # Year
            text = (date_start + timedelta(days=i)).strftime('%Y')

            pdf.set_font(font_family, font_style, 16)
            pdf.set_text_color(26, 26, 26)

            width = pdf.get_string_width(text)
            pdf.set_xy(35.44223-(4+width), 15.4)
            pdf.cell(width, 5.75, text=text, align='L')

            # Weekend shading
            pdf.set_xy(146.72143, 23.27580)
            pdf.set_fill_color(230, 230, 230)
            pdf.rect(146.72143, 23.27580, 55.64, 126.50, style='F')

            # Horizontal grid lines
            for x in range(6):
                pdf.set_draw_color(26, 26, 26)
                pdf.set_line_width(0.5)
                pdf.line(
                    7.65,
                    23.27580 + 25.3*x,
                    202.3,
                    23.27 + 25.3*x,
                )
            # Vertical grid lines
            for x in range(8):
                pdf.set_draw_color(26, 26, 26)
                pdf.set_line_width(0.5)
                pdf.line(
                    7.6 + (27.82*x),
                    23.3,
                    7.62500 + (27.82*x),
                    149.75,
                )

        date_links[date] = {}
        date_links[date][m] = link_id

    for i in range(date_days):
        if i == 0:
            pdf.add_page()
            link_id = pdf.add_link()
            pdf.set_link(link_id)
            x_off = 0
        elif i % 2 == 0:
            pdf.add_page()
            link_id = pdf.add_link()
            pdf.set_link(link_id)
            x_off = 0
        else:
            x_off = 101.25884

        # Month day
        date = (date_start + timedelta(days=i)).strftime('%F')
        text = (date_start + timedelta(days=i)).strftime('%d')

        date_links[date][text] = link_id

        pdf.set_font(font_family, font_style, 48)
        pdf.set_text_color(26, 26, 26)

        width = pdf.get_string_width(text)
        pdf.set_xy((18.56500+x_off)-(width/2), 8.4)
        pdf.cell(width, 11.331, text=text, align='C')

        # Week name
        text = (date_start + timedelta(days=i)).strftime('%A').upper()

        pdf.set_font(font_family, font_style, 22)
        pdf.set_text_color(26, 26, 26)

        width = pdf.get_string_width(text)
        pdf.set_xy((33.5+x_off), 8.5)
        pdf.cell(width, 5.25, text=text, align='R')

        # Month name
        date = (date_start + timedelta(days=i)).strftime('%F')
        text = (date_start + timedelta(days=i)).strftime('%B')
        link = date_links[date][text]

        pdf.set_font(font_family, font_style, 16)
        pdf.set_text_color(26, 26, 26)

        width = pdf.get_string_width(text)
        pdf.set_xy((33.5+x_off), 15)
        pdf.cell(width, 5.75, text=text, align='R', link=link)

        # Separator line
        pdf.set_draw_color(26, 26, 26)
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

        # Horizontal grid lines
        for x in range(24):
            pdf.line(
                7.63 + x_off,
                23.27580 + 5.5*x,
                101.13 + x_off,
                23.27 + 5.5*x,
            )
        # Vertical grid lines
        for x in range(18):
            if x == 2:
                pdf.set_draw_color(26, 26, 26)
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
        pdf.set_font(font_family, font_style, 14)
        pdf.set_line_width(1)
        pdf.set_draw_color(255, 255, 255)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(26, 26, 26)

        text = '12'
        width = pdf.get_string_width(text)

        pdf.set_xy((13.13+x_off)-(width/2), 82.275)
        pdf.cell(width, 3, text=text, align='C', fill=True, border=1)

    week = [
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday'
    ]
    x_off = 27.82
    y_off = 25.30

    page = 0
    month = None
    for i in range(date_days):
        date = (date_start + timedelta(days=i)).strftime('%F')
        m = (date_start + timedelta(days=i)).strftime('%B')
        text = (date_start + timedelta(days=i)).strftime('%d')
        week_name = (date_start + timedelta(days=i)).strftime('%A')

        # Set proper start of the month.
        if not month == m:
            month = m
            page += 1
            pdf.page = page
            # New month, start from top
            x = 0
            y = 0
            for n in week:
                if n == week_name.lower():
                    break
                elif x > 0 and x % 7 == 0:
                    x = 0
                    y += 1
                else:
                    x += 1

        if x > 0 and x % 7 == 0:
            x = 0
            y += 1

        pdf.set_text_color(26, 26, 26)
        pdf.set_font(font_family, font_style, 12)

        link = date_links[date][text]

        width = pdf.get_string_width(text)
        pdf.set_xy(10 + x*x_off, 24.3 + y*y_off)
        pdf.cell(width, 5.75, text=text, align='C', link=link)

        x += 1

    # Save
    pdf.output(save_path)


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
