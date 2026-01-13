FROM python:3.13

ENV PYTHONBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY mysite .

CMD ["gunicorn", "Django_Cache.mysite.wsgi:applicaton", "--bind", "0.0.0.0:8000"]

