# Stage 1: Build the base image with pre-installed requirements
FROM python:3.10 AS base
WORKDIR /query_service
COPY requirements.txt /query_service/requirements.txt
RUN pip install -r requirements.txt
RUN git clone https://github.com/deltawi/NaturalQuery.git \
    && pip install -e ./NaturalQuery

# Stage 2: Build your application image using the base image
FROM base AS app
COPY ./sql_db_service /query_service
COPY ./worker /query_service/worker

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]