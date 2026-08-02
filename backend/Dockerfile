FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

HEALTHCHECK --interval=5s --timeout=3s --start-period=10s --retries=12 CMD ["python", "scripts/wait_for_backend.py", "--timeout", "2"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
