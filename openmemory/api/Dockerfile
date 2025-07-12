FROM python:3.12-slim

LABEL org.opencontainers.image.name="mem0/openmemory-mcp"

WORKDIR /usr/src

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy and install mem0 package with Mistral support
COPY pyproject.toml .
COPY README.md .
COPY mem0/ ./mem0/
RUN pip install -e ".[llms]"

# Create openmemory directory and copy API code
WORKDIR /usr/src/openmemory
COPY api/requirements.txt .
RUN pip install -r requirements.txt

COPY api/config.json .
COPY api/auto_configure.py .
COPY api/entrypoint.sh .
COPY api/ .

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

EXPOSE 8765
CMD ["./entrypoint.sh"]
