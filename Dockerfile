# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD exec gunicorn -c ./gunicorn.conf.py -k uvworker.MyUvicornWorker main:app