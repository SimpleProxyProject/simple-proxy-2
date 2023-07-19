FROM python:3.11.3-alpine
WORKDIR /code
ADD . /code
RUN pip install -r requirements.txt
CMD exec uvicorn --loop uvloop --http httptools --host 0.0.0.0 --timeout-keep-alive 60 --port 8000 main:app