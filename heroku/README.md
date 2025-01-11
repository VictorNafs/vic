[🇫🇷 Lire en français](README.fr.md)

# **FastAPI - Converter and Viewer for VIC Files**

This application is a **FastAPI** service designed to convert PNG images, particularly full-page screenshots, into a custom `.vic` format. This format offers unique advantages in terms of **adaptive resizing** and **iframe embedding** with smooth vertical scrolling.

---

## **Introduction to the `.vic` Format**

The `.vic` files are designed to address common challenges with full-page screenshots:

### **1. Issues with Standard PNGs**
- Long screenshots are resized to fit standard screen sizes.
- Images become unreadable without zooming as they shrink excessively.

### **2. Advantages of the `.vic` Format**
- **Adaptive Resizing**:
  - `.vic` images automatically adjust to the width of screens or iframes, whether on mobile devices, tablets, or desktops.
- **Integrated Scrolling**:
  - A **vertical scroll** is added to display the entire screenshot regardless of its height.
- **Flexible Dimensions**:
  - Dimensions can be controlled via an iframe.

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

#### **1.1 Clone the Project**
```bash
git clone <repository-url>
cd <repository-directory>
```

#### **1.2 Install Dependencies**
Ensure Python 3.8+ is installed, then run:
```bash
pip install -r requirements.txt
```

#### **1.3 Start the Application**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
The application will be accessible at: `http://<your-ip>:8000`

---

### **2. Using the Features**

#### **2.1 PNG → VIC Conversion**
Access the `/convert` endpoint using a tool like Postman or the Swagger UI interface available at `http://<your-ip>:8000/docs`.

- **Parameters**:
  - `file`: A PNG image.
  - `for_iframe` (optional): Specify `true` to optimize the file for an iframe.

The API will return a `.vic` file ready for download.

#### **2.2 Metadata Extraction**
Access `/metadata` to extract metadata from a `.vic` file.

- **Steps**:
  - Upload a `.vic` file via POST.
  - Receive metadata such as:
    - Original and adjusted dimensions.
    - File type (regular image or screenshot).
    - Aspect ratio.
    - Image format.

#### **2.3 VIC File Preview**
Access `/preview` to view the image embedded in a `.vic` file.

- **Steps**:
  - Upload a `.vic` file to receive the embedded PNG image.

#### **2.4 Iframe Generation**
Access `/generate-iframe` and provide the public URL of a `.vic` file to generate an HTML iframe.

- **Example Request**:
  ```bash
  http://<your-ip>:8000/generate-iframe?file_url=http://<your-ip>:8000/static/sample.vic
  ```
- **Example Response**:
  ```html
  <iframe src="http://<your-ip>:8000/static/vic-viewer.html?file=http://<your-ip>:8000/static/sample.vic"
          width="560" height="315" frameborder="0" allowfullscreen></iframe>
  ```

#### **2.5 Conversion from a Public URL**
Access `/fetch-vic` and provide the URL of a public image (e.g., a Google image).

- **Example Request**:
  ```bash
  http://<your-ip>:8000/fetch-vic?file_url=<image-url>
  ```
- The image will be downloaded and converted to `.vic`.

---

### **3. Web Interfaces**

#### **3.1 Detailed Viewer: `visionneuse.html`**
A feature-rich interface to display `.vic` files and their metadata.
- Accessible at: `http://<your-ip>:8000/static/visionneuse.html`

#### **3.2 Iframe Viewer: `vic-viewer.html`**
A minimalist interface tailored for iframes.
- Accessible at: `http://<your-ip>:8000/static/vic-viewer.html?file=<file-url>`

### **4. Iframe Example**

To embed a `.vic` image in a website:
```html
<iframe
  src="http://<your-ip>:8000/static/vic-viewer.html?file=http://<your-ip>:8000/static/sample.vic"
  width="560"
  height="315"
  frameborder="0"
  allowfullscreen>
</iframe>
```

---

## **Important Notes**

### **Static Files**
- `.vic` files must be placed in the `static` directory to be served correctly.

### **CORS**
- If you embed the iframe on another site, configure the CORS headers accordingly.

---

## **Project Structure**

```plaintext
project/
├── compare_sizes.py       # Compare image dimensions
├── convert_to_my_format.py # PNG → VIC Conversion
├── main.py                # Main FastAPI Application
├── read_my_format.py      # Read VIC files
├── visionneuse.html       # Rich viewer
└── static/
    └── vic-viewer.html    # Minimalist iframe viewer
```