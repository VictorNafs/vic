# .vic Project

.vic is an innovative file format designed for full-page screenshots, providing a seamless user experience with smooth vertical scrolling and automatic width adaptation for screens. This repository contains tools, documentation, and examples to help users and contributors work with the .vic format.

## Key Features

- Convert PNG images into .vic format with optimized compression and metadata.
- Browser-based viewer (`visionneuse.html`) for displaying .vic files.
- Tools for file conversion and validation:
  - Command-line interface (CLI).
  - Graphical user interface (GUI).
  - File validation and size comparison scripts.
- Lightweight format optimized for quick sharing and compatibility with social media.

## Project Structure

```
project/
├── convert_to_my_format.py   # CLI tool to create .vic files
├── convert_gui.py            # GUI for file conversion
├── compare_sizes.py          # Compare sizes of original and converted files
├── read_my_format.py         # Validate and read .vic file contents
├── visionneuse.html          # HTML viewer for displaying .vic files
├── README.md                 # Project documentation
└── examples/                 # Example images and .vic files
    ├── example.png
    └── example.vic
```

## How to Use the Tools

### 1. CLI Converter

The `convert_to_my_format.py` script converts PNG files into .vic format via the command line.

**Usage:**

```bash
python convert_to_my_format.py input.png output.vic
```

**Options:**

- `--quality`: Compression quality (default: 75).
- `--max_width`: Maximum image width (default: 2000 pixels).
- `--max_height`: Maximum image height (default: 2000 pixels).

### 2. Graphical User Interface (GUI)

The `convert_gui.py` script provides a simple GUI for file conversion.

**Steps:**

1. Run the GUI:

   ```bash
   python convert_gui.py
   ```

2. Use the interface to:
   - Select a `.png` file as input.
   - Specify the output file path (e.g., `output.vic`).
   - Click "Convert" to generate the `.vic` file.

### 3. HTML Viewer

The `visionneuse.html` file allows you to view `.vic` files directly in your browser.

**Steps:**

1. Open `visionneuse.html` in your browser.
2. Use the interface to load a `.vic` file.
3. View the image along with its metadata.

### 4. File Validation

The `read_my_format.py` script reads and validates `.vic` files, displaying metadata, dimensions, and image size.

**Usage:**

```bash
python read_my_format.py file.vic [--save_image]
```

- Add `--save_image` to extract the PNG image from the `.vic` file.

### 5. Size Comparison

The `compare_sizes.py` script compares the sizes of an original PNG file and its `.vic` counterpart.

**Usage:**

```bash
python compare_sizes.py original.png converted.vic
```

## How to Contribute

We welcome contributions to the .vic project! Here's how you can get involved:

1. **Submit a Request:** Contact us at `cmoikvolelorange.com` or open an issue in this repository explaining your interest in contributing.
2. **Receive an Invitation:** Once your request is approved, you’ll gain access to the private repository.
3. **Start Contributing:** Follow the guidelines provided in the private repository.

## Contributions and Feedback

- See the `CONTRIBUTING.md` file for details on how to contribute.
- Submit issues or pull requests to report bugs or suggest improvements.

## Code of Conduct

This project adheres to a Code of Conduct. All contributors are expected to follow it.

## Acknowledgments

Thank you for your interest in the .vic project! We look forward to collaborating with you and making .vic a powerful and widely adopted format.

---

### What’s Next?

Let me know if you’d like additional adjustments or help with creating supporting files like `CONTRIBUTING.md` or `CODE_OF_CONDUCT.md`. 😊
