FROM python:3.11-slim

WORKDIR /app

# Copy entire app
COPY . .

# Install deps ONLY if requirements.txt exists
RUN if [ -f requirements.txt ]; then \
      pip install --no-cache-dir -r requirements.txt; \
    fi

# Command is provided by MinPaas at runtime
CMD ["sh", "-c", "echo 'no command provided'"]
