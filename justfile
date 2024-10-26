fix:
	black .
	ruff check --fix .

check:
	black --check .
	ruff check .
