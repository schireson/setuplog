.PHONY: init install-deps lint sync-deps build test clean

init:
	bin/pyenv-create-venv schireson-logger
	PYVERSION=2.7.14 bin/pyenv-create-venv schireson-logger-py2

set-py3:
	echo schireson-logger > .python-version

set-py2:
	echo schireson-logger-py2 > .python-version

install-deps:
	pip install -e .[develop]

lint:
	bin/lint
	bin/diffcheck

sync-deps:
	bin/sync-deps

build:
	python setup.py sdist bdist_wheel

test:
	pytest -m "not functional"

clean:
	rm -rf `find . -type d -name ".pytest_cache"`
	rm -rf `find . -type d -name "*.eggs"`
	rm -rf `find . -type d -name "*.egg-info"`
	rm -rf `find . -type d -name "__pycache__"`
	rm -rf `find . -type f -name "*.pyc"`
	rm -rf `find . -type f -name "*.pyo"`

	rm -f junit_results.xml .coverage
	rm -rf build dist coverage .mypy_cache .eggs

bump:
	# For an arbitrary or additive change.
	bumpversion patch

bump-minor:
	# For a backwards incompatible change.
	bumpversion minor
