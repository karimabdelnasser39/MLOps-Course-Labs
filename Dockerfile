FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

COPY app/ ./app/

COPY data/ ./data/

COPY main.py ./

EXPOSE 8000

CMD ["uv", "run", "litestar", "--app", "main:app", "run", "--host", "0.0.0.0", "--port", "8000"]