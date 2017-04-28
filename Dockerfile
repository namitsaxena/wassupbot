# Use an official Python runtime as a base image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install gcc - needed by one of the pips
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Define environment variable
# not needed
ENV NAME World

# Run run.py when the container launches
ENTRYPOINT ["python", "run.py"]

# arguments for the script
CMD ["-c", "bot"]