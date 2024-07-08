# Use an official Python runtime as a parent image
FROM python:3.10.6-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y libreoffice && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that your application will run on
EXPOSE 5000

# Run app.py when the container launches
CMD ["python3", "app.py"]
