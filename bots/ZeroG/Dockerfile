FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr (ensures logs appear immediately)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bridge.py .

CMD ["python", "bridge.py"]
