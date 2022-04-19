SHELL := /bin/bash
.PHONY: test deps lint format

deps:
	python3 setup.py develop

lint: deps
	pep8 --config ./pep8 . || true

format: deps
	autopep8 -i -r -j0 -a --experimental --max-line-length 100 --indent-size 2 .

test: deps tests.json
	python3 -m "nose" test

build:
	python3 setup.py sdist

publish:
	./publish.sh

tests.json:
	wget https://raw.githubusercontent.com/Clever/kayvee/master/tests.json -O test/tests.json
