#!/bin/bash

echo "========================================"
echo "🔊 Installation ALICE_SON"
echo "Contrôle du volume sans mode hotspot"
echo "========================================"
echo ""

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Vérifier qu'on est bien sur le Pi
if [ ! -d "/home/alice" ]; then
    echo -e "${YELLOW}⚠️  ATTENTION: Le dossier /home/alice n'existe pas.${NC}"
    echo "Ce script doit être exécuté sur le Raspberry Pi avec l'utilisateur 'alice'."
    read -p "Continuer quand même ? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${YELLOW}📦 Installation des dépendances Python...${NC}"
sudo pip3 install Flask==3.0.0 Werkzeug==3.0.1

echo ""
echo -e "${YELLOW}📋 Copie de ALICE_SON.py...${NC}"
sudo cp src/ALICE_SON.py /home/alice/ALICE_SON.py
sudo chown alice:alice /home/alice/ALICE_SON.py
sudo chmod +x /home/alice/ALICE_SON.py

echo ""
echo -e "${YELLOW}📡 Installation de l'interface hotspot (Racontine)...${NC}"
# Créer le dossier et copier les fichiers
sudo mkdir -p /home/alice/wifi_setup
sudo cp -r system/wifi_setup/* /home/alice/wifi_setup/
sudo chown -R alice:alice /home/alice/wifi_setup
sudo chmod +x /home/alice/wifi_setup/wifi_setup_server.py

# Update autohotspot script and configs
echo "Mise à jour du script Hotspot..."
sudo cp system/autohotspot.sh /home/alice/autohotspot.sh
sudo cp system/setup_hostapd.conf /home/alice/setup_hostapd.conf
sudo cp system/setup_dnsmasq.conf /home/alice/setup_dnsmasq.conf
sudo chown alice:alice /home/alice/autohotspot.sh /home/alice/setup_*.conf
sudo chmod +x /home/alice/autohotspot.sh

echo ""
echo -e "${YELLOW}⚙️  Installation du service systemd...${NC}"
sudo cp system/alice_son.service /etc/systemd/system/alice_son.service
sudo systemctl daemon-reload

echo ""
echo -e "${YELLOW}🔐 Configuration des permissions sudo...${NC}"
# Création directe du fichier pour éviter les erreurs de format (CRLF)
echo "alice ALL=(ALL) NOPASSWD: /bin/systemctl restart alice.service" | sudo tee /etc/sudoers.d/alice-son > /dev/null
echo "alice ALL=(ALL) NOPASSWD: /usr/bin/bash /home/alice/autohotspot.sh force" | sudo tee -a /etc/sudoers.d/alice-son > /dev/null
sudo chmod 0440 /etc/sudoers.d/alice-son

# Vérification de la syntaxe
if sudo visudo -c -f /etc/sudoers.d/alice-son; then
    echo "    ✅ Syntaxe sudoers valide"
else
    echo -e "${RED}❌ Erreur de syntaxe dans sudoers !${NC}"
    sudo rm /etc/sudoers.d/alice-son
fi

echo ""
echo -e "${YELLOW}🚀 Activation du service au démarrage...${NC}"
sudo systemctl enable alice_son.service

echo ""
echo -e "${YELLOW}▶️  Démarrage du service...${NC}"
sudo systemctl start alice_son.service

echo ""
echo -e "${GREEN}✅ Installation terminée !${NC}"
echo ""
echo "========================================"
echo "📊 Statut du service:"
echo "========================================"
sudo systemctl status alice_son.service --no-pager

echo ""
echo ""
echo -e "${YELLOW}🏷️  Configuration du nom réseau (Hostname)...${NC}"
CURRENT_HOSTNAME=$(cat /etc/hostname | tr -d " \t\n\r")
NEW_HOSTNAME="racontine"

if [ "$CURRENT_HOSTNAME" != "$NEW_HOSTNAME" ]; then
    echo "Changement du nom : $CURRENT_HOSTNAME -> $NEW_HOSTNAME"
    echo "$NEW_HOSTNAME" | sudo tee /etc/hostname > /dev/null
    sudo sed -i "s/127.0.1.1.*$CURRENT_HOSTNAME/127.0.1.1\t$NEW_HOSTNAME/g" /etc/hosts
    echo "✅ Nom changé. Un redémarrage sera nécessaire."
else
    echo "✅ Le nom est déjà 'racontine'."
fi

echo ""
echo "========================================"
echo "🌐 Accès à l'interface:"
echo "========================================"
IP=$(hostname -I | awk '{print $1}')
echo -e "${GREEN}http://racontine.local:8080${NC} (Recommandé)"
echo -e "${GREEN}http://${IP}:8080${NC} (IP Directe)"
echo ""
echo "📝 Commandes utiles:"
echo "  • Voir les logs:        sudo journalctl -u alice_son.service -f"
echo "  • Redémarrer:           sudo systemctl restart alice_son.service"
echo "  • Arrêter:              sudo systemctl stop alice_son.service"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANT : Si le hostname a changé, redémarrez le Pi maintenant :${NC}"
echo "   sudo reboot"
echo ""
