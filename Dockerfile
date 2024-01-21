# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Make port 8000 available to the world outside this container, because thats where the app is listening
EXPOSE 8000

# Run your application
CMD ["poetry", "run", "chainlit", "run", "app.py", "-w"]
