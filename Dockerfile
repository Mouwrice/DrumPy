# Docker file taken and inspired from
# https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0
FROM python:3.11-bookworm as builder

RUN pip install poetry

COPY . .

RUN poetry install --without dev

RUN poetry run python -m drumpy.app.main
