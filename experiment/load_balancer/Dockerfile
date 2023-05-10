# Use the official Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .
COPY load_balancer.py .

RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y iputils-ping

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the load_balancer.py script into the container
COPY load_balancer.py .

# Expose the port that the load balancer will run on
EXPOSE 80

# Start the load balancer script
CMD ["python", "load_balancer.py"]