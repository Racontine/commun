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
echo -e "${YELLOW}⚙️  Installation du service systemd...${NC}"
sudo cp system/alice_son.service /etc/systemd/system/alice_son.service
sudo systemctl daemon-reload

echo ""
echo -e "${YELLOW}🔐 Configuration des permissions sudo...${NC}"
sudo cp system/alice-sudoers /etc/sudoers.d/alice-son
sudo chmod 0440 /etc/sudoers.d/alice-son
echo "    → alice peut maintenant redémarrer alice.service sans mot de passe"

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
echo "========================================"
echo "🌐 Accès à l'interface:"
echo "========================================"
IP=$(hostname -I | awk '{print $1}')
echo -e "${GREEN}http://${IP}:8080${NC}"
echo ""
echo "📝 Commandes utiles:"
echo "  • Voir les logs:        sudo journalctl -u alice_son.service -f"
echo "  • Redémarrer:           sudo systemctl restart alice_son.service"
echo "  • Arrêter:              sudo systemctl stop alice_son.service"
echo "  • Désactiver au boot:   sudo systemctl disable alice_son.service"
echo ""
