import asyncio
import random
from datetime import datetime, timedelta

from myapp.data.storage import (
    insert_reading,
    get_all_entrances,
    get_camera1_passed_vehicle_ids
)
from myapp.data.models import Reading


CAMERA_ID = "CAMERA2"
LOCATION = "Kamera Umag"

TRAVEL_TIME_FROM_PULA = 45
TRAVEL_TIME_FROM_RIJEKA = 55
TRAVEL_TIME_FROM_UMAG = 15
TRAVEL_VARIATION = 5

RIJEKA_CAMERA2_CHANCE = 0.4

def generate_speed():
    return random.randint(90, 150)


async def run_camera2_simulation():

    processed = set()

    while True:
        entrances = get_all_entrances()
        camera1_passed = get_camera1_passed_vehicle_ids()

        for e in entrances:
            vehicle_id = e["vehicle_id"]
            origin = e["camera_id"]
            timestamp = e["timestamp"]

            key = f"{vehicle_id}_{origin}_{timestamp}"
            if key in processed:
                continue

            try:
                entry_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue

            must_pass = False
            travel_time = None

            if origin == "UMAG-ENTRANCE":
                must_pass = True
                travel_time = TRAVEL_TIME_FROM_UMAG

            elif origin == "RIJEKA-ENTRANCE":
                if random.random() <= RIJEKA_CAMERA2_CHANCE:
                    must_pass = True
                    travel_time = TRAVEL_TIME_FROM_RIJEKA

            elif origin == "PULA-ENTRANCE":
                if vehicle_id not in camera1_passed:
                    must_pass = True
                    travel_time = TRAVEL_TIME_FROM_PULA

            if not must_pass:
                processed.add(key)
                continue

            travel_time += random.randint(-TRAVEL_VARIATION, TRAVEL_VARIATION)
            travel_time = max(1, travel_time)
            passage_time = entry_time + timedelta(minutes=travel_time)

            reading = Reading(
                camera_id=CAMERA_ID,
                camera_location=LOCATION,
                vehicle_id=vehicle_id,
                timestamp=passage_time.strftime("%Y-%m-%d %H:%M:%S"),
                is_camera=True,
                speed=generate_speed(),
                speed_limit=110
            )

            insert_reading(reading)

            print(
                f"[CAMERA2] Vozilo {vehicle_id} prošlo u "
                f"{reading.timestamp} brzinom {reading.speed} km/h"
            )

            processed.add(key)

            await asyncio.sleep(random.uniform(1.0, 2.5))

        await asyncio.sleep(10)
