FROM ghcr.io/astral-sh/uv:debian-slim

ARG VERSION=dev

ENTRYPOINT [ "uv", "run", "webserver.py" ]

WORKDIR /app
EXPOSE 8023

ENV RUN_MIGRATIONS=true
ENV AUTO_RELOAD=false

RUN uv python install 3.14

COPY uv.lock pyproject.toml /app/
RUN uv sync --locked

COPY main.py /app/
COPY webserver.py /app/
COPY backend /app/backend

RUN echo "version = '${VERSION}'" > /app/backend/buildinfo.py