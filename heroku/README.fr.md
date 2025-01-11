[🇬🇧 Read in English](README.md)

# **FastAPI - Convertisseur et Visionneuse pour Fichiers VIC**

Cette application est un service **FastAPI** conçu pour convertir des images PNG, en particulier des captures d'écran pleine page, en un format personnalisé `.vic`. Ce format offre des avantages uniques en termes de **redimensionnement adaptatif** et d'**intégration dans des iframes** avec un défilement vertical fluide.

---

## **Introduction au Format `.vic`**

Les fichiers `.vic` sont conçus pour résoudre des problèmes courants rencontrés avec les captures d'écran pleine page :

### **1. Problèmes avec les PNG Standards**
- Les captures d'écran longues sont redimensionnées pour s'adapter aux tailles d'écran standards.
- Les images deviennent illisibles sans zoom car elles rétrécissent excessivement.

### **2. Avantages du Format `.vic`**
- **Redimensionnement Adaptatif** :
  - Les images `.vic` s'adaptent automatiquement à la largeur des écrans ou des iframes, que ce soit sur mobile, tablette ou ordinateur.
- **Défilement Intégré** :
  - Un **défilement vertical** est ajouté pour afficher l'ensemble de la capture d'écran, quelle que soit sa hauteur.
- **Dimensions Flexibles** :
  - Les dimensions peuvent être contrôlées via une iframe.

---

## **Principales Fonctionnalités**

1. **Conversion PNG → VIC**
   - Convertit des images PNG, en particulier des captures d'écran, au format `.vic`.
   - Redimensionne automatiquement les images pour s'adapter aux écrans ou aux iframes.

2. **Extraction de Métadonnées**
   - Extrait des détails tels que les dimensions originales, le type de fichier (capture d'écran ou image classique), et d'autres informations.

3. **Prévisualisation des Fichiers VIC**
   - Diffuse le PNG intégré dans les fichiers `.vic`.

4. **Génération d'Iframes**
   - Génère une iframe pour intégrer facilement les fichiers `.vic` dans des pages web.

5. **Conversion à partir d'une URL Publique**
   - Télécharge une image depuis son URL (par exemple, une image Google) et la convertit en `.vic`.

---

## **Guide Pas à Pas**

### **1. Installation**

#### **1.1 Cloner le Projet**
```bash
git clone <repository-url>
cd <repository-directory>
```

#### **1.2 Installer les Dépendances**
Assurez-vous que Python 3.8+ est installé, puis exécutez :
```bash
pip install -r requirements.txt
```

#### **1.3 Lancer l'Application**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
L'application sera accessible à l'adresse : `http://<votre-ip>:8000`

---

### **2. Utilisation des Fonctionnalités**

#### **2.1 Conversion PNG → VIC**
Accédez au point de terminaison `/convert` en utilisant un outil comme Postman ou l'interface Swagger UI disponible à `http://<votre-ip>:8000/docs`.

- **Paramètres** :
  - `file` : Une image PNG.
  - `for_iframe` (optionnel) : Spécifiez `true` pour optimiser le fichier pour une iframe.

L'API renverra un fichier `.vic` prêt à être téléchargé.

#### **2.2 Extraction de Métadonnées**
Accédez à `/metadata` pour extraire les métadonnées d'un fichier `.vic`.

- **Étapes** :
  - Téléchargez un fichier `.vic` via POST.
  - Recevez les métadonnées telles que :
    - Dimensions originales et ajustées.
    - Type de fichier (image classique ou capture d'écran).
    - Ratio d'aspect.
    - Format de l'image.

#### **2.3 Prévisualisation des Fichiers VIC**
Accédez à `/preview` pour afficher l'image intégrée dans un fichier `.vic`.

- **Étapes** :
  - Téléchargez un fichier `.vic` pour recevoir l'image PNG intégrée.

#### **2.4 Génération d'Iframes**
Accédez à `/generate-iframe` et fournissez l'URL publique d'un fichier `.vic` pour générer une iframe HTML.

- **Exemple de Requête** :
  ```bash
  http://<votre-ip>:8000/generate-iframe?file_url=http://<votre-ip>:8000/static/sample.vic
  ```
- **Exemple de Réponse** :
  ```html
  <iframe src="http://<votre-ip>:8000/static/vic-viewer.html?file=http://<votre-ip>:8000/static/sample.vic" 
          width="560" height="315" frameborder="0" allowfullscreen></iframe>
  ```

#### **2.5 Conversion à partir d'une URL Publique**
Accédez à `/fetch-vic` et fournissez l'URL d'une image publique (par exemple, une image Google).

- **Exemple de Requête** :
  ```bash
  http://<votre-ip>:8000/fetch-vic?file_url=<image-url>
  ```
- L'image sera téléchargée et convertie en `.vic`.

---

### **3. Interfaces Web**

#### **3.1 Visionneuse Détaillée : `visionneuse.html`**
Une interface riche pour afficher les fichiers `.vic` et leurs métadonnées.
- Accessible à : `http://<votre-ip>:8000/static/visionneuse.html`

#### **3.2 Visionneuse pour Iframes : `vic-viewer.html`**
Une interface minimaliste conçue pour les iframes.
- Accessible à : `http://<votre-ip>:8000/static/vic-viewer.html?file=<file-url>`

### **4. Exemple d'Iframe**

Pour intégrer une image `.vic` dans un site web :
```html
<iframe
  src="http://<votre-ip>:8000/static/vic-viewer.html?file=http://<votre-ip>:8000/static/sample.vic"
  width="560"
  height="315"
  frameborder="0"
  allowfullscreen>
</iframe>
```

---

## **Notes Importantes**

### **Fichiers Statiques**
- Les fichiers `.vic` doivent être placés dans le répertoire `static` pour être correctement servis.

### **CORS**
- Si vous intégrez l'iframe sur un autre site, configurez les en-têtes CORS en conséquence.

---

## **Structure du Projet**

```plaintext
project/
├── compare_sizes.py       # Comparer les dimensions des images
├── convert_to_my_format.py # Conversion PNG → VIC
├── main.py                # Application principale FastAPI
├── read_my_format.py      # Lecture des fichiers VIC
├── visionneuse.html       # Visionneuse riche
└── static/
    └── vic-viewer.html    # Visionneuse minimaliste pour iframes
```