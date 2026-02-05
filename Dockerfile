# Base image
FROM python:3.13-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update && apt install -y && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG UID
ARG GID

RUN groupadd -g ${GID} appuser && \
    useradd -u ${UID} -g appuser -m -s /bin/bash appuser

USER appuser
ENV PATH="/home/appuser/.local/bin:${PATH}"
WORKDIR /home/appuser/app

COPY --chown=appuser:appuser ./app .
CMD ["sleep", "infinity"]