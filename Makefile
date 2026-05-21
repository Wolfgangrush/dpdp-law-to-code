.PHONY: install test typecheck lint examples clean

install:
	pip install -e ".[dev]"

test:
	pytest -v

typecheck:
	mypy --strict dpdp/

lint:
	ruff check .

examples:
	@echo '=== consent banner ==='
	@python examples/consent_banner_check.py
	@echo
	@echo '=== breach 72hr ==='
	@python examples/breach_72hr_check.py
	@echo
	@echo '=== employee data legitimacy ==='
	@python examples/employee_data_legitimacy.py

clean:
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
