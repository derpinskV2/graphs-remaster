FROM python:3.12.8-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DOCKER_BUILDKIT=0
ENV POETRY_VERSION=1.8.3

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  gcc \
  libpq-dev \
  gettext \
  vim \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==$POETRY_VERSION

WORKDIR /app

COPY ../pyproject.toml poetry.lock /app/

RUN poetry install --no-root --no-interaction --no-ansi

COPY secrets/private_key.pem secrets/public_key.pem /app/secrets/
COPY . /app/


# Add these lines at the end
RUN chmod 644 /app/secrets/private_key.pem /app/secrets/public_key.pem
RUN ls -l /app/secrets/private_key.pem /app/secrets/public_key.pem
#RUN mkdir -p /app/logs
#RUN touch ./app/logs/uvicorn.log \
#    && touch ./app/logs/access.log \
#    && touch ./app/logs/error.log


EXPOSE 8000
