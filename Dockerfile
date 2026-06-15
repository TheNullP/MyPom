FROM python:3.13-slim


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache poetry

WORKDIR .

COPY . .

RUN poetry install --no-root

CMD ["poetry", "run", "uvicorn", "MyPom.app:app", "--host", "0.0.0.0", "--port", "8080"]
