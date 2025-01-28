import argparse
import struct
import json
import os
from PIL import Image, ImageOps
import io

def compress_input_image(input_file_path, temp_file_path, max_width):
    """
    Compresse et redimensionne l'image en entrée si nécessaire.
    """
    with Image.open(input_file_path) as img:
        img = img.convert("RGB")  # Supprime les canaux alpha inutiles
        if img.size[0] > max_width:  # Redimensionne si la largeur dépasse la limite
            scale_factor = max_width / img.size[0]
            new_height = int(img.size[1] * scale_factor)
            img = img.resize((max_width, new_height), Image.LANCZOS)
        # Compression PNG sans perte
        img.save(temp_file_path, format="PNG", optimize=True)


def convert_to_my_format(input_file, output_file, max_width=2000, max_height=2000, for_iframe=False):
    """
    Convertit une image en entrée au format VIC personnalisé, avec compression et métadonnées intégrées.
    """
    try:
        print(f"Processing input file: {input_file}")
        
        # Étape 1 : Compression et prétraitement
        temp_compressed_file = f"{input_file}.compressed.png"
        compress_input_image(input_file, temp_compressed_file, max_width)
        input_file = temp_compressed_file  # Utilise l'image compressée
        
        # Étape 2 : Ouverture de l'image
        with Image.open(input_file) as img:
            original_width, original_height = img.size
            print(f"Original dimensions: {original_width}x{original_height}")

            # Détection de screenshots pleine page
            ratio = original_height / original_width
            is_full_page_screenshot = ratio > 4
            print(f"Full-page screenshot detected: {is_full_page_screenshot}")

            # Optimisation des dimensions
            if is_full_page_screenshot:
                print("Adjusting dimensions for full-page screenshot...")
                new_width = min(max_width * 2, 4000)
                scale_factor = new_width / original_width
                new_height = int(original_height * scale_factor)
            elif original_width > max_width or original_height > max_height:
                print(f"Resizing image to fit within {max_width}x{max_height}...")
                img = ImageOps.contain(img, (max_width, max_height))
                new_width, new_height = img.size
            else:
                new_width, new_height = original_width, original_height

            print(f"New dimensions: {new_width}x{new_height}")

            # Resize image seulement si les dimensions changent
            if new_width != original_width or new_height != original_height:
                img = img.resize((new_width, new_height), Image.LANCZOS)

            # Sauvegarde dans un buffer PNG compressé
            png_buffer = io.BytesIO()
            img.save(png_buffer, format="PNG", optimize=True, compress_level=9)
            img_data = png_buffer.getvalue()
            png_buffer.close()
            print(f"Image successfully saved to PNG buffer. Size: {len(img_data)} bytes")

        # Étape 3 : Construction des métadonnées
        metadata = {
            "scroll": "vertical" if is_full_page_screenshot or for_iframe else "none",
            "width": "iframe" if for_iframe else "screen",
            "type": "full_page_screenshot" if is_full_page_screenshot else "regular_image",
            "ratio": round(ratio, 2),
            "dimensions": {"width": new_width, "height": new_height},
            "format": "PNG"  # Indique le format PNG
        }
        metadata_json = json.dumps(metadata, separators=(',', ':')).encode('utf-8')
        print(f"Metadata: {metadata}")

        # Étape 4 : Écriture du fichier VIC
        with open(output_file, 'wb') as f:
            f.write(b"VIC")  # Signature
            f.write(struct.pack('B', 1))  # Version
            f.write(struct.pack('II', original_width, original_height))  # Dimensions originales
            f.write(struct.pack('I', len(metadata_json)))  # Taille des métadonnées
            f.write(metadata_json)  # Métadonnées
            f.write(struct.pack('I', len(img_data)))  # Taille des données image
            f.write(img_data)  # Données PNG
            f.write(b"EOF\0")  # Marqueur de fin
            print(f"Output file {output_file} successfully written!")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Nettoyage des fichiers temporaires
        if os.path.exists(temp_compressed_file):
            os.remove(temp_compressed_file)

# Command-line interface
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
