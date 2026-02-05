# 📊 ALICE BOX - Tableau de Bord

Accès rapide à toutes les ressources du projet Alice Box.

---

## 🌐 Accès Web

| Service | URL | Description |
|---------|-----|-------------|
| **ALICE_SON** 🆕 | `http://<IP_PI>:8080` | Contrôle du volume (recommandé) |
| **Mode Hotspot** | `http://192.168.50.1` | Configuration complète (WiFi + Volume) |

### 🔍 Trouver l'IP du Pi

```bash
hostname -I
```

---

## 📁 Documentation

### 🚀 Pour Démarrer Rapidement

| Fichier | Objectif | Niveau |
|---------|----------|--------|
| [GUIDE_RAPIDE.md](GUIDE_RAPIDE.md) | Installation et utilisation en 5 minutes | ⭐ Débutant |
| [RECAP_ALICE_SON.txt](RECAP_ALICE_SON.txt) | Vue d'ensemble visuelle avec ASCII | ⭐ Débutant |
| [AIDE_ALICE_SON.txt](AIDE_ALICE_SON.txt) | Pense-bête commandes | ⭐ Débutant |

### 📖 Documentation Complète

| Fichier | Objectif | Niveau |
|---------|----------|--------|
| [README.md](README.md) | Vue d'ensemble du projet | ⭐⭐ Intermédiaire |
| [README_ALICE_SON.md](README_ALICE_SON.md) | Doc ALICE_SON détaillée | ⭐⭐ Intermédiaire |
| [docs/ALICE_SON_DOCUMENTATION.md](docs/ALICE_SON_DOCUMENTATION.md) | Doc technique complète | ⭐⭐⭐ Avancé |

### 📜 Autres Documents

| Fichier | Objectif |
|---------|----------|
| [CHANGELOG.md](CHANGELOG.md) | Historique des versions |
| [config.json.example](config.json.example) | Exemple de configuration |
| [docs/HOW TO wifi.txt](docs/HOW%20TO%20wifi.txt) | Configuration WiFi |
| [docs/HOW_TO_AUTOSTART.md](docs/HOW_TO_AUTOSTART.md) | Configuration autostart |
| [waltrhought.txt](waltrhought.txt) | Notes d'installation hotspot |

---

## 🛠️ Scripts d'Installation

| Script | Commande | Description |
|--------|----------|-------------|
| **Installation ALICE_SON** | `sudo ./install_alice_son.sh` | Installe le contrôle du volume |
| **Désinstallation ALICE_SON** | `sudo ./uninstall_alice_son.sh` | Supprime le contrôle du volume |

### Installation Complète (Première fois)

```bash
# 1. Transférer les fichiers sur le Pi
scp -r ALICE_PI_INSTALL alice@<IP_PI>:/home/alice/

# 2. Se connecter
ssh alice@<IP_PI>

# 3. Installer Alice (principal)
cd /home/alice/ALICE_PI_INSTALL
sudo cp src/alice.py /home/alice/alice.py
sudo cp system/alice.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable alice.service
sudo systemctl start alice.service

# 4. Installer ALICE_SON (contrôle volume)
chmod +x install_alice_son.sh
sudo ./install_alice_son.sh
```

---

## 🎯 Cas d'Usage

### 📊 Changer le Volume (Quotidien)

**🆕 Méthode Recommandée : ALICE_SON**
1. Ouvrir `http://<IP_PI>:8080`
2. Ajuster le slider
3. Cliquer "Sauvegarder"

**Alternative : Mode Hotspot**
1. `sudo bash /home/alice/autohotspot.sh force`
2. Connecter au WiFi ALICE_SETUP
3. Aller sur `http://192.168.50.1`
4. Configurer et valider

### 🔧 Configuration Initiale (Une fois)

**Mode Hotspot requis**
1. Le Pi démarre en mode hotspot automatiquement (pas de WiFi configuré)
2. Connecter au WiFi ALICE_SETUP (mot de passe : `alicebox`)
3. Aller sur `http://192.168.50.1`
4. Configurer WiFi + Volume
5. Valider → Le Pi redémarre en mode normal

### 🐛 Dépannage

**Consulter :**
1. [README_ALICE_SON.md](README_ALICE_SON.md) - Section Dépannage
2. [docs/ALICE_SON_DOCUMENTATION.md](docs/ALICE_SON_DOCUMENTATION.md) - Dépannage avancé
3. Logs du service : `sudo journalctl -u alice_son.service -f`

---

## 🔧 Commandes Rapides

### Alice (Principal)

```bash
# Statut
sudo systemctl status alice.service

# Logs
sudo journalctl -u alice.service -f

# Redémarrer
sudo systemctl restart alice.service

# Arrêter
sudo systemctl stop alice.service

# Démarrer
sudo systemctl start alice.service
```

### ALICE_SON (Contrôle Volume)

```bash
# Statut
sudo systemctl status alice_son.service

# Logs
sudo journalctl -u alice_son.service -f

# Redémarrer
sudo systemctl restart alice_son.service

# Arrêter
sudo systemctl stop alice_son.service

# Démarrer
sudo systemctl start alice_son.service

# Désinstaller
cd /home/alice/ALICE_PI_INSTALL
chmod +x uninstall_alice_son.sh
sudo ./uninstall_alice_son.sh
```

### Mode Hotspot

```bash
# Forcer le mode hotspot
sudo bash /home/alice/autohotspot.sh force

# Statut
sudo systemctl status autohotspot.service

# Logs
sudo journalctl -u autohotspot.service -f
```

### Système

```bash
# Trouver l'IP
hostname -I

# Voir la config
cat /home/alice/media/config.json

# Redémarrer le Pi
sudo reboot

# Éteindre le Pi
sudo shutdown -h now
```

---

## 📦 Structure des Fichiers

```
ALICE_PI_INSTALL/
│
├── 📂 src/
│   ├── alice.py              # ⭐ Application principale
│   ├── ALICE_SON.py          # 🆕 Serveur web contrôle volume
│   ├── player.py             # Module lecture audio
│   └── startup.py            # Script démarrage
│
├── 📂 system/
│   ├── alice.service         # Service alice.py
│   ├── alice_son.service     # 🆕 Service ALICE_SON.py
│   ├── alice-sudoers         # 🆕 Permissions sudo
│   ├── autohotspot.service   # Service hotspot
│   ├── autohotspot.sh        # Script bascule WiFi/Hotspot
│   ├── setup_dnsmasq.conf    # Config DHCP
│   └── setup_hostapd.conf    # Config point d'accès
│
├── 📂 docs/
│   ├── ALICE_SON_DOCUMENTATION.md  # 🆕 Doc technique
│   ├── HOW TO wifi.txt             # Guide WiFi
│   └── HOW_TO_AUTOSTART.md         # Guide autostart
│
├── 📄 README.md                    # ⭐ Vue d'ensemble
├── 📄 README_ALICE_SON.md          # 🆕 Doc ALICE_SON
├── 📄 GUIDE_RAPIDE.md              # 🆕 Guide rapide
├── 📄 RECAP_ALICE_SON.txt          # 🆕 Récap visuel
├── 📄 AIDE_ALICE_SON.txt           # 🆕 Pense-bête
├── 📄 CHANGELOG.md                 # 🆕 Historique versions
├── 📄 INDEX.md                     # ⭐ Ce fichier
├── 📄 config.json.example          # 🆕 Exemple config
├── 📄 requirements_son.txt         # 🆕 Dépendances Python
├── 🔧 install_alice_son.sh         # 🆕 Installation
├── 🔧 uninstall_alice_son.sh       # 🆕 Désinstallation
└── 📄 waltrhought.txt              # Notes hotspot
```

**Légende :**
- ⭐ Fichier important
- 🆕 Nouveau dans v1.1.0
- 📂 Dossier
- 📄 Documentation
- 🔧 Script

---

## 🎓 Parcours d'Apprentissage

### Niveau 1 : Débutant (Utilisation)

1. Lire : [GUIDE_RAPIDE.md](GUIDE_RAPIDE.md)
2. Installer : Suivre les étapes du guide
3. Utiliser : Ouvrir `http://<IP_PI>:8080`

**Objectif :** Contrôler le volume en 30 secondes

---

### Niveau 2 : Intermédiaire (Configuration)

1. Lire : [README.md](README.md)
2. Lire : [README_ALICE_SON.md](README_ALICE_SON.md)
3. Configurer : Mode hotspot, WiFi, volumes

**Objectif :** Maîtriser les deux modes (normal et hotspot)

---

### Niveau 3 : Avancé (Personnalisation)

1. Lire : [docs/ALICE_SON_DOCUMENTATION.md](docs/ALICE_SON_DOCUMENTATION.md)
2. Modifier : ALICE_SON.py pour personnaliser l'interface
3. Créer : Services systemd personnalisés

**Objectif :** Personnaliser et étendre Alice Box

---

## 🔗 Liens Utiles

### Dépendances

| Outil | Documentation |
|-------|---------------|
| Flask | https://flask.palletsprojects.com/ |
| Picamera2 | https://github.com/raspberrypi/picamera2 |
| OpenCV | https://docs.opencv.org/ |
| pyzbar | https://github.com/NaturalHistoryMuseum/pyzbar |

### Raspberry Pi

| Resource | URL |
|----------|-----|
| Documentation officielle | https://www.raspberrypi.com/documentation/ |
| Forums | https://forums.raspberrypi.com/ |
| GPIO | https://pinout.xyz/ |

---

## 💡 Astuces

### 🎯 Accès Ultra-Rapide au Contrôle du Volume

1. **Sur smartphone :**
   - Ouvrir `http://<IP_PI>:8080` dans le navigateur
   - Menu → "Ajouter à l'écran d'accueil"
   - Vous avez maintenant une app dédiée !

2. **Sur ordinateur :**
   - Ajouter `http://<IP_PI>:8080` aux favoris
   - Créer un raccourci sur le bureau

3. **Impression QR code :**
   - Générer un QR code pointant vers `http://<IP_PI>:8080`
   - Imprimer et coller sur le frigo/bureau

---

## 🆘 Support

### En cas de problème :

1. **Consulter la documentation** (ce tableau de bord)
2. **Vérifier les logs** : `sudo journalctl -u <service> -f`
3. **Consulter le dépannage** : [README_ALICE_SON.md](README_ALICE_SON.md)

### Checklist de dépannage :

- [ ] Le service tourne ? `sudo systemctl status <service>`
- [ ] L'IP est correcte ? `hostname -I`
- [ ] Le fichier config existe ? `cat /home/alice/media/config.json`
- [ ] Flask est installé ? `python3 -c "import flask"`
- [ ] Le port est libre ? `sudo netstat -tulpn | grep 8080`

---

## 📊 Statistiques du Projet

| Métrique | Valeur |
|----------|--------|
| **Fichiers Python** | 4 |
| **Services systemd** | 3 |
| **Scripts d'installation** | 2 |
| **Fichiers de documentation** | 11 |
| **Lignes de code (ALICE_SON.py)** | ~400 |
| **Temps d'installation** | ~2 minutes |
| **Temps changement volume** | ~30 secondes |

---

## 🎉 Prochaines Étapes

### Immédiat
- [ ] Installer ALICE_SON : `./install_alice_son.sh`
- [ ] Tester l'interface : `http://<IP_PI>:8080`
- [ ] Créer un raccourci sur votre smartphone

### À Court Terme
- [ ] Configurer le WiFi via mode hotspot
- [ ] Ajuster le volume selon vos préférences
- [ ] Explorer les fonctionnalités de scan QR

### À Long Terme
- [ ] Personnaliser l'interface (couleurs, texte)
- [ ] Ajouter de nouveaux médias
- [ ] Contribuer aux améliorations futures

---

**Version :** 1.1.0  
**Dernière mise à jour :** 2026-02-05  
**Auteur :** Alice Box Project

---

🎯 **Objectif principal :** Rendre le contrôle d'Alice aussi simple et rapide que possible !
