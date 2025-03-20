from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from facenet_pytorch import MTCNN
from PIL import Image
import io

app = FastAPI()

# Initialize MTCNN model
mtcnn = MTCNN(keep_all=True)

@app.post("/detect-faces/")
async def detect_faces(file: UploadFile = File(...)):
    # Check file type
    if not file.content_type.startswith('image/'):
        return JSONResponse(content={"error": "File type not supported. Please upload an image."}, status_code=400)

    # Read the image file
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # Detect faces
    boxes, probs = mtcnn.detect(image)

    # Prepare results
    results = []
    if boxes is not None:
        for i, (box, prob) in enumerate(zip(boxes, probs)):
            result = {
                "face_id": i + 1,
                "box_coordinates": [int(coord) for coord in box],
                "confidence": float(prob)
            }
            results.append(result)
        return {"faces_detected": len(results), "details": results}
    else:
        return {"faces_detected": 0, "details": []}
