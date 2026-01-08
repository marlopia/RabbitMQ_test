import time
import requests
from faker import Faker

fake = Faker()
session = requests.Session()

URL = "http://localhost:8000/publish"

RATE = 5  # messages per second
DURATION = 60  # seconds

interval = 1 / RATE
end = time.time() + DURATION

sent = 0

while time.time() < end:
    payload = {"email": fake.email(), "message": fake.sentence()}

    r = session.post(URL, json=payload)

    print(f"JSON: {payload}")
    print(f"Status: {r.status_code}")

    if r.status_code == 200:
        sent += 1

    time.sleep(interval)

print(f"Sent {sent} messages")
