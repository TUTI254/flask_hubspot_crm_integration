# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to avoid buffering and ensure stdout/stderr are shown
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies if needed (for example, gcc for psycopg2)
RUN apt-get update && apt-get install -y gcc

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]