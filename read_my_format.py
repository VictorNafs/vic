import struct
import json
import argparse

def read_my_format(file_path, save_image=False):
    with open(file_path, 'rb') as f:
        # Read signature
        signature = f.read(3).decode('utf-8')
        if signature != "VIC":
            raise ValueError("Invalid file signature.")

        # Read version
        version = struct.unpack('B', f.read(1))[0]

        # Read dimensions
        original_width, original_height = struct.unpack('II', f.read(8))

        # Read metadata
        metadata_size = struct.unpack('I', f.read(4))[0]
        metadata_json = f.read(metadata_size).decode('utf-8')
        metadata = json.loads(metadata_json)

        # Read image data
        img_data_size = struct.unpack('I', f.read(4))[0]
        img_data = f.read(img_data_size)

        # Check EOF
        eof = f.read(4)
        if eof != b"EOF\0":
            raise ValueError("File end marker not found.")

    # Print file information
    print(f"File: {file_path}")
    print(f"Signature: {signature}")
    print(f"Version: {version}")
    print(f"Original Dimensions: {original_width}x{original_height}")
    print(f"Metadata: {json.dumps(metadata, indent=2)}")
    print(f"Image data size: {img_data_size} bytes")

    # Optionally save the extracted image data
    if save_image:
        output_image_path = file_path.replace(".vic", ".png")
        with open(output_image_path, 'wb') as img_file:
            img_file.write(img_data)
        print(f"Extracted image saved as: {output_image_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read and analyze a VIC file.")
    parser.add_argument("file_path", help="Path to the VIC file to analyze.")
    parser.add_argument("--save_image", action="store_true", help="Save the extracted image as a PNG file.")
    args = parser.parse_args()

    read_my_format(args.file_path, save_image=args.save_image)
