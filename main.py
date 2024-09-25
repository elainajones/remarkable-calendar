import os
import argparse
import timedelta
from datetime import datetime

import dateparser
from fpdf import FPDF
from pypdf import PdfReader, PdfWriter, PaperSize
from pypdf.annotations import FreeText



def main(date_start, date_end, save_path):
    script_path = os.path.realpath(__file__)

    date_days = (date_end - date_start).days
    template = os.path.join(
        os.path.dirname(script_path),
        'res',
        'template.pdf'
    )
    fname = os.path.join(
        os.path.dirname(script_path),
        'res',
        'GentiumPlus-6.200',
        'GentiumPlus-Regular.ttf'
    )

    pdf = FPDF()
    pdf.add_font(
        family='Gentium Plus',
        style='',
        fname=fname,
    )
    reader = PdfReader(template)
    writer = PdfWriter()

    template = reader.pages[0]

    # for i in range(1, date_days):
    #     writer.add_page(template)
    writer.add_page(template)

    i = 0
    calendar = FreeText(
        text=(date_start + timedelta(days=i)).strftime('%d'),
        font='Gentium Plus',
        font_size='52pt',
        font_color='333333ff',
    )


    with open(save_path, 'wb') as f:
        pdf.write(f)


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
    parser.add_argument('--out', default=save_path)

    args = parser.parse_args()
    # Convert user input date string to datetime obj
    start_date = dateparser.parse(args.start_date)
    end_date = dateparser.parse(args.end_date)
    save_path = args.out

    main(start_date, end_date, save_path)
