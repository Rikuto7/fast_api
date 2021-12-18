FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY /requirements /requirements

RUN apk add --no-cache build-base \
 && pip install --no-cache-dir --trusted-host pypi.python.org -r /requirements/requirements.txt \
 && apk del build-base

COPY main.py .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]