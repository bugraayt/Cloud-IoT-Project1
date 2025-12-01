from db_operations import insert_telemetry
import time
import random

for i in range(5):
    telemetry = {
        "device_id": f"SmartLight1",
        "room": "living_room",
        "room_temperature": round(random.uniform(20, 28), 2),
        "room_humidity": round(random.uniform(40, 60), 2),
        "motion_detected": random.choice([True, False]),
        "alarm_armed": True,
        "light_state": "OFF",
        "timestamp": time.time()
    }
    insert_telemetry(telemetry)
