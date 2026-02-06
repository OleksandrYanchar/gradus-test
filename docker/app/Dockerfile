FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root

COPY . /app/

RUN chmod +x /app/docker/app/entrypoint.sh

CMD ["python", "/app/src/manage.py", "runserver", "0.0.0.0:8000"]

ENTRYPOINT ["/app/docker/app/entrypoint.sh"]