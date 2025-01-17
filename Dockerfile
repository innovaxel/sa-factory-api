# Dockerfile
FROM python:3.9

# Install system dependencies for SQL Server
RUN apt-get update && \
    apt-get install -y \
    curl \
    gnupg \
    unixodbc-dev && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools

# Add SQL Server tools to path
ENV PATH="/opt/mssql-tools/bin:${PATH}"


# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Create static files directory
RUN mkdir -p /app/staticfiles

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8100

# Start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8100"]