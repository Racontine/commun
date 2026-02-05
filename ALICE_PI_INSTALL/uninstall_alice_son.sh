#!/bin/bash

echo "========================================"
echo "🗑️  Désinstallation ALICE_SON"
echo "========================================"
echo ""

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${RED}⚠️  ATTENTION : Cette action va supprimer ALICE_SON${NC}"
echo ""
read -p "Êtes-vous sûr de vouloir continuer ? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Annulé."
    exit 0
fi

echo ""
echo -e "${YELLOW}⏸️  Arrêt du service...${NC}"
sudo systemctl stop alice_son.service

echo ""
echo -e "${YELLOW}🚫 Désactivation du service au démarrage...${NC}"
sudo systemctl disable alice_son.service

echo ""
echo -e "${YELLOW}🗑️  Suppression du service systemd...${NC}"
sudo rm -f /etc/systemd/system/alice_son.service
sudo systemctl daemon-reload

echo ""
echo -e "${YELLOW}🗑️  Suppression de ALICE_SON.py...${NC}"
sudo rm -f /home/alice/ALICE_SON.py

echo ""
echo -e "${YELLOW}🗑️  Suppression de la config sudoers...${NC}"
sudo rm -f /etc/sudoers.d/alice-son

echo ""
echo -e "${GREEN}✅ Désinstallation terminée !${NC}"
echo ""
echo "Note : Flask reste installé (peut être utilisé par d'autres applications)."
echo "Pour désinstaller Flask : sudo pip3 uninstall Flask Werkzeug"
echo ""
echo "Le fichier config.json a été conservé dans /home/alice/media/"
echo ""
