$path = (Resolve-Path res/GentiumPlus-6.200/GentiumPlus-Regular.ttf).Path
$year = (date).Year

for ($i = 1; $i -le 4; $i++) {
    python main.py --start-date "$($year + $i)/01/01" --end-date "$($year + $i + 1)/01/01" --hour-interval 6 --out "build/$($year + $i)_calendar.pdf"
}

for ($i = 1; $i -le 4; $i++) {
    python main.py --start-date "$($year + $i)/01/01" --end-date "$($year + $i + 1)/01/01" --week-start sunday --hour-interval 6 --out "build/$($year + $i)_sunday_start_calendar.pdf"
}

pyinstaller --noconfirm --onefile --clean --specpath .pyinstaller/spec --distpath ./build --workpath .pyinstaller/build --name calendar-creator-win64 --add-data "${path}:./res/GentiumPlus-6.200/"  main.py
