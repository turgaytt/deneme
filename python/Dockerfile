# python/Dockerfile
FROM ubuntu:20.04

# Gerekli paketleri yükle
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app.py ./

CMD ["python3", "app.py"]
