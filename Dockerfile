FROM python:3.12-slim-trixie
ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


WORKDIR /app

COPY app/requirements.txt .
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -r requirements.txt --system

COPY app/main.py .

EXPOSE 8000

#CMD ["python", "fast", "dev","main.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

