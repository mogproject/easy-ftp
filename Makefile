PYTHON = python3
PIP = pip3
PROGRAM = easy-ftp
OPEN_EXISTS = command -v open >/dev/null

build:
	$(PYTHON) setup.py build

install:
	$(PIP) install .

uninstall:
	$(PIP) uninstall $(PROGRAM)

dev-install:
	$(PYTHON) setup.py develop

dev-uninstall:
	$(PYTHON) setup.py develop -u

dev-setup:
	$(PIP) install pycodestyle coverage

style:
	pycodestyle --max-line-length=140 src test
	@echo "\nOK"

test: style
	$(PYTHON) setup.py test

coverage:
	coverage erase
	coverage run --source=src setup.py test
	coverage html
	$(OPEN_EXISTS) && open htmlcov/index.html || coverage report

clean:
	$(PYTHON) setup.py clean

console:
	cd src && $(PYTHON)

.PHONY: build install uninstall dev_install dev_uninstall style test coverage clean console

