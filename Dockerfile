FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
	PYTHONDONTWRITEBYTECODE=1 \
	PIP_NO_CACHE_DIR=1 \
	PIP_DISABLE_PIP_VERSION_CHECK=1

RUN pip install poetry

ENV POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root --only=main && rm -rf $POETRY_CACHE_DIR

COPY . .

# Install the root package
RUN poetry install --only=main && rm -rf $POETRY_CACHE_DIR

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose port (adjust as needed)
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "start"]
