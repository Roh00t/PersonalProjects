# **Smart Emergency Detection System Proof Of Concept Version 2**

## **Objective**
The Smart Emergency Detection System is a proof-of-concept designed to demonstrate real-time detection of predefined emergency keywords, triggering automated alerts and notifications. This system provides a framework for enhancing personal safety and public response times in critical situations.

---

## **Features**
- **Real-Time Audio Monitoring**: Listens for emergency keywords like "help," "fire," "stop," and "emergency."
- **Automated Alerts**: Sends notifications via SMS to predefined contacts using Twilio.
- **Continuous Monitoring**: Keeps the system active to detect emergencies without manual intervention.
- **Emergency Logging**: Records detected incidents in a local database for review and analysis.
- **Web Interface (Optional)**: Displays real-time logs of detected emergencies.

---

## **System Requirements**
- **Programming Language**: Python
- **Libraries/Tools**:
  - `SpeechRecognition`: For speech-to-text conversion.
  - `PyAudio`: For real-time audio capture.
  - `Twilio`: For sending SMS notifications to predefined contacts.
  - `Flask` or `Streamlit` (optional): For creating a user-friendly interface.
  - `SQLite3`: For storing emergency logs.

---

## **Environment Setup**
### **Install Python Dependencies**
 Run the following command to install the required libraries:
 ```bash
 pip install SpeechRecognition pyaudio twilio flask
 ```
## Twilio Setup
 Create a Twilio account at Twilio.
 
 Obtain your Twilio Account SID, Auth Token, and phone number.
 
 Replace placeholders (your_account_sid, your_auth_token, your_twilio_phone_number, your_phone_number) with your actual credentials.

## Database Initialization
 Use SQLite to create a database for storing emergency logs.
 
 The system will automatically create the necessary table during setup.

## How It Works
 The system listens for predefined keywords or phrases (e.g., "help," "fire").

### When an emergency keyword is detected:
 An SMS alert is sent to predefined emergency contacts.

 The event is logged into a local database for tracking and analysis.

 Optional: Detected emergencies are displayed on a web interface for real-time monitoring.

## Testing the System
### Run the System
 Start the application and ensure the microphone is active.
 ```bash
 python app.py
 ```

## Simulate an Emergency
 Speak one of the predefined keywords, such as "Help!" or "Fire!"

### Verify that the system:
 Recognizes the keyword.
 Sends an SMS alert via Twilio.
 Logs the event in the local database.
 Access the Web Interface (Optional)
 Open your browser and navigate to http://127.0.0.1:5000.
 View a log of detected emergencies in real time.

## Enhancements
 Background Noise Filtering: Implement preprocessing techniques to improve keyword detection accuracy in noisy environments.

 Real-Time Loop: Enable continuous monitoring to keep the microphone active for prolonged periods.

 Custom Alerts: Allow users to define custom keywords and notification methods.

 IoT Integration: Connect with smart home devices to trigger alarms or record footage during emergencies.

 Multilingual Support: Expand detection capabilities to include keywords in multiple languages.

## Future Potential
 ### This proof of concept lays the groundwork for advanced applications, such as:
 Integration into smartphones, smartwatches, or other IoT devices for enhanced personal safety.
 Deployment in high-risk areas to provide instant emergency detection and response.
 Collaboration with public safety networks to streamline incident reporting.

# License
 This project is for demonstration purposes and is not yet a full-fledged emergency response solution. Use at your own discretion.