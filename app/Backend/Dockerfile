# Use the official Python image as a base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory into the container
COPY . .

# Copy the templates directory from the parent directory into the container
COPY ./templates ./templates

# Expose the port on which Flask app will run
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "main.py"]