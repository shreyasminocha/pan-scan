fix:
	black src
	ruff check --fix src

check:
	black --check src
	ruff check src
	mypy src
