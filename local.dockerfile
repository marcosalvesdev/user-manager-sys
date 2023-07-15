FROM ubuntu:22.04

ENV PYTHONUNBUFFERED 1

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y \
    python3-pip \
    python3.10-dev \
	python3.10-distutils \
    build-essential \
    postgresql-client \
    libpq-dev \
    postgresql \
    postgresql-contrib \
    nginx \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ADD ./Pipfile /app/Pipfile
ADD ./Pipfile.lock /app/Pipfile.lock

RUN pip3 install --upgrade pip
RUN pip3 install pipenv

RUN pipenv requirements --dev > requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app/

CMD [ "python3", "manage.py", "runserver 0.0.0.0:8000" ]