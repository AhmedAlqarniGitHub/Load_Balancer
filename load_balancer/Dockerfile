FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY load_balancer.py .

RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y iputils-ping

RUN pip install --no-cache-dir -r requirements.txt

COPY load_balancer.py .

EXPOSE 80

CMD ["python", "load_balancer.py"]