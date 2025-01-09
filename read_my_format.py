def read_my_format(file_path):
    with open(file_path, 'rb') as f:
        # 1. Lire la signature
        signature = f.read(4)
        if signature != b"MYFT":
            raise ValueError("Fichier invalide ou signature non reconnue.")

        # 2. Lire la version
        version = struct.unpack('B', f.read(1))[0]

        # 3. Lire les dimensions
        width, height = struct.unpack('II', f.read(8))

        # 4. Lire les métadonnées
        metadata_size = struct.unpack('I', f.read(4))[0]
        metadata_json = f.read(metadata_size).decode('utf-8')
        metadata = json.loads(metadata_json)

        # 5. Lire les données de l'image
        img_data_size = struct.unpack('I', f.read(4))[0]
        img_data = f.read(img_data_size)

        # 6. Vérifier la fin du fichier
        eof = f.read(4)
        if eof != b"EOF\0":
            raise ValueError("Fin de fichier incorrecte.")

    print(f"Lecture terminée : {file_path}")
    print(f"Signature : {signature}")
    print(f"Version : {version}")
    print(f"Dimensions : {width}x{height}")
    print(f"Métadonnées : {metadata}")
    print(f"Taille des données d'image : {img_data_size} octets")
