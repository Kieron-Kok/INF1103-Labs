FROM python:3.12-slim
WORKDIR /app
COPY persistent_auditor.py .
ENV DATA_DIR=/data
CMD ["python", "persistent_auditor.py"]