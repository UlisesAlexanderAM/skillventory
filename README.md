# Personal inventory

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/605a85c99203416ba5a633e4db8e599d)](https://app.codacy.com/gh/UlisesAlexanderAM/Personal-inventory?utm_source=github.com&utm_medium=referral&utm_content=UlisesAlexanderAM/Personal-inventory&utm_campaign=Badge_Grade)

[Documentation](https://ulisesalexanderam.github.io/Personal-inventory)
[Source code](https://github.com/UlisesAlexanderAM/Personal-inventory)

Originally a web app to use as a personal inventory.
Now an API to use, create, and manage a personal inventory.

> **What's a personal inventory?**
> In this case a personal inventory is a set of skills,
> knowledge and competences that a person has or is
> interested in obtain.

This project primary focus is as a self-hosted API for experimentation and personal
use but as I don't want to delimitate the user, I add a dockerfile and a compose
file so you can deploy it on the cloud.

## From a web app to an API

I came to the conclusion that at the moment I know more about backend development
than frontend development. Another reason is that if the user want to do some highly
personalized websites to show their personal inventories I shouldn't restrict them
to follow my choices of how to display and interact with the personal inventory.

Probably I'll use simple templates with ninja for my personal use and as an simple
example.

## Objectives of the project

This project have some objectives:

- Help me build experience in non-trivial code projects
- Help to know me, and however use this API, better.
- Track skills, knowledge and competences.
- Help to prioritize the learning/practice of skills.

## Get the server up

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

## Usage

After getting the server up, you can start making requests using your favorite tool,
or connect using your favorite frontend framework.
