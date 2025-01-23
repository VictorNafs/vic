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

            # Detect full-page screenshots
            ratio = original_height / original_width
            is_full_page_screenshot = ratio > 4
            print(f"Full-page screenshot detected: {is_full_page_screenshot}")

            # Adjust dimensions for full-page screenshots
            if is_full_page_screenshot:
                print("Adjusting dimensions for full-page screenshot...")
                new_width = min(max_width * 2, 4000)  # Larger width for full-page screenshots
                scale_factor = new_width / original_width
                new_height = int(original_height * scale_factor)
                img = img.resize((new_width, new_height), Image.LANCZOS)
                print(f"New dimensions (full-page): {new_width}x{new_height}")
            elif for_iframe:
                # Special resizing for iframe embedding
                print("Adjusting dimensions for iframe display...")
                new_width = max_width  # Constrain to iframe width
                scale_factor = new_width / original_width
                new_height = int(original_height * scale_factor)
                img = img.resize((new_width, new_height), Image.LANCZOS)
                print(f"New dimensions (iframe): {new_width}x{new_height}")
            else:
                # Regular image resizing
                if original_width > max_width or original_height > max_height:
                    print(f"Resizing image to fit within {max_width}x{max_height}...")
                    img = ImageOps.contain(img, (max_width, max_height))
                    print(f"Resized dimensions: {img.size[0]}x{img.size[1]}")

            # Save the image as PNG in memory (universal format for processing)
            png_buffer = io.BytesIO()
            try:
                img.save(png_buffer, format="PNG")
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
        quality = 95  # Start with high quality
        temp_buffer = io.BytesIO()

        # Save based on format
        if format.lower() in ["jpeg", "jpg"]:
            img.save(temp_buffer, format="JPEG", quality=quality)
        elif format.lower() in ["png"]:
            img.save(temp_buffer, format="PNG", optimize=True)
        else:
            img.save(temp_buffer, format=format)  # Fallback for other formats

        size_in_bytes = temp_buffer.tell()

        # Reduce quality iteratively for large files
        while size_in_bytes > max_size_in_bytes and quality > 10:
            temp_buffer.seek(0)
            if format.lower() in ["jpeg", "jpg"]:
                img.save(temp_buffer, format="JPEG", quality=quality)
            else:
                img.save(temp_buffer, format=format)  # No quality control for some formats
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

# Command-line interface
def main():
    parser = argparse.ArgumentParser(description="Convert an image to VIC format.")
    parser.add_argument("input_file", help="Path to the input file (image).")
    parser.add_argument("output_file", help="Path to the output file (VIC).")
    parser.add_argument("--quality", type=int, default=75, help="WebP compression quality (default: 75).")
    parser.add_argument("--max_width", type=int, default=2000, help="Maximum width (default: 2000 pixels).")
    parser.add_argument("--max_height", type=int, default=2000, help="Maximum height (default: 2000 pixels).")
    parser.add_argument("--for_iframe", action="store_true", help="Optimize dimensions for iframe embedding.")

    args = parser.parse_args()

    # Compress the input file if necessary
    compressed_file = compress_image(args.input_file, max_size_in_mb=5)
    try:
        convert_to_my_format(compressed_file, args.output_file, args.quality, args.max_width, args.max_height, args.for_iframe)
    finally:
        os.remove(compressed_file)  # Clean up temporary compressed file


if __name__ == "__main__":
    main()
