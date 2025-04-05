import os
import tensorflow as tf
import cv2
import numpy as np
import json
import base64
import websockets
import asyncio

# Load trained model
model = tf.keras.models.load_model(os.path.join(os.path.abspath('./trained_models/'), 'dog_identifier.h5'))

def preprocess_frame(frame):
  # Resize frame to the size your model expects
  resized_frame = cv2.resize(frame, (224, 224))  # Change size as per your model's input size
  # Normalize the frame (if your model was trained with normalization)
  normalized_frame = resized_frame / 255.0
  # Add batch dimension: (224, 224, 3) -> (1, 224, 224, 3)
  input_frame = np.expand_dims(normalized_frame, axis=0)
  return input_frame

def detect_dog(frame):
    # Preprocess the frame
    input_frame = preprocess_frame(frame)

    # Perform inference
    predictions = model.predict(input_frame)

    # Assuming your model returns bounding box and class probabilities
    # If using a classification model, you'd check if a "dog" is detected:
    # Example: predictions = [prob_class_0, prob_class_1, ..., prob_class_n]
    if predictions[0] > 0.5:  # Assume index 0 is the "dog" class
        # Draw a bounding box around the dog (for simplicity, assume fixed box here)
        x, y, w, h = 100, 100, 200, 200  # Replace with your model's output
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Dog", (x + 10, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    return frame
