FROM python:3.13-slim

WORKDIR /server

COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/* && pip install --no-cache-dir -r requirements.txt

COPY server.py ./server.py

EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
