PYTHON_VERSION=python3.5
.PHONY: clean server

all: | env $(DB)

clean:
	rm -rf env

env:
	$(PYTHON_VERSION) -m venv env && \
	. env/bin/activate && \
	pip install -e . \
		ipython \
		coloredlogs

server: | env $(DB)
	. env/bin/activate && \
	labor-api

open:
	curl -d 'open=1' -X POST http://localhost:8081/api/room/

close:
	curl -d 'open=0' -X POST http://localhost:8081/api/room/
