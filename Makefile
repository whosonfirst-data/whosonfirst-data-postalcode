data:
	./bin/mk-data-json.py -r $(root) -o data.json
	./bin/mk-data-markdown.py -d data.json -o DATA.md
