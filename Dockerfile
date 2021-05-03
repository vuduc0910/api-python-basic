FROM python:3.9

RUN pip install bottle gunicorn

WORKDIR /main

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:main

