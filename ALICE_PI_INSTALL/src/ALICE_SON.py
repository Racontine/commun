#!/usr/bin/env python3
"""
ALICE_SON.py - Serveur web léger pour contrôler le volume d'Alice
Sans avoir besoin de basculer en mode hotspot !

Usage:
    sudo python3 /home/alice/ALICE_SON.py

Accès:
    http://<IP_DU_PI>:8080

Le serveur tourne en parallèle d'alice.py et permet de modifier le volume
sans interrompre le WiFi ni l'application principale.
"""

from flask import Flask, render_template_string, request, jsonify
import json
import os
import subprocess
import socket

app = Flask(__name__)

# Configuration
CONFIG_FILE = "/home/alice/media/config.json"
DEFAULT_PORT = 8080

# Fallback local pour développement
if not os.path.exists(CONFIG_FILE):
    CONFIG_FILE = "config.json"
    os.makedirs(os.path.dirname(CONFIG_FILE) or ".", exist_ok=True)


def load_config():
    """Charge la configuration depuis config.json"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        else:
            # Config par défaut
            return {"volume": 90, "wifi_priority": []}
    except Exception as e:
        print(f"⚠️ Erreur chargement config: {e}")
        return {"volume": 90, "wifi_priority": []}


def save_config(config_data):
    """Sauvegarde la configuration dans config.json"""
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE) or ".", exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=2)
        print(f"✅ Configuration sauvegardée : {config_data}")
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde config: {e}")
        return False


def get_local_ip():
    """Récupère l'IP locale du Raspberry Pi"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def restart_alice_service():
    """Redémarre le service Alice pour appliquer les changements"""
    try:
        subprocess.run(["sudo", "systemctl", "restart", "alice.service"], check=True)
        return True
    except Exception as e:
        print(f"⚠️ Impossible de redémarrer alice.service: {e}")
        return False


def get_audio_files():
    """Liste tous les fichiers audio dans /home/alice/media/audio"""
    audio_dir = "/home/alice/media/audio"
    
    # Fallback pour développement
    if not os.path.exists(audio_dir):
        audio_dir = "./media/audio"
        os.makedirs(audio_dir, exist_ok=True)
    
    try:
        files = []
        if os.path.exists(audio_dir):
            for filename in sorted(os.listdir(audio_dir)):
                filepath = os.path.join(audio_dir, filename)
                if os.path.isfile(filepath):
                    # Calculer la taille du fichier
                    size_bytes = os.path.getsize(filepath)
                    size_mb = size_bytes / (1024 * 1024)
                    
                    files.append({
                        'name': filename,
                        'size': f"{size_mb:.2f} MB",
                        'size_bytes': size_bytes
                    })
        return files
    except Exception as e:
        print(f"⚠️ Erreur lors du listage des fichiers: {e}")
        return []


def delete_audio_file(filename):
    """Supprime un fichier audio"""
    audio_dir = "/home/alice/media/audio"
    
    # Fallback pour développement
    if not os.path.exists(audio_dir):
        audio_dir = "./media/audio"
    
    try:
        filepath = os.path.join(audio_dir, filename)
        
        # Vérification de sécurité : le fichier doit être dans le dossier audio
        if not filepath.startswith(audio_dir):
            return False, "Chemin invalide"
        
        if os.path.exists(filepath) and os.path.isfile(filepath):
            os.remove(filepath)
            print(f"🗑️ Fichier supprimé : {filename}")
            return True, f"Fichier {filename} supprimé avec succès"
        else:
            return False, "Fichier introuvable"
    except Exception as e:
        print(f"❌ Erreur suppression : {e}")
        return False, str(e)


# Template HTML avec design moderne
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔊 Alice - Contrôle du Son</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 100%;
        }
        
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2em;
            text-align: center;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 0.9em;
        }
        
        .volume-section {
            margin-bottom: 30px;
        }
        
        .volume-display {
            text-align: center;
            font-size: 3.5em;
            font-weight: bold;
            color: #667eea;
            margin: 20px 0;
        }
        
        .slider-container {
            position: relative;
            padding: 20px 0;
        }
        
        input[type="range"] {
            -webkit-appearance: none;
            width: 100%;
            height: 12px;
            border-radius: 6px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            outline: none;
            opacity: 0.9;
            transition: opacity 0.2s;
        }
        
        input[type="range"]:hover {
            opacity: 1;
        }
        
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: white;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }
        
        input[type="range"]::-webkit-slider-thumb:hover {
            transform: scale(1.1);
        }
        
        input[type="range"]::-moz-range-thumb {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: white;
            cursor: pointer;
            border: none;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        .volume-labels {
            display: flex;
            justify-content: space-between;
            margin-top: 10px;
            color: #999;
            font-size: 0.9em;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1.1em;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 0.95em;
            display: none;
        }
        
        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .info-box {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-top: 30px;
            border-left: 4px solid #667eea;
        }
        
        .info-box h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1em;
        }
        
        .info-box p {
            color: #666;
            font-size: 0.9em;
            line-height: 1.5;
        }
        
        .quick-buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin: 20px 0;
        }
        
        .quick-btn {
            background: #f8f9fa;
            border: 2px solid #667eea;
            color: #667eea;
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9em;
            font-weight: bold;
            transition: all 0.2s;
        }
        
        .quick-btn:hover {
            background: #667eea;
            color: white;
        }
        
        
        .media-section {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
        }
        
        .media-section h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .media-count {
            font-size: 0.8em;
            color: #999;
            font-weight: normal;
        }
        
        .media-list {
            max-height: 400px;
            overflow-y: auto;
            margin-bottom: 10px;
        }
        
        .media-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s;
        }
        
        .media-item:hover {
            background: #e9ecef;
            transform: translateX(5px);
        }
        
        .media-info {
            flex: 1;
        }
        
        .media-name {
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
            word-break: break-all;
        }
        
        .media-size {
            font-size: 0.85em;
            color: #999;
        }
        
        .delete-btn {
            background: #dc3545;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.2s;
            white-space: nowrap;
        }
        
        .delete-btn:hover {
            background: #c82333;
            transform: scale(1.05);
        }
        
        .empty-media {
            text-align: center;
            color: #999;
            padding: 40px 20px;
            font-style: italic;
        }
        
        @media (max-width: 480px) {
            .container {
                padding: 25px;
            }
            
            h1 {
                font-size: 1.5em;
            }
            
            .volume-display {
                font-size: 2.5em;
            }
            
            .media-item {
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }
            
            .delete-btn {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔊 Alice - Contrôle du Son</h1>
        <p class="subtitle">Ajustez le volume sans couper le WiFi</p>
        
        <div class="volume-section">
            <div class="volume-display" id="volumeDisplay">{{ current_volume }}%</div>
            
            <div class="quick-buttons">
                <button class="quick-btn" onclick="setVolume(25)">25%</button>
                <button class="quick-btn" onclick="setVolume(50)">50%</button>
                <button class="quick-btn" onclick="setVolume(75)">75%</button>
                <button class="quick-btn" onclick="setVolume(100)">100%</button>
            </div>
            
            <div class="slider-container">
                <input type="range" id="volumeSlider" min="0" max="100" value="{{ current_volume }}" 
                       oninput="updateVolumeDisplay(this.value)">
                <div class="volume-labels">
                    <span>🔇 Muet</span>
                    <span>🔊 Max</span>
                </div>
            </div>
        </div>
        
        <button class="btn" onclick="saveVolume()">💾 Sauvegarder et Redémarrer Alice</button>
        
        
        <div id="status" class="status"></div>
        
        <!-- Section Gestion des Médias -->
        <div class="media-section">
            <h2>
                📁 Bibliothèque Audio
                <span class="media-count" id="mediaCount">{{ audio_files|length }} fichier(s)</span>
            </h2>
            
            <div class="media-list" id="mediaList">
                {% if audio_files %}
                    {% for file in audio_files %}
                    <div class="media-item" id="media-{{ loop.index }}">
                        <div class="media-info">
                            <div class="media-name">🎵 {{ file.name }}</div>
                            <div class="media-size">{{ file.size }}</div>
                        </div>
                        <button class="delete-btn" onclick="deleteMedia('{{ file.name }}', {{ loop.index }})">
                            🗑️ Supprimer
                        </button>
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="empty-media">
                        📭 Aucun fichier audio pour le moment
                    </div>
                {% endif %}
            </div>
        </div>
        
        <div class="info-box">
            <h3>ℹ️ Comment ça marche ?</h3>
            <p>
                <strong>1.</strong> Ajustez le volume avec le curseur<br>
                <strong>2.</strong> Cliquez sur "Sauvegarder"<br>
                <strong>3.</strong> Alice redémarre automatiquement avec le nouveau volume<br>
                <br>
                <strong>IP du serveur:</strong> {{ server_ip }}:{{ server_port }}
            </p>
        </div>
    </div>
    
    <script>
        function updateVolumeDisplay(value) {
            document.getElementById('volumeDisplay').innerText = value + '%';
        }
        
        function setVolume(value) {
            document.getElementById('volumeSlider').value = value;
            updateVolumeDisplay(value);
        }
        
        async function saveVolume() {
            const volume = document.getElementById('volumeSlider').value;
            const statusDiv = document.getElementById('status');
            
            statusDiv.style.display = 'none';
            
            try {
                const response = await fetch('/save', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ volume: parseInt(volume) })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    statusDiv.className = 'status success';
                    statusDiv.innerText = '✅ ' + data.message + ' Alice va redémarrer...';
                } else {
                    statusDiv.className = 'status error';
                    statusDiv.innerText = '❌ Erreur: ' + data.message;
                }
                
                statusDiv.style.display = 'block';
                
            } catch (error) {
                statusDiv.className = 'status error';
                statusDiv.innerText = '❌ Erreur de connexion: ' + error.message;
                statusDiv.style.display = 'block';
            }
        }
        
        async function deleteMedia(filename, index) {
            if (!confirm(`Êtes-vous sûr de vouloir supprimer "${filename}" ?`)) {
                return;
            }
            
            const statusDiv = document.getElementById('status');
            statusDiv.style.display = 'none';
            
            try {
                const response = await fetch('/delete', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ filename: filename })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Supprimer visuellement l'élément
                    const mediaItem = document.getElementById('media-' + index);
                    if (mediaItem) {
                        mediaItem.style.opacity = '0';
                        mediaItem.style.transform = 'translateX(-20px)';
                        setTimeout(() => {
                            mediaItem.remove();
                            
                            // Mettre à jour le compteur
                            const remaining = document.querySelectorAll('.media-item').length;
                            document.getElementById('mediaCount').innerText = remaining + ' fichier(s)';
                            
                            // Afficher message vide si plus de fichiers
                            if (remaining === 0) {
                                document.getElementById('mediaList').innerHTML = 
                                    '<div class="empty-media">📭 Aucun fichier audio pour le moment</div>';
                            }
                        }, 300);
                    }
                    
                    statusDiv.className = 'status success';
                    statusDiv.innerText = '✅ ' + data.message;
                } else {
                    statusDiv.className = 'status error';
                    statusDiv.innerText = '❌ Erreur: ' + data.message;
                }
                
                statusDiv.style.display = 'block';
                
            } catch (error) {
                statusDiv.className = 'status error';
                statusDiv.innerText = '❌ Erreur de connexion: ' + error.message;
                statusDiv.style.display = 'block';
            }
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            const slider = document.getElementById('volumeSlider');
            if (e.key === 'ArrowUp' || e.key === '+') {
                slider.value = Math.min(100, parseInt(slider.value) + 5);
                updateVolumeDisplay(slider.value);
            } else if (e.key === 'ArrowDown' || e.key === '-') {
                slider.value = Math.max(0, parseInt(slider.value) - 5);
                updateVolumeDisplay(slider.value);
            } else if (e.key === 'Enter') {
                saveVolume();
            }
        });
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Page principale de contrôle du volume"""
    config = load_config()
    current_volume = config.get("volume", 90)
    local_ip = get_local_ip()
    audio_files = get_audio_files()
    
    return render_template_string(
        HTML_TEMPLATE,
        current_volume=current_volume,
        server_ip=local_ip,
        server_port=DEFAULT_PORT,
        audio_files=audio_files
    )


@app.route('/save', methods=['POST'])
def save():
    """API pour sauvegarder le volume"""
    try:
        data = request.get_json()
        volume = int(data.get('volume', 90))
        
        # Validation
        if not 0 <= volume <= 100:
            return jsonify({
                'success': False,
                'message': 'Le volume doit être entre 0 et 100'
            })
        
        # Charger la config existante
        config = load_config()
        config['volume'] = volume
        
        # Sauvegarder
        if save_config(config):
            # Redémarrer Alice pour appliquer
            restart_alice_service()
            
            return jsonify({
                'success': True,
                'message': f'Volume réglé à {volume}%.'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Erreur lors de la sauvegarde'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })


@app.route('/api/volume', methods=['GET'])
def get_volume():
    """API pour récupérer le volume actuel"""
    config = load_config()
    return jsonify({
        'volume': config.get('volume', 90)
    })


@app.route('/delete', methods=['POST'])
def delete():
    """API pour supprimer un fichier audio"""
    try:
        data = request.get_json()
        filename = data.get('filename', '')
        
        if not filename:
            return jsonify({
                'success': False,
                'message': 'Nom de fichier manquant'
            })
        
        success, message = delete_audio_file(filename)
        
        return jsonify({
            'success': success,
            'message': message
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })


if __name__ == '__main__':
    print("=" * 50)
    print("🔊 ALICE_SON - Serveur de contrôle du volume")
    print("=" * 50)
    
    local_ip = get_local_ip()
    print(f"📡 IP locale: {local_ip}")
    print(f"🌐 URL d'accès: http://{local_ip}:{DEFAULT_PORT}")
    print(f"📁 Fichier config: {CONFIG_FILE}")
    print("=" * 50)
    print("Appuyez sur CTRL+C pour arrêter\n")
    
    # Lancement du serveur
    app.run(host='0.0.0.0', port=DEFAULT_PORT, debug=False)
