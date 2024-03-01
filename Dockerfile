FROM python:3.9-slim
WORKDIR /targys
COPY requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt
