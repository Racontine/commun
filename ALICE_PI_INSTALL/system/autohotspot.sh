#!/bin/bash

# Chemins
HOSTAPD_CONF="/home/alice/setup_hostapd.conf"
DNSMASQ_CONF="/home/alice/setup_dnsmasq.conf"
SETUP_SCRIPT="/home/alice/wifi_setup/wifi_setup_server.py"

# --- FIX LINE ENDINGS (CRLF -> LF) ---
# Sécurité : on nettoie les fichiers de conf au cas où ils viennent de Windows
sed -i 's/\r//' "$HOSTAPD_CONF"
sed -i 's/\r//' "$DNSMASQ_CONF"

# Fonction pour démarrer le Hotspot
start_hotspot() {
    echo "🌐 Mode Hotspot activé"
    # Arrêt du wifi client et services concurrents
    systemctl stop wpa_supplicant
    systemctl mask wpa_supplicant
    systemctl stop dhcpcd  # CONFLIT POTENTIEL : On arrête aussi le gestionnaire DHCP client
    systemctl stop dnsmasq
    systemctl stop hostapd
    systemctl stop alice.service # On arrête Alice pour libérer les ressources et éviter les conflits
    killall dnsmasq 2>/dev/null
    
    # Configuration IP statique temporaire
    
    # Configuration IP statique temporaire
    ip link set wlan0 down
    ip addr flush dev wlan0
    ip link set wlan0 up
    ip addr add 192.168.50.1/24 dev wlan0
    iw wlan0 set power_save off  # Désactive l'économie d'énergie
    
    # Démarrage des services
    systemctl unmask hostapd
    # Unblock all radios
    rfkill unblock wlan
    
    hostapd -B "$HOSTAPD_CONF"
    dnsmasq -C "$DNSMASQ_CONF"
    
    echo "📊 DIAGNOSTIC WIFI :"
    iw dev wlan0 info
    iwconfig wlan0
    
    # Lancement du serveur Web de config
    python3 "$SETUP_SCRIPT"
}

# Fonction pour tester la connexion
check_connection() {
    # On attend un peu que le wifi se connecte au boot
    sleep 20
    # On ping un DNS google ou autre
    if ping -c 1 8.8.8.8 &> /dev/null; then
        return 0 # Connecté
    else
        return 1 # Pas connecté
    fi
}

# --- Main Logic ---

# Check if "force" argument is passed
if [ "$1" == "force" ]; then
    echo "💪 Mode FORCE activé. Démarrage du Hotspot..."
    start_hotspot
    exit 0
fi

echo "🔍 Vérification de la connexion internet..."
if check_connection; then
    echo "✅ Connecté à Internet via WiFi. Lancement normal."
    # Ici, on ne fait rien de spécial, alice.py sera lancé par son propre service
    exit 0
else
    echo "⚠️ Pas de connexion Internet."
    start_hotspot
fi
