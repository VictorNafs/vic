import argparse
import struct
import json
import os
from PIL import Image, ImageOps
import io

def convert_to_my_format(input_file, output_file, quality=75, max_width=2000, max_height=2000):
    try:
        print(f"Processing input file: {input_file}")
        with Image.open(input_file) as img:
            original_width, original_height = img.size
            print(f"Original dimensions: {original_width}x{original_height}")

            # Detect full-page screenshots
            ratio = original_height / original_width
            is_full_page_screenshot = ratio > 4
            print(f"Full-page screenshot detected: {is_full_page_screenshot}")

            # Adjust dimensions for full-page screenshots
            if is_full_page_screenshot:
                print("Adjusting dimensions for full-page screenshot...")
                new_width = min(max_width * 2, 4000)
                scale_factor = new_width / original_width
                new_height = int(original_height * scale_factor)
                img = img.resize((new_width, new_height), Image.LANCZOS)
                print(f"New dimensions: {new_width}x{new_height}")
            else:
                if original_width > max_width or original_height > max_height:
                    print(f"Resizing image to fit within {max_width}x{max_height}...")
                    img = ImageOps.contain(img, (max_width, max_height))
                    print(f"Resized dimensions: {img.size[0]}x{img.size[1]}")

            # Save the entire image as PNG
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
            "scroll": "vertical",
            "width": "screen",
            "type": "full_page_screenshot" if is_full_page_screenshot else "regular_image",
            "ratio": ratio,
            "dimensions": {"width": img.size[0], "height": img.size[1]},
            "format": "PNG"  # Indicate PNG format
        }
        metadata_json = json.dumps(metadata).encode('utf-8')
        print(f"Metadata: {metadata}")

        # Build binary file
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

# Command-line interface
def main():
    parser = argparse.ArgumentParser(description="Convert a PNG image to VIC format.")
    parser.add_argument("input_file", help="Path to the input file (PNG).")
    parser.add_argument("output_file", help="Path to the output file (VIC).")
    parser.add_argument("--quality", type=int, default=75, help="WebP compression quality (default: 75).")
    parser.add_argument("--max_width", type=int, default=2000, help="Maximum width (default: 2000 pixels).")
    parser.add_argument("--max_height", type=int, default=2000, help="Maximum height (default: 2000 pixels).")

    args = parser.parse_args()

    convert_to_my_format(args.input_file, args.output_file, args.quality, args.max_width, args.max_height)

if __name__ == "__main__":
    main()