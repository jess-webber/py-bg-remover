import io
import logging
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from rembg import remove
from PIL import Image

logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/remove-background/")
async def remove_background(file: UploadFile) -> FileResponse:
    """Function to remove background from an image"""
    try:
        file_contents = await file.read()
        input_image = Image.open(io.BytesIO(file_contents))
        output_path = "output.png"
        output = remove(input_image)
        output.save(output_path)
        return FileResponse(output_path)
    except Exception as e:
        logger.warning("Request to /remove-background failed. Error: %s", str(e))
        return {"status": f"bad request: {e}"}


@app.get("/healthcheck")
def healthcheck():
    """Function to check the health of the API"""
    return {"status": "ok"}
