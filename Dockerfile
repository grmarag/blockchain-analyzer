# Use the official Python 3.12 slim image as the base image
FROM python:3.12-slim

# Install system dependencies needed for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Poetry
RUN pip install --upgrade pip && pip install poetry

# Set the working directory in the container
WORKDIR /app

# Copy the dependency files for Poetry
COPY pyproject.toml poetry.lock ./

# Install only production dependencies (skip dev dependencies)
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copy the rest of the project files
COPY . .

# Set the default command to run the blockchain analyzer.
CMD ["python", "-m", "src.analyzer", "--input", "data/raw/transfers.jsonl"]