import json
import pika
import time

# Nos conectamos a RabbitMQ con pika
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Nos subscribimos a la cola "tasks" y pillamos
# lotes de uno en uno dado a que no procesamos en multihilo
channel.queue_declare(queue="tasks", durable=True)
channel.basic_qos(prefetch_count=1)


# Creamos un método que se dispare al recibir una nueva tarea,
# donde procesamos el JSON e imprimos por pantalla su información
def callback(ch, method, properties, body):
    task = json.loads(body)
    print(f"Sending message to {task['email']}")
    time.sleep(2)  # simulate work
    print(f"Message sent: {task['message']}")
    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )  # Le marcamos a RabbitMQ la etiqueta de "recibido" (ack)


# Consumimos del canal usando el método respuesta
channel.basic_consume(queue="tasks", on_message_callback=callback)

# Comenzamos a estar a la escucha
print("Worker waiting for tasks...")
channel.start_consuming()
