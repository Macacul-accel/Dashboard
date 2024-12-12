FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc python3-dev postgresql-client nginx && \
    rm -rf /var/lib/apt/lists/*

COPY . /app/

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
RUN ln -s /etc/nginx/nginx.conf /etc/nginx/sites-enabled/nginx.conf && \
    rm -rf /etc/nginx/sites-enabled/default

EXPOSE 80

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "dashboard.wsgi:application", "--chdir", "/app/backend", "--bind", "unix:/tmp/gunicorn.sock", "--workers", "3"]
