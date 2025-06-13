FROM python:3.11-slim

# Install git and curl
RUN apt-get update \
    && apt-get install -y --no-install-recommends git curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (18.x)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get update \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Python tooling
# Use explicit index to avoid firewall blocks
RUN pip install --no-cache-dir \
    -i https://pypi.org/simple \
    --trusted-host pypi.org \
    pre-commit black ruff

WORKDIR /workspace
