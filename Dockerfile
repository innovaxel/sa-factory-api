# Use Python 3.9 base image
FROM python:3.9

# Install system dependencies for SQL Server and Python dependencies
RUN apt-get update && \
    apt-get install -y \
    curl \
    gnupg \
    unixodbc-dev \
    gcc \
    g++ && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools && \
    rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Add SQL Server tools to path
ENV PATH="/opt/mssql-tools/bin:${PATH}"

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
COPY . /app/

# Create static files directory for Django
RUN mkdir -p /app/staticfiles

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1

# Expose port for the application
EXPOSE 8100

# Command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8100"]
