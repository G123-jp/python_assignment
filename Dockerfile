# set the official slim version of Python 3.9.16 image as the base:
FROM python:3.9.16-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt requirements.txt

# Install the required packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the needed source code to the container
COPY model.py /app/
COPY financial/api.py /app/
COPY utilities.py /app/