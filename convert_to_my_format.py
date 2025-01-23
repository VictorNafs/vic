import argparse
import struct
import json
import os
from PIL import Image, ImageOps
import io
from tempfile import NamedTemporaryFile


def convert_to_my_format(input_file, output_file, quality=75, max_width=2000, max_height=2000, for_iframe=False):
    try:
        print(f"Processing input file: {input_file}")

        # Open the image file and validate the format
        with Image.open(input_file) as img:
            original_width, original_height = img.size
            format = img.format  # Detect input format (e.g., PNG, JPEG, etc.)
            print(f"Original dimensions: {original_width}x{original_height}, Format: {format}")

            # Convert unsupported formats to PNG or JPEG
            if format.lower() in ["bmp", "gif", "tiff"]:
                print(f"Converting {format} to PNG for better compression...")
                img = img.convert("RGB")  # Convert to RGB for compatibility
                format = "PNG"

            # Immediate resizing for extremely large images
            max_initial_size = 4000
            if original_width > max_initial_size or original_height > max_initial_size:
                print("Image is extremely large, resizing for memory optimization...")
                scale_factor = min(max_initial_size / original_width, max_initial_size / original_height)
                img = img.resize(
                    (int(original_width * scale_factor), int(original_height * scale_factor)),
                    Image.LANCZOS
                )
                print(f"Initial resized dimensions: {img.size[0]}x{img.size[1]}")

            # Detect full-page screenshots
            ratio = original_height / original_width
            is_full_page_screenshot = ratio > 4
            print(f"Full-page screenshot detected: {is_full_page_screenshot}")

            # Resize to fit within the maximum dimensions
            if for_iframe or original_width > max_width or original_height > max_height:
                print(f"Resizing image to fit within {max_width}x{max_height}...")
                img = ImageOps.contain(img, (max_width, max_height))
                print(f"Final resized dimensions: {img.size[0]}x{img.size[1]}")

            # Save the image as PNG in memory (universal format for processing)
            png_buffer = io.BytesIO()
            try:
                img.save(png_buffer, format="PNG", optimize=True, compress_level=9)  # High compression
                img_data = png_buffer.getvalue()
                png_buffer.close()
                print(f"Image successfully saved to PNG buffer. Size: {len(img_data)} bytes")
            except Exception as e:
                print(f"Error saving image to PNG buffer: {e}")
                return

        # Build metadata
        metadata = {
            "scroll": "vertical" if is_full_page_screenshot or for_iframe else "none",
            "width": "iframe" if is_full_page_screenshot or for_iframe else "screen",
            "type": "full_page_screenshot" if is_full_page_screenshot else "iframe_image" if for_iframe else "regular_image",
            "ratio": ratio,
            "dimensions": {"width": img.size[0], "height": img.size[1]},
            "format": format  # Include original format
        }
        metadata_json = json.dumps(metadata).encode('utf-8')
        print(f"Metadata: {metadata}")

        # Write the VIC file
        with open(output_file, 'wb') as f:
            f.write(b"VIC")  # Signature
            f.write(struct.pack('B', 1))  # Version
            f.write(struct.pack('II', original_width, original_height))  # Original dimensions
            f.write(struct.pack('I', len(metadata_json)))  # Metadata size
            f.write(metadata_json)  # Metadata
            f.write(struct.pack('I', len(img_data)))  # Image data size
            f.write(img_data)  # Image data
            f.write(b"EOF\0")  # End of file marker
            print(f"Output file {output_file} successfully written!")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def compress_image(input_file, max_size_in_mb=5):
    """
    Compress an image to ensure it does not exceed a specified size.
    """
    max_size_in_bytes = max_size_in_mb * 1024 * 1024
    with Image.open(input_file) as img:
        format = img.format  # Detect original format
        quality = 85  # Start with high quality
        temp_buffer = io.BytesIO()

        # Resizing extremely large images before compression
        max_initial_size = 4000
        original_width, original_height = img.size
        if original_width > max_initial_size or original_height > max_initial_size:
            print("Compressing and resizing very large image before processing...")
            scale_factor = min(max_initial_size / original_width, max_initial_size / original_height)
            img = img.resize((int(original_width * scale_factor), int(original_height * scale_factor)), Image.LANCZOS)

        # Save based on format with reduced quality for JPEG
        if format.lower() in ["jpeg", "jpg"]:
            img.save(temp_buffer, format="JPEG", quality=quality, optimize=True)
        elif format.lower() == "png":
            img.save(temp_buffer, format="PNG", optimize=True, compress_level=9)
        else:
            img.save(temp_buffer, format=format)

        size_in_bytes = temp_buffer.tell()

        # Iteratively reduce quality for large files
        while size_in_bytes > max_size_in_bytes and quality > 10:
            temp_buffer.seek(0)
            if format.lower() in ["jpeg", "jpg"]:
                img.save(temp_buffer, format="JPEG", quality=quality)
            else:
                img.save(temp_buffer, format=format)
            size_in_bytes = temp_buffer.tell()
            quality -= 10

        # Save the compressed image to a temporary file
        temp_output = NamedTemporaryFile(delete=False, suffix=f".{format.lower()}")
        temp_output.write(temp_buffer.getvalue())
        temp_output.close()

        return temp_output.name


def is_supported_image(file_path):
    """
    Check if a file is a supported image format.
    """
    try:
        with Image.open(file_path) as img:
            img.verify()  # Verify that it's a valid image
        return True
    except Exception:
        return False


if __name__ == "__main__":
    main()
