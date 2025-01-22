// Global loader functions
function showLoader() {
    const loader = document.getElementById("loader");
    if (loader) loader.style.display = "flex";
}

function hideLoader() {
    const loader = document.getElementById("loader");
    if (loader) loader.style.display = "none";
}

// Common logic for main-page navigation
document.addEventListener('DOMContentLoaded', () => {
    const iframe = document.querySelector('iframe[name="content-frame"]');
    const links = document.querySelectorAll('nav a');

    // Show the loader when iframe starts loading
    links.forEach(link => {
        link.addEventListener('click', () => {
            if (iframe && loader) {
                showLoader();
            }
        });
    });

    // Hide the loader when iframe finishes loading
    if (iframe) {
        iframe.addEventListener('load', () => {
            hideLoader();
        });
    }
});

// Convert Page (convert.html and browser.html)
function initializeConvertPage() {
    const convertForm = document.getElementById('convertForm');
    const convertResult = document.getElementById('convertResult');
    const vicDownloadLink = document.getElementById('vicDownloadLink');
    const fileError = document.getElementById('fileError');

    if (!convertForm) return; // Skip if not on convert page

    convertForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const fileInput = document.getElementById('pngFile');
        if (!fileInput.files.length) {
            fileError.style.display = "block";
            fileInput.focus();
            return;
        }
        fileError.style.display = "none";

        showLoader();

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

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
            alert('Une erreur s\'est produite.');
        } finally {
            hideLoader();
        }
    });
}

// Metadata Page (metadata.html)
function initializeMetadataPage() {
    const metadataForm = document.getElementById('metadataForm');
    const metadataResult = document.getElementById('metadataResult');
    const fileError = document.getElementById('fileError');

    if (!metadataForm) return; // Skip if not on metadata page

    metadataForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const fileInput = document.getElementById('vicFile');
        if (!fileInput.files.length) {
            fileError.style.display = "block";
            fileInput.focus();
            return;
        }
        fileError.style.display = "none";

        showLoader();

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            const response = await fetch('/metadata', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                metadataResult.textContent = JSON.stringify(data.metadata, null, 2); // Pretty-print JSON
                metadataResult.style.display = 'block';
            } else {
                alert('Erreur lors de l\'extraction des métadonnées.');
            }
        } catch (error) {
            alert("Une erreur s'est produite lors de l'extraction des métadonnées.");
        } finally {
            hideLoader();
        }
    });
}

// Preview Page (preview.html)
function initializePreviewPage() {
    const previewForm = document.getElementById('previewForm');
    const previewContainer = document.getElementById('previewContainer');
    const fileError = document.getElementById('fileError');

    if (!previewForm) return; // Skip if not on preview page

    previewForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const fileInput = document.getElementById('vicPreviewFile');
        if (!fileInput.files.length) {
            fileError.style.display = "block";
            fileInput.focus();
            return;
        }
        fileError.style.display = "none";

        showLoader();

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            const response = await fetch('/preview', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const blob = await response.blob();
                const img = document.createElement('img');
                img.src = URL.createObjectURL(blob);
                img.loading = "lazy";
                img.alt = "Prévisualisation du fichier VIC";

                previewContainer.innerHTML = '';
                previewContainer.appendChild(img);
            } else {
                alert('Erreur lors de la prévisualisation.');
            }
        } catch (error) {
            alert("Une erreur s'est produite lors de la prévisualisation.");
        } finally {
            hideLoader();
        }
    });
}

// Iframe Page (iframe.html)
function initializeIframePage() {
    const iframeForm = document.getElementById('iframeForm');
    const iframePreview = document.getElementById('iframePreview');
    const iframeResult = document.getElementById('iframeResult');
    const urlError = document.getElementById('urlError');

    if (!iframeForm) return; // Skip if not on iframe page

    iframeForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const urlInput = document.getElementById('vicUrl');
        const url = urlInput.value.trim();

        if (!url || !/^https?:\/\/.+\..+/.test(url)) {
            urlError.style.display = "block";
            urlInput.focus();
            return;
        }
        urlError.style.display = "none";

        showLoader();

        try {
            iframePreview.src = `/generate-iframe?file_url=${encodeURIComponent(url)}`;
            iframeResult.style.display = 'block';

            iframePreview.onload = () => {
                hideLoader();
            };
        } catch (error) {
            alert("Erreur lors de la génération de l'iframe.");
            hideLoader();
        }
    });
}

// Initialize the correct page
document.addEventListener('DOMContentLoaded', () => {
    initializeConvertPage();
    initializeMetadataPage();
    initializePreviewPage();
    initializeIframePage();
});
