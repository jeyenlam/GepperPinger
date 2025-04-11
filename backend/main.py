import cv2
import numpy as np
import tensorflow as tf
import base64
import asyncio
from picamera2 import Picamera2
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import os

app = FastAPI()

# Load the trained dog identifier model
model = tf.keras.models.load_model(os.path.join(os.path.abspath('./../training/trained_models/'), 'dog_identifier.h5'))

dog_names = ["Ginger", "Pepper"]
CONFIDENCE_THRESHOLD = 0.7  # Only draw the bounding box if confidence > 0.7

# Initialize the camera once
camera = Picamera2()
camera.start()

# Load YOLO model (or replace with another detection model if necessary)
net = cv2.dnn.readNet('./../training/trained_models/yolov4-tiny.weights', './../training/trained_models/yolov4-tiny.cfg')  # Use your YOLO model
layer_names = net.getLayerNames()
output_layers = net.getLayerNames()
output_layers = [output_layers[i - 1] for i in net.getUnconnectedOutLayers()]

# Preprocess frame to match the model's input
def preprocess_frame(frame):
    resized_frame = cv2.resize(frame, (224, 224))  # Resize as per model's input size
    normalized_frame = resized_frame / 255.0  # Normalize to [0, 1]
    input_frame = np.expand_dims(normalized_frame, axis=0)  # Add batch dimension
    return input_frame

# Object detection (find dogs in the frame using YOLO or similar model)
def detect_dog(frame):
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    boxes = []
    class_ids = []
    confidences = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 16:  # Class ID 16 corresponds to dogs in YOLO
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                w = int(detection[2] * frame.shape[1])
                h = int(detection[3] * frame.shape[0])

                x = center_x - w // 2
                y = center_y - h // 2

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    return boxes, confidences

# Dog identifier (to classify the detected dog region)
def identify_dog(frame, boxes):
    for box in boxes:
        x, y, w, h = box
        cropped_dog = frame[y:y + h, x:x + w]  # Crop the detected dog region

        # Preprocess the cropped image to match the model's input
        cropped_dog_resized = cv2.resize(cropped_dog, (224, 224))
        cropped_dog_normalized = cropped_dog_resized / 255.0
        input_frame = np.expand_dims(cropped_dog_normalized, axis=0)

        # Make the prediction
        predictions = model.predict(input_frame)
        predicted_class = np.argmax(predictions, axis=1)[0]
        predicted_label = dog_names[predicted_class]

        # Get the confidence score for the prediction
        confidence = predictions[0][predicted_class]
        print(f"Predicted: {predicted_label}, Confidence: {confidence:.2f}")

        # Draw the bounding box and label on the frame
        if confidence > CONFIDENCE_THRESHOLD:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, predicted_label, (x + 10, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return frame

# WebSocket for video streaming
async def video_stream(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            frame = camera.capture_array()  # Capture frame from camera
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Step 1: Detect dog in the frame
            boxes, confidences = detect_dog(frame_rgb)

            # Step 2: Identify the dog in the detected region
            if len(boxes) > 0:
                processed_frame = identify_dog(frame_rgb, boxes)
            else:
                processed_frame = frame_rgb  # No dog detected, return the original frame

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
