# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r ./requirements.txt

# Copy the application code
COPY . /app/

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the app using Gunicorn
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "main:app"]
