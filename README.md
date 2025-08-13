# ReMarkable Calender

## Images

![Monthly view](img/remarkable_monthly.png)

![Daily view](img/remarkable_daily.png)

![Habit tracker](img/remarkable_habit.png)

## Contents

- [What is this?](#what-is-this)
    - [Features](#features)
- [How do I use this?](#how-do-i-use-this)
- [Customizing your calendar](#customizing-your-calendar)
    - [Using the bundled calendar creator tool](#using-the-bundled-calendar-creator-tool)
    - [Formatting options](#formatting-options)
    - [Adding custom dates](#adding-custom-dates)
- [Using the source code](#using-the-source-code)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
    - [Usage](#usage)

## What is this?

> [!TIP]
> Looking for downloads? [Downloads are under the "Assets" drop-down here](https://github.com/elainajones/remarkable-calendar/releases/latest).

This is a minimalist PDF calendar for the ReMarkable 2 inspired by the  
Hobonichi Techo planner. The included code is for creating this calendar  
but free, pre-made PDF calendars can be download from [the releases page](https://github.com/elainajones/remarkable-calendar/releases/latest).

### Features

- **Completely free and open-source!**
    - Don't mind the spaghetti code (it had to be done)
- **Filled calendar** with "real" dates.
- 24-hour grid ruling for each day (perfect for scheduling).
- Habit tracker.
- Clickable links to each section.
    - Navigating between sections is always 1 click to make the most  
      of the Remarkable 2 performance (it can be slow).
- Supports custom date ranges.
    - 1 year, 5 years, etc.
- Support for [custom holidays/dates](#adding-custom-dates).
    - Common US holidays added by default.
- Supports both left and right toolbar placements.
    - For example, generate using `--toolbar-position right` for lefties.
- Custom week start.
    - Monday start, Sunday start, Taco Tuesday start. Whatever.
- [Gentium Font](https://software.sil.org/gentium/)

## How do I use this?

To use, simply [download a copy of the PDF](https://github.com/elainajones/remarkable-calendar/releases/latest) and upload to the Remarkable 2.  
Once uploaded, open the PDF and **set the viewing for landscape mode**.  
Be sure to set the page scaling to fit the screen width.

## Customizing your calendar

Although existing calendars cannot be modified, new ones can  
be generated with the desired features to meet your needs.

Currently the following customization options are supported
- Calendar date range.
- Hour label increments in the day view.
- Toolbar position (for both left and right handed users)
- Day used as the start of the week.
- Custom dates

There are 2 methods you can use to create your customized calendar.

1. [Using the bundled calendar creator tool](#using-the-bundled-calendar-creator-tool) (Recommended) 
    - Easy to use (no need to download Python)
    - Recommended for people with limited experience with Python.
2. [Using the source code](#using-the-source-code)
    - Alternative if the bundled calendar creator tool is failing.
    - Recommended for advanced users and developers.

### Using the bundled calendar creator tool

> [!NOTE]
> Skip this step if you are [using the source code](#using-the-source-code)

> [!IMPORTANT]
> Steps assume you are using Windows. Steps are identical for Linux users  
> using the Linux version of the bundled calendar creator tool.

1. From [the releases page](https://github.com/elainajones/remarkable-calendar/releases/latest), download the appropriate calendar creator  
   tool for your operating system.
2. Download the sample [dates.csv](https://raw.githubusercontent.com/elainajones/remarkable-calendar/refs/heads/main/dates.csv) file.
    - The raw file will be shown. Click "save" or press `ctrl+s` on your  
      keyboard.
3. From the start menu, type "PowerShell" and click the first option.
4. Find the downloaded calendar creator tool (usually under `Downloads/`)
5. In the PowerShell windows, enter the command  
  ` .\Downloads\calendar-creator-win64.exe --out Downloads\calendar.pdf`
    - A calendar PDF named `calendar.pdf` will be created inside your  
      Downloads folder.

Once you have successfully completed the above steps, you are ready to  
customize formatting or add your own dates by simply changing the  
command arguments in step 5.

### Formatting options

> [!NOTE]
> If you are [using the source code](#using-the-source-code), use the  
> python command from the [Usage](#usage) section instead.

The `-h` or `--help` option can be added to the end of the command to  
show additional options.

```ps1
.\Downloads\calendar-creator-win64.exe --help
```

This includes the following options to customize the calendar.

- `--toolbar-position OPTION`
    - `OPTION` should be either `left` (default) or `right` (lefty mode).
- `--start-date`
    - Human readable date with support for multiple formats
    - eg: `"2024/09/27"` or `"Sept 9, 2024"` (make sure to enclose inside `"`)
- `--end-date`
    - Human readable date with support for multiple formats
    - eg: `"2024/09/27"` or `"Sept 9, 2024"` (make sure to enclose inside `"`)


For example, to create a left-handed calendar for the year 2025, the  
following command will be used.

```ps1
.\Downloads\calendar-creator-win64.exe --toolbar-position right --start-date "2025/01/01" --end-date "2026/01/01" --out Downloads\calendar.pdf
```

### Adding custom dates

Custom dates can be added to the calendar by editing the `dates.csv`  
file or supplying a custom path using the `--date-file` argument.  
The file `dates.csv` will contain examples you can use as reference.

If you're [using the bundled calendar creator tool](#using-the-bundled-calendar-creator-tool) and have downloaded  
the sample [dates.csv](https://raw.githubusercontent.com/elainajones/remarkable-calendar/refs/heads/main/dates.csv) file, refer to the following command to create  
a calendar with dates.

```ps1
.\Downloads\calendar-creator-win64.exe --date-file Downloads\dates.csv --out Downloads\calendar.pdf
```

You can modify `dates.csv` using Microsoft Excel (or similar), following  
the steps below.

- Dates are processed in the same order they are provided in `dates.csv`.
- If no "Long Description" is provided, the "Short description" will be  
  used instead.
- "Short Descriptions" should be kept under 16 chars for best results.
    - A longer description can still be added as the "Long Description".
- Fixed dates (any event that falls on the same day of the month).
    - "Order" MUST be left blank.
    - "Month", "Day", and "Short Description" columns MUST be filled.
- Non-fixed dates (dates that fall on the second Sunday of the month, etc)
    - "Day" MUST be left blank (the "Order" column is used instead).
    - "Month", "Week Day", "Order" columns need to be filled.
    - "Order" is order in which the event falls on a given "Week day".  
      For example, if an event falls on the 2nd Sunday of the "Month"  
      use 2 for the "Order". If an event falls on the last Friday of the  
      "Month" use -1. The second to last Friday is -2. Etc.

The following is the expected structure of the `dates.csv` file,  
including examples for dates you can add. Notice some cells may remain  
blank — this is normal.

|Month|Day|Week Number|Week Day|Order|Short Description|Long Description         |
|----:|--:|----------:|:-------|----:|:----------------|:------------------------|
|1    |1  |           |        |     |New Year's       |Happy New year!          |
|1    |7  |           |        |     |Example Range 1  |Example Range 1          |
|1    |8  |           |        |     |                 |Example Range 1          |
|1    |8  |           |        |     |Example Range 2  |Example Range 2          |
|1    |9  |           |        |     |                 |                         |
|1    |9  |           |        |     |Example Range 2  |Example Range 2          |
|5    |   |           |Monday  |-1   |Memorial Day     |                         |

- Multiple events can be added for the same day.
    - These will be displayed one after the other in the same order they  
      are provided in `dates.csv`.
- A date range can be achieved by adding consecutive dates.
    - For overlapping ranges, a blank entry can be added for alignment  
      (refer to the example table above).
    - The short description can be left blank for the consecutive dates  
      if only the first day of the range should be labeled. The "Long  
      Description" will still be present on the day page for each.

For example, using the above table:
![](./img/example_date_range.png)

## Using the source code

Steps for advanced users, developers, and contributors.

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

> [!TIP]
> Remarkable Paper Pro users can customize color by editing `main.py`.  
> Color settings are defined near the top, starting at line 32.

The simplest way to run the code is to enter the following command.  
The current year will be automatically determined from your computer's  
date settings.

```
python3 main.py
```
*This assumes your Python interpreter is named `python3`.*

A calendar PDF will be created locally as `calendar.pdf`. By default  
this will add dates from the sample `dates.csv` file to your calendar.

To customize formatting or to add your own dates, see the section  
[customizing your calendar](#customizing-your-calendar) for more options.
