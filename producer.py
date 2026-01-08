import json
import pika
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Task(BaseModel):
    email: str
    message: str


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="tasks", durable=True)


@app.post("/publish")
def publish(task: Task):
    channel.basic_publish(
        exchange="",
        routing_key="tasks",
        body=json.dumps(task.dict()),
        properties=pika.BasicProperties(delivery_mode=2),  # persistent
    )
    return {"status": "queued"}
