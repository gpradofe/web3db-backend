# Use an official Python runtime as the parent image
FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# If you have a requirements.txt file, this will handle all the pip installations including Flask, requests, pyspark, and flask-restx
#RUN pip install --no-cache-dir -r requirements.txt

# If you don't want to use a requirements.txt, then you can directly install packages like this:
RUN pip install --no-cache-dir --trusted-host pypi.python.org Flask requests pyspark flask-restx

# Specify the port number the container should expose
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "db_engine/app.py"]
