# IntelliQueryRouter
![arch](./img/arch_diag.png)

## Overview
This service provides an API for processing SQL and vector queries, leveraging Celery for task management and FastAPI for handling HTTP requests.

## Features
- **Asynchronous Query Processing:** Uses Celery for handling SQL and vector database queries asynchronously.
- **LLM Provider Integration:** Utilizes a provider from `naturalquery.query_translator.llm_interface` for generating combined responses from different sources.

## Endpoints
- `POST /query`: Submits a query for processing. Returns task IDs for tracking.
- `POST /generate`: Combines results from SQL and vector queries to generate a response.
- `GET /task/{task_id}/status`: Retrieves the status of a submitted task.
- `GET /task/{task_id}/result`: Fetches the result of a completed task.

## Setup
The service is containerized using Docker, with the following services:
- `query_service`: The main FastAPI application.
- `celery_worker`: Celery worker for processing tasks.
- `redis`: Redis server for Celery's message broker.
- `postgres`: PostgreSQL database.
- `flower`: Celery Flower for monitoring Celery tasks.
- `weaviate`: Weaviate as the vector database.

## Configuration
Ports, environment variables, and other configurations are set in the `docker-compose.yml` file and `.env` file.

## Usage
To start the service, use docker-compose:
```bash
docker-compose up -d
```
# API Endpoints
![api](./img/api_endpoints.png)