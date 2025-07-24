FROM python:3.10-bookworm  
WORKDIR /app
COPY . /app


RUN apt-get update && \
    apt-get install -y --no-install-recommends awscli curl unzip && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "app.py"]






