# Stage 1: Build the base image with pre-installed requirements
FROM python:3.10 AS base
# Set the working directory in the container
WORKDIR /usr/src/worker
COPY requirements.txt /usr/src/worker/requirements.txt
RUN pip install -r requirements.txt
RUN git clone https://github.com/deltawi/NaturalQuery.git \
    && pip install -e ./NaturalQuery

# Stage 2: Build your application image using the base image
FROM base AS app

# Copy the current directory contents into the container at /usr/src/worker
COPY . /usr/src/worker

# Run the worker script
CMD ["celery", "-A", "celery_worker", "worker", "--loglevel=info"]
