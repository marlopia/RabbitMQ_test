import json
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="tasks", durable=True)
channel.basic_qos(prefetch_count=1)


def callback(ch, method, properties, body):
    task = json.loads(body)
    print(f"Sending message to {task['email']}")
    time.sleep(2)  # simulate work
    print(f"Message sent: {task['message']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue="tasks", on_message_callback=callback)
print("Worker waiting for tasks...")
channel.start_consuming()
