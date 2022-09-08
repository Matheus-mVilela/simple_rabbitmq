FROM ubuntu:latest
WORKDIR /app
COPY . /app/
RUN apt update
RUN apt install python3-pip -y
RUN pip install --upgrade pip && pip install -r requirements.txt

