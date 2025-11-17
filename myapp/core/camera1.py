import asyncio
import random
from datetime import datetime, timedelta

from myapp.data.storage import insert_reading, get_all_entrances
from myapp.data.models import Reading


CAMERA_ID = "CAMERA1"
LOCATION = "Kamera Rijeka"

TRAVEL_TIME_FROM_RIJEKA = 35
TRAVEL_TIME_FROM_PULA = 55
TRAVEL_TIME_FROM_UMAG = 35
TRAVEL_VARIATION = 5  # +- min


def generate_speed():
    return random.randint(90, 160)


async def run_camera1_simulation():

    processed = set()

    while True:
        entrances = get_all_entrances()

        for e in entrances:
            vehicle_id = e["vehicle_id"]
            timestamp = e["timestamp"]
            origin = e["camera_id"]

            key = f"{vehicle_id}_{timestamp}_{origin}"
            if key in processed:
                continue

            try:
                entry_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue

            must_pass = False
            travel_time = None

            if origin == "RIJEKA-ENTRANCE":
                must_pass = True
                travel_time = TRAVEL_TIME_FROM_RIJEKA

            elif origin == "PULA-ENTRANCE":
                if random.random() <= 0.4:
                    must_pass = True
                    travel_time = TRAVEL_TIME_FROM_PULA

            elif origin == "UMAG-ENTRANCE":
                if random.random() <= 0.25:
                    must_pass = True
                    travel_time = TRAVEL_TIME_FROM_UMAG

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
                speed_limit=120
            )

            insert_reading(reading)

            print(
                f"[CAMERA1] Vozilo {vehicle_id} prošlo u "
                f"{reading.timestamp} brzinom {reading.speed} km/h"
            )

            processed.add(key)

            await asyncio.sleep(random.uniform(1.0, 2.5))

        await asyncio.sleep(10)
