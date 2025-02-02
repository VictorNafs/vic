// Sélection des éléments
const iframe = document.querySelector('iframe[name="content-frame"]');
const loader = document.getElementById("loader");
const installButton = document.getElementById("install-button");
let deferredPrompt = null;

console.log("JavaScript est bien chargé !");
alert("JavaScript fonctionne !");

// Gestion de l'affichage du loader lors de la navigation entre les pages
if (iframe && loader) {
  const links = document.querySelectorAll('nav a');
  links.forEach(link => {
    link.addEventListener('click', () => {
      loader.style.display = "flex";
    });
  });

  iframe.addEventListener('load', () => {
    console.log("Iframe chargé !");
    loader.style.display = "none";
  });
}

// Configuration des annonces Google AdSense
(adsbygoogle = window.adsbygoogle || []).push({
  google_ad_client: "ca-pub-6308308780527097",
  enable_page_level_ads: true,
});

// Fonction Fetch avec Timeout pour éviter les blocages
async function fetchWithTimeout(resource, options = {}, timeout = 10000) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);
  
  try {
    const response = await fetch(resource, { ...options, signal: controller.signal });
    clearTimeout(id);
    return response;
  } catch (error) {
    console.error("Erreur de fetch :", error);
    alert("Erreur réseau ou serveur. Vérifiez votre connexion.");
    return null;
  }
}

// Gestion du formulaire de conversion
document.addEventListener('DOMContentLoaded', () => {
  console.log("DOM chargé !");

  const convertForm = document.getElementById('convertForm');
  const convertResult = document.getElementById('convertResult');
  const vicDownloadLink = document.getElementById('vicDownloadLink');
  const fileError = document.getElementById('fileError');
  const fileInput = document.getElementById('imageFile');

  if (fileInput) {
    fileInput.addEventListener('change', () => {
      console.log("Fichier sélectionné :", fileInput.files[0]?.name);
    });
  }

  if (convertForm) {
    convertForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      console.log("Le formulaire de conversion a bien été soumis !");

      if (!fileInput || !fileInput.files.length) {
        fileError.style.display = "block";
        fileInput?.focus();
        return;
      }

      fileError.style.display = "none";
      if (loader) {
        loader.style.display = "flex";
        setTimeout(() => {
          loader.style.display = "none";
        }, 10000);
      }

      const formData = new FormData();
      formData.append('file', fileInput.files[0]);

      try {
        const response = await fetchWithTimeout('/convert', { method: 'POST', body: formData });
        if (response && response.ok) {
          const blob = await response.blob();
          vicDownloadLink.href = URL.createObjectURL(blob);
          convertResult.style.display = 'block';
        } else {
          alert('Erreur lors de la conversion.');
        }
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
        const response = await fetchWithTimeout('/metadata', { method: 'POST', body: formData });
        if (response && response.ok) {
          const data = await response.json();
          metadataResult.textContent = JSON.stringify(data.metadata, null, 2);
          metadataResult.style.display = 'block';
        } else {
          alert('Erreur lors de l\'extraction des métadonnées.');
        }
      } finally {
        if (loader) loader.style.display = "none";
      }
    });
  }
});
