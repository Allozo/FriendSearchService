TESTS = tests


CODE = tests src


.PHONY: venv
venv:
	python -m pip install --upgrade pip
	python -m pip install poetry
	poetry install


# .PHONY: tests
# test: ## Runs pytest
# 	poetry run python -m pytest $(TESTS)


# .PHONY: lint
# lint: ## Lint code
# 	poetry run python -m flake8 --jobs 4 --statistics --show-source $(CODE)
# 	poetry run python -m pylint --jobs 4 --rcfile=setup.cfg $(CODE)
# 	poetry run python -m mypy --install-types $(CODE)
# 	poetry run python -m black --skip-string-normalization --check $(CODE)


# .PHONY: format
# format: ## Formats all files
# 	poetry run python -m isort $(CODE)
# 	poetry run python -m black --skip-string-normalization $(CODE)
# 	poetry run python -m autoflake --recursive --in-place --remove-all-unused-imports $(CODE)
# 	poetry run python -m unify --in-place --recursive $(CODE)


# .PHONY: ci
# ci:	lint test ## Lint code then run tests


# .PHONY: check
# check: test format lint ## Fast check and fix


.PHONY: up
up:
	poetry run python FriendSearchService/manage.py runserver


.PHONY: migrate
migrate:
	poetry run python FriendSearchService/manage.py makemigrations
	poetry run python FriendSearchService/manage.py migrate

# .PHONY: docker-up
# docker-up:
# 	docker-compose up --build -d

