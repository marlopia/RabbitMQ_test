import json
import pika
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Creamos un objeto básico para darle una tarea al RabbitMQ
class Task(BaseModel):
    email: str
    message: str


# Usando pika nos conectamos a RabbitMQ, siendo el puerto 5672 el por defecto, sino iría tras "localhost"
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
# Abrimos canal para agregar tareas
channel = connection.channel()

# Creamos cola de tareas
channel.queue_declare(queue="tasks", durable=True)


# Al recibir contra la API un JSON publicamos el mismo como tarea.
# Aqui se podría agregar verificación del JSON y una devolución de un 400 Bad Request si está mal formado
@app.post("/publish")
def publish(task: Task):
    channel.basic_publish(
        exchange="",
        routing_key="tasks",
        body=json.dumps(task.dict()),
        properties=pika.BasicProperties(delivery_mode=2),  # persistent
    )
    return {"status": "queued"}
