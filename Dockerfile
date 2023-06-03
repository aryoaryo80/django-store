FROM python:slim-buster

WORKDIR /src
COPY ./ /src

RUN pip install -U pip
RUN pip --timeout 40 install -r  requirements.txt

EXPOSE 8000

CMD [ "gunicorn", "t.wsgi", "-b", "0.0.0.0:8000" ]

