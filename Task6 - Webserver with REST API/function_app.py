# function_app.py
import azure.functions as func
import logging
import json
import datetime

app = func.FunctionApp()


# In-memory Smart House state

house_state = {
    "light": {
        "status": "off",
        "lastCommandSource": None,
        "lastUpdate": None,
    },
    "temperature": {
        "room": "living_room",
        "value": 24,
        "humidity": 45,
        "lastUpdate": None,
    },
    "security": {
        "motionDetected": False,
        "lastAlertTime": None,
        "lastAlertLocation": None,
    },
}


def _now_iso() -> str:
    """Helper: current time in ISO format."""
    return datetime.datetime.utcnow().isoformat() + "Z"



# 0) Health-check / info
# GET /api/hello

@app.function_name(name="Hello")
@app.route(route="hello", methods=[func.HttpMethod.GET])
def hello(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Hello endpoint called.")

    msg = (
        "Smart House API is running. "
        "Use /api/house/status (GET), /api/light (GET/POST) and /api/telemetry (POST)."
    )

    return func.HttpResponse(msg, status_code=200)



# 1) House status
# GET /api/house/status

@app.function_name(name="GetHouseStatus")
@app.route(route="house/status", methods=[func.HttpMethod.GET])
def get_house_status(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("House status requested.")

    body = json.dumps(house_state, indent=2)
    return func.HttpResponse(
        body,
        status_code=200,
        mimetype="application/json",
    )



# 2) Light control (UC-1)
# GET /api/light -> current state of the light
# POST /api/light -> {"command": "light_on" or "light_off", "source": "..."}

@app.function_name(name="LightController")
@app.route(
    route="light",
    methods=[func.HttpMethod.GET, func.HttpMethod.POST],
)
def light_controller(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Light endpoint called. Method: %s", req.method)

    # --- GET: sadece durumu döndür ---
    if req.method == "GET":
        body = json.dumps(house_state["light"], indent=2)
        return func.HttpResponse(
            body,
            status_code=200,
            mimetype="application/json",
        )

    # --- POST: execute command ---
    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON body.",
            status_code=400,
        )

    command = (data.get("command") or "").lower()
    source = data.get("source", "unknown")

    if command not in ("light_on", "light_off"):
        return func.HttpResponse(
            'Invalid command. Use "light_on" or "light_off".',
            status_code=400,
        )

    # Update status
    if command == "light_on":
        house_state["light"]["status"] = "on"
    else:
        house_state["light"]["status"] = "off"

    house_state["light"]["lastCommandSource"] = source
    house_state["light"]["lastUpdate"] = _now_iso()

    logging.info("Light status changed to %s by %s", house_state["light"]["status"], source)

    body = json.dumps(
        {
            "message": "Light command applied.",
            "light": house_state["light"],
        },
        indent=2,
    )

    return func.HttpResponse(
        body,
        status_code=200,
        mimetype="application/json",
    )


# ==========================
# 3) Telemetry ingest (UC-2 & UC-3)
# POST /api/telemetry
#
# Örnek JSON:
# {
#   "room": "living_room",
#   "temperature": 25.3,
#   "humidity": 48,
#   "motionDetected": true,
#   "location": "living_room"
# }
# ==========================
@app.function_name(name="TelemetryIngest")
@app.route(
    route="telemetry",
    methods=[func.HttpMethod.POST],
)
def telemetry_ingest(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Telemetry endpoint called.")

    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON body.",
            status_code=400,
        )

    # ---- update temperature / humidity ----
    if "temperature" in data:
        house_state["temperature"]["value"] = data["temperature"]
        house_state["temperature"]["room"] = data.get(
            "room", house_state["temperature"]["room"]
        )
        if "humidity" in data:
            house_state["temperature"]["humidity"] = data["humidity"]
        house_state["temperature"]["lastUpdate"] = _now_iso()

    # ---- security / motion detection ----
    if "motionDetected" in data:
        md = bool(data["motionDetected"])
        house_state["security"]["motionDetected"] = md
        if md:
            house_state["security"]["lastAlertTime"] = _now_iso()
            house_state["security"]["lastAlertLocation"] = data.get("location", "unknown")

    logging.info("Updated house_state with telemetry: %s", json.dumps(data))

    body = json.dumps(
        {
            "message": "Telemetry received.",
            "currentState": house_state,
        },
        indent=2,
    )

    return func.HttpResponse(
        body,
        status_code=200,
        mimetype="application/json",
    )
