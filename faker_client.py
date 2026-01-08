import time
import requests
from faker import Faker

fake = Faker()

# Creamos una única sesión para poder enviar más rápido las peticiones HTTP
session = requests.Session()

# Parámetros
URL = "http://localhost:8000/publish"
RATE = 5  # Mensajes/seg
DURATION = 60  # Segundos de la prueba

interval = 1 / RATE
end = time.time() + DURATION

sent = 0

# Bucle del faker
while time.time() < end:
    # Nos inventamos un email y una frase
    payload = {"email": fake.email(), "message": fake.sentence()}

    # Con requests hacemos un POST básico del JSON
    r = session.post(URL, json=payload)

    # Mensajes de debug
    print(f"JSON: {payload}")
    print(f"Status: {r.status_code}")

    if r.status_code == 200:
        sent += 1

    # Cuello de botella
    time.sleep(interval)

print(f"Sent {sent} messages")
