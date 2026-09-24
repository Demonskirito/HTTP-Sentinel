FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir mitmproxy==9.0.1

COPY backend/proxy/addon.py /app/addon.py

RUN mkdir -p /app/data

EXPOSE 8080

CMD ["mitmdump", "-s", "/app/addon.py", "--mode", "upstream:http://host.docker.internal:7897", "--listen-host", "0.0.0.0", "--listen-port", "8080"]