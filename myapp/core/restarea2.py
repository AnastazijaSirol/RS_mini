import asyncio
import random
from datetime import datetime, timedelta

from myapp.data.models import Reading
from myapp.data.storage import (
    get_entrances_by_id,
    get_exits_by_id,
    insert_reading,
)

RESTAREA_ID = "RESTAREA2"
LOCATION = "Odmorište Rijeka"

TRAVEL_TO_RESTAREA_FROM_ENTRANCE = (3, 7)
TRAVEL_TO_RESTAREA_BEFORE_EXIT = (3, 7)
STOP_DURATION = (15, 30)

RIJEKA_ENTRANCE_ID = "RIJEKA-ENTRANCE"
RIJEKA_EXIT_ID = "RIJEKA-EXIT"

ENTRANCE_PASS_CHANCE = 0.6
EXIT_PASS_CHANCE = 0.5


async def run_restarea2_simulation():

    processed = set()

    while True:
        entrances = get_entrances_by_id(RIJEKA_ENTRANCE_ID)
        exits = get_exits_by_id(RIJEKA_EXIT_ID)

        for vehicle in entrances:
            vehicle_id = vehicle["vehicle_id"]
            timestamp = vehicle["timestamp"]

            key = f"{vehicle_id}_entry_{timestamp}"
            if key in processed:
                continue

            if random.random() > ENTRANCE_PASS_CHANCE:
                processed.add(key)
                continue

            try:
                t_entry = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except:
                processed.add(key)
                continue

            travel_delay = random.randint(*TRAVEL_TO_RESTAREA_FROM_ENTRANCE)
            rest_entry = t_entry + timedelta(minutes=travel_delay)

            stop_time = random.randint(*STOP_DURATION)
            rest_exit = rest_entry + timedelta(minutes=stop_time)

            stop = Reading(
                camera_id=RESTAREA_ID,
                camera_location=LOCATION,
                vehicle_id=vehicle_id,
                is_restarea=True,
                timestamp_entrance=rest_entry.strftime("%Y-%m-%d %H:%M:%S"),
                timestamp_exit=rest_exit.strftime("%Y-%m-%d %H:%M:%S"),
            )
            insert_reading(stop)

            print(f"[RESTAREA2] {vehicle_id} sa ulaza RIJEKA staje u {stop.timestamp_entrance}")

            processed.add(key)
            await asyncio.sleep(random.uniform(1.0, 2.0))

        for vehicle in exits:
            vehicle_id = vehicle["vehicle_id"]
            timestamp = vehicle["timestamp"]

            key = f"{vehicle_id}_exit_{timestamp}"
            if key in processed:
                continue

            if random.random() > EXIT_PASS_CHANCE:
                processed.add(key)
                continue

            try:
                t_exit = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except:
                processed.add(key)
                continue

            rest_exit = t_exit - timedelta(
                minutes=random.randint(*TRAVEL_TO_RESTAREA_BEFORE_EXIT)
            )

            stop_time = random.randint(*STOP_DURATION)
            rest_entry = rest_exit - timedelta(minutes=stop_time)

            stop = Reading(
                camera_id=RESTAREA_ID,
                camera_location=LOCATION,
                vehicle_id=vehicle_id,
                is_restarea=True,
                timestamp_entrance=rest_entry.strftime("%Y-%m-%d %H:%M:%S"),
                timestamp_exit=rest_exit.strftime("%Y-%m-%d %H:%M:%S"),
            )
            insert_reading(stop)

            print(f"[RESTAREA2] {vehicle_id} prije RIJEKA-EXIT staje u {stop.timestamp_entrance}")

            processed.add(key)
            await asyncio.sleep(random.uniform(1.0, 2.0))

        await asyncio.sleep(10)
