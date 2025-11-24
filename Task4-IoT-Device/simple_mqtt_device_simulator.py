# Smart House MQTT device simulator for Azure IoT Hub

import random
import time
import json
import ssl
from paho.mqtt import client as mqtt


# Azure IoT Hub connection details
path_to_root_cert = "root_cert.pem"
device_id = "gateway-01"
sas_token = "SharedAccessSignature sr=smarthousehubceren.azure-devices.net%2Fdevices%2Fgateway-01&sig=aLzMbESuXT8%2BhtHhRoiReSiEVyK19d2hQb9al7rMKII%3D&se=1763908932"
iot_hub_name = "smarthousehubceren"
mqtt_hub_hostname = f"{iot_hub_name}.azure-devices.net"
mqtt_hub_port = 8883
mqtt_topic = f"devices/{device_id}/messages/events/"

telemetry_topic = f"devices/{device_id}/messages/events/"
c2d_topic_filter = f"devices/{device_id}/messages/devicebound/#"

light_state = "OFF"
alarm_armed = True 

def on_connect(client, userdata, flags, rc, properties=None):
    print("on_connect, result code:", rc)
    if rc == 0:
        print("Connected to Azure IoT Hub")

        print(f"Subscribing to C2D topic: {c2d_topic_filter}")
        client.subscribe(c2d_topic_filter, qos=1)
    else:
        print("Connect failed")


def on_disconnect(client, userdata, rc, properties=None):
    print("Disconnected with rc =", rc)


def on_publish(client, userdata, mid, properties=None):
    print("Message published, mid =", mid)


def on_subscribe(client, userdata, mid, granted_qos):
    print("Topic subscribed!")


def on_message(client, userdata, msg):
    """
    Runs when a cloud-to-device message arrives.
    Example: {“command”: “light_on”} or {‘command’: “light_off”}
    """

    global light_state

    print("\n C2D message received!")
    print("Topic :", msg.topic)
    print("Payload:", msg.payload.decode("utf-8"))

    try:
        data = json.loads(msg.payload.decode("utf-8"))
    except json.JSONDecodeError:
        print("The payload is not in JSON format, so it is ignored..")
        return

    command = data.get("command")

    # UC-1: Turn lights on/off remotely
    if command == "light_on":
        light_state = "ON"
        print(" Light turned ON (from cloud command)")
    elif command == "light_off":
        light_state = "OFF"
        print(" Light turned OFF (from cloud command)")
    else:
        print("Unknown command:", command)


def build_telemetry_payload():
    """
    Payload according to BusinessContext:

    - UC-2: room_temperature, room_humidity
    - UC-3: motion_detected, alarm_armed
    - UC-1: light_state
    """
    # UC-2: Room temperature and humidity (e.g., living room)
    room_temperature = round(random.uniform(20.0, 28.0), 2)
    room_humidity = round(random.uniform(40.0, 60.0), 2)

    # UC-3: Motion sensor and alarm
    # Let's simulate motion with a 20% probability
    motion_detected = random.random() < 0.2

    # UC-1: Light status (varies according to the cloud command)
    global light_state

    payload = {
        "device_id": device_id,
        "room": "living_room",
        "room_temperature": room_temperature,   # UC-2
        "room_humidity": room_humidity,         # UC-2
        "motion_detected": motion_detected,     # UC-3
        "alarm_armed": alarm_armed,             # UC-3
        "light_state": light_state,             # UC-1
        "timestamp": time.time()
    }

    return payload

def send_telemetry(client):
    payload = build_telemetry_payload()
    message = json.dumps(payload)

    # Azure IoT Hub'a publish
    result = client.publish(telemetry_topic, message, qos=1)
    status = result[0]

    if status == 0:
        print(f" Message SENT to {telemetry_topic}: {message}")
    else:
        print(f" Failed to send message, result code = {status}")


def simulate_device():

    client = mqtt.Client(client_id=device_id, protocol=mqtt.MQTTv311)

    # callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    client.on_message = on_message

    # MQTT username (Azure IoT format)
    username = f"{iot_hub_name}.azure-devices.net/{device_id}/?api-version=2021-04-12"
    client.username_pw_set(username=username, password=sas_token)

    print("Using username:", username)
    print("Using SAS token:", sas_token[:40], "...")

    # TLS settings
    client.tls_set(
        ca_certs=path_to_root_cert,
        certfile=None,
        keyfile=None,
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLSv1_2,
        ciphers=None
    )
    client.tls_insecure_set(False)

    print("Connecting to:", mqtt_hub_hostname)

    topic = f"devices/{device_id}/messages/events/"

    client.connect(mqtt_hub_hostname, port=mqtt_hub_port)
    client.loop_start()

    while True:
        temperature = random.uniform(20, 30)
        humidity = random.uniform(40, 60)
        pressure = random.uniform(900, 1100)

        payload = {
            "device_id": device_id,
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure,
            "timestamp": time.time()
        }

        client.publish(topic, json.dumps(payload))
        print(f"Message SENT: {payload}")

        
        motion_detected = random.choice([True, False])

        if motion_detected:
            alert_payload = {
            "device_id": device_id,
            "event": "motion_detected",
            "location": "living_room",
            "timestamp": time.time()
        }


        client.publish(topic, json.dumps(alert_payload))
        print(" SECURITY ALERT: Motion detected!")

        time.sleep(10)


simulate_device()
