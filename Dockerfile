FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./library.py /app/ 


CMD ["/bin/bash"]