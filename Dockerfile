FROM python:3.9

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    curl \
    gnupg \
    unixodbc-dev

# Add Microsoft repository for SQL Server tools
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Install SQL Server tools (fixed package name)
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools18 && \
    echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc

# Install python dependencies
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . /app/

# Start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]