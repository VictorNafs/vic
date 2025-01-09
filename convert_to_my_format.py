import struct
import json
from PIL import Image, ImageOps  # Importer Image et ImageOps
import io


def convert_to_my_format(input_file, output_file, quality=75, max_width=2000, max_height=2000):
    # Vérifier que l'entrée est un fichier PNG
    if not input_file.endswith(".png"):
        raise ValueError("Seuls les fichiers PNG sont acceptés pour le moment.")

    # Ouvrir l'image source
    with Image.open(input_file) as img:
        width, height = img.size

        # Redimensionner si l'image dépasse les dimensions maximales
        if width > max_width or height > max_height:
            print(f"Redimensionnement : {width}x{height} vers {max_width}x{max_height}")
            img = ImageOps.contain(img, (max_width, max_height))

        # Convertir l'image en WebP compressé (dans un buffer mémoire)
        webp_buffer = io.BytesIO()
        img.save(webp_buffer, format="WEBP", quality=quality)  # Compression WebP
        img_data = webp_buffer.getvalue()  # Récupérer les données compressées
        webp_buffer.close()

    # Construire la section de métadonnées
    metadata = {
        "scroll": "vertical",
        "width": "screen"
    }
    metadata_json = json.dumps(metadata).encode('utf-8')  # Convertir en JSON binaire

    # Construire le fichier binaire
    with open(output_file, 'wb') as f:
        # 1. Signature
        f.write(b"MYFT")
        # 2. Version
        f.write(struct.pack('B', 1))  # Version 1
        # 3. Dimensions
        f.write(struct.pack('II', width, height))  # Largeur et hauteur (4 octets chacun)
        # 4. Métadonnées
        f.write(struct.pack('I', len(metadata_json)))  # Taille des métadonnées
        f.write(metadata_json)  # Les métadonnées elles-mêmes
        # 5. Données de l'image
        f.write(struct.pack('I', len(img_data)))  # Taille des données d'image
        f.write(img_data)  # Les données compressées en WebP
        # 6. Fin du fichier
        f.write(b"EOF\0")

    # Informations de confirmation
    print(f"Conversion terminée : {output_file}")
    print(f"Dimensions originales : {width}x{height}")
    print(f"Dimensions redimensionnées : {img.size}")
    print(f"Taille des métadonnées : {len(metadata_json)} octets")
    print(f"Taille des données compressées (WebP) : {len(img_data)} octets")


# Exemple d'utilisation
convert_to_my_format("img2.png", "img2.myft")
