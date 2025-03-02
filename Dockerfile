FROM python:3.10-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY src/urlnk ./urlnk

# Install the application dependencies.
RUN uv sync --frozen --no-cache

EXPOSE 8000

# Run from CLI.
CMD ["uv", "run", "fastapi", "dev", "urlnk/app.py", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Run from package.
# CMD ["uv", "run", "python", "-m", "urlnk"]
