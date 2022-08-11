FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY api.py api.py

CMD [ "gunicorn", "api:app", "--bind", "0.0.0.0:5000"]