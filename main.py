import os
from fastapi import FastAPI, File, UploadFile, Query, Header
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from tempfile import NamedTemporaryFile
from convert_to_my_format import convert_to_my_format
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException
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

@app.get("/service-worker.js", include_in_schema=False)
async def serve_service_worker():
    """
    Serve the service worker file.
    """
    return FileResponse(os.path.join(STATIC_DIR, "service-worker.js"))

from fastapi import Header

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

import base64
import re

@app.post("/fetch-and-convert-vic")
def fetch_and_convert_vic(file_url: str, for_iframe: bool = False):
    """
    Download a PNG image from a public URL or decode a base64 URL, and convert it to VIC format.

    Parameters:
    - file_url (str): Public URL of the PNG image or base64 encoded data.
    - for_iframe (bool): Optimize the image for iframe display if True.

    Returns:
    - The generated .vic file as a response.
    
    Note:
    If using base64, the image must be in PNG format.
    """
    temp_file_path = None
    output_file_path = None

    try:
        # Handle Base64 input
        if file_url.startswith("data:image/"):
            # Validate and extract Base64 image data
            match = re.match(r"data:image/(png);base64,(.+)", file_url)
            if not match:
                raise HTTPException(status_code=400, detail="Invalid base64 image format.")
            
            image_format = match.group(1)
            if image_format != "png":
                raise HTTPException(status_code=400, detail="Only PNG images are supported for base64 input.")
            
            # Decode Base64 image data
            image_data = base64.b64decode(match.group(2))
            
            # Save the decoded data as a temporary PNG file
            with NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                temp_file.write(image_data)
                temp_file_path = temp_file.name
        else:
            # Handle URL input
            if not validators.url(file_url):
                raise HTTPException(status_code=400, detail="Invalid URL provided.")

            # Fetch the image from the URL
            response = requests.get(file_url, stream=True)
            response.raise_for_status()  # Ensure the request was successful

            # Check Content-Type header
            content_type = response.headers.get('Content-Type', '')
            if 'image/png' not in content_type:
                raise HTTPException(status_code=400, detail="The provided URL does not point to a PNG image.")

            # Save the downloaded PNG image
            with NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

        # Define the output path for the VIC file
        output_file_path = temp_file_path.replace(".png", ".vic")

        # Convert the image to VIC format
        convert_to_my_format(temp_file_path, output_file_path, for_iframe=for_iframe)

        # Return the generated VIC file
        return FileResponse(output_file_path, media_type="application/octet-stream", filename="output.vic")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching the file: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during conversion: {str(e)}")
    finally:
        # Clean up temporary files
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

# Héberger visionneuse.html à la racine
@app.get("/vic-viewer.html")
async def serve_viewer():
    return FileResponse("vic-viewer.html")

@app.get("/sitemap.xml", response_class=FileResponse)
async def serve_sitemap():
    return FileResponse("sitemap.xml")