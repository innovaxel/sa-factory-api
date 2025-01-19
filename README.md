# SA-Factory API

## Overview

The SA-factory API project is built using Django with Docker and MSSQL. This setup ensures an efficient development workflow with Docker containers and PostgreSQL as the database. The project also includes configuration for PEP8 style checking and `pre-commit` hooks to enforce code quality.

## Prerequisites

Before getting started, ensure you have the following tools installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Python**: [Install Python](https://www.python.org/downloads/) (needed for `pre-commit` setup)

## Project Structure

The project directory includes the following key files and folders:

- **`Dockerfile`**: Dockerfile for building the Django image.
- **`docker-compose.yml`**: Docker Compose configuration to manage services.
- **`django_project/`**: The Django project directory.
- **`django_project/settings.py`**: Configuration for Django settings.
- **`.env`**: Environment variables for local development.
- **`.env.prod`**: Environment variables for production.
- **`.pre-commit-config.yaml`**: Configuration file for `pre-commit` hooks.
- **`requirements.txt`**: Python dependencies, including `flake8` for PEP8 checking.
- **`README.md`**: This file.

## Getting Started

Follow these steps to get the project up and running locally.

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/innovaxel/sa-factory-api.git
cd sa-factory-api
```

### 2. Set Up Environment Variables

Create a `.env` file for local development with the following environment variables:

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

Make sure to replace the placeholders with actual values, such as your secret key and database credentials.

### 3. Build and Start Containers

Next, run the following command to build the Docker images and start the containers:

```bash
docker-compose up --build
```

This will:
- Build the Django Docker image.
- Start the PostgreSQL database container.
- Launch the Django development server.

### 4. Set Up Pre-commit Hooks

To maintain code quality, `pre-commit` hooks are configured for automatic formatting and PEP8 checking.

#### Install `pre-commit`

First, install `pre-commit` in your local environment:

```bash
pip install pre-commit
```

#### Run Pre-commit Hooks

After installing `pre-commit`, run the hooks to check and format your code:

```bash
pre-commit run --all-files
```
