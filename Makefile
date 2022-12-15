all: isort black lint test bandit
lint:
	flake8 .
black:
	black .
isort:
	isort .
test:
	pytest
bandit:
	bandit -r kittens_store/
requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes