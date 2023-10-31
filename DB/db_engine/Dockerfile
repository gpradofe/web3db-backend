# Using Python 3.8 slim image
FROM python:3.8-slim

# Set a working directory
WORKDIR /app

# Install necessary build dependencies for compiling packages
# Combining RUN commands into a single RUN to reduce image layers
RUN apt-get update -y \
    && apt-get install -y gcc g++ libc-dev libffi-dev libsasl2-dev libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy your application code to the container
COPY . /app

# Install Python dependencies
# Using a requirements.txt file is generally a good practice to manage dependencies
RUN pip install --no-cache-dir --trusted-host pypi.python.org \
    Flask==2.0.1 \
    flask-restx==0.5.1 \
    Werkzeug==2.0.1 \
    requests \
    pyspark \
    pyhive \
    thrift \
    thrift_sasl \
    --upgrade

# Expose port 5000 for the application
EXPOSE 5000

# Command to run the application
CMD ["python", "db_engine/app.py"]
