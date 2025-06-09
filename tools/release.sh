#! /usr/bin/env bash

main() {
    declare year_today=$(date +%Y);

    for i in $(seq 0 4); do
        declare args=( \
            "--start-date \"$((year_today+i))/01/01\" " \
            "--end-date \"$((year_today+i+1))/02/01\" " \
            "--hour-interval 6" \
            "--toolbar-space right" \
            "--out $((year_today+i))_calendar.pdf"
        );
        python main.py ${args[@]};
    done

    for i in $(seq 0 4); do
        declare args=( \
            "--start-date \"$((year_today+i))/01/01\" " \
            "--end-date \"$((year_today+i+1))/02/01\" " \
            "--week-start sunday " \
            "--hour-interval 6" \
            "--toolbar-space right" \
            "--out $((year_today+i))_sunday_start_calendar.pdf"
        );
        python main.py ${args[@]};
    done
}
main;
