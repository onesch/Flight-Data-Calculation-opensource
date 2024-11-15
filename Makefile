test:
	poetry pytest -vv

coverage:
	poetry run coverage run -m pytest
	poetry run coverage report
