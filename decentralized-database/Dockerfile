FROM python:3.8

# Set up environment variables
ENV HADOOP_CONF_DIR=/config
ENV SPARK_CONF_DIR=/config
ENV HIVE_CONF_DIR=/config

# Copy application files
COPY . /app
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Make scripts executable
RUN chmod +x /app/scripts/*.sh

CMD ["/bin/bash"]