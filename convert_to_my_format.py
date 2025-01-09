import argparse
import struct
import json
from PIL import Image, ImageOps
import io

def convert_to_my_format(input_file, output_file, quality=75, max_width=2000, max_height=2000):
    with Image.open(input_file) as img:
        width, height = img.size

        # Redimensionner si l'image dépasse les dimensions maximales
        if width > max_width or height > max_height:
            print(f"Redimensionnement : {width}x{height} vers {max_width}x{max_height}")
            img = ImageOps.contain(img, (max_width, max_height))

        # Convertir l'image en WebP compressé
        webp_buffer = io.BytesIO()
        img.save(webp_buffer, format="WEBP", quality=quality)
        img_data = webp_buffer.getvalue()
        webp_buffer.close()

    # Construire les métadonnées
    metadata = {"scroll": "vertical", "width": "screen"}
    metadata_json = json.dumps(metadata).encode('utf-8')

    # Construire le fichier binaire
    with open(output_file, 'wb') as f:
        f.write(b"VIC")  # Signature corrigée
        f.write(struct.pack('B', 1))  # Version
        f.write(struct.pack('II', width, height))  # Dimensions
        f.write(struct.pack('I', len(metadata_json)))  # Taille des métadonnées
        f.write(metadata_json)  # Métadonnées
        f.write(struct.pack('I', len(img_data)))  # Taille des données d'image
        f.write(img_data)  # Données de l'image
        f.write(b"EOF\0")  # Fin de fichier

    print(f"Conversion terminée : {output_file}")

# Interface en ligne de commande
def main():
    parser = argparse.ArgumentParser(description="Convertir une image PNG en format VIC.")
    parser.add_argument("input_file", help="Chemin du fichier d'entrée (PNG).")
    parser.add_argument("output_file", help="Chemin du fichier de sortie (VIC).")
    parser.add_argument("--quality", type=int, default=75, help="Qualité de compression WebP (par défaut : 75).")
    parser.add_argument("--max_width", type=int, default=2000, help="Largeur maximale (par défaut : 2000 pixels).")
    parser.add_argument("--max_height", type=int, default=2000, help="Hauteur maximale (par défaut : 2000 pixels).")

    args = parser.parse_args()

    convert_to_my_format(args.input_file, args.output_file, args.quality, args.max_width, args.max_height)

if __name__ == "__main__":
    main()
