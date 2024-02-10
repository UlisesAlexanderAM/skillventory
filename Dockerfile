FROM python:3.11-alpine

ARG APP_NAME=skillventory
ARG APP_PATH=/home/nonroot/${APP_NAME}
ARG POETRY_VERSION=1.7.1

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1

ENV POETRY_VERSION=${POETRY_VERSION} \
    POETRY_HOME="/home/nonroot/.local/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN apk -U upgrade && \
    apk add curl

RUN adduser -D nonroot

USER nonroot

WORKDIR /home/nonroot/

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${POETRY_HOME}/bin:${PATH}"

COPY --chown=nonroot ./pyproject.toml ./poetry.lock ./

RUN poetry install --no-root

COPY --chown=nonroot ./app ./app

ENTRYPOINT ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80
