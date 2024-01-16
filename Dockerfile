FROM python:3.11-slim

WORKDIR /code

RUN ["pip", "install", "poetry==1.7"]

COPY ./pyproject.toml ./poetry.lock* /code/

RUN ["poetry", "install"]

COPY ./app /code/app

ENTRYPOINT ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80
