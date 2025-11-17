import sqlite3
from pathlib import Path
from .models import Reading

DB_PATH = Path("traffic.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            camera_id TEXT NOT NULL,
            camera_location TEXT NOT NULL,
            vehicle_id TEXT NOT NULL,
            timestamp TEXT,
            is_entrance INTEGER,
            is_exit INTEGER,
            is_camera INTEGER,
            is_restarea INTEGER,
            speed INTEGER,
            speed_limit INTEGER,
            timestamp_entrance TEXT,
            timestamp_exit TEXT
        );
    """)

    conn.commit()
    conn.close()

def insert_reading(reading: Reading):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO readings (
            camera_id, camera_location, vehicle_id, timestamp,
            is_entrance, is_exit, is_camera, is_restarea,
            speed, speed_limit, timestamp_entrance, timestamp_exit
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            reading.camera_id,
            reading.camera_location,
            reading.vehicle_id,
            reading.timestamp,
            int(reading.is_entrance) if reading.is_entrance is not None else None,
            int(reading.is_exit) if reading.is_exit is not None else None,
            int(reading.is_camera) if reading.is_camera is not None else None,
            int(reading.is_restarea) if reading.is_restarea is not None else None,
            reading.speed,
            reading.speed_limit,
            reading.timestamp_entrance,
            reading.timestamp_exit
        )
    )

    conn.commit()
    conn.close()

def get_all_entrances():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT camera_id, camera_location, vehicle_id, timestamp
        FROM readings
        WHERE is_entrance = 1
    """)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "camera_id": row[0],
            "camera_location": row[1],
            "vehicle_id": row[2],
            "timestamp": row[3]
        }
        for row in rows
    ]

def get_camera1_passed_vehicle_ids():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT vehicle_id
        FROM readings
        WHERE camera_id = 'CAMERA1' AND is_camera = 1
    """)

    rows = cur.fetchall()
    conn.close()

    return {row[0] for row in rows}


def get_camera2_passed_vehicle_ids():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT vehicle_id
        FROM readings
        WHERE camera_id = 'CAMERA2' AND is_camera = 1
    """)

    rows = cur.fetchall()
    conn.close()

    return {row[0] for row in rows}

def get_entrances_by_id(camera_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT camera_id, camera_location, vehicle_id, timestamp
        FROM readings
        WHERE is_entrance = 1 AND camera_id = ?
    """, (camera_id,))

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "camera_id": row[0],
            "camera_location": row[1],
            "vehicle_id": row[2],
            "timestamp": row[3],
        }
        for row in rows
    ]


def get_exits_by_id(camera_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT camera_id, camera_location, vehicle_id, timestamp
        FROM readings
        WHERE is_exit = 1 AND camera_id = ?
    """, (camera_id,))

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "camera_id": row[0],
            "camera_location": row[1],
            "vehicle_id": row[2],
            "timestamp": row[3],
        }
        for row in rows
    ]

def get_vehicle_entrance(vehicle_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT timestamp, camera_id
        FROM readings
        WHERE vehicle_id = ? AND is_entrance = 1
        ORDER BY timestamp ASC
        LIMIT 1
    """, (vehicle_id,))
    row = cur.fetchone()
    conn.close()
    return row

def get_vehicle_exit(vehicle_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT timestamp, camera_id
        FROM readings
        WHERE vehicle_id = ? AND is_exit = 1
        ORDER BY timestamp DESC
        LIMIT 1
    """, (vehicle_id,))
    row = cur.fetchone()
    conn.close()
    return row

def get_restarea_stops(vehicle_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT timestamp_entrance, timestamp_exit
        FROM readings
        WHERE vehicle_id = ? AND is_restarea = 1
    """, (vehicle_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_all_vehicles():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT vehicle_id FROM readings")
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows]