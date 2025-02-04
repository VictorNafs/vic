// Sélection des éléments
const iframe = document.querySelector('iframe[name="content-frame"]');
const loader = document.getElementById("loader");
const installButton = document.getElementById("install-button");
let deferredPrompt = null;

// Gestion de l'affichage du loader lors de la navigation entre les pages
if (iframe && loader) {
  const links = document.querySelectorAll('nav a');
  links.forEach(link => {
    link.addEventListener('click', () => {
      loader.style.display = "flex";
    });
  });

  iframe.addEventListener('load', () => {
    loader.style.display = "none";
  });
}

// Configuration des annonces Google AdSense
(adsbygoogle = window.adsbygoogle || []).push({
  google_ad_client: "ca-pub-6308308780527097",
  enable_page_level_ads: true,
});

// Gestion du formulaire de conversion
document.addEventListener('DOMContentLoaded', () => {
  const convertForm = document.getElementById('convertForm');
  const convertResult = document.getElementById('convertResult');
  const vicDownloadLink = document.getElementById('vicDownloadLink');
  const fileError = document.getElementById('fileError');

  if (convertForm) {
    convertForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const fileInput = document.getElementById('imageFile');
      if (!fileInput || !fileInput.files.length) {
        fileError.style.display = "block";
        fileInput?.focus();
        return;
      }

      const file = fileInput.files[0];
      const allowedExtensions = [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff"];
      const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();

      if (!allowedExtensions.includes(fileExtension)) {
        fileError.textContent = "Format non supporté. Formats acceptés : PNG, JPEG, BMP, GIF, TIFF.";
        fileError.style.display = "block";
        fileInput.focus();
        return;
      }

      fileError.style.display = "none";
      if (loader) loader.style.display = "flex";

      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('/convert', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const blob = await response.blob();
          vicDownloadLink.href = URL.createObjectURL(blob);
          convertResult.style.display = 'block';
        } else {
          alert('Erreur lors de la conversion.');
        }
      } catch (error) {
        alert('Une erreur s\'est produite. Veuillez réessayer.');
      } finally {
        if (loader) loader.style.display = "none";
      }
    });
  }

  // Gestion de l'installation PWA
  if (installButton) {
    window.addEventListener("beforeinstallprompt", (e) => {
      e.preventDefault();
      deferredPrompt = e;

      installButton.style.display = "block";
      installButton.addEventListener("click", () => {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((choiceResult) => {
          console.log(choiceResult.outcome === "accepted"
            ? "PWA installée avec succès."
            : "Installation PWA refusée.");
          deferredPrompt = null;
        });
      });
    });
  }

  // Gestion de la génération d'iframe
  const iframeForm = document.getElementById('iframeForm');
  const iframePreview = document.getElementById('iframePreview');
  const iframeResult = document.getElementById('iframeResult');
  const urlError = document.getElementById('urlError');

  if (iframeForm) {
    iframeForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const urlInput = document.getElementById('vicUrl');
      const url = urlInput.value.trim();

      // Valider le format de l'URL
      if (!url || !/^https?:\/\/.+\..+/.test(url)) {
        urlError.style.display = "block"; // Afficher une erreur si l'URL est invalide
        urlInput.focus();
        return;
      }
      urlError.style.display = "none"; // Masquer l'erreur si l'URL est valide

      if (loader) loader.style.display = "flex"; // Afficher le loader

      try {
        iframePreview.src = `/generate-iframe?file_url=${encodeURIComponent(url)}`;
        iframeResult.style.display = 'block';

        // Masquer le loader une fois l'iframe chargé
        iframePreview.onload = () => {
          if (loader) loader.style.display = "none";
        };
      } catch (error) {
        alert("Erreur lors de la génération de l'iframe."); // Gérer les erreurs
        if (loader) loader.style.display = "none";
      }
    });
  }

  // Gestion de l'extraction des métadonnées
  const metadataForm = document.getElementById('metadataForm');
  const metadataResult = document.getElementById('metadataResult');

  if (metadataForm) {
    metadataForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const fileInput = document.getElementById('vicFile');
      if (!fileInput || !fileInput.files.length) {
        fileError.style.display = "block";
        fileInput.focus();
        return;
      }
      fileError.style.display = "none";

      if (loader) loader.style.display = "flex";

      const formData = new FormData();
      formData.append('file', fileInput.files[0]);

      try {
        const response = await fetch('/metadata', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          metadataResult.textContent = JSON.stringify(data.metadata, null, 2);
          metadataResult.style.display = 'block';
        } else {
          alert('Erreur lors de l\'extraction des métadonnées.');
        }
      } catch (error) {
        alert("Une erreur s'est produite lors de l'extraction des métadonnées.");
      } finally {
        if (loader) loader.style.display = "none";
      }
    });
  }

  // Gestion de la prévisualisation des fichiers VIC
  const previewForm = document.getElementById('previewForm');
  const previewContainer = document.getElementById('previewContainer');

  if (previewForm) {
    previewForm.addEventListener('submit', async (e) => {
      e.preventDefault(); // Empêche l'envoi classique du formulaire
      if (loader) loader.style.display = "flex"; // Affiche le loader

      const fileInput = document.getElementById('vicPreviewFile');
      const file = fileInput.files[0];

      if (!file) {
        alert("Veuillez sélectionner un fichier à prévisualiser.");
        if (loader) loader.style.display = "none";
        return;
      }

      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('/preview', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const blob = await response.blob();
          const img = document.createElement('img');
          img.src = URL.createObjectURL(blob);
          img.loading = "lazy"; // Active le lazy loading
          img.alt = "Prévisualisation du fichier VIC";

          previewContainer.innerHTML = ''; // Vide le conteneur avant d'ajouter une nouvelle image
          previewContainer.appendChild(img);
        } else {
          alert('Erreur lors de la prévisualisation.');
        }
      } catch (error) {
        alert("Une erreur s'est produite lors de la prévisualisation.");
      } finally {
        if (loader) loader.style.display = "none"; // Masque le loader après traitement
      }
    });
  }
});