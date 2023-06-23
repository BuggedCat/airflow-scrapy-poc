FROM python:3.10-slim

ENV POETRY_VERSION="1.4.0"\
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 


RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code

RUN mkdir -p /code/logs/sample_spider
RUN mkdir -p /code/data/sample_spider

COPY poetry.lock pyproject.toml /code/
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY . /code

# CMD sh -c "scrapy crawl ${SPIDER_NAME}"
# && tail -f /dev/null
