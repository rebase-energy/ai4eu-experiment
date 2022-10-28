FROM python:3.9-slim

RUN apt-get update
RUN apt-get install -y libgomp1

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir /app
WORKDIR /app

ADD . /app


RUN useradd app
RUN chown -R app:app /app
USER app


ENTRYPOINT [ "python", "-m", "server" ]
