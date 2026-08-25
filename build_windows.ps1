New-Item -ItemType Directory -Path dist -Force > $null

$year = (date).Year

for ($i = 1; $i -le 4; $i++) {
    python main.py `
        --start-date "$($year + $i)/01/01" `
        --end-date "$($year + $i + 1)/01/01" `
        --hour-interval 6 `
        --out "dist/$($year + $i)_calendar.pdf"
}

for ($i = 1; $i -le 4; $i++) {
    python main.py `
        --start-date "$($year + $i)/01/01" `
        --end-date "$($year + $i + 1)/01/01" `
        --week-start sunday `
        --hour-interval 6 `
        --out "dist/$($year + $i)_sunday_start_calendar.pdf"
}

$python_version="$(python --version)"
$pyinstaller_version="$(pyinstaller --version)"
$built = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$branch="$(git symbolic-ref --short HEAD)"
$version="$(git describe --exact-match --tags 2> $null)"
if (-Not "$version") {
    $version="$(git describe --tags --abbrev=0 main 2> $null) dev"
}

@"
branch=$branch
version=$version
python=$python_version
pyinstaller=$pyinstaller_version
built=$built
"@ | Set-Content version.txt

$path = (Resolve-Path res/GentiumPlus-6.200/GentiumPlus-Regular.ttf).Path

pyinstaller `
    --noconfirm `
    --onefile `
    --clean `
    --specpath .pyinstaller/spec `
    --workpath .pyinstaller/build `
    --distpath ./dist `
    --name calendar-creator-win64.exe `
    --add-data "${path}:./res/GentiumPlus-6.200/" `
    --add-data "$((Resolve-Path version.txt).Path):." `
    --path . `
    main.py
