SHELL := /usr/bin/env bash
.PHONY: all clean

all:
	. .venv/bin/activate && \
	pyinstaller \
		--noconfirm \
		--onefile \
		--clean \
		--specpath .pyinstaller/spec \
		--distpath ./build \
		--workpath .pyinstaller/build \
		--name calendar-creator \
		--add-data "$(realpath res/GentiumPlus-6.200/GentiumPlus-Regular.ttf):res/GentiumPlus-6.200/" \
		main.py

env: clean
	python -m venv .venv
	. .venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements-dev.txt

clean:
	find . -maxdepth 1 -type d -iname .pyinstaller -exec rm -r {} \;
	find . -maxdepth 1 -type d -iname build -exec rm -r {} \;
	find . -maxdepth 1 -type d -iname .venv -exec rm -r {} \;
