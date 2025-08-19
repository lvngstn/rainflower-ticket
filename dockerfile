# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry==1.8.4

# Instruct Poetry not to create virtualenvs in the container
RUN poetry config virtualenvs.create false

# Copy dependency files first for caching
COPY pyproject.toml poetry.lock ./

# Install dependencies (no dev deps for production)
RUN poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application code
COPY . .

EXPOSE 8080

CMD ["adk", "run", "rainflower_ticket_agent"]