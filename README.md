# ReMarkable Calender

![Month view](img/remarkable_monthly.png)

![Daily view](img/remarkable_daily.png)

## Contents

- [What is this?](#what-is-this)
    - [Features](#features)
- [How do I use this?](#how-do-i-use-this)
- [Using the creation script](#using-the-creation-script)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
    - [Usage](#usage)
    - [Customization](#customization)

## What is this?

A minimal PDF calendar for the ReMarkable 2, inspired by the Hobonichi  
Techo planner. This PDF calendar is created using a script but pre-made  
calendars can be [downloaded from here](https://github.com/elainajones/remarkable-calendar/releases/latest).

### Features

- Optional PDF creation script for custom date ranges.
- Clickable dates for fast navigation!
    - From the month view, click the dates to jump to the  
      corresponding day view page.
    - From the day view, click the month name to jump to the  
      corresponding month view page.
- Hour rulings for each day.
- 1:1 scaling suitable for print.
- A4 document size (also supports US letter)
- 5.5mm grid line spacing
- [Gentium Font](https://software.sil.org/gentium/)
- Spaghetti code?

## How do I use this?

To use, simply download a copy of the PDF and upload to the Remarkable 2.  
Once uploaded, open the PDF and set the viewing for landscape mode.  
Be sure to set the page scaling to fit the screen width.

Continue reading for instructions using the code included in this repository.

## Using the creation script

### Prerequisites

- [Python3](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- Basic familiarity with Python
- Basic familiarity with running shell commands

### Setup

1. Ensure that both Git and Python3 have been installed.
2. `git clone https://github.com/elainajones/remarkable-calendar.git`
    - This will download the code locally on your machine.
3. `cd remarkable-calendar`
4. `python3 -m venv venv`
    - This will create a [Python3 virtual environment](https://docs.python.org/3/library/venv.html).
5. `.\venv\Scripts\activate`
    - `(venv)` should appear in the shell.
    - Linux users only: `. venv/bin/activate`
6. `python3 -m pip install -r requirements.txt`
    - This will install necessary dependencies.

### Usage

The simplest way to run the code is to enter the following command.  
The current year will be automatically determined from your computer's  
date settings.

```
python3 main.py
```

A calendar PDF will be saved locally as `calendar.pdf`.

### Customization

The `-h` or `--help` option can be added to the end of the command to  
show additional options.

```
python3 main.py --help
```

This includes the following options to customize the date range.

- `--start-date`
    - Human readable date with support for multiple formats
    - eg: `'2024/09/27'` or `'Sept 9, 2024'` (make sure to enclose inside `'`)
- `--end-date`
    - Human readable date with support for multiple formats
    - eg: `'2024/09/27'` or `'Sept 9, 2024'` (make sure to enclose inside `'`)

Advanced users familiar with Python can customize the font by providing  
their own font files.

### Adding Important Dates

Important dates can be added to the calendar by editing the 'dates.csv'  
file or supplying a custom path using the `--date-file` argument.

- Rows will be added in the order they are listed.
- If no Long Description is provided, the Short description will be  
  used instead.
- Short descriptions should be kept under 16 chars to avoid overlapping.
- Fixed dates
    - Month, Day, and Short Description columns need to be filled
- Non-fixed dates
    - Day must be left blank
    - Month, Week Day, Order columns need to be filled

The following is the expected structure of the `dates.csv` file,  
including examples for dates you can add. Not all columns need to to  
contain values.

|Month|Day|Week Number|Week Day|Order|Short Description|Long Description         |
|----:|--:|----------:|:-------|----:|:----------------|:------------------------|
|1    |1  |           |        |     |New Year's       |Happy New year!          |
|1    |7  |           |        |     |Example Range 1  |Example Range 1          |
|1    |8  |           |        |     |                 |Example Range 1          |
|1    |8  |           |        |     |Example Range 2  |Example Range 2          |
|1    |9  |           |        |     |                 |                         |
|1    |9  |           |        |     |Example Range 2  |Example Range 2          |
|5    |   |           |Monday  |-1   |Memorial Day     |                         |

Multiple events can be added for the same day and will be displayed in  
the same order they are added. A date range can be achieved by adding  
consecutive dates. For overlapping ranges, a blank entry can be added  
for alignment (refer to the example table above). The short description  
can be left blank for the consecutive days.

For example:

![](./img/example_date_range.png)
