import os
from fastapi import FastAPI, File, UploadFile, Query, Header
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from tempfile import NamedTemporaryFile
from convert_to_my_format import convert_to_my_format, compress_image, is_supported_image
from fastapi.exceptions import HTTPException
import requests
import validators
import struct
import json
import io
import base64
import re

app = FastAPI()

# Chemin racine pour le projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_homepage(user_agent: str = Header(default="")):
    """
    Serve main-page.html with default iframe pointing to convert.html.
    """
    try:
        iframe_src = "/static/pages/convert/convert.html"  # Always redirect to convert.html
        with open(os.path.join(STATIC_DIR, "main-page.html"), "r", encoding="utf-8") as file:
            main_page = file.read()
        # Replace the placeholder with the appropriate iframe source
        main_page = main_page.replace("{{DEFAULT_IFRAME_SRC}}", iframe_src)
        return HTMLResponse(content=main_page)
    except Exception as e:
        print(f"Error serving homepage: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/convert")
async def convert_to_vic(file: UploadFile, for_iframe: bool = False):
    """
    Convert an image file to the VIC format with optional compression for large files.
    """
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff")):
        return JSONResponse(status_code=400, content={"error": "Unsupported file format. Supported formats: PNG, JPEG, BMP, GIF, TIFF."})

    if file.size == 0:
        return JSONResponse(status_code=400, content={"error": "The uploaded file is empty."})

    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        if not is_supported_image(temp_file_path):
            return JSONResponse(status_code=400, content={"error": "Unsupported or corrupted image format."})

        max_file_size_mb = 5
        compressed_path = (
            compress_image(temp_file_path, max_size_in_mb=max_file_size_mb)
            if os.path.getsize(temp_file_path) > max_file_size_mb * 1024 * 1024
            else temp_file_path
        )

        output_file_path = compressed_path.replace(os.path.splitext(compressed_path)[1], ".vic")

        convert_to_my_format(compressed_path, output_file_path, for_iframe=for_iframe)

        return FileResponse(output_file_path, media_type="application/octet-stream", filename="output.vic")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Conversion failed: {str(e)}"})
    finally:
        os.remove(temp_file_path)
        if 'compressed_path' in locals() and compressed_path != temp_file_path and os.path.exists(compressed_path):
            os.remove(compressed_path)

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
            f.seek(12)  # Skip signature and version
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
        with open(temp_file_path, "rb") as f:
            f.seek(12)  # Skip signature and version
            metadata_size = struct.unpack("I", f.read(4))[0]
            metadata = json.loads(f.read(metadata_size))
            img_data_size = struct.unpack("I", f.read(4))[0]
            img_data = f.read(img_data_size)

        return StreamingResponse(io.BytesIO(img_data), media_type="image/png")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        os.remove(temp_file_path)

@app.post("/fetch-and-convert-vic")
def fetch_and_convert_vic(file_url: str, for_iframe: bool = False):
    """
    Download an image from a public URL or decode base64 data, and convert it to VIC format.
    """
    temp_file_path = None
    output_file_path = None

    try:
        if file_url.startswith("data:image/"):
            match = re.match(r"data:image/(.+);base64,(.+)", file_url)
            if not match:
                raise HTTPException(status_code=400, detail="Invalid base64 image format.")
            image_format = match.group(1)
            image_data = base64.b64decode(match.group(2))

            if image_format not in ["png", "jpeg", "bmp", "gif", "tiff"]:
                raise HTTPException(status_code=400, detail=f"Unsupported format: {image_format}")

            with NamedTemporaryFile(delete=False, suffix=f".{image_format}") as temp_file:
                temp_file.write(image_data)
                temp_file_path = temp_file.name
        else:
            if not validators.url(file_url):
                raise HTTPException(status_code=400, detail="Invalid URL provided.")
            response = requests.get(file_url, stream=True)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail="The provided URL does not point to an image.")

            extension = content_type.split("/")[1]
            with NamedTemporaryFile(delete=False, suffix=f".{extension}") as temp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

        if not is_supported_image(temp_file_path):
            raise HTTPException(status_code=400, detail="Unsupported or corrupted image format.")

        output_file_path = temp_file_path.replace(os.path.splitext(temp_file_path)[1], ".vic")
        convert_to_my_format(temp_file_path, output_file_path, for_iframe=for_iframe)

        return FileResponse(output_file_path, media_type="application/octet-stream", filename="output.vic")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during conversion: {str(e)}")
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if output_file_path and os.path.exists(output_file_path):
            os.remove(output_file_path)

@app.get("/generate-iframe")
def generate_iframe(
    file_url: str = Query(..., description="Public URL where the .vic file is hosted."),
    width: int = Query(560, description="Width of the iframe in pixels."),
    height: int = Query(315, description="Height of the iframe in pixels."),
):
    """
    Generate an iframe to display a VIC file using vic-viewer.html.
    """
    viewer_url = "https://vicfile.io/static/vic-viewer.html"
    iframe_code = f"""
    <iframe src="{viewer_url}?file={file_url}" width="{width}" height="{height}"
    frameborder="0" style="overflow:auto;" allowfullscreen></iframe>
    """
    return HTMLResponse(content=iframe_code)

@app.get("/vic-viewer.html")
async def serve_viewer():
    return FileResponse("vic-viewer.html")

@app.get("/sitemap.xml", response_class=FileResponse)
async def serve_sitemap():
    return FileResponse("sitemap.xml")
