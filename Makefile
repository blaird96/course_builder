# ---- config --------------------------------------------------
PY := .venv/bin/python
PIP := .venv/bin/pip
VENV := .venv
REQ := requirements.txt

# ---- meta ----------------------------------------------------
.PHONY: help setup install run clean fmt lint reset google-check

help:
	@echo "make setup         # create venv and install deps"
	@echo "make install       # install deps (after setup)"
	@echo "make run           # run the app (python -m course_builder)"
	@echo "make fmt           # format with black"
	@echo "make lint          # lint with ruff"
	@echo "make google-check  # verify credentials.json exists"
	@echo "make clean         # remove __pycache__"
	@echo "make reset         # nuke venv and reinstall"

$(VENV)/bin/python:
	python3 -m venv $(VENV) --upgrade-deps

setup: $(VENV)/bin/python install

api:
	$(PY) -m uvicorn api.main:app --reload --port 8000


install:
	@if [ -f $(REQ) ]; then \
		$(PIP) install -r $(REQ); \
	else \
		echo "No requirements.txt found; skipping pip install."; \
	fi

run:
	$(PY) -m course_builder $(ARGS)

fmt:
	@$(PIP) install black >/dev/null || true
	$(PY) -m black course_builder

lint:
	@$(PIP) install ruff >/dev/null || true
	$(VENV)/bin/ruff check course_builder

google-check:
	@test -f credentials.json && echo "credentials.json found." || (echo "credentials.json missing – place it in project root."; exit 1)

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +

reset:
	rm -rf $(VENV)
	$(MAKE) setup
