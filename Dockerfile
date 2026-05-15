FROM python:3.12-slim

WORKDIR /app

ENV MODEL_PATH=/app/data/model.pkl

COPY pyproject.toml README.md ./
COPY app/ ./app/
COPY main.py ./

RUN pip install --no-cache-dir .

COPY data/ ./data/

EXPOSE 8000

CMD ["litestar", "--app", "main:app", "run", "--host", "0.0.0.0", "--port", "8000"]