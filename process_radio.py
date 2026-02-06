import os
import subprocess
import requests
import qrcode
import time

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "media", "audio", "Radio_Classique")
# FOLDERS détectés automatiquement si le nom est un nombre (ex: "16" -> 16s)


# GitHub Config (Auto-detected)
REPO_OWNER = "lumios-le-jeu"
REPO_NAME = "alice-media"
BRANCH = "main"

def trim_audio(file_path, cut_seconds):
    """
    Trims the first `cut_seconds` from the MP3 file using ffmpeg.
    Replaces the original file.
    """
    filename = os.path.basename(file_path)
    temp_file = file_path + ".temp.mp3"
    
    print(f"✂️  Traitement de {filename} (-{cut_seconds}s)...")
    
    # Commande ffmpeg: -ss pour le début, -c copy pour ne pas ré-encoder (rapide et sans perte)
    # -y pour écraser le fichier temp si existant
    cmd = [
        "ffmpeg", 
        "-y",
        "-i", file_path,
        "-ss", str(cut_seconds),
        "-c", "copy",
        temp_file
    ]
    
    try:
        # Exécution silencieuse sauf erreur
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        
        # Remplacement du fichier original
        os.replace(temp_file, file_path)
        print(f"   ✅ {filename} modifié avec succès.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Erreur FFMPEG sur {filename}: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return False

def generate_short_url(raw_url):
    """
    Génère une URL courte via TinyURL.
    """
    try:
        api_url = f"https://tinyurl.com/api-create.php?url={raw_url}"
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"   ⚠️ Erreur raccourcisseur URL: {e}")
    return raw_url

def create_qr_code(data, output_path):
    """
    Génère un QR code PNG.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    print(f"   🏷️  Tag généré: {os.path.basename(output_path)}")

def git_push_changes():
    """
    Ajoute, commit et push les modifications sur Git.
    """
    print("\n📦 Mise à jour Git...")
    try:
        # Git Add
        subprocess.run(["git", "add", "."], cwd=BASE_DIR, check=True)
        
        # Git Commit
        commit_msg = "Auto-update: Trim audio files & tags"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=BASE_DIR, check=False) # check=False car commit peut être vide
        
        # Git Push
        subprocess.run(["git", "push", "origin", BRANCH], cwd=BASE_DIR, check=True)
        print("✅  Git Push effectué avec succès !")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur Git: {e}")

def main():
    print("="*50)
    print("🎧 SCRIPT DE TRAITEMENT ABONNÉS RADIO CLASSIQUE")
    print("="*50)
    
    files_processed = 0
    
    # Vérification du dossier racine
    if not os.path.exists(AUDIO_DIR):
        print(f"❌ Dossier racine introuvable: {AUDIO_DIR}")
        return

    # Scan des dossiers numériques (ex: "12", "16", "40"...)
    for folder_name in os.listdir(AUDIO_DIR):
        folder_path = os.path.join(AUDIO_DIR, folder_name)
        
        # On ignore les fichiers et les dossiers non-numériques
        if not os.path.isdir(folder_path) or not folder_name.isdigit():
            continue

        cut_duration = int(folder_name)
        print(f"\n📁 Dossier '{folder_name}' (Coupe auto à {cut_duration}s)")

        
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".mp3"):
                file_path = os.path.join(folder_path, filename)
                
                # Nom du fichier QR
                qr_filename = os.path.splitext(filename)[0] + "_qr.png"
                qr_path = os.path.join(folder_path, qr_filename)
                
                # Check safeguards: if QR exists, assume file already processed
                if os.path.exists(qr_path):
                    print(f"   ⏩ {filename} déjà traité (Tag existant). Ignoré.")
                    continue

                # 1. Modifier le MP3
                if trim_audio(file_path, cut_duration):
                    files_processed += 1
                
                # 2. Générer le Tag (QR Code) (Moved logic here)
                # Structure URL GitHub Raw
                # media/audio/Radio_Classique/16/filename.mp3
                rel_path = f"media/audio/Radio_Classique/{folder_name}/{filename}"
                # Encoding URL path parts properly
                rel_path_encoded = requests.utils.quote(rel_path) 
                
                raw_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{rel_path_encoded}"
                
                # Raccourcir l'URL (comme app.js)
                short_url = generate_short_url(raw_url)
                
                create_qr_code(short_url, qr_path)

    if files_processed > 0:
        git_push_changes()
    else:
        print("\nℹ️  Aucun fichier MP3 n'a été traité.")

    print("\n✅ Opération terminée.")

if __name__ == "__main__":
    main()
