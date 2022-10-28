FROM python:3.9-slim


COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir /app
WORKDIR /app

ADD . /app

ENV HOST_NAME='https://api.rebase.energy'
#ENV HOST_NAME='http://host.docker.internal:8001'

RUN useradd app
RUN chown -R app:app /app
USER app


ENTRYPOINT [ "python", "-m", "server" ]
