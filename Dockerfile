# Use the official Python image as base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY config.py run.py ./
COPY app/ ./app/

# Expose port 5000 to the outside world
EXPOSE 5000

# Define the command to run the Flask application
CMD ["python", "run.py"]
