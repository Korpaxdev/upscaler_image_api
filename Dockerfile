FROM python:latest
EXPOSE 5000
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install libgl1 -y  \
    && pip install -r requirements.txt

COPY . .

CMD flask --app main run -h 0.0.0.0 -p 5000
