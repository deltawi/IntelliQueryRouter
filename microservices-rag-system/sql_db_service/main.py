from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from worker.celery_worker import celery_app, process_sql_query_task, process_vector_query_task # Import the Celery instance

# Define request model
class QueryRequest(BaseModel):
    query: str

class GenerativeRequest(BaseModel):
    task_sql_id: str
    task_vector_id: str

app = FastAPI()

@app.post("/query")
async def process_query(request: QueryRequest):
    try:
        # Dispatch the task to Celery
        task_sql = process_sql_query_task.delay(request.query)
        task_vector = process_vector_query_task.delay(request.query)
        # Return the task ID to the client
        return {"task_sql_id": task_sql.id,
                "task_vector_id": task_vector.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
async def generate(request: GenerativeRequest):
    from naturalquery.query_translator.llm_interface import get_provider
    import os
    import json
    sql_task_result = json.loads(AsyncResult(request.task_sql_id, app=celery_app).get())
    vector_task_result = json.loads(AsyncResult(request.task_vector_id, app=celery_app).get())
    config = {"llm": {"provider":"anyscale", "api_key": os.environ.get("ANYSCALE_APIKEY"), 'model': 'meta-llama/Llama-2-7b-chat-hf'}}
    provider = get_provider(config)
    combined_response = provider.send_prompt(
        prompt=
            [
            {"role": "system", "content": "You are a helpful assistant.\n- If one of the answers is irrelevant to the question, ignore it.\
             \n- Answer the question directly without giving explanations.\
             \n- When giving the answer briefly mention which source helped getting the answer."},
            {"role": "user", "content": f"Help me combine two responses I got to answer the question : {sql_task_result['context']}.\n\
             Response 1 from SQL database: {sql_task_result['response']}\n\
             Response 2 from Vector database: {vector_task_result['response']}"}
          ]
    )

    return combined_response

@app.get("/task/{task_id}/status")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    return {"task_id": task_id, "status": task_result.status}


@app.get("/task/{task_id}/result")
async def get_task_result(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)

    if task_result.status == 'SUCCESS':
        return {"task_id": task_id, "status": task_result.status, "result": task_result.get()}
    elif task_result.status == 'FAILURE':
        return {"task_id": task_id, "status": task_result.status, "result": str(task_result.result)}
    else:
        raise HTTPException(status_code=202, detail="Task not completed yet")
