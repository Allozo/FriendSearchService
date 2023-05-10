FROM python:3.11-slim


ENV POETRY_VERSION=1.3.2 \
    # install a handler for SIGSEGV, SIGFPE, SIGABRT, SIGBUS and SIGILL signals to dump the Python traceback
    PYTHONFAULTHANDLER=1 \
    # Python won't try to write .pyc files on the import of source modules.
    PYTHONDONTWRITEBYTECODE=on \
    # Force the stdout and stderr streams to be unbuffered.
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # Disable package cache.
    PIP_NO_CACHE_DIR=off \
    # Don't periodically check PyPI to determine whether a new version of pip is available for download.
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100


ARG ENVIRONMENT=production

RUN apt-get update \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false

WORKDIR /code

COPY pyproject.toml .

RUN poetry config virtualenvs.create false \
    && poetry install $(if test "$ENVIRONMENT" = production; then echo "--only main"; fi) --no-interaction --no-ansi

COPY . .
