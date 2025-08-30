FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
ENV SERVICE_ACCOUNT_JSON=/secrets/service_account.json

CMD ["python", "main.py"]
