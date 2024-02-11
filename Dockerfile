FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1

ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN apk -U upgrade && \
    apk add pipx

RUN adduser -D nonroot

USER nonroot

WORKDIR /home/nonroot/

ENV PATH="/home/nonroot/.local/bin:${PATH}"

RUN pipx install poetry==1.7.1

COPY --chown=nonroot ./pyproject.toml ./poetry.lock ./

RUN poetry install --no-root

COPY --chown=nonroot ./app ./app

ENTRYPOINT ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80
