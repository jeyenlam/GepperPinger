from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import cv2
import base64
import asyncio
from picamera2 import Picamera2
from PIL import Image
import io
import tensorflow as tf
import numpy as np
import os

app = FastAPI()

# Load the trained dog identifier model
model = tf.keras.models.load_model(os.path.join(os.path.abspath('./../training/trained_models/'), 'dog_identifier.h5'))

dog_names = ["Ginger", "Pepper"]
CONFIDENCE_THRESHOLD = 0.7  # Only draw the bounding box if confidence > 0.7

# Initialize the camera once
camera = Picamera2()
camera.start()

# Preprocess frame to match the model's input
def preprocess_frame(frame):
    resized_frame = cv2.resize(frame, (224, 224))  # Resize as per model's input size
    normalized_frame = resized_frame / 255.0  # Normalize to [0, 1]
    input_frame = np.expand_dims(normalized_frame, axis=0)  # Add batch dimension
    return input_frame

# Detect dog in the frame and draw bounding box
def identify_dog(frame):
  input_frame = preprocess_frame(frame)
    
  # Perform inference to get predictions
  predictions = model.predict(input_frame)

  # Get the predicted class (dog breed) with the highest probability
  predicted_class = np.argmax(predictions, axis=1)[0]  # Get the index of the highest probability
  predicted_label = dog_names[predicted_class]  # Get the corresponding dog name

  # Get the confidence score for the prediction
  confidence = predictions[0][predicted_class]
  print(f"Predicted: {predicted_label}, Confidence: {confidence:.2f}")
  
  # Check if the confidence is above the threshold
  if confidence > CONFIDENCE_THRESHOLD:
    # Example: Let's dynamically calculate bounding box size based on dog size (this is just a placeholder)
    frame_height, frame_width, _ = frame.shape

    # Calculate the bounding box size dynamically based on the confidence score
    scale_factor = 0.2 + (confidence * 0.3)  # Confidence affects the bounding box size
    w = int(frame_width * scale_factor)
    h = int(frame_height * scale_factor)
    
    # Set the top-left corner of the bounding box to be in the center of the frame
    x = (frame_width - w) // 2
    y = (frame_height - h) // 2

    # Draw the bounding box and label it with the predicted dog name
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw green box
    cv2.putText(frame, predicted_label, (x + 10, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  # Label the box
  
  return frame


# WebSocket for video streaming
async def video_stream(websocket: WebSocket):
  await websocket.accept()
  
  try:
    while True:
      frame = camera.capture_array()  # Capture frame from camera
      frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      
      # Detect dog and draw bounding box
      processed_frame = identify_dog(frame_rgb)
      
      # Encode the processed frame as JPEG
      _, encoded_frame = cv2.imencode('.jpg', processed_frame)
      frame_b64 = base64.b64encode(encoded_frame).decode('utf-8')  # Convert to base64

      # Send the encoded frame over WebSocket
      await websocket.send_json({"image": frame_b64})
      
      # Small delay for smoother streaming
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
