import typer
import sqlite3
from pathlib import Path
from datetime import datetime
from analytics import calculate_total_travel_time, detect_fast_vehicle
from myapp.data.storage import get_all_vehicles

app = typer.Typer()
DB_PATH = Path("traffic.db")


def query(sql: str, params: tuple = ()):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return rows


@app.command()
def count_entrances(camera_id: str):
    rows = query("""
        SELECT COUNT(*) FROM readings
        WHERE camera_id = ? AND is_entrance = 1
    """, (camera_id,))
    count = rows[0][0]
    typer.echo(f"Ukupno vozila na ulazu {camera_id}: {count}")


@app.command()
def count_exits(camera_id: str):
    rows = query("""
        SELECT COUNT(*) FROM readings
        WHERE camera_id = ? AND is_exit = 1
    """, (camera_id,))
    count = rows[0][0]
    typer.echo(f"Ukupno vozila na izlazu {camera_id}: {count}")


@app.command()
def speeding(camera: str):
    camera_id = camera.upper()

    rows = query("""
        SELECT vehicle_id, speed, speed_limit, timestamp
        FROM readings
        WHERE camera_id = ? AND is_camera = 1
    """, (camera_id,))

    speeding_list = [
        (v, s, limit, t)
        for v, s, limit, t in rows
        if s is not None and limit is not None and s > limit
    ]

    if not speeding_list:
        typer.echo(f"Nema vozila koja su premašila brzinu na {camera_id}.")
        return

    typer.echo(f"\nVozila koja su premašila brzinu na {camera_id}:\n")

    for vehicle_id, speed, speed_limit, timestamp in speeding_list:
        typer.echo(f"- {vehicle_id}: {speed} km/h (ograničenje: {speed_limit}) u {timestamp}")

    typer.echo(f"\nUkupno prekoračenja na {camera_id}: {len(speeding_list)}")

@app.command()
def avg_rest(restarea_id: str):
    rows = query("""
        SELECT timestamp_entrance, timestamp_exit
        FROM readings
        WHERE camera_id = ? AND is_restarea = 1
    """, (restarea_id,))

    durations = []
    for entry, exit_ in rows:
        if entry and exit_:
            try:
                t1 = datetime.strptime(entry, "%Y-%m-%d %H:%M:%S")
                t2 = datetime.strptime(exit_, "%Y-%m-%d %H:%M:%S")
                durations.append((t2 - t1).total_seconds() / 60)
            except:
                pass

    if not durations:
        typer.echo(f"Nema zabilježenih zadržavanja na {restarea_id}.")
        return

    avg_minutes = sum(durations) / len(durations)
    typer.echo(f"Prosječno vrijeme zadržavanja na {restarea_id}: {avg_minutes:.2f} min")

@app.command()
def fast_travel():

    vehicles = get_all_vehicles()
    typer.echo("\nAnaliza brzine ukupnog putovanja\n")

    fast = []

    for vehicle_id in vehicles:
        record = calculate_total_travel_time(vehicle_id)
        if record is None:
            continue

        result = detect_fast_vehicle(record)
        if result:
            fast.append(result)

    if not fast:
        typer.echo("Nema vozila koja su putovala brže od očekivanog vremena.")
        return

    typer.echo("Vozila koja su putovala prebrzo:\n")
    for f in fast:
        typer.echo(
            f"- {f['vehicle_id']} ruta {f['route'][0]} → {f['route'][1]} "
            f": {f['actual_minutes']} min (očekivano {f['expected_minutes']} min)"
        )


if __name__ == "__main__":
    app()
