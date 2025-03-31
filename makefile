# Testing commands

test:
	coverage run -m pytest

report:
	coverage report -m

full-test: test report

# Server commands

start:
	flask --app main run

start-dev:
	flask --app main run --debug
