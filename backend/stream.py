from picamera2 import Picamera2
import time
import cv2
import numpy as np

# Initialize the camera
camera = Picamera2()

# Configure the camera with the desired resolution
camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))

# Start the camera preview (optional)
camera.start_preview()

# Start capturing video
camera.start()

# OpenCV to display video (optional)
while True:
    frame = camera.capture_array()  # Capture a frame as a NumPy array
    if frame is not None:
        # Perform any image processing here, like object detection
        # You can process the frame here (e.g., use a model to detect dogs)
        
        # Example: Show frame in OpenCV (optional, for local viewing)
        cv2.imshow("Video", frame)

    # Break condition (for example, when user presses 'q' to quit)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
camera.stop()
cv2.destroyAllWindows()
