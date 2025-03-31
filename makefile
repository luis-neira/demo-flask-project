test:
	coverage run -m pytest

report:
	coverage report -m

full-test: test report
