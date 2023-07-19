# syntax=docker/dockerfile:1
FROM tiangolo/uvicorn-gunicorn:python3.8
ENV PYTHONUNBUFFERED=1
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD exec gunicorn -w 2 -k uvicorn.workers.UvicornWorker main:app