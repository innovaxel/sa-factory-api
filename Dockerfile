# Dockerfile
FROM python:3.9

# Install MSSQL dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    unixodbc \
    unixodbc-dev \
    curl \
    gnupg2

# Add Microsoft repository for SQL Server tools
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbc17

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8100"]