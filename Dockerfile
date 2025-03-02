FROM python:3.10-slim

WORKDIR /usr/src/app
COPY pyproject.toml ./
COPY uv.lock ./

RUN pip install uv --no-cache-dir
RUN uv sync

COPY main.py ./

EXPOSE 8000

CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000", "main.py"]
