# GepperPinger

![image](https://github.com/user-attachments/assets/09eba082-ce4f-45e7-90db-292f0489fccb)

## Roadmap
**Step 1: Setup Raspberry Pi**  
- [x] Install Raspberry Pi OS using the Raspberry Pi Imager (from your Windows laptop).  
- [x] Connect Raspberry Pi to Wi-Fi and set up SSH if you want to access it remotely.   
- [x] Connect the Camera Module to the CSI port on the Raspberry Pi.  
- [x] Install necessary software (Python, FastAPI, OpenCV,..).  

**Step 2: Set Up Machine Learning Models**  
- [x] Dog Identification Model  
- [ ] Activity Recognition Model  

**Step 3: Build FastAPI Backend**  
- [ ] Create Endpoints for the mobile app to interact with  
  /identify-dog: Accepts an image and returns the dog’s identity (Dog 1 or Dog 2).  
  /detect-activity: Accepts an image and returns the dog’s activity (e.g., playing, sitting).
- [ ] Process Incoming Images from the mobile app and pass them through the ML models for inference.  

**Step 4: Develop the Expo Mobile App (Frontend)**  
- [x] Expo Setup: Set up an Expo project with React Native.  
- [ ] Integrate HTTP Requests: Send captured images to the FastAPI backend using Axios or fetch.  
- [ ] Display Results: Show the dog’s identity and detected activity to the user in the mobile app.  

**Simple system flow**
- Capture real-time video using Raspberry module 2 and OpenCV.  
- Raspberry Pi backend processes the video using the ML models. 
- Backend returns predictions (dog identity and activity).  
- App displays predictions in real-time for the user.  

## Architecture  
![GepperPinger (1)](https://github.com/user-attachments/assets/944a2144-2464-4306-8a70-bff5421663c3)

