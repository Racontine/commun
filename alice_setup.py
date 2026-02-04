import os
import json
import subprocess
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Paths
CONFIG_FILE = "/home/alice/media/config.json"
WPA_SUPPLICANT_FILE = "/etc/wpa_supplicant/wpa_supplicant.conf"

# Fallback for dev/testing
if not os.path.exists(CONFIG_FILE) and os.path.exists("./config.json"):
    CONFIG_FILE = "./config.json"
    WPA_SUPPLICANT_FILE = "./wpa_supplicant.mock.conf"  # Mock for testing

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(volume):
    data = load_config()
    data['volume'] = int(volume)
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def append_wifi(ssid, psk, priority=60):
    if not ssid:
        return False
    
    # Simple formatting for wpa_supplicant
    try:
        prio = int(priority)
    except:
        prio = 60

    block = f"""
network={{
    ssid="{ssid}"
    psk="{psk}"
    priority={prio}
}}
"""
    try:
        with open(WPA_SUPPLICANT_FILE, "a") as f:
            f.write(block)
        return True
    except Exception as e:
        print(f"Error writing wifi config: {e}")
        return False

def get_ip():
    try:
        cmd = "hostname -I | awk '{print $1}'"
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except:
        return "Unknown"

@app.route("/", methods=["GET"])
def index():
    config = load_config()
    volume = config.get("volume", 90)
    ip = get_ip()
    return render_template("setup.html", volume=volume, ip_address=ip)

@app.route("/configure", methods=["POST"])
def configure():
    volume = request.form.get("volume")
    ssid = request.form.get("ssid")
    psk = request.form.get("psk")
    priority = request.form.get("priority", 60)

    # Save Volume
    if volume:
        save_config(volume)

    # Save WiFi if provided
    if ssid and psk:
        append_wifi(ssid, psk, priority)

    # Trigger restart
    # In a real scenario, we might want to just restart wifi or reboot.
    # We will trigger a reboot after a small delay to allow the response to return.
    subprocess.Popen("sleep 3 && sudo reboot", shell=True)

    return f"""
    <div style='font-family:sans-serif; text-align:center; padding:50px;'>
        <h1>Configuration Sauvegardée !</h1>
        <p>Volume réglé sur {volume}%.</p>
        <p>{f"WiFi '{ssid}' ajouté." if ssid else "Aucun changement WiFi."}</p>
        <p>Le système va redémarrer dans 3 secondes...</p>
        <p><a href="/">Retour</a></p>
    </div>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
