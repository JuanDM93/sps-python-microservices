# syntax=docker/dockerfile:1
FROM python:3-slim
RUN mkdir /code
WORKDIR /code
ENV FLASK_APP=flaskr
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["flask", "run"]
