from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.get("/image/{image_name}")
def get_image(image_name: str):
    # Corrected the path construction
    image_path = os.path.abspath(f"./{image_name}")
    print(image_path)
    
    # Check if the image exists and return the file response
    if os.path.exists(image_path):
        return FileResponse(image_path)
    return {"error": "Image not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
