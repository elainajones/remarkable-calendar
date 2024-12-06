import os
import csv
import argparse
from datetime import datetime, timedelta

import dateparser
from fpdf import FPDF


def main(
    date_start: str,
    date_end: str,
    hour_interval: int,
    save_path: str,
    week_start: str = 'monday',
    handedness=None,
    margin_links=False,
    date_file=None,
) -> None:
    if not handedness:
        toolbar = 0
    elif handedness.lower() == 'left':
        toolbar = -5
        toolbar_links = (210 - 12, 15.624 - 5.5/2)
    elif handedness.lower() == 'right':
        toolbar = 5
        toolbar_links = (12, 15.624 - 5.5/2)

    # Text color (90% gray)
    color_text = (26, 26, 26)
    # Text color (50% gray)
    color_text_light = (
        color_text[0] + 127,
        color_text[1] + 127,
        color_text[2] + 127,
    )
    # Bg color for weekend shading (10% gray)
    color_weekend_bg = (230, 230, 230)
    # Lighter color for grid ruling lines (30% gray)
    color_ruling = (179, 179, 179)
    # Page background (white)
    color_page_bg = (255, 255, 255)
    color_event_bg = (205, 205, 205)

    # x, y for top right corner of grid
    grid_start = (8.002, 22.62500)

    # x, y for separator line in header
    daily_header_sep = (toolbar + 30.00166, 6.80812)
    # x, y for daily day number (e.g. 31)
    daily_day_num = (toolbar + 19.00169, 4.48600)
    # x, y for daily day name (e.g. Monday)
    daily_day_name = (daily_header_sep[0] + 3, 6.91612)
    # x, y for daily month name (e.g. June)
    daily_month_name = (daily_header_sep[0] + 3, 14.34300)
    # x, y for daily hour rulings (e.g. 01-23)
    daily_hour_num = (toolbar + 13.50161, 15.624)
    # x, y for event description.
    daily_day_event = (
        toolbar + grid_start[0] + (5.5 * 3.5),
        grid_start[1] + 5.5 - 1.8
    )

    # x, y for separator line in header
    monthly_header_sep = (toolbar + 35.7142, 6.80812)
    # x, y for monthly month name (e.g. June)
    monthly_month_name = (monthly_header_sep[0] + 4, 4.48600)
    # x, y for monthly month number (e.g. 06)
    monthly_month_num = (monthly_header_sep[0] - 3, 6.91612)
    # x, y for year (e.g. 2024)
    monthly_year = (monthly_header_sep[0] - 3, 14.34300)
    # x, y for monthly day number (e.g. 31)
    monthly_day_num = (toolbar + grid_start[0] + 3, grid_start[1] + 3)
    monthly_day_event = (toolbar + grid_start[0], grid_start[1] + 8)

    # Dumb fix for text y position not matching my Inkscape draft
    # exactly. Need to correct the render position by a fixed value from
    # guess-and-check. This is probably a quirk with inkscape and doesn't
    # need to be NASA precise anyway.
    fix_font_y_pos = {
        42: 1.1,
        22: -1.2,
        16: -1,
        14: -1,
        10: +.32,
        12: +0.3,
        8: +.25,
    }

    week = [
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday',
    ]
    week_start = week_start.lower()
    # Reorder based on preferred start of the week.
    week = [*week[week.index(week_start):], *week[:week.index(week_start)]]
    date_days = (date_end - date_start).days
    script_path = os.path.realpath(__file__)

    important_dates = {}
    if os.path.exists(date_file):
        with open(date_file, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[0] not in important_dates.keys():
                    important_dates[row[0]] = [row[1:]]
                else:
                    important_dates[row[0]].append(row[1:])
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
    pdf.set_font(font_family, font_style, 42)

    # eg: {'2024-10-27' : {'10': month_link, '27': day_link}}
    date_links = {}
    # eg: [('2024-10', link)]
    month_links = []

    last_month = None
    link_id = None
    # Iterate the days to make blank month pages. This also creates
    # page links for the daily view.
    for i in range(date_days):
        date = date_start + timedelta(days=i)
        month = date.strftime('%B')
        if not last_month == month:
            # New month, make page.
            pdf.add_page()

            link_id = pdf.add_link()
            pdf.set_link(link_id)
            last_month = month

            # Separator line
            pdf.set_draw_color(color_text)
            pdf.set_line_width(0.5)

            x, y = monthly_header_sep
            # 13mm long
            pdf.line(
                x,
                y,
                x,
                y + 13,
            )

            # Month name
            pdf.set_font_size(42)
            pdf.set_text_color(color_text)

            text = date.strftime('%B')
            width = pdf.get_string_width(text)

            x, y = monthly_month_name
            pdf.set_xy(x, y + fix_font_y_pos[42])
            pdf.cell(width, text=text, align='C')

            # Month number
            pdf.set_font_size(22)
            pdf.set_text_color(color_text)

            text = date.strftime('%m')
            width = pdf.get_string_width(text)

            x, y = monthly_month_num
            pdf.set_xy(x - width, y + fix_font_y_pos[22])
            pdf.cell(width, text=text, align='C')

            # Year
            pdf.set_font_size(16)
            pdf.set_text_color(color_text)

            text = date.strftime('%Y')
            width = pdf.get_string_width(text)

            x, y = monthly_year
            pdf.set_xy(x - width, y + fix_font_y_pos[16])
            pdf.cell(width, text=text, align='C')

            # Weekend shading
            x, y = grid_start
            pdf.set_xy(x + ((210 - 2 * x) / 7) * 5 + toolbar, y)
            pdf.set_fill_color(color_weekend_bg)

            pdf.rect(
                x+((210-2*x)/7)*week.index('saturday')+toolbar, y,
                ((210-2*x)/7)*1, 149.12500-y,
                style='F'
            )
            pdf.rect(
                x+((210-2*x)/7)*week.index('sunday')+toolbar, y,
                ((210-2*x)/7)*1, 149.12500-y,
                style='F'
            )

            month_links.append((date, link_id))

        date_links[date.strftime('%F')] = {}
        date_links[date.strftime('%F')][month] = link_id

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
        pdf.set_font_size(42)
        pdf.set_text_color(color_text)

        date = date_start + timedelta(days=i)
        text = date.strftime('%d')
        width = pdf.get_string_width(text)

        date_links[date.strftime('%F')][text] = link_id

        x, y = daily_day_num
        pdf.set_xy((x + x_off) - (width / 2), y + fix_font_y_pos[42])
        pdf.cell(width, text=text, align='C')

        # Week name
        pdf.set_font_size(22)
        pdf.set_text_color(color_text)

        text = date.strftime('%A').upper()
        width = pdf.get_string_width(text)

        x, y = daily_day_name
        pdf.set_xy((x + x_off), y + fix_font_y_pos[22])
        pdf.cell(width, text=text, align='C')

        # Month name
        pdf.set_font_size(16)
        pdf.set_text_color(color_text)

        text = date.strftime('%B')
        width = pdf.get_string_width(text)

        link = date_links[date.strftime('%F')][text]

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
                x + x_off + toolbar,
                y + 5.5 * n,
                x + 5.5 * 17 + x_off + toolbar,
                y + 5.5 * n,
            )
        # Vertical grid lines
        for n in range(18):
            if n == 2:
                # Make the third line bold for styling.
                pdf.set_draw_color(color_text)
                pdf.set_line_width(0.5)
                pdf.line(
                    x + 5.5 * n + x_off + toolbar,
                    y + (0.5 / 2) - (0.25 / 2),
                    x + 5.5 * n + x_off + toolbar,
                    y + 5.5 * 23 - ((0.5 / 2) - (0.25 / 2)),
                )
            else:
                pdf.set_draw_color(color_ruling)
                pdf.set_line_width(0.25)
                pdf.line(
                    x + 5.5 * n + x_off + toolbar,
                    y,
                    x + 5.5 * n + x_off + toolbar,
                    y + 5.5 * 23,
                )

        # Hour labels
        x, y = daily_hour_num
        pdf.set_font_size(14)
        # Fill the hour cell and add a border so the hour is seperated
        # from the ruling lines.
        pdf.set_line_width(1)
        pdf.set_draw_color(color_page_bg)
        pdf.set_fill_color(color_page_bg)
        pdf.set_text_color(color_text)
        for n in list(range(0, 24, hour_interval))[1:]:
            text = str(n)
            width = pdf.get_string_width(text)

            pdf.set_xy(
                (x + x_off) - (width / 2),
                y + (5.5 * n) + fix_font_y_pos[14]
            )
            pdf.cell(width, text=text, align='C', fill=True, border=1)

        # Add event description.
        event = date.strftime('%m-%d')
        event_list = important_dates.get(event, [])
        x, y = daily_day_event
        # pdf.set_font_size(12)

        for event in event_list:
            text = event[1] or event[0]
            width = pdf.get_string_width(text)

            pdf.set_xy(
                x + x_off,
                y + fix_font_y_pos[14]
            )

            if text:
                pdf.cell(width, text=text, align='C', fill=True, border=0.5)
                y += 5.5

    x, y = grid_start
    # page width is 210mm (A4) and grid extends to 149.125mm
    x_off = (210 - 2 * x) / 7
    y_off = (149.125 - y) / 5

    x, y = monthly_day_num

    page = 0
    last_month = None
    # Add month numbers with links.
    for i in range(date_days):
        pdf.set_font_size(14)
        date = (date_start + timedelta(days=i))
        month = date.strftime('%m')

        # Set proper start of the month.
        if not last_month == month:
            # New month, start from top
            last_month = month
            page += 1
            pdf.page = page

            # Counters to determine how much to shift text x and y
            # while iterating down the monthly calendar boxes.
            # x = x * a
            a = 0
            # y = y * b
            b = 0
            # Find the start of the month.
            week_name = date.strftime('%A')
            for n in week:
                if n == week_name.lower():
                    break
                # This doesn't occur (right?)
                elif a > 0 and a % 7 == 0:
                    a = 0
                    b += 1
                else:
                    a += 1

            # Only prepend dates in the date range to avoid key errors.
            if page > 1:
                # Back fill leading dates from last month up to start of
                # new month.
                for n in range(a, 0, -1):
                    pdf.set_xy(x + (a - n) * x_off, y + fix_font_y_pos[14])
                    pdf.set_text_color(color_text_light)

                    # Temporary date var
                    d = (date_start + timedelta(days=i))

                    # Temporary text var
                    t = (d - timedelta(days=n)).strftime('%d')
                    event = (d - timedelta(days=n)).strftime('%m-%d')

                    # Temporary date var (formatted)
                    d = (d - timedelta(days=n)).strftime('%F')
                    link = date_links[d][t]

                    width = pdf.get_string_width(t)
                    pdf.cell(width, text=t, align='C', link=link)

                    # Add event banner
                    event_list = important_dates.get(event, [])
                    ex, ey = monthly_day_event

                    pdf.set_font_size(10)

                    # VERY dumb bug where the font size changes to the wrong
                    # value EVEN THOUGH I SET IT. Somehow setting it to
                    # a different value makes the following change back
                    # actually persist.
                    pdf.set_fill_color(color_page_bg)
                    pdf.set_draw_color(color_page_bg)
                    for event in event_list:
                        pdf.set_fill_color(color_event_bg)
                        pdf.set_draw_color(color_event_bg)
                        pdf.set_xy(
                            ex + (a - n) * x_off,
                            ey + fix_font_y_pos[10]
                        )

                        t = event[0]
                        width = (210 - 2 * grid_start[0]) / 7
                        if int(event[-1]) and t:
                            pdf.cell(
                                width,
                                text=t,
                                align='C',
                                fill=True,
                                border=1,
                            )
                        elif not int(event[-1]) and t:
                            pdf.cell(
                                width,
                                text=' ',
                                align='C',
                                fill=True,
                                border=1,
                            )
                        ey += 4.5

                    pdf.set_font_size(14)

        if a > 0 and a % 7 == 0:
            # End of week, start new line.
            a = 0
            b += 1
        if b <= 4:
            pdf.set_text_color(color_text)

            text = date.strftime('%d')
            link = date_links[date.strftime('%F')][text]

            width = pdf.get_string_width(text)
            pdf.set_xy(x + (a * x_off), y + (b * y_off) + fix_font_y_pos[14])
            pdf.cell(width, text=text, align='C', link=link)

            # Add event banner
            event = date.strftime('%m-%d')
            event_list = important_dates.get(event, [])
            ex, ey = monthly_day_event

            pdf.set_font_size(10)

            # VERY dumb bug where the font size changes to the wrong
            # value EVEN THOUGH I SET IT. Somehow setting it to
            # a different value makes the following change back
            # actually persist.
            pdf.set_fill_color(color_page_bg)
            pdf.set_draw_color(color_page_bg)
            for event in event_list:
                pdf.set_draw_color(color_event_bg)
                pdf.set_fill_color(color_event_bg)
                pdf.set_xy(
                    ex + (a * x_off),
                    ey + (b * y_off) + fix_font_y_pos[10]
                )

                t = event[0]
                width = (210 - 2 * grid_start[0]) / 7
                if int(event[-1]) and t:
                    pdf.cell(
                        width,
                        text=t,
                        align='C',
                        fill=True,
                        border=1,
                    )
                elif not int(event[-1]) and t:
                    pdf.cell(
                        width,
                        text=' ',
                        align='C',
                        fill=True,
                        border=1,
                    )
                ey += 4.5

            pdf.set_font_size(14)
            a += 1

        d = (date_start + timedelta(days=i+1))
        m = d.strftime('%m')
        if b > 4 or not m == month:
            # No more rows or next day is a new month, skip to next month.
            # This will still be visible in the next month even if they
            # don't all fit on one page.

            # Don't append dates before the date range to avoid key
            # errors.
            if b == 3:
                # Dumb bug for Months which have 28 days
                # which fit perfectly in 3 weeks.
                a = 0
                b += 1
            if page > 0:
                for n in range(35 - (a + b * 7)):
                    # Don't ask. I forgot.
                    pdf.set_xy(
                        x + (a * x_off) + (n * x_off),
                        y + fix_font_y_pos[14] + (b * y_off)
                    )
                    # Use lighter ruling color when filling in leftover
                    # spaces with preview of next month dates.
                    pdf.set_text_color(color_text_light)
                    pdf.set_font_size(14)

                    # Temporary date var
                    d = date_start + timedelta(days=i+n+1)
                    t = d.strftime('%d')
                    link = date_links.get(d.strftime('%F'), {})
                    link = link.get(t, None)

                    width = pdf.get_string_width(t)
                    pdf.cell(width, text=t, align='C', link=link)

                    pdf.set_font_size(10)
                    # VERY dumb bug where the font color to the wrong
                    # value EVEN THOUGH I SET IT. Somehow setting it to
                    # a different value makes the following change back
                    # actually persist.
                    pdf.set_fill_color(color_page_bg)
                    pdf.set_draw_color(color_page_bg)
                    event = d.strftime('%m-%d')
                    event_list = important_dates.get(event, [])
                    ex, ey = monthly_day_event
                    for event in event_list:
                        pdf.set_fill_color(color_event_bg)
                        pdf.set_draw_color(color_event_bg)
                        pdf.set_xy(
                            ex + (a * x_off) + (n * x_off),
                            ey + fix_font_y_pos[10] + (b * y_off)
                        )

                        t = event[0]
                        width = (210 - 2 * grid_start[0]) / 7
                        if int(event[-1]) and t:
                            pdf.cell(
                                width,
                                text=t,
                                align='C',
                                fill=True,
                                border=1,
                            )
                        elif not int(event[-1]) and t:
                            pdf.cell(
                                width,
                                text=' ',
                                align='C',
                                fill=True,
                                border=1,
                            )
                        ey += 4.5

                pdf.set_font_size(14)

            # Horizontal grid lines
            pdf.set_draw_color(color_text)
            pdf.set_line_width(0.5)

            x, y = grid_start
            for n in range(6):
                # page width is 210mm (A4) and grid extends to 149.125mm
                pdf.line(
                    x + toolbar,
                    y + ((149.12500 - y) / 5) * n,
                    210 - x + toolbar,
                    y + ((149.12500 - y) / 5) * n,
                )
            # Vertical grid lines
            for n in range(8):
                # page width is 210mm (A4) and grid extends to 149.125mm
                pdf.line(
                    x + ((210 - 2 * x) / 7) * n + toolbar,
                    y,
                    x + ((210 - 2 * x) / 7) * n + toolbar,
                    149.12500,
                )
            x, y = monthly_day_num
            continue

    if margin_links and toolbar:
        i = 0
        # Embrace the recursion (I know. It's bad)
        for p in range(len(month_links)):
            pdf.page = p + 1
            # Limit range of months to 12 since this is the
            # most we can fit in the side bar.
            display_range = month_links[i: 12+i]
            # VERY dumb bug where the font size changes to the wrong
            # value EVEN THOUGH I SET IT TO BE 14. Somehow setting it to
            # a different value makes the following change back to 14
            # actually persist.
            pdf.set_font_size(12)

            # Embrace the recursion (I know)
            for d in range(len(display_range)):
                date, link = display_range[d]
                text = date.strftime('%B')
                text = text[:3]

                pdf.set_font_size(14)
                width = pdf.get_string_width(text)

                x, y = toolbar_links
                if month_links[p][0].strftime('%F') == date.strftime('%F'):
                    pdf.set_text_color(color_text)
                    link = None
                else:
                    pdf.set_text_color(color_text_light)

                if toolbar > 0:
                    # Right handed
                    pdf.set_xy(
                        x - width - 1.5,
                        y + ((5.5 * 2) * (d + 1)) + fix_font_y_pos[14]
                    )
                else:
                    # Left handed
                    pdf.set_xy(
                        x + 1.5,
                        y + ((5.5 * 2) * (d + 1)) + fix_font_y_pos[14]
                    )

                pdf.cell(width, text=text, align='C', link=link)

            if any([
                len(month_links) <= 12,
                len(month_links) == 12+i,
                p < 5,
            ]):
                pass
            else:
                i += 1

        i = 0
        n = 0
        page = pdf.page
        last_month = None
        pdf.set_font_size(14)
        for p in range(0, date_days, 2):
            date = date_start + timedelta(days=p)

            if p == 0:
                date = date + timedelta(days=1)
                page += 1
            elif p % 2 == 0:
                date = date + timedelta(days=1)
                page += 1
            else:
                continue

            pdf.page = page

            month = date.strftime('%B')
            year_month = date.strftime('%Y-%m')

            display_range = month_links[i: 12+i]

            for d in range(len(display_range)):
                date, link = display_range[d]
                # Get link for first of the month.
                # link = date_links[date.strftime('%Y-%m-01')]['01']
                text = date.strftime('%B')
                text = text[:3]
                width = pdf.get_string_width(text)

                x, y = toolbar_links
                if all([
                    year_month == date.strftime('%Y-%m'),
                ]):
                    pdf.set_text_color(color_text)
                else:
                    pdf.set_text_color(color_text_light)

                if toolbar > 0:
                    # Right handed
                    pdf.set_xy(
                        x - width - 1.5,
                        y + ((5.5 * 2) * (d + 1)) + fix_font_y_pos[14]
                    )
                else:
                    # Left handed
                    pdf.set_xy(
                        x + 1.5,
                        y + ((5.5 * 2) * (d + 1)) + fix_font_y_pos[14]
                    )

                pdf.cell(width, text=text, align='C', link=link)

            if not last_month == month:
                last_month = month
                if any([
                    len(month_links) <= 12,
                    len(month_links) == 12+i,
                    n < 5,
                ]):
                    pass
                else:
                    i += 1
                n += 1

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
    date_file = os.path.join(
        os.path.dirname(script_path),
        'dates.csv'
    )

    parser = argparse.ArgumentParser(
        description='Remarkable 2 calender creator'
    )
    parser.add_argument('--start-date', default=start_date)
    parser.add_argument('--end-date', default=end_date)
    parser.add_argument(
        '--hour-interval',
        type=int,
        default=12,
        choices=range(1, 24)
    )
    parser.add_argument(
        '--toolbar-space',
        default=False,
        choices=['left', 'right']
    )
    parser.add_argument(
        '--week-start',
        default='monday',
        choices=[
            'monday',
            'tuesday',
            'wednesday',
            'thursday',
            'friday',
            'saturday',
            'sunday',
        ]
    )
    parser.add_argument(
        '--enable-toolbar-links',
        help='Only takes effect when combined with --toolbar-space',
        action='store_true',
    )
    parser.add_argument('--out', default=save_path)
    parser.add_argument('--date-file', default=date_file)

    args = parser.parse_args()
    # Convert user input date string to datetime obj
    start_date = dateparser.parse(args.start_date)
    end_date = dateparser.parse(args.end_date)
    hour_interval = args.hour_interval
    week_start = args.week_start
    handedness = args.toolbar_space
    margin_links = args.enable_toolbar_links
    date_file = args.date_file
    save_path = args.out

    main(
        start_date,
        end_date,
        hour_interval,
        save_path,
        week_start,
        handedness,
        margin_links,
        date_file,
    )
