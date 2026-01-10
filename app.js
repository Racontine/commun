const REPO_OWNER = 'lumios-le-jeu';
const REPO_NAME = 'alice-media';
const BRANCH = 'main';

/* DOM Elements */
const tokenInput = document.getElementById('githubToken');
const saveTokenBtn = document.getElementById('saveTokenBtn');
const tokenStatus = document.getElementById('tokenStatus');
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const uploadSection = document.querySelector('.upload-section');
const resultSection = document.getElementById('resultSection');
const progressContainer = document.getElementById('progressContainer');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const qrContainer = document.getElementById('qrcode');
const uploadedFilename = document.getElementById('uploadedFilename');
const toast = document.getElementById('toast');

/* Library DOM */
const libraryList = document.getElementById('libraryList');
const searchInput = document.getElementById('searchInput');
const starFilter = document.getElementById('starFilter');

/* State */
let availableFiles = []; // { name: "foo.mp3", url: "...", type: "audio" }
let ratings = {}; // { "foo.mp3": 4 }

document.addEventListener('DOMContentLoaded', () => {
    const savedToken = localStorage.getItem('gh_pat');
    if (savedToken) {
        tokenInput.value = savedToken;
        validateToken(savedToken);
        initLibrary(savedToken); // Load library if token exists
    } else {
        libraryList.innerHTML = '<div class="loader">Veuillez entrer un token pour voir la bibliothèque.</div>';
    }
});

saveTokenBtn.addEventListener('click', () => {
    const token = tokenInput.value.trim();
    if (token) {
        localStorage.setItem('gh_pat', token);
        validateToken(token);
        showToast('Token sauvegardé !');
        initLibrary(token);
    }
});

/* --- LIBRARY LOGIC --- */
async function initLibrary(token) {
    libraryList.innerHTML = '<div class="loader">Chargement des sons...</div>';

    // 1. Fetch Ratings
    try {
        const r = await fetch(`https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/ratings.json`, {
            headers: { 'Authorization': `Bearer ${token}`, 'If-None-Match': '' } // No cache
        });
        if (r.ok) {
            const data = await r.json();
            const content = atob(data.content);
            ratings = JSON.parse(content);
        } else {
            ratings = {}; // No ratings yet
        }
    } catch (e) {
        console.warn("Could not load ratings:", e);
        ratings = {};
    }

    // 2. Fetch Files (flat list from media/audio)
    availableFiles = [];
    try {
        const r = await fetch(`https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/media/audio`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (r.ok) {
            const items = await r.json();
            availableFiles = items
                .filter(item => item.type === 'file')
                .map(item => ({
                    name: item.name,
                    url: item.download_url, // raw url
                    path: item.path
                }));
            renderLibrary();
        } else {
            throw new Error("Impossible de lister les fichiers audio.");
        }
    } catch (e) {
        libraryList.innerHTML = `<div class="loader" style="color:#ff7675">${e.message}</div>`;
    }
}

function renderLibrary() {
    libraryList.innerHTML = '';

    // Safety check if elements exist (e.g. if partial HTML load)
    if (!searchInput || !starFilter) return;

    const term = searchInput.value.toLowerCase();
    const minStars = parseInt(starFilter.value) || 0;

    const filtered = availableFiles.filter(file => {
        const score = ratings[file.name] || 0;
        const matchesName = file.name.toLowerCase().includes(term);

        if (minStars === 5) return score === 5 && matchesName;
        return score >= minStars && matchesName;
    });

    if (filtered.length === 0) {
        libraryList.innerHTML = '<div class="loader">Aucun résultat.</div>';
        return;
    }

    filtered.forEach(file => {
        const row = document.createElement('div');
        row.className = 'library-item';

        const score = ratings[file.name] || 0;

        // Note: passing strings to onclick requires escaping, but filenames represent simple MP3s mostly.
        // We use data attributes to be safer if we attach Listeners, but for now inline is faster for this Prototype.
        row.innerHTML = `
            <div class="item-info" onclick="generateQRFromUrl('${file.url}', '${file.name}')">
                <div class="item-icon">🎵</div>
                <div class="item-name" title="${file.name}">${file.name}</div>
            </div>
            <div class="item-rating">
                ${[1, 2, 3, 4, 5].map(i => `
                    <span class="star ${i <= score ? 'filled' : ''}" 
                          onclick="rateFile('${file.name}', ${i})">★</span>
                `).join('')}
            </div>
        `;
        libraryList.appendChild(row);
    });
}

// Search & Filter Listeners
if (searchInput) searchInput.addEventListener('input', renderLibrary);
if (starFilter) starFilter.addEventListener('change', renderLibrary);

/* --- RATING LOGIC --- */
async function rateFile(filename, score) {
    const token = localStorage.getItem('gh_pat');
    if (!token) return;

    // Update local state optimistic
    ratings[filename] = score;
    renderLibrary(); // Re-render to show stars immediately

    // Save to GitHub
    try {
        // 1. Get SHA of existing ratings.json (if any)
        let sha = null;
        try {
            const r = await fetch(`https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/ratings.json`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (r.ok) {
                const data = await r.json();
                sha = data.sha;
            }
        } catch (e) { }

        // 2. Upload new content
        const content = btoa(JSON.stringify(ratings, null, 2));
        const body = {
            message: `Update rating for ${filename}`,
            content: content,
            branch: BRANCH
        };
        if (sha) body.sha = sha;

        await fetch(`https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/ratings.json`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        });

        console.log(`Rating saved for ${filename}: ${score}`);
        showToast(`Note enregistrée : ${score}/5 ⭐`);

    } catch (e) {
        console.error("Save rating failed", e);
        showToast("Erreur sauvegarde note");
    }
}

/* --- QR Helper --- */
async function generateQRFromUrl(rawUrl, name) {
    // Show UI loading
    console.log("Generating QR for existing file:", name);
    resetUIForUpload();
    updateProgress(50, "Génération lien is.gd...");

    // Use the existing logic part? Or simplify because we already have the URL.
    // We need to SHORTEN it again because we don't store shortened URLs.

    try {
        let finalUrl = rawUrl;
        const encodedTarget = encodeURIComponent(rawUrl);
        const shortenerUrl = `https://corsproxy.io/?` + encodeURIComponent(`https://is.gd/create.php?format=simple&url=${encodedTarget}`);

        const shortRes = await fetch(shortenerUrl);
        if (shortRes.ok) {
            const text = await shortRes.text();
            if (text.startsWith('http') && text.length < 100) finalUrl = text;
        }

        updateProgress(100, "Terminé !");

        // Show result manually
        showResult(finalUrl, name);

    } catch (e) {
        showToast("Erreur génération QR");
        resetApp();
    }
}


/* --- EXISTING AUTH & UPLOAD LOGIC --- */

async function validateToken(token) {
    if (!token) {
        updateTokenStatus(false);
        return;
    }

    // Optimistic checking (grey out while checking)
    tokenStatus.className = 'status-indicator';

    try {
        const response = await fetch('https://api.github.com/user', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            updateTokenStatus(true);
        } else {
            updateTokenStatus(false);
        }
    } catch (e) {
        updateTokenStatus(false);
    }
}

function updateTokenStatus(isValid) {
    tokenStatus.className = 'status-indicator'; // Reset
    if (isValid) {
        tokenStatus.classList.add('valid');
        tokenStatus.title = "Token valide";
    } else {
        tokenStatus.classList.add('invalid');
        tokenStatus.title = "Token invalide";
    }
}

dropZone.addEventListener('click', () => fileInput.click());

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) { e.preventDefault(); e.stopPropagation(); }

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
});

dropZone.addEventListener('drop', (e) => handleFiles(e.dataTransfer.files));
fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

function handleFiles(files) {
    if (files.length > 0) {
        processAndUpload(files[0]);
    }
}

async function processAndUpload(file) {
    const token = localStorage.getItem('gh_pat');
    if (!token) {
        showToast('Erreur: Veuillez entrer un Token GitHub valide.');
        return;
    }

    resetUIForUpload();

    try {
        let fileToUpload = file;
        let filename = file.name;
        const ext = filename.split('.').pop().toLowerCase();

        // 1. Audio Conversion (if needed)
        // If it's an audio file but NOT mp3, convert it.
        // Also if it's a WAV, OGG, etc.
        const isAudio = file.type.startsWith('audio/') || ext === 'wav' || ext === 'ogg';
        const isVideo = file.type.startsWith('video/') || ['mp4', 'mpeg', 'avi', 'mov', 'mkv', 'webm'].includes(ext);

        if ((isAudio || isVideo) && ext !== 'mp3') {
            updateProgress(10, "Compression Audio (64kbps)...");
            try {
                const mp3Blob = await convertToMp3(file);

                // Create new File object
                const newName = filename.substring(0, filename.lastIndexOf('.')) + ".mp3";
                fileToUpload = new File([mp3Blob], newName, { type: 'audio/mp3' });
                filename = newName;
                console.log("Conversion successful:", filename);
            } catch (err) {
                console.warn("Conversion failed, uploading original:", err);
                if (isVideo) {
                    showToast("Impossible d'extraire l'audio. Upload de la vidéo brute...");
                } else {
                    showToast("Conversion MP3 échouée. Upload du fichier original...");
                }
            }
        }

        // Re-evaluate extension after potential conversion
        const finalExt = filename.split('.').pop().toLowerCase();
        let folder = 'media/audio';

        // If conversion failed and we still have a video file, put it in video folder
        if (['mp4', 'mkv', 'avi', 'mov', 'mpeg', 'webm'].includes(finalExt)) {
            folder = 'media/video';
        }
        const sanitizedName = filename.replace(/[^a-zA-Z0-9._-]/g, '_');
        const path = `${folder}/${sanitizedName}`;

        // 3. Convert to Base64
        updateProgress(30, "Préparation...");
        const content = await toBase64(fileToUpload);

        // 4. Check for existing SHA
        let sha = null;
        try {
            const checkReq = await fetch(`https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${path}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (checkReq.ok) {
                const data = await checkReq.json();
                sha = data.sha;
            }
        } catch (e) { }

        // 5. Upload
        updateProgress(50, "Envoi vers GitHub...");
        const body = {
            message: `Add ${sanitizedName} via Web Uploader`,
            content: content,
            branch: BRANCH
        };
        if (sha) body.sha = sha;

        const response = await fetch(`https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${path}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        });

        if (!response.ok) throw new Error(`Erreur GitHub: ${response.statusText}`);

        // 6. Generate Link
        updateProgress(80, "Génération lien is.gd...");
        const rawUrl = `https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/${BRANCH}/${path}`;

        // 7. Shorten URL
        let finalUrl = rawUrl;
        try {
            // Encode the target URL Component safely
            const encodedTarget = encodeURIComponent(rawUrl);

            // Switch to is.gd for DIRECT redirection (TinyURL adds an interstitial page sometimes)
            // API: https://is.gd/create.php?format=simple&url=...
            const shortenerUrl = `https://corsproxy.io/?` + encodeURIComponent(`https://is.gd/create.php?format=simple&url=${encodedTarget}`);

            console.log("Requesting shortener (is.gd):", shortenerUrl);
            const shortRes = await fetch(shortenerUrl);
            if (shortRes.ok) {
                const text = await shortRes.text();
                // Basic validation: must start with http and be short
                if (text.startsWith('http') && text.length < 100) {
                    finalUrl = text;
                } else {
                    console.warn("Shortener returned non-url:", text);
                }
            }
        } catch (e) {
            console.warn("Shortener failed, using raw URL", e);
        }

        updateProgress(100, "Terminé !");

        // Finalize Result
        showResult(finalUrl, sanitizedName);

        // Refresh Library in background to show new file
        initLibrary(token);

    } catch (error) {
        console.error(error);
        showToast(error.message);
        resetApp();
    }
}

// --- CONVERSION LOGIC ---
function convertToMp3(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = async (e) => {
            try {
                const arrayBuffer = e.target.result;
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

                // Decode audio (WAV, OGG, etc -> PCM)
                const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);

                // Encode to MP3
                const mp3Data = encodeBufferToMp3(audioBuffer);
                resolve(new Blob(mp3Data, { type: 'audio/mp3' }));
            } catch (err) {
                reject(err);
            }
        };
        reader.onerror = reject;
        reader.readAsArrayBuffer(file);
    });
}

function encodeBufferToMp3(audioBuffer) {
    const channels = 1; // Mono is enough for Alice and saves space/time, but let's try to keep stereo if possible.
    // LameJS supports stereo.
    const sampleRate = audioBuffer.sampleRate;
    const mp3encoder = new lamejs.Mp3Encoder(channels, sampleRate, 64); // 64kbps (Optimized for Alice Box)

    const samples = audioBuffer.getChannelData(0); // Get Left Channel (or Mono)
    // Convert float samples to 16-bit PCM
    const sampleBlock = new Int16Array(samples.length);
    for (let i = 0; i < samples.length; i++) {
        // Float to 16bit PCM
        sampleBlock[i] = samples[i] < 0 ? samples[i] * 0x8000 : samples[i] * 0x7FFF;
    }

    const mp3Data = [];
    const blockSize = 1152; // must be multiple of 576
    for (let i = 0; i < sampleBlock.length; i += blockSize) {
        const chunk = sampleBlock.subarray(i, i + blockSize);
        const mp3buf = mp3encoder.encodeBuffer(chunk);
        if (mp3buf.length > 0) {
            mp3Data.push(mp3buf);
        }
    }

    const endBuf = mp3encoder.flush();
    if (endBuf.length > 0) {
        mp3Data.push(endBuf);
    }

    return mp3Data;
}

// --- UTILS ---
function toBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result.split(',')[1]);
        reader.onerror = reject;
    });
}

function resetUIForUpload() {
    dropZone.classList.add('hidden');
    progressContainer.classList.remove('hidden');
    updateProgress(0, "Démarrage...");
}

function updateProgress(percent, text) {
    progressFill.style.width = `${percent}%`;
    progressText.innerText = text || `${percent}%`;
}

function showResult(url, name) {
    uploadSection.classList.add('hidden');
    resultSection.classList.remove('hidden');
    uploadedFilename.innerText = name;
    qrContainer.innerHTML = '';

    // Generate QR
    new QRCode(qrContainer, {
        text: url,
        width: 200,
        height: 200,
        correctLevel: QRCode.CorrectLevel.L
    });

    // Add clickable link for verification
    const linkContainer = document.createElement('div');
    linkContainer.style.marginTop = '1rem';
    linkContainer.style.fontSize = '0.9rem';
    linkContainer.style.wordBreak = 'break-all';

    const link = document.createElement('a');
    link.href = url;
    link.innerText = url;
    link.target = '_blank';
    link.style.color = '#00b894';

    linkContainer.appendChild(link);
    qrContainer.appendChild(linkContainer);
}

function resetApp() {
    uploadSection.classList.remove('hidden');
    dropZone.classList.remove('hidden');
    progressContainer.classList.add('hidden');
    resultSection.classList.add('hidden');
    progressFill.style.width = '0%';
    fileInput.value = '';
}

function showToast(msg) {
    const toast = document.getElementById('toast');
    toast.innerText = msg;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), 3000);
}
