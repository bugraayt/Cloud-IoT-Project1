# Smart House MQTT device simulator for Azure IoT Hub

import random
import time
import json
import ssl
from paho.mqtt import client as mqtt


# Azure IoT Hub connection details
path_to_root_cert = "root_cert.pem"
device_id = "gateway-01"
sas_token = "SharedAccessSignature sr=smarthousehubceren.azure-devices.net%2Fdevices%2Fgateway-01&sig=Gr2NzQV6%2FmAYtumJv0rwGYC%2BRmTGVqha%2BzscerhvWvM%3D&se=1763571444"
iot_hub_name = "smarthousehubceren"
mqtt_hub_hostname = f"{iot_hub_name}.azure-devices.net"
mqtt_hub_port = 8883
mqtt_topic = f"devices/{device_id}/messages/events/"

def on_connect(client, userdata, flags, rc, properties=None):
    print("on_connect, result code:", rc)
    if rc == 0:
        print("Connected to Azure IoT Hub")
    else:
        print("Connect failed")


def on_disconnect(client, userdata, rc, properties=None):
    print("Disconnected with rc =", rc)


def on_publish(client, userdata, mid, properties=None):
    print("Message published, mid =", mid)


def on_subscribe(client, userdata, mid, granted_qos):
    print("Topic subscribed!")


def on_message(client, userdata, msg):
    print("Received message!\n")
    print("Topic: '" + msg.topic+"', payload: " + str(msg.payload))


def simulate_device():

    client = mqtt.Client(client_id=device_id, protocol=mqtt.MQTTv311)

    # callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

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

        msg = json.dumps(payload)
        client.publish(mqtt_topic, msg, qos=1)
        print("Message SENT:", msg)

        time.sleep(5)


simulate_device()
