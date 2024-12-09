FROM python:3.12.0-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc python3-dev postgresql-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python", "-m", "gunicorn", "dashboard.asgi:application", "-k", "uvicorn.workers.UvicornWorker"]