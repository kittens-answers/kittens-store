all: isort black lint test
lint:
	flake8 .
black:
	black .
isort:
	isort .
test:
	pytest
