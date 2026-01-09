import os
import urllib.parse
import requests

BASE_DIR = "/home/alice/media"
AUDIO_DIR = f"{BASE_DIR}/audio"
VIDEO_DIR = f"{BASE_DIR}/video"

def _normalize_url(raw: str) -> str:
    raw = (raw or "").strip()
    if not raw:
        return raw
    if raw.startswith("http://") or raw.startswith("https://"):
        return raw
    return "https://" + raw

def resolve_final_url(raw_url: str) -> str:
    url = _normalize_url(raw_url)
    try:
        r = requests.head(url, allow_redirects=True, timeout=10)
        if r.url:
            return r.url
    except Exception:
        pass
    r = requests.get(url, allow_redirects=True, stream=True, timeout=15)
    return r.url

def ensure_file(raw_url: str) -> str:
    final_url = resolve_final_url(raw_url)
    print(f"🔗 URL finale : {final_url}")

    filename = urllib.parse.urlparse(final_url).path.split("/")[-1]
    ext = os.path.splitext(filename)[1].lower()

    if ext in [".mp3", ".wav"]:
        dest_dir = AUDIO_DIR
    else:
        dest_dir = VIDEO_DIR

    os.makedirs(dest_dir, exist_ok=True)
    local_path = os.path.join(dest_dir, filename)

    if not os.path.exists(local_path):
        print(f"⬇️ Téléchargement : {final_url}")
        r = requests.get(final_url, timeout=30)
        r.raise_for_status()
        with open(local_path, "wb") as f:
            f.write(r.content)
        print(f"✅ Téléchargé : {local_path}")
    else:
        print(f"📁 Déjà présent : {local_path}")

    return local_path
