# .vic Project

**.vic** is an innovative file format designed for full-page screenshots, offering an optimized user experience with smooth scrolling and automatic width adaptation for screens. This public repository serves to inform potential contributors on how to join the project and contribute to its development.

---

## Key Features

- Convert PNG images into the `.vic` format with optimized compression (WebP).
- HTML/CSS/JavaScript viewer to display `.vic` files.
- User-friendly tools (CLI and GUI) for seamless usage.
- A lightweight format designed for quick sharing and social media compatibility.

---

## Project Structure

The project is organized as follows:

project/ ├── convert_to_my_format.py # CLI converter to create .vic files ├── convert_gui.py # Graphical interface for file conversion ├── compare_sizes.py # Size comparison tool between original and converted files ├── read_my_format.py # Tool to read and validate .vic files ├── visionneuse.html # HTML viewer to display .vic files in a browser ├── README.md # Project documentation └── examples/ # Folder containing example images and .vic files ├── example.png └── example.vic

yaml
Copier le code

---

## How to Use the Tools

### 1. **CLI Converter**
The `convert_to_my_format.py` script allows you to convert a PNG file into the `.vic` format via the command line.

**Example usage:**
```bash
python convert_to_my_format.py example.png example.vic --quality 80 --max_width 2000 --max_height 3000
Available options:

--quality: WebP compression quality (default: 75).
--max_width: Maximum image width (default: 2000 pixels).
--max_height: Maximum image height (default: 2000 pixels).
2. Graphical User Interface (GUI)
The convert_gui.py script provides a simple graphical interface for file conversion without needing to use the command line.

Steps:

Run the script:
bash
Copier le code
python convert_gui.py
Use the interface to:
Select an input file (.png).
Define the output file path (.vic).
Adjust parameters like quality and maximum dimensions.
3. HTML Viewer
The visionneuse.html file enables .vic file display directly in a browser.

How to use:

Open visionneuse.html in your browser.
Load a .vic file through the interface to view the image and its metadata.
4. File Validation
The read_my_format.py script is designed to read .vic files and check their validity.

Example usage:

bash
Copier le code
python read_my_format.py example.vic
This script displays metadata, dimensions, and the size of the image data.

How to Contribute
We welcome contributions! Here’s how you can participate:

Submit a Request: Contact us at cmoikvolelorange.com or open an issue in this repository explaining why you want to participate.
Receive an Invitation: If your request is accepted, you will receive an invitation to access the private repository containing the full application.
Start Contributing: Once you have access to the repository, follow the instructions to begin contributing.
Contributions and Feedback
See the CONTRIBUTING.md file for detailed contribution guidelines.
Feel free to submit issues or pull requests to report bugs or suggest improvements.
Code of Conduct
This project adheres to a Code of Conduct that all contributors are expected to follow.

Thank you for your interest in the .vic project! We look forward to collaborating with you.

markdown
Copier le code

---

### **Changes and Highlights:**
1. **Consistent English translation**: Maintained clarity while ensuring accurate context.
2. **Expanded tool usage**: Clear instructions for CLI, GUI, and viewer tools.
3. **Professional formatting**: Structured for easy navigation.
4. **Contribution process**: Streamlined explanation for contributors.

If you’d like additional adjustments or need help creating any linked files (`CONTRIBUTING.md`, `