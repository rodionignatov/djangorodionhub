FROM python:3.13

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip "poetry==2.3.2"
RUN poetry config virtualenvs.create false --local

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root  # Добавлен флаг --no-root

COPY mysite ./mysite



CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]  # Исправлено: было applicaton