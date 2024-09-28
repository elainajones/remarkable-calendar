# ReMarkable Calender

![](img/remarkable_daily.png)

## Contents

- [What is this?](#what-is-this)
- [How do I use this?](#how-do-i-use-this)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
    - [Usage](#usage)
    - [Customization](#customization)

## What is this?

A programmatically-created PDF calendar designed for the ReMarkable 2, inspired by the Hobonichi Techo. This contains a simple script to create a calendar for the present year, including necessary resources, such as the TrueTypeFont files for the [Gentium typeface](https://software.sil.org/gentium/).

This has been designed with 1:1 scaling in mind, also allowing for the PDF pages to be printed. Although PDFs can be read by practically all e-readers and tablets, the formatting of the displayed PDF may not align as perfectly with the screen of other readers.

## How do I use this?

You can find a pre-made copy of the calendar included in the [latest release here](https://github.com/elainajones/remarkable-calendar/releases/latest). In the more than likely event this is outdated, you can easily create your own copy following the instructions below.

Once copied to the ReMarkable 2, the PDF will need to be set for landscape viewing with the page fit to the screen width.

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

The simplest way to run the code is to enter the following command. The current
year will be automatically determined from your computer's date settings.

```
python3 main.py
```

A calendar PDF will be saved locally as `calendar.pdf`.

### Customization

The `-h` or `--help` option can be added to the end of the command to show additional options.

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

Advanced users familiar with Python can customize the font by providing their own font files.
