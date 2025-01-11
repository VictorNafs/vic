# **FastAPI - Converter and Viewer for VIC Files**

This application is a **FastAPI designed to convert PNG images, especially full-page screenshots**, into a custom `.vic` format. This format offers unique advantages in terms of **adaptive resizing** and **iframe embedding** with smooth vertical scrolling.

---

## **Introduction to the `.vic` Format**

The `.vic` files are designed to solve common issues encountered with full-page screenshots:

1. **Issues with Standard PNGs**:
   - Long screenshots are resized to fit standard screen sizes.
   - Images become unreadable without zooming as they shrink excessively.

2. **Advantages of the `.vic` Format**:
   - **Adaptive Resizing**:
     - `.vic` images automatically adjust to the width of screens or iframes, whether on mobile devices, tablets, or desktops.
   - **Integrated Scrolling**:
     - A **vertical scroll** is added to display the entire screenshot regardless of its height.
   - **Flexible Dimensions**:
     - The dimensions can be controlled via an iframe.

---

## **Main Features**

1. **PNG → VIC Conversion**
   - Converts PNG images, especially screenshots, into the `.vic` format.
   - Automatically resizes images to adapt to screens or iframes.

2. **Metadata Extraction**
   - Extracts details such as original dimensions, file type (screenshot or regular image), and other information.

3. **VIC File Preview**
   - Streams the PNG embedded in `.vic` files.

4. **Iframe Generation**
   - Generates an iframe to easily integrate `.vic` files into web pages.

5. **Conversion from a Public URL**
   - Downloads an image from its URL (e.g., a Google image) and converts it to `.vic`.

---

## **Step-by-Step Guide**

### **1. Installation**

1. **Clone the Project**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
Install Dependencies:
Ensure Python 3.8+ is installed, then run:

bash
Copier le code
pip install -r requirements.txt
Start the Application:

bash
Copier le code
uvicorn main:app --host 0.0.0.0 --port 8000
The application will be accessible at http://<your-ip>:8000.

2. Using the Features
2.1. PNG → VIC Conversion
Access the /convert endpoint using a tool like Postman or directly via the Swagger UI interface available at http://<your-ip>:8000/docs.
Upload a PNG file with the following parameters:
File: A PNG image.
For iframe (optional): Specify true to optimize the file for an iframe.
The API will return a .vic file ready for download.

2.2. Metadata Extraction
Access /metadata to extract metadata from a .vic file.
Upload a .vic file via POST, and receive the following information:
Original and adjusted dimensions.
File type (regular image or screenshot).
Aspect ratio.
Image format.
2.3. VIC File Preview
Access /preview to view the image embedded in a .vic file.
Upload a .vic file to receive a PNG image.
2.4. Iframe Generation
Access /generate-iframe and provide the public URL of a .vic file to generate an HTML iframe.
Example:

bash
Copier le code
http://<your-ip>:8000/generate-iframe?file_url=http://<your-ip>:8000/static/sample.vic
The API will return the following HTML code:

html
Copier le code
<iframe src="http://<your-ip>:8000/static/vic-viewer.html?file=http://<your-ip>:8000/static/sample.vic" width="560" height="315" frameborder="0" allowfullscreen></iframe>
2.5. Conversion from a Public URL
Access /fetch-vic and provide the URL of a public image (e.g., a Google image):
bash
Copier le code
http://<your-ip>:8000/fetch-vic?file_url=<image-url>
The image will be downloaded and converted to .vic.
3. Web Interfaces
Detailed Viewer: visionneuse.html
A feature-rich interface to display .vic files and their metadata.
Accessible at: http://<your-ip>:8000/static/visionneuse.html.
Iframe Viewer: vic-viewer.html
A minimalist interface tailored for iframes.
Accessible at: http://<your-ip>:8000/static/vic-viewer.html?file=<file-url>.
4. Iframe Example
To embed a .vic image in a website:

html
Copier le code
<iframe
  src="http://<your-ip>:8000/static/vic-viewer.html?file=http://<your-ip>:8000/static/sample.vic"
  width="560"
  height="315"
  frameborder="0"
  allowfullscreen>
</iframe>
5. Important Notes
Static Files:
.vic files must be placed in the static directory to be served correctly.

CORS:
If you embed the iframe on another site, configure the CORS headers accordingly.

6. Project Structure
csharp
Copier le code
heroku/
├── compare_sizes.py       # Compare image dimensions
├── convert_to_my_format.py # PNG → VIC Conversion
├── main.py                # Main FastAPI Application
├── read_my_format.py      # Read VIC files
├── visionneuse.html       # Rich viewer
└── static/
    └── vic-viewer.html    # Minimalist iframe viewer