#! /usr/bin/env bash

mkdir dist 2> /dev/null

year=$(date +%Y)

for i in $(seq 0 4); do
    declare args=( \
        "--start-date \"$((year+i))/01/01\" " \
        "--end-date \"$((year+i+1))/02/01\" " \
        "--hour-interval 6" \
        "--out dist/$((year+i))_calendar.pdf"
    );
    python main.py ${args[@]};
done

for i in $(seq 0 4); do
    declare args=( \
        "--start-date \"$((year+i))/01/01\" " \
        "--end-date \"$((year+i+1))/02/01\" " \
        "--week-start sunday " \
        "--hour-interval 6" \
        "--out dist/$((year+i))_sunday_start_calendar.pdf"
    );
    python main.py ${args[@]};
done

python_version="$(python --version)"
pyinstaller_version="$(pyinstaller --version)"
built="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
branch="$(git symbolic-ref --short HEAD)"
version="$(git describe --exact-match --tags 2> /dev/null)"
if ! [[ "$version" ]]; then
    version="$(git describe --tags --abbrev=0 main 2> /dev/null) dev"
fi

cat > version.txt <<EOF
branch=$branch
version=$version
python=$python_version
pyinstaller=$pyinstaller_version
built=$built
EOF

path="$(realpath res/GentiumPlus-6.200/GentiumPlus-Regular.ttf)"

pyinstaller \
	--noconfirm \
	--onefile \
	--clean \
	--specpath .pyinstaller/spec \
	--workpath .pyinstaller/build \
	--distpath ./dist \
	--name calendar-creator-linux64.bin \
	--add-data "${path}:res/GentiumPlus-6.200/" \
	--add-data "$(realpath version.txt):." \
    --path . \
	main.py
