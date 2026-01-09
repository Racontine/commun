#!/usr/bin/env python3

import time
import cv2
import subprocess
import signal
import sys
from pathlib import Path
from picamera2 import Picamera2
from pyzbar.pyzbar import decode
from gpiozero import Button


# ======================
# DOWNLOADER LOGIC (Integrated)
# ======================
import os
import urllib.parse
import requests

BASE_DL_DIR = "/home/alice/media"
AUDIO_DIR = f"{BASE_DL_DIR}/audio"
VIDEO_DIR = f"{BASE_DL_DIR}/video"

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


# ======================
# CONFIG
# ======================
DEFAULT_VOLUME_PERCENT = 90
DEFAULT_GAIN = int(8192 * DEFAULT_VOLUME_PERCENT / 100)

COOLDOWN_SEC = 3
WELCOME_AUDIO = "/home/alice/media/audio/welcome_alice_woman.mp3"
DETECTED_AUDIO = "/home/alice/media/audio/carte_detected.mp3"

TOUCH_GPIO = 12        # bouton tactile → play / pause
HAT_BUTTON_GPIO = 17   # bouton HAT → reset scan QR

# Optimization Config
FRAME_SKIP = 3  # Analyze 1 out of every 3 frames


# ======================
# AUDIO PLAYER CLASS
# ======================
class AudioPlayer:
    def __init__(self):
        self.process = None
        self.paused = False
        self.current_path = None

    def play_blocking(self, path: str):
        """Plays audio and waits for it to finish."""
        print(f"▶️  Lecture (bloquante) : {path}")
        cmd = self._get_cmd(path)
        subprocess.run(cmd, check=False)

    def start(self, path: str):
        """Starts audio in background (kill previous if any)."""
        self.stop()
        self.current_path = path
        self.paused = False
        
        print(f"▶️  Lecture : {path}")
        cmd = self._get_cmd(path)
        self.process = subprocess.Popen(cmd)

    def stop(self):
        """Stops current background audio."""
        if self.process:
            if self.process.poll() is None:
                try:
                    self.process.terminate()
                    self.process.wait(timeout=2)
                except Exception:
                    self.process.kill()
            self.process = None
        self.paused = False
        self.current_path = None

    def toggle_pause(self):
        """Toggles pause/resume for current background audio."""
        if not self.process or self.process.poll() is not None:
            return

        if self.current_path and self.current_path.lower().endswith(".wav"):
            print("ℹ️  Pause ignorée sur WAV (aplay ne gère pas SIGSTOP correctement)")
            return

        try:
            if not self.paused:
                self.process.send_signal(signal.SIGSTOP)
                self.paused = True
                print("⏸️  Pause")
            else:
                self.process.send_signal(signal.SIGCONT)
                self.paused = False
                print("▶️  Reprise")
        except Exception as e:
            print(f"⚠️  Erreur pause/play: {e}")

    def _get_cmd(self, path: str):
        if path.lower().endswith(".mp3"):
            return ["mpg123", "-q", "-f", str(DEFAULT_GAIN), path]
        else:
            return ["aplay", "-q", "-f", str(DEFAULT_GAIN), path]


# ======================
# GLOBAL STATE
# ======================
player = AudioPlayer()


# ======================
# CAMERA INIT
# ======================
def init_camera():
    cam = Picamera2()
    # Optimized: 640x480 resolution for faster processing
    config = cam.create_still_configuration(
        main={"size": (640, 480), "format": "RGB888"},
        buffer_count=2
    )
    cam.configure(config)
    cam.start()
    time.sleep(0.5)
    return cam


# ======================
# BUTTONS HANDLERS
# ======================
def on_touch_pressed():
    print("👆 Touch → play/pause")
    player.toggle_pause()

def on_hat_pressed():
    print("🔄 Bouton HAT → retour scan QR")
    player.stop()
    if Path(DETECTED_AUDIO).exists():
        player.play_blocking(DETECTED_AUDIO)


# ======================
# MAIN LOOP
# ======================
def main():
    cam = init_camera()
    
    # Init Buttons
    touch_button = Button(TOUCH_GPIO)
    hat_button = Button(HAT_BUTTON_GPIO)
    touch_button.when_pressed = on_touch_pressed
    hat_button.when_pressed = on_hat_pressed

    print("📸 Alice prête – scan QR optimisé en cours (CTRL+C pour quitter)")

    if Path(WELCOME_AUDIO).exists():
        player.play_blocking(WELCOME_AUDIO)
    else:
        print("⚠️ WELCOME_AUDIO introuvable")

    last_play_time = 0
    frame_count = 0

    try:
        while True:
            # Optimized: Capture directly to array (memory)
            # Picamera2 returns RGB by default with our config, perfect for cv2 (needs converting to BGR mainly for display, but for QR detection Gray is enough)
            image = cam.capture_array()
            
            # Optimization: Frame Skipping
            frame_count += 1
            if frame_count % FRAME_SKIP != 0:
                # Skip detection for this frame
                continue

            # Standard cv2 conversion
            # picamera2 returns RGB, we need Gray for pyzbar
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            codes = decode(gray)
            if not codes:
                # Small sleep to be nice to CPU if we are looping very fast
                time.sleep(0.05)
                continue

            # Check Cooldown
            now = time.time()
            if now - last_play_time < COOLDOWN_SEC:
                continue

            # Process Code
            qr_text = codes[0].data.decode("utf-8").strip()
            print(f"🔍 QR détecté : {qr_text}")

            if Path(DETECTED_AUDIO).exists():
               player.play_blocking(DETECTED_AUDIO)

            # Download & Play
            local_path = ensure_file(qr_text)
            player.start(local_path)

            last_play_time = time.time()

    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé")
    except Exception as e:
        print(f"\n⚠️ Erreur fatale: {e}")
    finally:
        cam.stop()
        player.stop()


if __name__ == "__main__":
    main()
