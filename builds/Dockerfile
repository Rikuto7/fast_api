# FROM python:3.10-slim-buster
FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /work_dir

RUN apt update \
    && apt install -y default-mysql-client \
    && apt install --no-install-recommends -y tzdata \
    && apt clean

COPY /scripts /scripts
RUN chmod +x ../scripts/run.sh

COPY /requirements /requirements
RUN pip install --upgrade pip
RUN pip install -r /requirements/requirements.txt

COPY . /work_dir
