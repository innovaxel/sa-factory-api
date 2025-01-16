# Use the official Python image as a base
FROM python:3.9

# Install system dependencies for SQL Server connection and Azure Blob Storage
RUN apt-get update && \
    apt-get install -y \
    curl \
    gnupg \
    unixodbc-dev && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file into the container and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8100"]