FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY /api_yamdb .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "api_yamdb.wsgi"]
