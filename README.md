# Skillventory

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/UlisesAlexanderAM/skillventory/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/UlisesAlexanderAM/skillventory/tree/main)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/3da0d7410cef405ea37f2c1aae0bd803)](https://app.codacy.com/gh/UlisesAlexanderAM/skillventory/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/3da0d7410cef405ea37f2c1aae0bd803)](https://app.codacy.com/gh/UlisesAlexanderAM/skillventory/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
![GitHub License](https://img.shields.io/github/license/UlisesAlexanderAM/skillventory)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/UlisesAlexanderAM/skillventory/main.svg)](https://results.pre-commit.ci/latest/github/UlisesAlexanderAM/skillventory/main)
![Testing with poetry workflow](https://github.com/UlisesAlexanderAM/skillventory/actions/workflows/testing.yml/badge.svg)
![Build docker image workflow](https://github.com/UlisesAlexanderAM/skillventory/actions/workflows/build-docker-image.yml/badge.svg)


[📘 Documentation](https://ulisesalexanderam.github.io/skillventory)
[💻 Source code](https://github.com/UlisesAlexanderAM/skillventory)

An API to manage a personal inventory.

> **What's a personal inventory?**
> In this case a personal inventory is a set of skills,
> knowledge and competences that a person has or is
> interested in obtain.

## 💡 Motivation

While taking a course about [*Career Plan Design and Development*](https://platzi.com/cursos/plan-carrera/) in Platzi.
I came access this concept of a Personal Inventory and how this is part of
the self-knowledge toolkit. I wanted to use it but I wasn't happy with
my first iteration using worksheets. So I decide to build it as a webapp,
then I decide to first build the API. In the future I'll add one or more
front-end as demos.

## 🚀 Quickstart

### Clone the repository

The first thing you need to do to use this tool is get the source code from the repository.

#### Git

``` shell
git clone https://github.com/UlisesAlexanderAM/Personal-inventory
```

#### GitHub ClI

```shell
gh repo clone UlisesAlexanderAM/Personal-inventory
```

### Docker compose (Recommended)

#### Local Development/Use

If you want to use it for local development of the frontend or personal use.
And you have the port 8000 in use, you need to change the port in `compose.yml`

```dockerfile
services:
  app:
    image: personal-inventory
    ports:
      - "8000:80"
```

Then you can get the service up with:

```shell
docker compose up
```

#### Deployment

If you want to deploy it, you have to avoid sending the
`compose.override.yml` file. Then you can get the service up with:

```shell
docker compose up
```

### Docker

#### Local Development/Use

```shell
docker run -p <Local_Port>:80 personal-inventory
```

Where the `Local_Port` is the port where you want to access the container
from the host.

#### Deployment

```shell
docker run -p <Deployment_Host_Port>:80 personal-inventory
```

Where the `Deployment_Host_Port` is the port in the deployment host from where
you give access to the container.

## 🎯 Roadmap

Here is a little roadmap of what I want to implement and what its already implemented.

- [x] Complete CRUD API (functions that interact with the DB)
- [x] Rest API for the personal inventory
- [ ] Upload Docker image to Docker Hub
- [ ] Simple demo web client
- [ ] Simple gtk+ desktop client

## 🙌 Contributing

I really appreciate any kind of contributions but I list how you can contribute
in some specific ways. **Skillventory** is currently develop and maintain by
[Ulises Alexander AM](https://github.com/UlisesAlexanderAM). I'm looking for
additional maintainers that can help improve this project.

### Providing feedback

You can provide feedback using the issues feature of GitHub.
[Open an Issue](https://github.com/UlisesAlexanderAM/skillventory/issues/new)
to request features, report bugs, or ask a question.

### Graphic Design

At the moment **Skillventory** doesn't have a logo or any kind of supplemental
imagery. So I welcome any submissions or suggestions for the logo and graphics
associated with **Skillventory**

### Documentation

You can help me proofreading and fixing any typo or formatting issues in the `docs/`
or `README` files. [*Material for MkDocs*](https://squidfunk.github.io/mkdocs-material/)
is use to build and publish the documentation.

!!! note
    The `index.md` and `README.md` files are content equals.

### Code

You can also help with code.

#### Setting up your dev enviroment

The first thing you probably want to do is fork the project. You can do it
from the web or if you have GH CLI installed in your system, with the following
command:

```shell
gh repo fork UlisesAlexanderAM/skillventory
```

If you haven't clone your fork into your system, proceed to do it.

This project uses [poetry](https://python-poetry.org/),
so I recommend you install it first, if you don't already have it installed.

**With pipx**

```shell
pipx install poetry
```

**With the official installer**

***Linux, macOS, Windows(WSL)***

```shell
curl -sSL https://install.python-poetry.org | python3 -
```

***Windows(Powershell)***

```shell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

With **poetry** already in your system, and your fork, is time to install the dependencies.

**Basic dev environment**

```shell
poetry install --no-root --with test
```

**With linting tools**

```shell
poetry install --no-root --with test linting
```

**Working with docs**

```shell
poetry install --no-root --with docs
```

**All included**

```shell
poetry install --no-root -with test linting docs
```

You can use `poetry shell` to spawn a subshell,
or is possible that your IDE already detects your environment.

To test your code, simply use `pytest`.

**Inside the environment**

```shell
pytest
```

**Outside the environment (environment not active)**

```shell
poetry run pytest
```

Finally open a pull request, if you add new funtionality please add
some tests. In case you don't know how or need help open your PR as
a draft pull request.
