FROM python:3.9-slim-bullseye

# Set JAVA_HOME to OpenJDK 11
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/

# Install dependencies
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    build-essential \
    libffi-dev \
    libgmp-dev \
    pkg-config \
    libssl-dev \
    libkrb5-dev \
    libsasl2-dev \
    libldap2-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ src/
COPY src/config.py /app/src/
COPY gunicorn.conf.py .

EXPOSE 3001 7175

CMD ["gunicorn", "--config", "gunicorn.conf.py", "src:create_app()"]
