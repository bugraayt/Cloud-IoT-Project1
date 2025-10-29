## 1. Project Overview

The Smart House system connects different smart devices such as sensors, actuators, and controllers through a central IoT gateway.
The gateway collects data from devices and sends it to a cloud server. Users can see this information and control their home devices through a mobile or web application.

The system uses the internet to communicate between the home devices and the user interface. For example, when a user turns on a light from the app, the command goes to the cloud, then to the IoT gateway, and finally to the smart light.

## 2. Business Goals
- Increase home energy efficiency.
- Improve comfort and convenience for users.
- Enhance home safety through smart sensors and alerts.
- Provide a scalable IoT platform for future smart devices.


## 3. Stakeholders
Stakeholder | Role | Interest |

| Homeowner | End User | Wants to control home devices remotely |
| IoT Developer | System Designer | Builds and maintains IoT infrastructure |
| University Instructor | Supervisor | Evaluates the project implementation |
| Network Provider | Service Provider | Ensures reliable internet connectivity |



## 4. Use Cases
### UC-1: Control Lights Remotely
**Actor:** User  
**Goal:** Turn on/off lights from a mobile app.  
**Trigger:** User presses “Light On/Off” in the app.  
**Flow:**
1. User opens the mobile app.
2. The app sends a command to the IoT hub.
3. The smart light receives the signal and changes its state.
4. Confirmation message is shown to the user.



### UC-2: Monitor Room Temperature
**Actor:** User  
**Goal:** View real-time temperature data.  
**Trigger:** User opens the dashboard.  
**Flow:**
1. Sensor sends temperature data to the IoT platform.
2. The app displays the live temperature reading.
3. If temperature exceeds threshold, an alert is generated.



### UC-3: Security Alert System
**Actor:** User, System  
**Goal:** Detect unauthorized movement and send alerts.  
**Flow:**
1. Motion sensor detects movement.
2. The system checks whether the alarm is armed.
3. If armed, sends a push notification or email to the user.



## 5. User Stories
- **As a user**, I want to control my lights via an app, so I can turn them on before arriving home.  
- **As a user**, I want to monitor room temperature remotely, so I can manage heating efficiently.  
- **As a user**, I want to receive security alerts if motion is detected, so I can react quickly.  
- **As a developer**, I want a modular system design, so I can easily add new devices in the future.



## 6. System Context
The Smart House system integrates multiple IoT devices (sensors, actuators, controllers) through a central IoT gateway connected to the cloud.  
Users interact with the system via a mobile or web dashboard.