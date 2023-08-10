# Use the official Python base image
FROM python:3.9-alpine

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apk update \
    && apk add --no-cache gcc musl-dev libffi-dev openssl-dev cargo \
    && pip install --upgrade pip \
    && pip install virtualenv

# Create and activate a virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install project dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Django project files into the container
COPY . .

# Print environment variables
RUN printenv

# Set the command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]