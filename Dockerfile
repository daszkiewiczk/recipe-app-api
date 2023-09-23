FROM python:3.9-alpine3.13
LABEL maintainer="Kazimierz Daszkiewicz"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements-dev.txt /tmp/requirements-dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; then /py/bin/pip install -r /tmp/requirements-dev.txt; fi && \
    rm -rf /tmp && \
    adduser --disabled-password --no-create-home django-user
RUN chown -R django-user:django-user /app
VOLUME /app

ENV PATH="$PATH:/py/bin"

USER django-user