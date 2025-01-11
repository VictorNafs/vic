# .vic Project

.vic est un format de fichier innovant conçu pour les captures d'écran pleine page, offrant une expérience utilisateur fluide avec un défilement vertical et une adaptation automatique de la largeur aux écrans. Ce dépôt contient des outils, de la documentation et des exemples pour aider les utilisateurs et les contributeurs à travailler avec le format .vic.

[🇬🇧 Read in English](README.md)

---

## Fonctionnalités Clés

- Convertir des images PNG en format .vic avec une compression optimisée et des métadonnées.
- Visionneuse basée sur le navigateur (`visionneuse.html`) pour afficher les fichiers .vic.
- Outils pour la conversion et la validation des fichiers :
  - Interface en ligne de commande (CLI).
  - Interface graphique (GUI).
  - Scripts de validation et de comparaison des tailles de fichiers.
- Format léger optimisé pour un partage rapide et une compatibilité avec les réseaux sociaux.

---

## Structure du Projet

```plaintext
├── convert_to_my_format.py   # Outil CLI pour créer des fichiers .vic
├── convert_gui.py            # Interface graphique pour la conversion
├── compare_sizes.py          # Comparer les tailles des fichiers originaux et convertis
├── read_my_format.py         # Validation et lecture des fichiers .vic
├── visionneuse.html          # Visionneuse HTML pour afficher les fichiers .vic
├── LICENSE                   # Licence du projet
├── CONTRIBUTING.md           # Instructions pour contribuer
├── CODE_OF_CONDUCT.md        # Code de conduite des contributeurs
└── examples/                 # Exemples d'images et de fichiers .vic
    ├── example.png
    └── example.vic
```

---

## Utilisation des Outils

### 1. Convertisseur CLI

Le script `convert_to_my_format.py` convertit les fichiers PNG en format .vic via la ligne de commande.

**Utilisation :**

```bash
python3 convert_to_my_format.py input.png output.vic
```

**Options :**

- `--quality` : Qualité de compression (par défaut : 75).
- `--max_width` : Largeur maximale de l'image (par défaut : 2000 pixels).
- `--max_height` : Hauteur maximale de l'image (par défaut : 2000 pixels).

Le script détecte automatiquement si l'image est une capture d'écran pleine page. Si `--max_width` et `--max_height` ne sont pas fournis, les dimensions s'ajusteront automatiquement aux exigences du format .vic.

### 2. Interface Graphique (GUI)

Le script `convert_gui.py` fournit une interface graphique simple pour la conversion de fichiers.

**Étapes :**

1. Lancez l'interface graphique :
   ```bash
   python3 convert_gui.py
   ```
2. Utilisez l'interface pour :
   - Sélectionner un fichier `.png` comme entrée.
   - Spécifier le chemin de sortie du fichier (par exemple, `output.vic`).
   - Cliquer sur "Convertir" pour générer le fichier `.vic`.

### 3. Visionneuse HTML

Le fichier `visionneuse.html` permet d'afficher les fichiers `.vic` directement dans un navigateur.

**Étapes :**

1. Ouvrez `visionneuse.html` dans votre navigateur.
2. Utilisez l'interface pour charger un fichier `.vic`.
3. Affichez l'image avec ses métadonnées.

### 4. Validation des Fichiers

Le script `read_my_format.py` lit et valide les fichiers `.vic`, affichant les métadonnées, dimensions et tailles d'image.

**Utilisation :**

```bash
python3 read_my_format.py file.vic [--save_image]
```

- Ajoutez `--save_image` pour extraire l'image PNG du fichier `.vic`.

### 5. Comparaison des Tailles

Le script `compare_sizes.py` compare les tailles d'un fichier PNG original et de son équivalent `.vic`.

**Utilisation :**

```bash
python3 compare_sizes.py original.png converted.vic
```

---

## Contribuer au Projet

Nous accueillons les contributions au projet .vic ! Voici comment participer :

1. **Soumettre une demande :** Contactez-nous à `cmoikvolelorange.com` ou ouvrez une issue dans ce dépôt pour expliquer votre intérêt.
2. **Recevoir une invitation :** Une fois votre demande approuvée, vous recevrez un accès au dépôt privé.
3. **Commencez à contribuer :** Suivez les instructions fournies dans le dépôt privé.

---

## Contributions et Retours

- Consultez le fichier `CONTRIBUTING.md` pour les détails sur la manière de contribuer.
- Soumettez des issues ou des pull requests pour signaler des bugs ou proposer des améliorations.

## Code de Conduite

Ce projet respecte un Code de Conduite. Tous les contributeurs sont tenus de le suivre.

---

## Remerciements

Merci pour votre intérêt dans le projet .vic ! Nous sommes impatients de collaborer avec vous pour faire de .vic un format puissant et largement adopté.