import random
import string
import asyncio
from datetime import datetime

from myapp.data.models import Reading
from myapp.data.storage import insert_reading


CAMERA_ID = "PULA-ENTRANCE"
LOCATION = "Ulaz Pula"


def generate_random_registration():
    region = random.choice(["PU", "RI", "ZG", "ST", "ZD", "OS"])
    digits = ''.join(random.choices(string.digits, k=3))
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    return f"{region}{digits}{letters}"


def generate_vehicle_reading():
    vehicle_id = generate_random_registration()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return Reading(
        camera_id=CAMERA_ID,
        camera_location=LOCATION,
        vehicle_id=vehicle_id,
        timestamp=timestamp,
        is_entrance=True
    )


async def run_entrance_simulation_pula():
    
    while True:
        reading = generate_vehicle_reading()
        insert_reading(reading)
        print(f"[PULA] Vozilo {reading.vehicle_id} ušlo u {reading.timestamp}")

        delay = 30
        if random.random() < 0.1:
            delay += random.choice([-5, 5])
            delay = max(1, delay)

        await asyncio.sleep(delay)