
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y git \
    && pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install -r requirements.txt

RUN pip install pre-commit

COPY . /app/

RUN cd /app && pre-commit install

EXPOSE 8000

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
