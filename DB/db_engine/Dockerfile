FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY gunicorn.conf.py .

EXPOSE 3001 8000

CMD ["gunicorn", "--config", "gunicorn.conf.py", "src:create_app()"]