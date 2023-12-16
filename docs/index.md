# Welcome to Personal Inventory

[Documentation](https://ulisesalexanderam.github.io/Personal-inventory)
[Source code](https://github.com/UlisesAlexanderAM/Personal-inventory)

Originally a web app to use as a personal inventory.
Now an API to use, create, and manage a personal inventory.

???+ info "What's a personal inventory?"
     In this case a personal inventory is a set of skills,
     knowledge and competences that a person has or is
     interest in obtain.

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

=== "Git"

    ``` shell
    git clone https://github.com/UlisesAlexanderAM/Personal-inventory
    ```

=== "GitHub ClI"

    ``` bash
    gh repo clone UlisesAlexanderAM/Personal-inventory
    ```

### Docker compose (Recommended)

=== "Local Development/Use"
    If you want to use it for local development of the frontend or personal use.
    And you have the port 8000 in use, you need to change the port in `#!shell compose.yml`

    ``` title="compose.yml" hl_lines="5"
    --8<-- "compose.yml"
    ```

    Then you can get the service up with:

    ``` shell
    docker compose up
    ```

=== "Deployment"
    If you want to deploy it, you have to avoid sending the
    `compose.override.yml` file. Then you can get the service up with:

    ```
    docker compose up
    ```

### Docker

=== "Local Development/Use"

    ```
    docker run -p <Local_Port>:80 personal-inventory
    ```

    Where the `Local_Port` is the port where you want to access the container
    from the host.

=== "Deployment"

    ```
    docker run -p <Deployment_Host_Port>:80 personal-inventory
    ```

    Where the `Deployment_Host_Port` is the port in the deployment host from where
    you give access to the container.

## Usage

After getting the server up, you can start making requests using your favorite tool,
or connect using your favorite frontend framework.
