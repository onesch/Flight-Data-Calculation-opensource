run:
	poetry run python example_code.py

test:
	poetry run pytest -vv

coverage:
	poetry run coverage run -m pytest
	poetry run coverage report
