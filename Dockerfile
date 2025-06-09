FROM python:3.12.11-slim-bookworm
WORKDIR /app
COPY app/ /app
RUN pip install -r requirements.txt  --no-cache-dir  && playwright install chromium --with-deps
EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host","0.0.0.0","--port","8000" ]
