FROM python:3.11-alpine as base
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONFAULTHANDLER=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_VIRTUALENVS_OPTIONS_NO_SETUPTOOLS=true
ENV HOME="/home/nonroot"
ENV PATH="${HOME}/.local/bin:${PATH}"

RUN apk add "pipx=~1.4" --no-cache
RUN adduser -D nonroot

USER nonroot

WORKDIR ${HOME}

RUN pipx install poetry==1.8.2 && poetry self add poetry-plugin-export
COPY --chown=nonroot ./pyproject.toml ./poetry.lock ./README.md ./
COPY --chown=nonroot ./skillventory ./skillventory


FROM base as build
WORKDIR ${HOME}

RUN poetry build --format wheel && \
  poetry export --format requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-alpine as executable
ENV HOME="/home/nonroot"
ENV PATH="${HOME}/.local/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONFAULTHANDLER=1

RUN apk --no-cache upgrade
RUN adduser -D nonroot

USER nonroot

WORKDIR ${HOME}

COPY --from=build --chown=nonroot ${HOME}/dist/skillventory*.whl ./
COPY --from=build --chown=nonroot ${HOME}/requirements.txt ./

RUN pip install --no-cache-dir ./skillventory*.whl --requirement requirements.txt

ENTRYPOINT ["uvicorn", "skillventory.main:app", "--host", "0.0.0.0", "--port", "8080"]
EXPOSE 8080
