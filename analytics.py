from datetime import datetime, timedelta
from myapp.data.storage import (
    get_vehicle_entrance,
    get_vehicle_exit,
    get_restarea_stops
)

def calculate_total_travel_time(vehicle_id):
    entrance = get_vehicle_entrance(vehicle_id)
    exit = get_vehicle_exit(vehicle_id)

    if not entrance or not exit:
        return None
    t_in = datetime.strptime(entrance[0], "%Y-%m-%d %H:%M:%S")
    t_out = datetime.strptime(exit[0], "%Y-%m-%d %H:%M:%S")

    total_raw = t_out - t_in

    stops = get_restarea_stops(vehicle_id)
    total_stops = timedelta()

    for s_in, s_out in stops:
        if s_in and s_out:
            t_s_in = datetime.strptime(s_in, "%Y-%m-%d %H:%M:%S")
            t_s_out = datetime.strptime(s_out, "%Y-%m-%d %H:%M:%S")
            total_stops += (t_s_out - t_s_in)

    adjusted = total_raw - total_stops

    return {
        "vehicle_id": vehicle_id,
        "entrance_camera": entrance[1],
        "exit_camera": exit[1],
        "total_raw": total_raw,
        "total_stop_time": total_stops,
        "total_adjusted": adjusted
    }

ROUTE_AVERAGES = {
    ("PULA-ENTRANCE", "RIJEKA-EXIT"): 90,
    ("UMAG-ENTRANCE", "RIJEKA-EXIT"): 70,
    ("PULA-ENTRANCE", "UMAG-EXIT"): 60,
    ("RIJEKA-ENTRANCE", "UMAG-EXIT"): 70,
}

def detect_fast_vehicle(record):
    route = (record["entrance_camera"], record["exit_camera"])

    if route not in ROUTE_AVERAGES:
        return None

    expected = ROUTE_AVERAGES[route]
    actual_minutes = record["total_adjusted"].total_seconds() / 60

    if actual_minutes < expected:
        return {
            "vehicle_id": record["vehicle_id"],
            "route": route,
            "actual_minutes": round(actual_minutes),
            "expected_minutes": expected
        }

    return None
