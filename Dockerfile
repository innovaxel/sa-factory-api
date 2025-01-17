# Dockerfile
FROM python:3.9


# Install SQL Server tools
RUN apt-get update && \
    apt-get install -y curl gnupg2 && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y mssql-tools unixodbc-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add SQL Server tools to path
ENV PATH="/opt/mssql-tools/bin:${PATH}"

USER mssql
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