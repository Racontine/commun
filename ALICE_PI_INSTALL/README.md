# 🐰 Alice Box - Raspberry Pi Installation

Ce dossier contient tous les fichiers nécessaires pour installer et configurer Alice Box sur un Raspberry Pi.

## 📁 Structure du Projet

```
ALICE_PI_INSTALL/
├── src/
│   ├── alice.py              # Application principale (scan QR + lecture audio)
│   ├── ALICE_SON.py          # 🆕 Serveur web de contrôle du volume
│   ├── player.py             # Module de lecture audio
│   └── startup.py            # Script de démarrage
├── system/
│   ├── alice.service         # Service systemd pour alice.py
│   ├── alice_son.service     # 🆕 Service systemd pour ALICE_SON.py
│   ├── alice-sudoers         # 🆕 Permissions sudo pour alice
│   ├── autohotspot.service   # Service systemd pour autohotspot
│   ├── autohotspot.sh        # Script de bascule Auto/Hotspot
│   ├── setup_dnsmasq.conf    # Config DHCP (mode hotspot)
│   └── setup_hostapd.conf    # Config point d'accès (mode hotspot)
├── docs/
│   ├── HOW TO wifi.txt       # Guide WiFi
│   ├── HOW_TO_AUTOSTART.md   # Guide autostart
│   └── ALICE_SON_DOCUMENTATION.md  # 🆕 Doc technique ALICE_SON
├── requirements_son.txt      # 🆕 Dépendances Python pour ALICE_SON
├── install_alice_son.sh      # 🆕 Script d'installation ALICE_SON
├── README_ALICE_SON.md       # 🆕 Documentation complète ALICE_SON
├── GUIDE_RAPIDE.md           # 🆕 Guide rapide utilisateur
├── waltrhought.txt           # Notes d'installation hotspot
└── README.md                 # Ce fichier
```

---

## 🎯 Deux Modes de Fonctionnement

### 1. **Mode Normal** (Utilisation quotidienne)
- Alice se connecte au WiFi de la maison
- Scanner les QR codes → Lecture audio automatique
- **🆕 Contrôle du volume** via `http://<IP_PI>:8080` (**Nouveau !**)

### 2. **Mode Hotspot** (Configuration initiale ou dépannage)
- Alice crée son propre réseau WiFi : `ALICE_SETUP`
- Interface de configuration complète sur `http://192.168.50.1`
- Configuration WiFi + Volume + Priorités réseau

---

## 🚀 Installation Initiale

### Prérequis
- Raspberry Pi (Zero 2W ou modèle supérieur)
- Carte SD avec Raspberry Pi OS
- Connexion Internet pendant l'installation
- Utilisateur `alice` créé

### Étape 1 : Installation des Dépendances Système

```bash
# Se connecter au Pi
ssh alice@<IP_DU_PI>

# Installer les packages requis
sudo apt update
sudo apt install -y \
  hostapd \
  dnsmasq \
  python3-pip \
  python3-opencv \
  python3-picamera2 \
  python3-gpiozero \
  python3-requests \
  mpg123 \
  alsa-utils

# Installer les dépendances Python
sudo pip3 install pyzbar Flask Werkzeug
```

### Étape 2 : Transférer les Fichiers

```bash
# Depuis votre ordinateur
scp -r ALICE_PI_INSTALL alice@<IP_DU_PI>:/home/alice/
```

### Étape 3 : Installation d'Alice (Principal)

```bash
ssh alice@<IP_DU_PI>
cd /home/alice/ALICE_PI_INSTALL

# Copier alice.py
sudo cp src/alice.py /home/alice/alice.py
sudo chown alice:alice /home/alice/alice.py
sudo chmod +x /home/alice/alice.py

# Installer le service
sudo cp system/alice.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable alice.service
sudo systemctl start alice.service
```

### Étape 4 : Installation du Mode Hotspot

```bash
# Copier les fichiers de configuration
sudo cp system/autohotspot.sh /home/alice/
sudo cp system/setup_hostapd.conf /home/alice/
sudo cp system/setup_dnsmasq.conf /home/alice/
sudo chmod +x /home/alice/autohotspot.sh

# Installer le service
sudo cp system/autohotspot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable autohotspot.service
```

### Étape 5 : 🆕 Installation d'ALICE_SON (Contrôle Volume)

```bash
cd /home/alice/ALICE_PI_INSTALL
chmod +x install_alice_son.sh
sudo ./install_alice_son.sh
```

Le script va :
- ✅ Installer Flask
- ✅ Copier ALICE_SON.py
- ✅ Configurer le service systemd
- ✅ Configurer les permissions sudo
- ✅ Démarrer le serveur
- ✅ Afficher l'URL d'accès

**Accès : `http://<IP_DU_PI>:8080`**

---

## 🔊 Contrôle du Volume - Deux Méthodes

### 🆕 **Méthode 1 : ALICE_SON (Recommandée)**

**Avantages :**
- ✅ **Pas de coupure WiFi**
- ✅ **Pas besoin de SSH**
- ✅ Rapide (30 secondes)
- ✅ Interface moderne et mobile-friendly
- ✅ Accessible depuis n'importe quel appareil sur le réseau

**Utilisation :**
1. Ouvrir `http://<IP_DU_PI>:8080` dans un navigateur
2. Ajuster le volume avec le slider (0-100%)
3. Cliquer sur "Sauvegarder"
4. Alice redémarre automatiquement

📖 **Documentation complète :** [README_ALICE_SON.md](README_ALICE_SON.md)  
📖 **Guide rapide :** [GUIDE_RAPIDE.md](GUIDE_RAPIDE.md)

---

### **Méthode 2 : Mode Hotspot (Configuration complète)**

**Utilisation :**
1. Se connecter en SSH
2. Forcer le mode hotspot :
   ```bash
   sudo bash /home/alice/autohotspot.sh force
   ```
3. Connecter le téléphone au WiFi `ALICE_SETUP` (mot de passe : `alicebox`)
4. Aller sur `http://192.168.50.1`
5. Configurer Volume + WiFi + Priorités
6. Valider → Le Pi redémarre

**Inconvénients :**
- ❌ Coupe la connexion WiFi
- ❌ Nécessite SSH
- ❌ Plus long (~5 minutes)

---

## 📊 Comparaison des Méthodes

| Critère | ALICE_SON | Mode Hotspot |
|---------|-----------|--------------|
| **Connexion WiFi** | ✅ Maintenue | ❌ Coupée |
| **Accès Internet** | ✅ Oui | ❌ Non |
| **Temps requis** | 30 sec | ~5 min |
| **Terminal SSH** | ❌ Non requis | ✅ Requis |
| **Multi-utilisateurs** | ✅ Oui | ❌ Non |
| **Mobile-friendly** | ✅ Excellent | Moyen |
| **Configuration WiFi** | ❌ Non | ✅ Oui |
| **Priorités réseau** | ❌ Non | ✅ Oui |

**💡 Recommandation :** 
- Utilisez **ALICE_SON** pour les ajustements quotidiens du volume
- Utilisez le **Mode Hotspot** uniquement pour la configuration initiale ou changement de réseau WiFi

---

## 📝 Configuration

### Fichier config.json

**Emplacement :** `/home/alice/media/config.json`

**Structure :**
```json
{
  "volume": 90,
  "wifi_priority": [
    "NomWiFi1",
    "NomWiFi2"
  ]
}
```

**Important :** Ce fichier DOIT être dans `/home/alice/media/` !

---

## 🔧 Commandes Utiles

### Alice (Principal)

```bash
# Statut du service
sudo systemctl status alice.service

# Voir les logs
sudo journalctl -u alice.service -f

# Redémarrer
sudo systemctl restart alice.service

# Arrêter
sudo systemctl stop alice.service
```

### ALICE_SON (Contrôle Volume)

```bash
# Statut du service
sudo systemctl status alice_son.service

# Voir les logs
sudo journalctl -u alice_son.service -f

# Redémarrer
sudo systemctl restart alice_son.service

# URL d'accès
hostname -I  # Récupérer l'IP, puis http://<IP>:8080
```

### Mode Hotspot

```bash
# Forcer le mode hotspot
sudo bash /home/alice/autohotspot.sh force

# Statut du service
sudo systemctl status autohotspot.service

# Voir les logs
sudo journalctl -u autohotspot.service -f
```

---

## 🐛 Dépannage

### Alice ne démarre pas

1. Vérifier les logs :
   ```bash
   sudo journalctl -u alice.service -n 50
   ```

2. Tester manuellement :
   ```bash
   cd /home/alice
   python3 alice.py
   ```

3. Vérifier les dépendances :
   ```bash
   python3 -c "import cv2, picamera2, pyzbar, gpiozero, requests"
   ```

### ALICE_SON ne démarre pas

Voir le [README_ALICE_SON.md](README_ALICE_SON.md) section "Dépannage"

### Mode Hotspot ne fonctionne pas

1. Vérifier le pays dans `setup_hostapd.conf` : `country_code=FR`
2. Vérifier que `alice.service` est bien arrêté (conflit de ressources)
3. Vérifier les logs : `sudo journalctl -u autohotspot.service -f`

### Le volume ne change pas

1. **Avec ALICE_SON :**
   - Vérifier que vous avez cliqué sur "Sauvegarder"
   - Vérifier que alice.service a redémarré
   - Vérifier `/home/alice/media/config.json`

2. **Avec Mode Hotspot :**
   - Vérifier que `config.json` est dans `/home/alice/media/`
   - Vérifier le contenu du fichier

---

## 📚 Documentation Détaillée

- **[README_ALICE_SON.md](README_ALICE_SON.md)** - Documentation complète ALICE_SON
- **[GUIDE_RAPIDE.md](GUIDE_RAPIDE.md)** - Guide rapide utilisateur
- **[docs/ALICE_SON_DOCUMENTATION.md](docs/ALICE_SON_DOCUMENTATION.md)** - Documentation technique
- **[docs/HOW TO wifi.txt](docs/HOW%20TO%20wifi.txt)** - Guide configuration WiFi
- **[docs/HOW_TO_AUTOSTART.md](docs/HOW_TO_AUTOSTART.md)** - Guide autostart
- **[waltrhought.txt](waltrhought.txt)** - Notes installation hotspot

---

## 🔒 Sécurité

### Permissions Sudo
- Alice peut redémarrer `alice.service` sans mot de passe
- Configuration : `/etc/sudoers.d/alice-son`

### Accès Réseau
- ALICE_SON écoute sur toutes les interfaces (0.0.0.0:8080)
- Accessible depuis tout le réseau local
- **Recommandation :** Utiliser uniquement sur réseau de confiance

---

## 🎉 Fonctionnalités

### ✅ Implémenté
- [x] Scan QR codes avec caméra
- [x] Téléchargement automatique des médias
- [x] Lecture audio MP3/WAV
- [x] Contrôle lecture via bouton tactile (play/pause)
- [x] Reset via bouton HAT
- [x] Configuration volume via `config.json`
- [x] Mode hotspot pour configuration initiale
- [x] 🆕 **Interface web de contrôle du volume (ALICE_SON)**
- [x] 🆕 **Sauvegarde automatique et redémarrage**
- [x] 🆕 **Interface responsive mobile-friendly**

### 🔮 Améliorations Futures
- [ ] Interface web pour gestion complète WiFi
- [ ] Historique des médias lus
- [ ] Statistiques d'utilisation
- [ ] Contrôle vocal
- [ ] Application mobile dédiée

---

## 📜 Historique

- **2026-02-05** : Ajout d'ALICE_SON pour contrôle volume sans hotspot
- **2026-01-XX** : Configuration mode hotspot
- **2025-XX-XX** : Version initiale d'alice.py

---

## 👤 Auteur

Projet Alice Box - Raspberry Pi Media Player with QR Code Scanner

---

## 📞 Support

Pour tout problème :
1. Consulter la section "Dépannage" ci-dessus
2. Vérifier les logs des services
3. Consulter la documentation détaillée dans `/docs`

---

**⚡ Astuce :** Créez un raccourci sur votre téléphone vers `http://<IP_PI>:8080` pour contrôler le volume d'Alice en 1 clic ! 🎯
