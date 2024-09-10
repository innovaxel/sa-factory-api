# Use the official Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install Git and Python dependencies
RUN apt-get update && apt-get install -y git \
    && pip install --upgrade pip

# Copy the requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Install pre-commit
RUN pip install pre-commit

# Copy the entire project to the container (including .git)
COPY . /app/

# Install pre-commit hooks (Run this command where .git is accessible)
RUN cd /app && pre-commit install

# Expose port 8000 for the Django server
EXPOSE 8000

# Set default command
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
