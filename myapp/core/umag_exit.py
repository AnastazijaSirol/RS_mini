import asyncio
import random
from datetime import datetime, timedelta

from myapp.data.models import Reading
from myapp.data.storage import (
    get_all_entrances,
    get_camera1_passed_vehicle_ids,
    get_camera2_passed_vehicle_ids,
    insert_reading,
)

EXIT_ID = "UMAG-EXIT"
LOCATION = "Izlaz Umag"

TRAVEL_TIME_FROM_PULA = 60
TRAVEL_TIME_FROM_RIJEKA = 70
TRAVEL_VARIATION = 10  # +- 10 min


async def run_umag_exit_simulation():

    processed = set()

    while True:
        entrances = get_all_entrances()
        cam1_passed = get_camera1_passed_vehicle_ids()
        cam2_passed = get_camera2_passed_vehicle_ids()

        for e in entrances:
            vehicle_id = e.get("vehicle_id")
            origin = e.get("camera_id")
            timestamp = e.get("timestamp")

            if not vehicle_id or not timestamp or not origin:
                continue

            key = f"{vehicle_id}_{origin}_{timestamp}"
            if key in processed:
                continue

            if origin == "UMAG-ENTRANCE":
                processed.add(key)
                continue

            try:
                entry_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                processed.add(key)
                continue

            must_exit = False
            travel_time = None

            if origin == "RIJEKA-ENTRANCE":
                if vehicle_id in cam2_passed:
                    must_exit = True
                    travel_time = TRAVEL_TIME_FROM_RIJEKA

            elif origin == "PULA-ENTRANCE":
                if vehicle_id in cam2_passed:
                    must_exit = True
                    travel_time = TRAVEL_TIME_FROM_PULA

            if not must_exit:
                processed.add(key)
                continue

            travel_time += random.randint(-TRAVEL_VARIATION, TRAVEL_VARIATION)
            travel_time = max(travel_time, 1)

            exit_time = entry_time + timedelta(minutes=travel_time)

            reading = Reading(
                camera_id=EXIT_ID,
                camera_location=LOCATION,
                vehicle_id=vehicle_id,
                timestamp=exit_time.strftime("%Y-%m-%d %H:%M:%S"),
                is_exit=True,
            )

            insert_reading(reading)

            print(f"[UMAG-EXIT] Vozilo {vehicle_id} ({origin}) izašlo u {reading.timestamp}")

            processed.add(key)

            await asyncio.sleep(random.uniform(1.0, 2.3))

        await asyncio.sleep(10)
