# Fastapi rest api

REST APIs built on python fastapi + postgresSQL DB, deployed on AWS using github actions + terraform + ansible

## Table of Contents

- [Fastapi rest api](#fastapi-rest-api)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Features](#features)
  - [API documentation](#api-documentation)
  - [Installation](#installation)
  - [Unit tests](#unit-tests)

## About

This a dockerised python fastapi REST API.

- dev tech stack:
  - python
  - fastapi
  - postgres
  - nginx
  - docker & docker-compose

- devOps stack
  - github actions
  - terraform
  - ansible
  - aws

## Features

- REST API endpoints:
  - get users list: http://localhost:99/api/V1/users (GET)
  - create a user: http://localhost:99/api/V1/users (POST)
  - update a user: http://localhost:99/api/V1/users (PATCH)
  - delete a user: http://localhost:99/api/V1/users (DELETE)
  - aggregation view: http://localhost:99/api/V1/users/analytics (GET)


## API documentation
- OpenAPI schema: http://localhost:99/openapi.json
- Swagger UI: http://localhost:99/docs
- ReDoc: http://localhost:99/redoc


## Installation

- clone the project: 

- go to project folder and setup the project: 
  - docker-compose up


## Unit tests
- connect to python container:
  - docker exec -it [fastapi-python container id] bash
- command:
  - poetry run pytest

<!-- ## Debug (vscode)

- in python dockerfile :
  - comment 1st CMD ...
  - uncomment CMD ["python", "main_debug.py"]--wait-for-client"]  
- in docker-compose.yaml : uncomment service python command
- re build images + start containers (docker-compose up --build)
- run vscode debug (profile -> Fastapi remote... -> launch.json) -->