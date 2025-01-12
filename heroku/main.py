import os
from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from tempfile import NamedTemporaryFile
from convert_to_my_format import convert_to_my_format
from fastapi.staticfiles import StaticFiles
import requests
import validators
import struct
import json
import io

app = FastAPI()

# Chemin racine pour le projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur ma page FastAPI!"}

@app.post("/convert")
async def convert_to_vic(file: UploadFile, for_iframe: bool = False):
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
        # Pass the `for_iframe` argument to the conversion function if needed
        convert_to_my_format(temp_file_path, output_file_path, for_iframe=for_iframe)

        # Return the VIC file as a response
        return FileResponse(output_file_path, media_type="application/octet-stream", filename="output.vic")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Conversion failed: {str(e)}"})
    finally:
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

@app.get("/fetch-vic")
def fetch_vic(file_url: str):
    """
    Récupère un fichier VIC à partir d'une URL et le renvoie en réponse.
    """
    # Vérifier si l'URL est valide
    if not validators.url(file_url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    try:
        # Tenter de télécharger le fichier depuis l'URL donnée
        response = requests.get(file_url)
        response.raise_for_status()  # Vérifie si l'URL a bien renvoyé un succès (status 200)

        # Retourne le contenu du fichier en tant que réponse
        return StreamingResponse(io.BytesIO(response.content), media_type="application/octet-stream")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération du fichier: {str(e)}")

# Endpoint pour générer le code iframe
@app.get("/generate-iframe")
def generate_iframe(
    file_url: str = Query(
        ...,
        description="Public URL where the .vic file is hosted (e.g., http://example.com/output.vic). This URL must be accessible over the internet."
    ),
    width: int = Query(560, description="Width of the iframe in pixels."),
    height: int = Query(315, description="Height of the iframe in pixels."),
):
    """
    Generate an iframe to display a VIC file using the hosted viewer.

    The `file_url` must point to a .vic file hosted on a public server or domain. 
    Files on localhost or private networks will not work for remote users.
    """
    viewer_url = "http://172.233.247.47:8000/static/vic-viewer.html"
    iframe_code = f"""
    <iframe src="{viewer_url}?file={file_url}" width="{width}" height="{height}"
    frameborder="0" style="overflow:auto;" allowfullscreen></iframe>
    """
    return HTMLResponse(content=iframe_code)

# Héberger visionneuse.html à la racine
@app.get("/vic-viewer.html")
async def serve_viewer():
    return FileResponse("vic-viewer.html")

