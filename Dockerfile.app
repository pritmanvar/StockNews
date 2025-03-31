# Dockerfile.app
FROM python:3.10-slim

WORKDIR /app

# Since Chrome is running in the Selenium container, you don’t need to install it here.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "app.py"]
