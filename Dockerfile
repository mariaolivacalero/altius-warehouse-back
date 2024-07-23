# Use an official Python runtime as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# The project code will be mounted as a volume, so we don't need to copy it here

# Expose the port the app runs on
EXPOSE 8000

# The command will be overridden by docker-compose for development
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]