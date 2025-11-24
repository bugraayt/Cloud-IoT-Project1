#define LED_PIN 13
#define BUTTON_PIN 2

bool lightState = false;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  Serial.begin(9600);
  Serial.println("Smart House Device Started...");
}

void loop() {

  // Button press = motion detection
  if (digitalRead(BUTTON_PIN) == LOW) {
    Serial.println("{\"event\":\"motion_detected\",\"location\":\"living_room\"}");
    delay(500);
  }

  // Simulated temperature & humidity
  float temperature = random(20, 30);
  float humidity = random(40, 60);

  Serial.print("{\"device\":\"gateway-01\",\"temperature\":");
  Serial.print(temperature);
  Serial.print(",\"humidity\":");
  Serial.print(humidity);
  Serial.println("}");

  // LED state output
  if (lightState) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }

  delay(2000);
}

// Simulated cloud command receiver
void serialEvent() {
  String cmd = Serial.readStringUntil('\n');
  cmd.trim();

  if (cmd == "light_on") {
    lightState = true;
    Serial.println("{\"status\":\"Light turned ON\"}");
  }

  if (cmd == "light_off") {
    lightState = false;
    Serial.println("{\"status\":\"Light turned OFF\"}");
  }
}