import argparse
import struct
import json
import os
import gc
from PIL import Image, ImageOps
import io

def get_compression_level(file_size):
    """ Détermine le niveau de compression en fonction de la taille du fichier d'entrée """
    if file_size > 10_000_000:
        return 50  # Compression forte
    elif file_size > 5_000_000:
        return 75  # Compression moyenne
    return 95  # Haute qualité

def compress_input_image(input_file_path, temp_file_path, max_width):
    """ Compresse et redimensionne l'image en entrée si nécessaire en flux """
    with Image.open(input_file_path) as img:
        img = img.convert("RGB")  # Suppression des canaux alpha inutiles
        
        # Réduction efficace en mémoire
        reduction_factor = max(img.size[0] // max_width, 1)
        img = img.reduce(reduction_factor)
        
        # Déterminer la compression dynamique
        compression_quality = get_compression_level(os.path.getsize(input_file_path))
        
        # Écriture directe dans un fichier sans stocker en RAM
        img.save(temp_file_path, format="JPEG", quality=compression_quality, optimize=True, progressive=True)

def convert_to_my_format(input_file, output_file, max_width=2000, max_height=2000, for_iframe=False):
    """ Convertit une image en .VIC avec optimisation mémoire """
    try:
        print(f"Processing input file: {input_file}")
        temp_compressed_file = f"{input_file}.compressed.jpg"
        compress_input_image(input_file, temp_compressed_file, max_width)
        input_file = temp_compressed_file
        
        with Image.open(input_file) as img:
            original_width, original_height = img.size
            ratio = original_height / original_width
            is_full_page_screenshot = ratio > 4
            print(f"Full-page screenshot detected: {is_full_page_screenshot}")
            
            new_width = max_width
            scale_factor = new_width / original_width
            new_height = int(original_height * scale_factor)
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
            png_buffer = io.BytesIO()
            img.save(png_buffer, format="PNG", optimize=True, compress_level=9)
            img_data = png_buffer.getvalue()
            png_buffer.close()
            
        metadata = {
            "scroll": "vertical" if is_full_page_screenshot or for_iframe else "none",
            "width": "screen",  # Ajustement automatique à la largeur de l'écran
            "type": "full_page_screenshot" if is_full_page_screenshot else "regular_image",
            "ratio": round(ratio, 2),
            "dimensions": {"width": new_width, "height": new_height},
            "format": img.format  # Détection dynamique du format
        }
        metadata_json = json.dumps(metadata, separators=(',', ':')).encode('utf-8')
        
        with open(output_file, 'wb') as f:
            f.write(b"VIC")
            f.write(struct.pack('B', 1))
            f.write(struct.pack('II', original_width, original_height))
            f.write(struct.pack('I', len(metadata_json)))
            f.write(metadata_json)
            f.write(struct.pack('I', len(img_data)))
            f.write(img_data)
            f.write(b"EOF\0")
        
        print(f"Output file {output_file} successfully written!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if os.path.exists(temp_compressed_file):
            os.remove(temp_compressed_file)
        gc.collect()

def main():
    parser = argparse.ArgumentParser(description="Convert an image to VIC format.")
    parser.add_argument("input_file", help="Path to the input file.")
    parser.add_argument("output_file", help="Path to the output file (VIC format).")
    parser.add_argument("--max_width", type=int, default=2000, help="Maximum width (default: 2000 pixels).")
    parser.add_argument("--max_height", type=int, default=2000, help="Maximum height (default: 2000 pixels).")
    parser.add_argument("--for_iframe", action="store_true", help="Optimize dimensions for iframe embedding.")
    
    args = parser.parse_args()
    convert_to_my_format(args.input_file, args.output_file, args.max_width, args.max_height, args.for_iframe)

if __name__ == "__main__":
    main()