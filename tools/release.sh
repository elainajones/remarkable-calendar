#! /usr/bin/env bash

main() {
    declare year_today=$(date +%Y);
    mkdir build 2> /dev/null;

    for i in $(seq 0 4); do
        declare args=( \
            "--start-date \"$((year_today+i))/01/01\" " \
            "--end-date \"$((year_today+i+1))/02/01\" " \
            "--hour-interval 6" \
            "--out build/$((year_today+i))_calendar.pdf"
        );
        python main.py ${args[@]};
    done

    for i in $(seq 0 4); do
        declare args=( \
            "--start-date \"$((year_today+i))/01/01\" " \
            "--end-date \"$((year_today+i+1))/02/01\" " \
            "--week-start sunday " \
            "--hour-interval 6" \
            "--out build/$((year_today+i))_sunday_start_calendar.pdf"
        );
        python main.py ${args[@]};
    done

	pyinstaller \
		--noconfirm \
		--onefile \
		--clean \
		--specpath .pyinstaller/spec \
		--distpath ./build \
		--workpath .pyinstaller/build \
		--name calendar-creator-linux64.bin \
		--add-data "$(realpath res/GentiumPlus-6.200/GentiumPlus-Regular.ttf):res/GentiumPlus-6.200/" \
		main.py
}
main;
