FROM python:3.12-slim

COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

WORKDIR /app 

ENV UV_COMPILE_BYTECODE=1

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=README.md,target=README.md \
    uv sync --frozen --no-install-project

COPY . . 

EXPOSE 8000

CMD [ "uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
