FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the entire project
COPY . /app/

# # Copy the entrypoint script
# COPY entrypoint.sh /entrypoint.sh

# # Make sure the entrypoint script is executable
# RUN chmod +x /entrypoint.sh

# # Specify the entrypoint
# ENTRYPOINT ["/entrypoint.sh"]

# Start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
