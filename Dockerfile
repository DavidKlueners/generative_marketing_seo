# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install project dependencies using pip instead of poetry
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container, because that's where the app is listening and this is the default port that Google Cloud Run utilizes
EXPOSE 8080

# Run your application
CMD ["chainlit", "run", "app.py"]
