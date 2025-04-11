from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import cv2
import base64
import asyncio
from picamera2 import Picamera2
from PIL import Image
import io

app = FastAPI()

# Initialize the camera once
camera = Picamera2()
camera.start()

# WebSocket for video streaming
async def video_stream(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            frame = camera.capture_array()  # Capture frame from camera
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            _, encoded_frame = cv2.imencode('.jpg', frame_rgb)  # Encode the frame as JPEG
            frame_b64 = base64.b64encode(encoded_frame).decode('utf-8')  # Convert to base64

            # Send the encoded frame over WebSocket
            await websocket.send_json({"image": frame_b64})
            
            # Small delay for smoother streaming (adjust as necessary)
            await asyncio.sleep(0.1)
        
    
    except WebSocketDisconnect:
        print("Client disconnected")
        camera.close()  # Close the camera properly when disconnected

# HTTP endpoint to serve a message
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI server with WebSocket video streaming"}

# WebSocket endpoint for real-time video streaming
@app.websocket("/video_feed")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await video_stream(websocket)  # Start streaming video
    except WebSocketDisconnect:
        print("Client disconnected")

# Main entry to start FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
