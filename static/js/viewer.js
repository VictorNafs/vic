const urlParams = new URLSearchParams(window.location.search);
const fileUrl = urlParams.get('file');

const loader = document.getElementById('loader');
const canvas = document.getElementById('vicCanvas');
const ctx = canvas.getContext('2d');

const showLoader = () => {
    loader.style.display = 'block';
};

const hideLoader = () => {
    loader.style.display = 'none';
};

const loadVicFile = async (fileUrl) => {
    showLoader();
    try {
        const response = await fetch(fileUrl);
        if (!response.ok) {
            throw new Error('Impossible de charger le fichier VIC.');
        }
        const vicData = await response.arrayBuffer();
        renderVicData(vicData);
    } catch (error) {
        console.error('Erreur :', error);
        alert('Erreur lors du chargement du fichier VIC.');
    } finally {
        hideLoader();
    }
};

const renderVicData = (vicData) => {
    canvas.width = 800;
    canvas.height = 600;
    ctx.fillStyle = '#1e1e1e';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#ff6700';
    ctx.font = '20px Arial';
    ctx.fillText('Aperçu du fichier VIC', 20, 50);
};

if (fileUrl) {
    loadVicFile(fileUrl);
} else {
    alert('Aucune URL de fichier VIC spécifiée.');
}
