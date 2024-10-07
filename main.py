import os
import argparse
from datetime import datetime, timedelta

import dateparser
from fpdf import FPDF


def main(date_start, date_end, hour_interval, save_path):
    # Text color (90% gray)
    color_text = (26, 26, 26)
    # Bg color for weekend shading (10% gray)
    color_weekend_bg = (230, 230, 230)
    # Lighter color for grid ruling lines (30% gray)
    color_ruling = (179, 179, 179)
    # Page background (white)
    color_page_bg = (255, 255, 255)

    # x, y for daily day number (e.g. 31)
    daily_day_num = (19.00169, 4.48600)
    # x, y for separator line in header
    daily_header_sep = (30.00166, 6.80812)
    # x, y for daily day name (e.g. Monday)
    #daily_day_name = (34.251140, 6.91612)
    daily_day_name = (daily_header_sep[0] + 3, 6.91612)
    # x, y for daily month name (e.g. June)
    #daily_month_name = (34.251140, 14.34300)
    daily_month_name = (daily_header_sep[0] + 3, 14.34300)
    # x, y for daily hour rulings (e.g. 01-23)
    daily_hour_num = (13.50161, 81.62400)
    # x, y for top right corner of grid
    grid_start = (8.00233, 22.62500)

    # Dumb fix for text y position not matching my Inkscape draft
    # exactly. Need to correct the render position by a fixed value from
    # guess-and-check. This is probably a quirk with inkscape and doesn't
    # need to be NASA precise anyway.
    fix_font_y_pos = {
        42: 1.1,
        22: -1.2,
        16: -1,
        14: -1,
    }

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
    # Iterate the days to make blank month pages. This also creates
    # page links for the daily view.
    for i in range(date_days):
        date = (date_start + timedelta(days=i)).strftime('%F')
        m = (date_start + timedelta(days=i)).strftime('%B')
        if not month == m:
            pdf.add_page()
            link_id = pdf.add_link()
            pdf.set_link(link_id)
            month = m

            # Separator line
            pdf.set_draw_color(color_text)
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
            pdf.set_text_color(color_text)

            width = pdf.get_string_width(text)
            pdf.set_xy(40.5, 6.8)
            pdf.cell(width, 14, text=text, align='R')

            # Month number
            text = (date_start + timedelta(days=i)).strftime('%m')

            pdf.set_font(font_family, font_style, 22)
            pdf.set_text_color(color_text)

            width = pdf.get_string_width(text)
            pdf.set_xy(35.2-(4+width), 8.6)
            pdf.cell(width, 5.25, text=text, align='L')

            # Year
            text = (date_start + timedelta(days=i)).strftime('%Y')

            pdf.set_font(font_family, font_style, 16)
            pdf.set_text_color(color_text)

            width = pdf.get_string_width(text)
            pdf.set_xy(35.2-(4+width), 15.2)
            pdf.cell(width, 5.75, text=text, align='L')

            # Weekend shading
            pdf.set_xy(146.72143, 23.27580)
            pdf.set_fill_color(color_weekend_bg)
            pdf.rect(146.72143, 23.27580, 55.64, 126.50, style='F')

            # Horizontal grid lines
            for x in range(6):
                pdf.set_draw_color(color_text)
                pdf.set_line_width(0.5)
                pdf.line(
                    7.65,
                    23.27580 + 25.3*x,
                    202.3,
                    23.27 + 25.3*x,
                )
            # Vertical grid lines
            for x in range(8):
                pdf.set_draw_color(color_text)
                pdf.set_line_width(0.5)
                pdf.line(
                    7.6 + (27.82*x),
                    23.3,
                    7.62500 + (27.82*x),
                    149.75,
                )

        date_links[date] = {}
        date_links[date][m] = link_id

    # Make daily view. This also makes page links for the monthly view.
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
            x_off = 100.497

        # Month day
        pdf.set_font(font_family, font_style, 42)
        pdf.set_text_color(color_text)

        date = (date_start + timedelta(days=i)).strftime('%F')
        text = (date_start + timedelta(days=i)).strftime('%d')
        width = pdf.get_string_width(text)

        date_links[date][text] = link_id

        x, y = daily_day_num
        pdf.set_xy((x + x_off) - (width / 2), y + fix_font_y_pos[42])
        pdf.cell(width, text=text, align='C')

        # Week name
        pdf.set_font(font_family, font_style, 22)
        pdf.set_text_color(color_text)

        text = (date_start + timedelta(days=i)).strftime('%A').upper()
        width = pdf.get_string_width(text)

        x, y = daily_day_name
        pdf.set_xy((x + x_off), y + fix_font_y_pos[22])
        pdf.cell(width, text=text, align='C')

        # Month name
        pdf.set_font(font_family, font_style, 16)
        pdf.set_text_color(color_text)

        date = (date_start + timedelta(days=i)).strftime('%F')
        text = (date_start + timedelta(days=i)).strftime('%B')
        width = pdf.get_string_width(text)

        link = date_links[date][text]

        x, y = daily_month_name
        pdf.set_xy((x + x_off), y + fix_font_y_pos[16])
        pdf.cell(width, text=text, align='C', link=link)

        # Separator line
        pdf.set_draw_color(color_text)
        pdf.set_line_width(0.5)

        x, y = daily_header_sep
        # 13mm long
        pdf.line(
            x + x_off,
            y,
            x + x_off,
            y + 13,
        )

        # Grid
        pdf.set_draw_color(color_ruling)
        pdf.set_line_width(0.25)

        # Horizontal grid lines
        x, y = grid_start
        for n in range(24):
            pdf.line(
                x + x_off,
                y + 5.5 * n,
                x + 5.5 * 17 + x_off,
                y + 5.5 * n,
            )
        # Vertical grid lines
        for n in range(18):
            if n == 2:
                # Make the third line bold for styling.
                pdf.set_draw_color(color_text)
                pdf.set_line_width(0.5)
                pdf.line(
                    x + 5.5 * n + x_off,
                    y + (0.5 / 2) - (0.25 / 2),
                    x + 5.5 * n + x_off,
                    y + 5.5 * 23 + (0.5 / 2) - (0.25 / 2),
                )
            else:
                pdf.set_draw_color(color_ruling)
                pdf.set_line_width(0.25)
                pdf.line(
                    x + 5.5 * n + x_off,
                    y,
                    x + 5.5 * n + x_off,
                    y + 5.5 * 23,
                )

        # Noon marker
        x, y = daily_hour_num
        pdf.set_font(font_family, font_style, 14)
        # Fill the hour cell and add a border so the hour is seperated
        # from the ruling lines.
        pdf.set_line_width(1)
        pdf.set_draw_color(color_page_bg)
        pdf.set_fill_color(color_page_bg)
        pdf.set_text_color(color_text)
        for n in list(range(0, 24, hour_interval))[1:]:
            text = str(n)
            width = pdf.get_string_width(text)

            pdf.set_xy((x + x_off) - (width / 2), y + fix_font_y_pos[14])
            pdf.cell(width, text=text, align='C', fill=True, border=1)

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
    # Add month numbers with links.
    for i in range(date_days):
        date = (date_start + timedelta(days=i)).strftime('%F')
        m = (date_start + timedelta(days=i)).strftime('%B')
        text = (date_start + timedelta(days=i)).strftime('%d')
        week_name = (date_start + timedelta(days=i)).strftime('%A')

        # Set proper start of the month.
        if not month == m:
            # Don't append dates before the date range to avoid key
            # errors.
            if page > 0:
                for c in range(35 - (x + y*7)):
                    pdf.set_xy(10 + x*x_off + c*x_off, 24.3 + y*y_off)
                    # Use lighter ruling color when filling in leftover
                    # spaces with preview of next month dates.
                    pdf.set_text_color(color_ruling)
                    pdf.set_font(font_family, font_style, 14)

                    d = (date_start + timedelta(days=i+c)).strftime('%F')
                    t = (date_start + timedelta(days=i+c)).strftime('%d')

                    link = date_links[d][t]

                    width = pdf.get_string_width(t)
                    pdf.cell(width, 5, text=t, align='C', link=link)

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

            # Prepend leading dates
            if page > 1:
                for c in range(x, 0, -1):
                    pdf.set_xy(10 + (x-c)*x_off, 24.3)
                    pdf.set_text_color(color_ruling)
                    pdf.set_font(font_family, font_style, 14)

                    d = (date_start + timedelta(days=i))
                    t = (d - timedelta(days=c)).strftime('%d')

                    d = (d - timedelta(days=c)).strftime('%F')
                    link = date_links[d][t]

                    width = pdf.get_string_width(t)
                    pdf.cell(width, 5, text=t, align='C', link=link)

        if x > 0 and x % 7 == 0:
            x = 0
            y += 1
        if y > 4:
            continue

        pdf.set_text_color(color_text)
        pdf.set_font(font_family, font_style, 14)

        link = date_links[date][text]

        width = pdf.get_string_width(text)
        pdf.set_xy(10 + x*x_off, 24.3 + y*y_off)
        pdf.cell(width, 5, text=text, align='C', link=link)

        x += 1

    # Save
    pdf.output(save_path)


if __name__ == '__main__':
    # Set default interval as string.
    start_date = f'{datetime.today().year}-01-01'
    end_date = f'{datetime.today().year + 1}-02-01'
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
    parser.add_argument('--hour-interval', default='12')
    parser.add_argument('--out', default=save_path)

    args = parser.parse_args()
    # Convert user input date string to datetime obj
    start_date = dateparser.parse(args.start_date)
    end_date = dateparser.parse(args.end_date)
    hour_interval = int(args.hour_interval)
    save_path = args.out

    main(start_date, end_date, hour_interval, save_path)
