import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from tempfile import NamedTemporaryFile
from convert_to_my_format import convert_to_my_format
import struct
import json
import io

# Chemin racine pour le projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur ma page FastAPI!"}

@app.post("/convert")
async def convert_to_vic(file: UploadFile):
    """
    Convert a PNG file to the VIC format.
    """
    if not file.filename.endswith(".png"):
        return JSONResponse(status_code=400, content={"error": "Only PNG files are supported."})

    if file.size == 0:
        return JSONResponse(status_code=400, content={"error": "The uploaded file is empty."})

    with NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    output_file_path = temp_file_path.replace(".png", ".vic")

    try:
        # Perform conversion
        convert_to_my_format(temp_file_path, output_file_path)

        # Return the VIC file as a response
        return FileResponse(output_file_path, media_type="application/octet-stream", filename="output.vic")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Conversion failed: {str(e)}"})
    finally:
        # Remove only the temporary PNG file
        os.remove(temp_file_path)

@app.post("/metadata")
async def extract_metadata(file: UploadFile):
    """
    Extract metadata from a VIC file.
    """
    if not file.filename.endswith(".vic"):
        return JSONResponse(status_code=400, content={"error": "Only .vic files are supported."})

    with NamedTemporaryFile(delete=False, suffix=".vic") as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        with open(temp_file_path, "rb") as f:
            # Skip signature and version
            f.seek(12)
            metadata_size = struct.unpack("I", f.read(4))[0]
            metadata = json.loads(f.read(metadata_size))
            return JSONResponse(content={"metadata": metadata})
    except (struct.error, json.JSONDecodeError):
        return JSONResponse(status_code=400, content={"error": "Invalid .vic file or corrupted metadata."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        os.remove(temp_file_path)

@app.post("/preview")
async def preview_vic(file: UploadFile):
    """
    Preview VIC file by streaming PNG data directly.
    """
    if not file.filename.endswith(".vic"):
        return JSONResponse(status_code=400, content={"error": "Only .vic files are supported."})

    with NamedTemporaryFile(delete=False, suffix=".vic") as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        # Read the VIC file and extract PNG data
        with open(temp_file_path, "rb") as f:
            f.seek(12)  # Skip signature and version
            metadata_size = struct.unpack("I", f.read(4))[0]
            metadata = json.loads(f.read(metadata_size))
            img_data_size = struct.unpack("I", f.read(4))[0]
            img_data = f.read(img_data_size)

        # Stream PNG data directly without saving to disk
        return StreamingResponse(io.BytesIO(img_data), media_type="image/png")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        os.remove(temp_file_path)

# Endpoint pour générer le code iframe
@app.get("/generate-iframe")
def generate_iframe(file_url: str):
    """
    Génère un iframe pour afficher un fichier VIC via la visionneuse hébergée.
    """
    viewer_url = "https://dotvic.herokuapp.com/vic-viewer.html"
    iframe_code = f"""
    <iframe src="{viewer_url}?file={file_url}" width="560" height="315" 
    frameborder="0" allowfullscreen></iframe>
    """
    return HTMLResponse(content=iframe_code)

# Héberger visionneuse.html à la racine
@app.get("/vic-viewer.html")
async def serve_viewer():
    return FileResponse("visionneuse.html")

# Héberger les fichiers statiques (par exemple CSS, JS)
static_dir = os.path.join(BASE_DIR, "heroku/static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")
