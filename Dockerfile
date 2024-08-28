FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make sure the entrypoint uses 0.0.0.0 as the host
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
