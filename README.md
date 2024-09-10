# SA-Stairs API

## Overview

This project sets up the SA-Stairs API using Django with Docker and PostgreSQL as the database. It includes configuration for PEP8 style checking and `pre-commit` hooks to ensure code quality. This README provides step-by-step instructions to get the project up and running.

## Prerequisites

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)
- Python: [Install Python](https://www.python.org/downloads/) (for `pre-commit` setup)

## Project Structure

- `Dockerfile`: Dockerfile for building the Django image.
- `docker-compose.yml`: Docker Compose configuration for managing services.
- `django_project/`: The Django project directory.
- `django_project/settings.py`: Django settings configuration.
- `.env`: Environment variables for local development.
- `.env.prod`: Environment variables for production.
- `.pre-commit-config.yaml`: Configuration for `pre-commit` hooks.
- `requirements.txt`: Python dependencies including `flake8` for PEP8 checking.
- `README.md`: This file.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/innovaxel/sa-stairs-api.git
cd sa-stairs-api

### 2. Set Up Environment Variables
```
DEBUG=
SECRET_KEY=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=
ALLOWED_HOSTS=
```

## 3. Build and Start Containers

Run the following command to build the Docker images and start the containers:

```
docker-compose up --build
```

This command will:
- Build the Django Docker image.
- Start the PostgreSQL database container.
- Start the Django development server.

## 4. Pre-commit Hooks

To ensure code quality and automatic formatting, `pre-commit` hooks are set up.

Install `pre-commit`
First, install `pre-commit` in your local environment:

```
pip install pre-commit
```

### Run it.

```
pre-commit run --all-files
```
