# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install project dependencies using pip instead of poetry
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container, because that's where the app is listening
EXPOSE 8000

# Run your application
CMD ["chainlit", "run", "app.py"]
