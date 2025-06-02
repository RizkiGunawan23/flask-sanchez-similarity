FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV PORT=8080  

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT} app.main:app"]