# Task5/db_operations.py
import uuid
import datetime
from db_config import container

def insert_telemetry(telemetry: dict):
    if "id" not in telemetry:
        telemetry["id"] = str(uuid.uuid4())

    # Normalize timestamp to ISO string
    if "timestamp" in telemetry and isinstance(telemetry["timestamp"], (int, float)):
        telemetry["timestamp"] = datetime.datetime.utcfromtimestamp(telemetry["timestamp"]).isoformat() + "Z"
    elif "timestamp" not in telemetry:
        telemetry["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"

    item = container.create_item(body=telemetry)
    print(f"[CosmosDB] Inserted id={item.get('id')} device_id={telemetry.get('device_id')}")
    return item

def query_latest_for_device(device_id: str, limit: int = 10):
    query = "SELECT TOP @limit * FROM c WHERE c.device_id = @device_id ORDER BY c.timestamp DESC"
    parameters = [
        {"name": "@limit", "value": limit},
        {"name": "@device_id", "value": device_id}
    ]
    items = list(container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))
    return items
