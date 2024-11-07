# Use an official Python runtime as a parent image
FROM python:3.9-slim


# Update the apt sources and install dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install dash-mantine-components dash-pdf dash-iconify pandas gunicorn

# Set the working directory
WORKDIR /dash
# CMD gunicorn --bind 0.0.0.0:433 app:server  
