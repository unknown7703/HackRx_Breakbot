FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y gcc

WORKDIR /app

# Copy requirements.txt from the backend directory
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the contents of the backend directory to /app
COPY . .

# Make sure the entrypoint uses 0.0.0.0 as the host
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
