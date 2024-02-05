from celery import Celery
from naturalquery.query_translator import QueryTranslator  # Import your query translator
import json
import os

broker_url = os.environ.get("CELERY_BROKER_URL")
celery_app = Celery('tasks', broker=broker_url, backend=broker_url)
# Initialize the translator with the configuration file
query_translator = QueryTranslator(config_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml"))


@celery_app.task(name="worker.celery_worker.process_sql_query_task")
def process_sql_query_task(query: str):
    try:
        #results = query_translator.answer(query)
        results = "We have 2 providers."
        return json.dumps({'context': query, 'response': results})
    except Exception as e:
        return str(e)

@celery_app.task(name="worker.celery_worker.process_vector_query_task")
def process_vector_query_task(query: str):
    try:
        import os 
        import weaviate
        with weaviate.connect_to_local(
            host=os.environ.get("WEAVIATE_HOST", "localhost"),
            headers={
                "X-AnyScale-Api-Key": os.environ["ANYSCALE_APIKEY"]  # Replace with your inference API key
            }
        ) as client:
                collection = client.collections.get("Article")
                response = collection.query.near_text(
                        query=query,
                        limit=2,
                )
        return json.dumps({'context': query, 'response': [item.properties for item in response.objects]})
    except Exception as e:
        return json.dumps({'error': str(e)})
