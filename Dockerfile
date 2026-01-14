FROM ghcr.io/astral-sh/uv:debian-slim

ENTRYPOINT [ "uv", "run", "webserver.py" ]

WORKDIR /app
EXPOSE 80

RUN uv python install 3.14

COPY uv.lock pyproject.toml /app/
RUN uv sync --locked

COPY main.py /app/
COPY webserver.py /app/
COPY backend /app/backend


